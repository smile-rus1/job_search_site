from sqlalchemy import Enum
from src.core.enums import (
    VacancyDuration,
    TypeUser,
    EmploymentType,
    WorkScheduleType,
    Currency,
    StatusRespond,
    ActorType,
    ChatType,
    TransactionType,
    TransactionStatus,
)

TypeUserEnumDB = Enum(TypeUser, name="typeuser", create_type=False)
EmploymentTypeEnumDB = Enum(EmploymentType, name="employment_type", create_type=False)
WorkScheduleTypeEnumDB = Enum(WorkScheduleType, name="type_work_schedule", create_type=False)
CurrencyEnumDB = Enum(Currency, name="currency", create_type=False)
VacancyDurationEnumDB = Enum(VacancyDuration, name="vacancyduration", create_type=False)
StatusRespondEnumDB = Enum(StatusRespond, name="status_of_response", create_type=False)
ActorTypeEnumDB = Enum(ActorType, name="actor_type", create_type=False)
ChatTypeEnumDB = Enum(ChatType, name="chat_type", create_type=False)
TransactionTypeEnumDB = Enum(TransactionType, name="transaction_type", create_type=False)
TransactionStatusEnumDB = Enum(TransactionStatus, name="transaction_status", create_type=False)
