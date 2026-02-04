from fastapi import APIRouter, Request, status, HTTPException, Depends

from src.api.providers.abstract.services import balance_service_provider
from src.core.config_reader import config
from src.dto.services.balance.balance import HandlePaymentBalanceDTO
from src.infrastructure.payments.stripe.client import stripe_instance
from src.services.balance.balance import BalanceService


stripe_router = APIRouter(prefix="/stripe", tags=["Stripe"])


@stripe_router.post(
    "/webhook",
    status_code=status.HTTP_200_OK
)
async def stripe_webhook(
        request: Request,
        balance_service: BalanceService = Depends(balance_service_provider)
):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:
        event = stripe_instance.Webhook.construct_event(payload, sig, config.payments.stripe_payment.webhook_secret)

    except stripe_instance.error.SignatureVerificationError:
        raise HTTPException(status_code=400)

    intent = event["data"]["object"]
    provider_event_id = event.id
    user_id = int(intent["metadata"]["user_id"])
    amount = intent["amount"] / 100
    transaction_id = int(intent["metadata"]["transaction_id"])

    dto = HandlePaymentBalanceDTO(
        user_id=user_id,
        amount=amount,
        transaction_id=transaction_id,
        provider_event_id=provider_event_id,
        from_currency=event["data"]["object"]["currency"]
    )
    if await balance_service.check_event_exists(provider_event_id):
        return {"status": "ok"}

    if event["type"] == "payment_intent.succeeded":
        await balance_service.replenishment_balance(dto)

        return {"status": "ok"}

    elif event.type in (
        "payment_intent.payment_failed",
        "payment_intent.canceled",
    ):
        dto.status = event.type
        await balance_service.handle_failure_payment(dto)

        return {"status": "payment failure"}
