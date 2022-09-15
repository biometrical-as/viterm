from enum import Enum

import cv2
import numpy as np


class Preprocessor(Enum):
    CANNY = "canny"
    GRAY = "gray"


def canny(image: np.ndarray):
    image = cv2.Canny(image, 100, 200)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image


def gray(image: np.ndarray):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Duplicates channel
    return image
