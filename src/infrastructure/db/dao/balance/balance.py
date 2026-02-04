from loguru import logger
from sqlalchemy import select, insert, update, exists
from sqlalchemy.exc import IntegrityError

from src.core.enums import TransactionType, TransactionStatus, Currency
from src.dto.db.balance.balance import BaseBalanceDTODAO
from src.exceptions.infrascructure.balance.balance import (
    BaseBalanceException,
    NegativeBalanceException
)
from src.infrastructure.db.models import BalanceDB, BalanceTransactionDB
from src.interfaces.infrastructure.dao.balance_dao import IBalanceDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class BalanceDAO(SqlAlchemyDAO, IBalanceDAO):
    async def create_intent(self, balance: BaseBalanceDTODAO):
        sql_balance = select(BalanceDB.balance_id).where(BalanceDB.user_id == balance.user_id).scalar_subquery()

        sql_transaction_balance = (
            insert(BalanceTransactionDB)
            .values(
                balance_id=sql_balance,
                amount=balance.amount,
                currency=balance.currency,
                type=TransactionType.REPLENISHMENT,
                status=TransactionStatus.PENDING,
            )
            .returning(BalanceTransactionDB.transaction_id)
        )

        try:
            res = await self._session.execute(sql_transaction_balance)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{BalanceDAO.__name__} in {self.create_intent.__name__}"
            ).error(f"WITH DATA {balance} IN CREATE INTENT\nMESSAGE: {exc}")
            raise self._error_parser(balance, exc)

        transaction_id = res.scalar_one()
        balance.transaction_id = transaction_id

        return balance

    async def replenishment_balance(self, balance: BaseBalanceDTODAO) -> BaseBalanceDTODAO:
        sql_transaction = (
            update(BalanceTransactionDB)
            .where(
                BalanceTransactionDB.transaction_id == balance.transaction_id,
                BalanceTransactionDB.status == TransactionStatus.PENDING,
            )
            .values(
                status=TransactionStatus.SUCCEEDED,
                provider_event_id=balance.provider_event_id
            )
            .returning(BalanceTransactionDB.status)
        )

        sql_balance = (
            update(BalanceDB)
            .where(
                BalanceDB.user_id == balance.user_id,
            )
            .values(
                amount=BalanceDB.amount + balance.amount
            )
            .returning(BalanceDB.balance_id)
        )

        try:
            res_status = await self._session.execute(sql_transaction)
            res_balance = await self._session.execute(sql_balance)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{BalanceDAO.__name__} in {self.replenishment_balance.__name__}"
            ).error(f"WITH DATA {balance} IN REPLENISHMENT BALANCE\nMESSAGE: {exc}")
            raise self._error_parser(balance, exc)

        balance_id = res_balance.scalar_one()
        status = res_status.scalar_one()

        balance.balance_id = balance_id
        balance.status = status
        return balance

    async def get_user_balance_currency(self, user_id: int) -> Currency:
        sql = select(BalanceDB.currency).where(BalanceDB.user_id == user_id)
        return (await self._session.execute(sql)).scalar()

    async def handle_failure_payment(self, balance: BaseBalanceDTODAO):
        sql_transaction = (
            update(BalanceTransactionDB)
            .where(
                BalanceTransactionDB.transaction_id == balance.transaction_id
            )
            .values(
                status=balance.status,
                provider_event_id=balance.provider_event_id
            )
        )

        try:
            await self._session.execute(sql_transaction)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{BalanceDAO.__name__} in {self.handle_failure_payment.__name__}"
            ).error(f"WITH DATA {balance} IN HANDLE FAILURE PAYMENT\nMESSAGE: {exc}")
            raise self._error_parser(balance, exc)

    async def check_event_exists(self, provider_event_id: str) -> bool:
        sql = select(
            exists()
            .where(BalanceTransactionDB.provider_event_id == provider_event_id)
        )
        return (await self._session.execute(sql)).scalar()

    @staticmethod
    def _error_parser(
            balance: BaseBalanceDTODAO,
            exc: IntegrityError
    ) -> BaseBalanceException:
        error_text = str(exc.orig)
        if "check_balance_non_negative" in error_text:
            return NegativeBalanceException(balance_id=balance.balance_id)

        return BaseBalanceException()
