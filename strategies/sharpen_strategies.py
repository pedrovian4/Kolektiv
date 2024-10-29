from abc import ABC, abstractmethod
from PyQt5.QtGui import QImage
import cv2
import numpy as np

class SharpenStrategy(ABC):
    @abstractmethod
    def sharpen(self, image: QImage) -> QImage:
        pass

class UnsharpMask(SharpenStrategy):
    def __init__(self, kernel_size: int = 5, sigma: float = 1.0, amount: float = 1.0, threshold: float = 0.0):
        """
        :param kernel_size: Tamanho do kernel para o blur Gaussiano.
        :param sigma: Desvio padrão para o blur Gaussiano.
        :param amount: Quanto a imagem deve ser realçada.
        :param threshold: Mínimo diferença para aplicar o realce.
        """
        self.kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1  # Garantir tamanho ímpar
        self.sigma = sigma
        self.amount = amount
        self.threshold = threshold

    def sharpen(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)

        blurred = cv2.GaussianBlur(np_image, (self.kernel_size, self.kernel_size), self.sigma)

        mask = cv2.subtract(np_image, blurred)

        sharpened = cv2.addWeighted(np_image, 1.0, mask, self.amount, 0)

        if self.threshold > 0:
            low_contrast_mask = np.absolute(mask) < self.threshold
            sharpened[low_contrast_mask] = np_image[low_contrast_mask]

        sharpened_qimage = self.numpy_to_qimage(sharpened)

        return sharpened_qimage

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
