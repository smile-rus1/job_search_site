from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO


@dataclass
class BaseUserDTODAO(BaseDTO):
    user_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    phone_number: str | None = None
    image_url: str | None = None
    is_superuser: bool | None = None
    is_admin: bool | None = None


@dataclass
class UserDTODAO(BaseDTO):
    email: str
    first_name: str
    last_name: str


@dataclass
class CreateUserDTODAO(UserDTODAO):
    password: str
    phone_number: str
    image_url: str


@dataclass
class UserOutDTODAO(BaseDTO):
    user_id: int
    first_name: str
    last_name: str
    email: str

