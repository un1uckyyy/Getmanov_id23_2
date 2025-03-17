from typing import Annotated

import cv2
from fastapi import APIRouter, File, Response

from ..services.binary import otsu_threshold, otsu_binarization
from ..services.grayscale import grayscale

router = APIRouter()


@router.post("/binary_image")
async def binary(image: Annotated[bytes, File()]):
    gray_img = grayscale(image)

    threshold = otsu_threshold(gray_img)
    binary_img = otsu_binarization(gray_img, threshold)

    _, encoded_img = cv2.imencode(".jpg", binary_img)

    return Response(content=encoded_img.tobytes(), media_type="image/jpeg")
