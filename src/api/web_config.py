from dataclasses import dataclass


@dataclass
class APIConfig:
    host: str
    port: int
    debug: bool
    api_v1_str: str
    base_url: str
    verify_endpoint: str
