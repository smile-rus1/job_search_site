from functools import wraps
from fastapi import HTTPException, status

from src.infrastructure.enums import TypeUser


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth = kwargs.get("auth")
        if auth is None:
            for arg in args:
                if hasattr(arg, "request"):
                    auth = arg
                    break

        if auth is None or getattr(auth.request.state.user, "user_id", None) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        return await func(*args, **kwargs)
    return wrapper


def applicant_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth = kwargs.get("auth")
        if auth is None:
            for arg in args:
                if hasattr(arg, "request"):
                    auth = arg
                    break

        user = getattr(auth.request.state, "user", None) if auth else None
        if user is None or getattr(user, "user_id", None) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        if getattr(user, "type", None) != TypeUser.APPLICANT.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Applicant access required"
            )

        return await func(*args, **kwargs)
    return wrapper


def company_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth = kwargs.get("auth")
        if auth is None:
            for arg in args:
                if hasattr(arg, "request"):
                    auth = arg
                    break

        user = getattr(auth.request.state, "user", None) if auth else None
        if user is None or getattr(user, "user_id", None) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        if getattr(user, "type", None) != TypeUser.COMPANY.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company access required"
            )

        return await func(*args, **kwargs)
    return wrapper
