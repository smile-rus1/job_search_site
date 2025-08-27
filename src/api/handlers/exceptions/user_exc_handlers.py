from fastapi.responses import JSONResponse

from src.exceptions.infrascructure.user.user import UserAlreadyExist, UserNotFoundByEmail, BaseUserException


def user_exception_handler(_, exc: BaseUserException):
    match exc:
        case (UserAlreadyExist() | UserNotFoundByEmail()):
            return JSONResponse(status_code=409, content={"message": exc.message()})

