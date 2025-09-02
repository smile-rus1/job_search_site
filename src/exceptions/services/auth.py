from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class AuthException(BaseExceptions):
    ...


@dataclass
class InvalidEmail(AuthException):
    email: str

    def message(self):
        return f"User with email {self.email} not registered"


class InvalidPassword(AuthException):
    def message(self):
        return f"Wrong password"


class RefreshTokenNotValid(AuthException):
    def message(self):
        return f"Refresh token is not valid"
