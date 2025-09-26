from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseWorkExperiencesException(BaseExceptions):
    ...


@dataclass
class WorkExperiences(BaseWorkExperiencesException):
    def message(self):
        return f"An error occurred while creating work experiences."


@dataclass
class WorkExperiencesNotFoundByID(BaseWorkExperiencesException):
    work_experience_id: int

    def message(self):
        return f"Work experiences with id {self.work_experience_id} not found!"
