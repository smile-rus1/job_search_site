from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseResumeException(BaseExceptions):
    ...


@dataclass
class ResumeException(BaseResumeException):
    def message(self):
        return f"An error occurred while creating your resume."


@dataclass
class ResumeIDException(BaseResumeException):
    resume_id: int


@dataclass
class ResumeNotFoundByID(ResumeIDException):
    def message(self):
        return f"Resume with id {self.resume_id} not found!"
