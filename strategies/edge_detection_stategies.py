from abc import ABC, abstractmethod
from PyQt5.QtGui import QImage
import cv2
import numpy as np

class EdgeDetectionStrategy(ABC):
    @abstractmethod
    def detect_edges(self, image: QImage) -> QImage:
        """Aplica o método de detecção de bordas à imagem."""
        pass

class SobelEdgeDetection(EdgeDetectionStrategy):
    def __init__(self, ksize: int = 3, scale: float = 1.0, delta: float = 0.0, border_type: int = cv2.BORDER_DEFAULT):
        self.ksize = ksize
        self.scale = scale
        self.delta = delta
        self.border_type = border_type

    def detect_edges(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)
        gray = cv2.cvtColor(np_image, cv2.COLOR_RGBA2GRAY)

        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self.ksize, scale=self.scale, delta=self.delta, borderType=self.border_type)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self.ksize, scale=self.scale, delta=self.delta, borderType=self.border_type)

        magnitude = cv2.magnitude(sobelx, sobely)
        magnitude = cv2.convertScaleAbs(magnitude)

        sobel_rgba = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2RGBA)
        sobel_qimage = self.numpy_to_qimage(sobel_rgba)
        return sobel_qimage

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

class PrewittEdgeDetection(EdgeDetectionStrategy):
    def __init__(self, ksize: int = 3, scale: float = 1.0, delta: float = 0.0, border_type: int = cv2.BORDER_DEFAULT):
        self.ksize = ksize
        self.scale = scale
        self.delta = delta
        self.border_type = border_type
        self.kernelx = np.array([[ -1, 0, 1],
                                 [ -1, 0, 1],
                                 [ -1, 0, 1]], dtype=np.float32)
        self.kernely = np.array([[ 1, 1, 1],
                                 [ 0, 0, 0],
                                 [ -1, -1, -1]], dtype=np.float32)

    def detect_edges(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)
        gray = cv2.cvtColor(np_image, cv2.COLOR_RGBA2GRAY)

        prewittx = cv2.filter2D(gray, cv2.CV_64F, self.kernelx)
        prewitty = cv2.filter2D(gray, cv2.CV_64F, self.kernely)

        magnitude = cv2.magnitude(prewittx, prewitty)
        magnitude = cv2.convertScaleAbs(magnitude)

        prewitt_rgba = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2RGBA)
        prewitt_qimage = self.numpy_to_qimage(prewitt_rgba)
        return prewitt_qimage

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

class CannyEdgeDetection(EdgeDetectionStrategy):
    def __init__(self, threshold1: float = 100.0, threshold2: float = 200.0, apertureSize: int = 3, L2gradient: bool = False):
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.apertureSize = apertureSize
        self.L2gradient = L2gradient

    def detect_edges(self, image: QImage) -> QImage:
        np_image = self.qimage_to_numpy(image)
        gray = cv2.cvtColor(np_image, cv2.COLOR_RGBA2GRAY)

        edges = cv2.Canny(gray, self.threshold1, self.threshold2, apertureSize=self.apertureSize, L2gradient=self.L2gradient)

        edges_rgba = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGBA)
        edges_qimage = self.numpy_to_qimage(edges_rgba)
        return edges_qimage

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
