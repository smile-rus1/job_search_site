from dataclasses import dataclass

from src.dto.base_dto import BaseDTO


@dataclass
class AuthUserDTO(BaseDTO):
    email: str
    password: str
