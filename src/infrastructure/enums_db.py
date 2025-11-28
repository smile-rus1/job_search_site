from sqlalchemy import Enum
from src.core.enums import (
    VacancyDuration,
    TypeUser,
    EmploymentType,
    WorkScheduleType,
    Currency, StatusRespond, ActorType,
)

TypeUserEnumDB = Enum(TypeUser, name="typeuser", create_type=False)
EmploymentTypeEnumDB = Enum(EmploymentType, name="employment_type", create_type=False)
WorkScheduleTypeEnumDB = Enum(WorkScheduleType, name="type_work_schedule", create_type=False)
CurrencyEnumDB = Enum(Currency, name="currency", create_type=False)
VacancyDurationEnumDB = Enum(VacancyDuration, name="vacancyduration", create_type=False)
StatusRespondEnumDB = Enum(StatusRespond, name="status_of_response")
ActorTypeEnumDB = Enum(ActorType, name="actor_type")
