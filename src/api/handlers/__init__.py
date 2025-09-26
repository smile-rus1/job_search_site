from src.api.handlers.applicant.applicant import applicant_router
from src.api.handlers.company.company import company_router
from src.api.handlers.resume.resume import resume_router
from src.api.handlers.user import auth_router, user_router
from src.api.handlers.work_experience.work_experience import work_experience_router


__all__ = [
    "auth_router",
    "user_router",
    "applicant_router",
    "company_router",
    "resume_router",
    "work_experience_router",
]

