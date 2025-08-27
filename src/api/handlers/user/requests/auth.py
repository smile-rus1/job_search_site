from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    image_url: str | None = None


class UserOut(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
