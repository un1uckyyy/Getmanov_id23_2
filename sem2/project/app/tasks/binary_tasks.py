from celery.result import AsyncResult

from app.core.celery import app
from app.services.binary import otsu_binarization, save_image_to_file


@app.task
def binarize_image_task(image_data: bytes) -> str:
    binarized_image = otsu_binarization(image_data)
    path = save_image_to_file(binarized_image)
    return path


def binarize_image_result(task_id: str):
    return AsyncResult(task_id, app=app)
