from src.core.config_reader import config


def create_confirm_link(token: str):
    """
    Create confirm link and return to user with them token.
    """
    return f"{config.api.base_url}/{config.api.verify_endpoint}/{token}"
