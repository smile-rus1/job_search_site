from dataclasses import dataclass
from datetime import datetime

from src.exceptions.base import BaseExceptions


class BaseVacancyException(BaseExceptions):
    ...


@dataclass
class VacancyException(BaseVacancyException):
    def message(self):
        return "An error occurred while creating vacancy."


@dataclass
class VacancyTypeException(BaseVacancyException):
    name: str

    def message(self):
        return f"Type of vacancy not found with name: {self.name}"


@dataclass
class VacancyNotFoundByID(BaseVacancyException):
    vacancy_id: int

    def message(self):
        return f"Vacancy with id {self.vacancy_id} not found!"


@dataclass
class NotUpdatedTimeVacancy(BaseVacancyException):
    name: str
    time_to_update: datetime

    def message(self):
        return f"The vacancy {self.name} can be updated in {self.time_to_update} hours"


@dataclass
class VacancyAlreadyInLiked(BaseVacancyException):
    vacancy_id: int

    def message(self):
        return f"Vacancy with id {self.vacancy_id} already in liked"
