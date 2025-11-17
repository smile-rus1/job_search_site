from pydantic import BaseModel


class UserOut(BaseModel):
    user_id: int
    email: str | None
    last_name: str | None
    first_name: str | None
    phone_number: str | None = None
    image_url: str | None = None
