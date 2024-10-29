from abc import ABC, abstractmethod
from PyQt5.QtGui import QImage
import cv2
import numpy as np

class TransformStrategy(ABC):
    @abstractmethod
    def transform(self, image: QImage) -> QImage:
        """Aplica a transformação à imagem."""
        pass

class ScaleTransform(TransformStrategy):
    def __init__(self, scale_x: float = 1.0, scale_y: float = 1.0, interpolation: int = cv2.INTER_LINEAR):
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.interpolation = interpolation

    def transform(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)
        width = int(np_image.shape[1] * self.scale_x)
        height = int(np_image.shape[0] * self.scale_y)
        scaled_image = cv2.resize(np_image, (width, height), interpolation=self.interpolation)
        return self.numpy_to_qimage(scaled_image)

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

class RotateTransform(TransformStrategy):
    def __init__(self, angle: float = 0.0, scale: float = 1.0, center: tuple = None, interpolation: int = cv2.INTER_LINEAR):
        self.angle = angle
        self.scale = scale
        self.center = center
        self.interpolation = interpolation

    def transform(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)
        (h, w) = np_image.shape[:2]
        if self.center is None:
            center = (w // 2, h // 2)
        else:
            center = self.center
        M = cv2.getRotationMatrix2D(center, self.angle, self.scale)
        rotated_image = cv2.warpAffine(np_image, M, (w, h), flags=self.interpolation)
        return self.numpy_to_qimage(rotated_image)

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

class TranslateTransform(TransformStrategy):
    def __init__(self, shift_x: int = 0, shift_y: int = 0, border_mode: int = cv2.BORDER_CONSTANT, border_value: tuple = (0, 0, 0, 0)):
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.border_mode = border_mode
        self.border_value = border_value

    def transform(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)
        M = np.float32([[1, 0, self.shift_x], [0, 1, self.shift_y]])
        shifted_image = cv2.warpAffine(np_image, M, (np_image.shape[1], np_image.shape[0]),
                                       borderMode=self.border_mode, borderValue=self.border_value)
        return self.numpy_to_qimage(shifted_image)

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
