from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseResponseException(BaseExceptions):
    ...


@dataclass
class ResponseAlreadyMaked(BaseResponseException):
    def message(self):
        return f"Response already maked. Yor can make once response"


@dataclass
class ResponseNotFoundOnVacancyOrResume(BaseResponseException):
    def message(self):
        return f"You cannot respond to a non-existent vacancy or resume"


@dataclass
class ResponsePermissionError(BaseResponseException):
    def message(self):
        return "You cannot respond to other people's vacancies or resumes"
