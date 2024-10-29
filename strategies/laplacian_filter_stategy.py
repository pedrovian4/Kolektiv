from abc import ABC, abstractmethod
from PyQt5.QtGui import QImage
import cv2
import numpy as np

class LaplacianFilterStrategy(ABC):
    @abstractmethod
    def laplacian_filter(self, image: QImage) -> QImage:
        pass

class SimpleLaplacianFilter(LaplacianFilterStrategy):
    def __init__(self, ksize: int = 3, scale: float = 1.0, delta: float = 0.0, border_type: str = "BORDER_DEFAULT"):
        self.ksize = ksize
        self.scale = scale
        self.delta = delta
        self.border_type = getattr(cv2, border_type, cv2.BORDER_DEFAULT)

    def laplacian_filter(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)

        gray = cv2.cvtColor(np_image, cv2.COLOR_RGBA2GRAY)

        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=self.ksize, scale=self.scale, delta=self.delta, borderType=self.border_type)

        laplacian = cv2.convertScaleAbs(laplacian)
        laplacian_rgba = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2RGBA)

        laplacian_qimage = self.numpy_to_qimage(laplacian_rgba)

        return laplacian_qimage

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
