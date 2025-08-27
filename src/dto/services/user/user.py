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
class OutUserDTO(BaseDTO):
    user_id: int
    first_name: str
    last_name: str
    email: str
