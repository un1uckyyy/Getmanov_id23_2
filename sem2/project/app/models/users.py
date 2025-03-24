from pydantic import BaseModel


class DbUser(BaseModel):
    id: int
    email: str
    hashed_password: str
