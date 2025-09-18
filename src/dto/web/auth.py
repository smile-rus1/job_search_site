from pydantic import BaseModel


class AnonymousUser(BaseModel):
    user_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    type: str | None = None


class ActiveUser(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    is_superuser: bool
    type: str
