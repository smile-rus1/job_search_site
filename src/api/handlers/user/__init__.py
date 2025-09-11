

__all__ = ["auth_router", "user_router"]

from src.api.handlers.user.user import user_router
from src.api.handlers.user.auth import auth_router