from datetime import date

from pydantic import BaseModel

from src.infrastructure.enums import GenderEnum, EducationEnum


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    image_url: str | None = None


class AuthDataRequest(BaseModel):
    email: str
    password: str


class CreateApplicantRequest(BaseModel):
    user: CreateUserRequest
    gender: GenderEnum
    description_applicant: str | None = None
    address: str | None = None
    level_education: EducationEnum | None = None
    date_born: date | None = None


class CreateCompanyRequest(BaseModel):
    user: CreateUserRequest
    company_name: str
    description_company: str | None
    address: str | None
