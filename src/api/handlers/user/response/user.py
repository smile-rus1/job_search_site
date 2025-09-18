from pydantic import BaseModel


class UserOut(BaseModel):
    user_id: int
    last_name: str
    first_name: str
    email: str
    phone_number: str | None = None
    image_url: str | None = None
