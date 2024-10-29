# strategies/highpass_filter_strategies.py

from abc import ABC, abstractmethod
from PyQt5.QtGui import QImage
import cv2
import numpy as np

class HighpassFilterStrategy(ABC):
    @abstractmethod
    def highpass_filter(self, image: QImage) -> QImage:
        pass

class SimpleHighpassFilter(HighpassFilterStrategy):
    def __init__(self, kernel_size: int = 3, sigma: float = 1.0, threshold: float = 0.0):
        self.kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1  # Garantir tamanho ímpar
        self.sigma = sigma
        self.threshold = threshold

    def highpass_filter(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)

        blurred = cv2.GaussianBlur(np_image, (self.kernel_size, self.kernel_size), self.sigma)

        highpass = cv2.subtract(np_image, blurred)

        if self.threshold > 0:
            mask = np.absolute(highpass) > self.threshold
            highpass[~mask] = 0

        highpass_normalized = cv2.normalize(highpass, None, 0, 255, cv2.NORM_MINMAX)

        highpass_qimage = self.numpy_to_qimage(highpass_normalized)

        return highpass_qimage

    def qimage_to_numpy(self, qimage: QImage) -> np.ndarray:
        qimage = qimage.convertToFormat(QImage.Format_RGBA8888)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        return arr.copy()

    def numpy_to_qimage(self, arr: np.ndarray) -> QImage:
        height, width, channel = arr.shape
        bytes_per_line = 4 * width
        return QImage(arr.data, width, height, bytes_per_line, QImage.Format_RGBA8888).copy()
