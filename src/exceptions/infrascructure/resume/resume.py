from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseResumeException(BaseExceptions):
    ...


@dataclass
class ResumeException(BaseResumeException):
    def message(self):
        return f"An error occurred while creating your resume."


@dataclass
class UserIDException(BaseResumeException):
    resume_id: int


@dataclass
class ResumeNotFoundByID(UserIDException):
    def message(self):
        return f"User with {self.resume_id} id not found!"
