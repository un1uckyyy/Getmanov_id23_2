from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str


class UserWithToken(User):
    token: str
