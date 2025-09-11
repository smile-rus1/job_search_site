from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO


@dataclass
class BaseUserDTO(BaseDTO):
    first_name: str
    last_name: str
    email: str
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class UserDTO(BaseUserDTO):
    user_id: int


@dataclass
class CreateUserDTO(BaseDTO):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    image_url: str | None = None


@dataclass
class UpdateUserDTO(BaseDTO):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone_number: str | None = None
    image_url: str | None = None


@dataclass
class UserOutDTO(BaseDTO):
    user_id: int
    first_name: str
    last_name: str
    email: str
