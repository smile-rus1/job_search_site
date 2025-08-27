from dataclasses import dataclass


@dataclass
class AuthConfig:
    algorithm: str
    secret_key: str
