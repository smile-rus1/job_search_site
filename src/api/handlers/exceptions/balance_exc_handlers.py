from starlette.responses import JSONResponse

from src.exceptions.infrascructure.balance.balance import BaseBalanceException, PaymentException, \
    NegativeBalanceException


def balance_exception_handler(_, exc: BaseBalanceException):
    match exc:
        case PaymentException():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case NegativeBalanceException():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case BaseBalanceException():
            return JSONResponse(status_code=500, content={"message": "Sorry, service not available, please try later"})
