from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    image_url: str | None = None
