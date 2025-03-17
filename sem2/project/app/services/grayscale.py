import numpy as np
import cv2


def grayscale(image: bytes):
    np_arr = np.frombuffer(image, np.uint8)

    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return gray_img
