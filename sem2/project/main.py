import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth, users, binary
from app.core.config import settings

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(binary.router)

app.mount(settings.static_content_path, StaticFiles(directory=settings.images_dir), name="images")


@app.get("/")
async def index():
    return FileResponse("./public/index.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
