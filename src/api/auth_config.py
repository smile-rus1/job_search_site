from dataclasses import dataclass


@dataclass
class AuthConfig:
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire: int = 60 * 15
    refresh_token_expire: int = 60 * 60 * 24 * 30
    access_token_name: str = "access_token"
    refresh_token_name: str = "refresh_token"
