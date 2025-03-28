import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api import auth, users, binary

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(binary.router)

app.mount("/", StaticFiles(directory="public"), name="public")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
