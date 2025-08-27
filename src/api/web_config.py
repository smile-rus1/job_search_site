from dataclasses import dataclass


@dataclass
class APIConfig:
    host: str
    port: int
    debug: bool
    api_v1_str: str
