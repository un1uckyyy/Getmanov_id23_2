from typing import List

from app.tasks.binary_tasks import binarize_image_task, binarize_image_result
from fastapi import APIRouter, File, UploadFile

from app.core.auth import CurrentUser

router = APIRouter(tags=["image binarization"])


@router.post("/binary_image")
async def binary_image(
        current_user: CurrentUser,
        images: List[UploadFile] = File(...)
):
    task_ids = []

    for image in images:
        image_bytes = await image.read()
        task = binarize_image_task.delay(image_bytes)
        task_ids.append(task.id)

    return {"tasks": task_ids}


@router.get("/binary_image/{task_id}/status")
async def binary_image_status(task_id: str):
    result = binarize_image_result(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.successful() else None
    }
