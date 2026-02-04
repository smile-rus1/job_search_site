from abc import ABC
from decimal import Decimal

from loguru import logger

from src.core.enums import TransactionStatus, Currency
from src.dto.db.balance.balance import BaseBalanceDTODAO
from src.dto.services.balance.balance import CreateIntentBalanceDTO, HandlePaymentBalanceDTO
from src.exceptions.infrascructure.balance.balance import BaseBalanceException, PaymentException
from src.exceptions.infrascructure.user.user import UserNotFoundByID
from src.infrastructure.payments.stripe.client import stripe_instance
from src.interfaces.infrastructure.currency_converter import ICurrencyConverter
from src.interfaces.infrastructure.notifications import AbstractNotifications
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.utils.utils import create_profile_link


class BalanceUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateIntentStripe(BalanceUseCase):
    async def __call__(self, dto: CreateIntentBalanceDTO) -> str:
        if dto.currency.upper() == Currency.BYN.value:
            currency = Currency.BYN
        elif dto.currency.upper() == Currency.RUB.value:
            currency = Currency.RUB
        elif dto.currency.upper() == Currency.EUR.value:
            currency = Currency.EUR
        elif dto.currency.upper() == Currency.USD.value:
            currency = Currency.USD
        else:
            currency = ""

        balance = BaseBalanceDTODAO(
            user_id=dto.user_id,
            amount=Decimal(dto.amount),
            balance_id=None,
            transaction_id=None,
            currency=currency,
        )

        try:
            res = await self._tm.balance_dao.create_intent(balance)
            await self._tm.commit()

        except BaseBalanceException as exc:
            logger.bind(
                app_name=f"{CreateIntentStripe.__name__}"
            ).error(f"WITH DATA {dto}")
            await self._tm.rollback()
            raise exc

        intent = stripe_instance.PaymentIntent.create(
            amount=dto.amount * 100,  # stripe get in cent's
            currency=dto.currency,
            automatic_payment_methods={"enabled": True},
            metadata={
                "user_id": dto.user_id,
                "purpose": "balance_topup",
                "schema": "balance_topup_v1",
                "transaction_id": str(res.transaction_id)
            }
        )

        return intent.client_secret


class ReplenishmentBalance(BalanceUseCase):
    async def __call__(
            self,
            dto: HandlePaymentBalanceDTO,
            notifications: AbstractNotifications,
            converter: ICurrencyConverter,
    ):

        currency = await self._tm.balance_dao.get_user_balance_currency(dto.user_id)
        currency_course = await converter.get_rate(
            from_currency=dto.from_currency,
            to_currency=currency.value
        )
        if currency_course is None:
            logger.bind(
                app_name=f"{ReplenishmentBalance.__name__}"
            ).error(f"Currency wasn't converted!")
            raise PaymentException()

        amount = Decimal(dto.amount) * currency_course
        balance = BaseBalanceDTODAO(
            user_id=dto.user_id,
            transaction_id=dto.transaction_id,
            amount=amount,
            provider_event_id=dto.provider_event_id,
            balance_id=None,
        )
        try:
            res = await self._tm.balance_dao.replenishment_balance(balance)

        except BaseBalanceException as exc:
            logger.bind(
                app_name=f"{ReplenishmentBalance.__name__}"
            ).error(f"WITH DATA {dto}")
            await self._tm.rollback()
            raise exc

        if res.status != TransactionStatus.SUCCEEDED:
            logger.bind(
                app_name=f"{ReplenishmentBalance.__name__}"
            ).error(f"PAYMENT IS NOT SUCCESS")
            await self._tm.rollback()
            raise PaymentException()

        await self._tm.commit()

        try:
            user = await self._tm.user_dao.get_user_by_id(dto.user_id)

        except UserNotFoundByID:
            return

        data_notification = {
            "subject": f"Вы пополнили баланс",
            "body": f"Вы пополнили свой баланс на {dto.amount} y.e\n"
                    f"Ссылка на кабинет {create_profile_link()}"
        }

        logger.bind(
            app_name=f"{ReplenishmentBalance.__name__}"
        ).info(f"SEND TO EMAIL {user.email} DATA {data_notification}")

        notifications.send(
            destination=user.email,
            template="send_message_replenishment_balance",
            data=data_notification
        )


class CheckEventExists(BalanceUseCase):
    async def __call__(self, provider_event_id: str) -> bool:
        return await self._tm.balance_dao.check_event_exists(provider_event_id)


class HandleFailurePayment(BalanceUseCase):
    async def __call__(self, dto: HandlePaymentBalanceDTO):
        status = None

        if dto.status == "payment_intent.payment_failed":
            status = TransactionStatus.FAILED

        elif dto.status == "payment_intent.canceled":
            status = TransactionStatus.CANCELED

        balance = BaseBalanceDTODAO(
            user_id=dto.user_id,
            transaction_id=dto.transaction_id,
            provider_event_id=dto.provider_event_id,
            status=status,
            balance_id=None,
            amount=None,
        )

        try:
            await self._tm.balance_dao.handle_failure_payment(balance)
            await self._tm.commit()

        except BaseBalanceException as exc:
            logger.bind(
                app_name=f"{HandleFailurePayment.__name__}"
            ).error(f"WITH DATA {dto}")
            await self._tm.rollback()
            raise exc


class BalanceService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            notifications: AbstractNotifications,
            converter: ICurrencyConverter
    ):
        self._tm = tm
        self._notifications = notifications
        self._converter = converter

    async def create_intent(self, dto: CreateIntentBalanceDTO) -> str:
        return await CreateIntentStripe(tm=self._tm)(dto)

    async def replenishment_balance(self, dto: HandlePaymentBalanceDTO):
        return await ReplenishmentBalance(tm=self._tm)(dto, self._notifications, self._converter)

    async def handle_failure_payment(self, dto: HandlePaymentBalanceDTO):
        return await HandleFailurePayment(tm=self._tm)(dto)

    async def check_event_exists(self, provider_event_id: str) -> bool:
        return await CheckEventExists(tm=self._tm)(provider_event_id)
