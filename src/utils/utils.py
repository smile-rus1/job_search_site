from src.core.config_reader import config


def create_confirm_link(token: str):
    """
    Create confirm link and return to user with them token.
    """
    return f"{config.api.base_url}/{config.api.verify_endpoint}/{token}"


def create_applicant_resume_link(slug: str | int):
    return f"{config.api.base_url}{config.api.api_v1_str}/resumes/{slug}"


def create_company_vacancy_link(slug: str | int):
    return f"{config.api.base_url}{config.api.api_v1_str}/vacancies/{slug}"
