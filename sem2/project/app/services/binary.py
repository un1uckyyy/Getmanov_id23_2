import cv2
import os
from uuid import uuid4
import numpy as np
from app.services.grayscale import grayscale
from app.core.config import settings


# https://en.wikipedia.org/wiki/Otsu%27s_method
def otsu_threshold(image):
    hist, bins = np.histogram(image, bins=256, range=(0, 256))  # Гистограмма яркости

    total_pixels = image.size
    prob = hist / total_pixels  # Нормализация гистограммы по частотам

    # Кумулятивные суммы
    cumulative_sum = np.cumsum(prob)  # W(T)
    cumulative_mean = np.cumsum(prob * np.arange(256))  # μ(T)

    # Общая средняя яркость
    global_mean = cumulative_mean[-1]  # μ_total

    # Межклассовая дисперсия для всех порогов
    numerator = (global_mean * cumulative_sum - cumulative_mean) ** 2
    denominator = cumulative_sum * (1 - cumulative_sum)
    inter_class_variance = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)

    # Оптимальный порог — максимум межклассовой дисперсии
    best_threshold = np.argmax(inter_class_variance)

    return best_threshold


def otsu_binarization(image: bytes) -> np.ndarray:
    gray_img = grayscale(image)

    threshold = otsu_threshold(gray_img)

    return (gray_img > threshold).astype(np.uint8) * 255


def save_image_to_file(image: np.ndarray) -> str:
    save_dir = settings.images_dir
    static_dir = settings.static_content_path

    os.makedirs(save_dir, exist_ok=True)
    filename = f"{uuid4().hex}.png"
    filepath = os.path.join(save_dir, filename)
    cv2.imwrite(filepath, image)

    static_path = os.path.join(static_dir, filename)
    return static_path
