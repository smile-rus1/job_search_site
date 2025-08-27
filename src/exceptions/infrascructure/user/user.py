from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseUserException(BaseExceptions):
    ...


@dataclass
class UserAlreadyExist(BaseUserException):
    email: str

    def message(self):
        return f"User with email {self.email} already exist"


@dataclass
class UserNotFoundByEmail(BaseUserException):
    email: str

    def message(self):
        return f"User with email {self.email} not found"
