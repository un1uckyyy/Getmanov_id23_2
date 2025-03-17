from fastapi import FastAPI

from app.api import auth, users, binary

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(binary.router)
