from dataclasses import dataclass

from src.dto.base_dto import BaseDTO


@dataclass
class AuthUserDTO(BaseDTO):
    email: str
    password: str


@dataclass
class AuthUserOutDTO(BaseDTO):
    user_id: int
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    is_superuser: bool
