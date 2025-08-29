from pydantic import BaseModel


class UserOut(BaseModel):
    user_id: int
    last_name: str
    first_name: str
    email: str
