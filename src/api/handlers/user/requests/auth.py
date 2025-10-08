from datetime import date

from fastapi import UploadFile, File, Form, Depends
from pydantic import BaseModel

from src.infrastructure.enums import GenderEnum, EducationEnum


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    image: UploadFile | None = None


def create_user(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        phone_number: str = Form(...),
        image: UploadFile | None = File(None)
):
    return CreateUserRequest(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        phone_number=phone_number,
        image=image
    )


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


def create_applicant(
        user: CreateUserRequest = Depends(create_user),
        gender: GenderEnum = Form(...),
        description_applicant: str | None = Form(None),
        address: str | None = Form(None),
        level_education: EducationEnum | None = Form(None),
        date_born: date | None = Form(None)
):
    return CreateApplicantRequest(
        user=user,
        gender=gender,
        description_applicant=description_applicant,
        address=address,
        level_education=level_education,
        date_born=date_born
    )


class CreateCompanyRequest(BaseModel):
    user: CreateUserRequest
    company_name: str
    description_company: str | None
    address: str | None


def create_company(
        user: CreateUserRequest = Depends(create_user),
        company_name: str = Form(...),
        description_company: str = Form(None),
        address: str = Form(None),
):
    return CreateCompanyRequest(
        user=user,
        company_name=company_name,
        description_company=description_company,
        address=address
    )
