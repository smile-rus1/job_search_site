from fastapi import APIRouter, Body, Depends

from src.api.permissions import login_required
from src.api.providers.abstract.services import balance_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.balance.balance import CreateIntentBalanceDTO
from src.services.balance.balance import BalanceService


balance_router = APIRouter(prefix="/balance", tags=["Balance"])


@balance_router.post("/top-up")
@login_required
async def replenishment_of_balance(
        auth: TokenAuthDep,
        currency: str = Body(embed=True),
        amount: int = Body(embed=True),
        balance_service: BalanceService = Depends(balance_service_provider)
):
    """
    amount: int - amount currency in cents.
    """

    dto = CreateIntentBalanceDTO(
        user_id=auth.request.state.user.user_id,
        amount=amount,
        currency=currency
    )
    intent_secret = await balance_service.create_intent(dto)

    return {"client_secret": intent_secret}
