import cv2
from PyQt5.QtGui import QImage, QPainter
from .layer import Layer
import numpy as np
import copy

class ImageProcessor:
    def __init__(self):
        self.layers = []
        self.history = []

    def load_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is not None:
            if len(image.shape) == 3 and image.shape[2] == 4:
                image_rgba = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
                height, width, channels = image_rgba.shape
                bytes_per_line = channels * width
                qt_image = QImage(image_rgba.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
            else:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, channels = image_rgb.shape
                bytes_per_line = channels * width
                qt_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            return qt_image
        return None

    def add_layer(self, name, image: QImage):
        layer = Layer(name, image)
        self.layers.append(layer)

    def remove_layer(self, index):
        if 0 <= index < len(self.layers):
            del self.layers[index]
        else:
            raise IndexError("Índice da camada fora do intervalo.")

    def move_layer_up(self, index):
        if 1 <= index < len(self.layers):
            self.layers[index - 1], self.layers[index] = self.layers[index], self.layers[index - 1]

    def move_layer_down(self, index):
        if 0 <= index < len(self.layers) - 1:
            self.layers[index + 1], self.layers[index] = self.layers[index], self.layers[index + 1]

    def toggle_layer_visibility(self, index):
        if 0 <= index < len(self.layers):
            self.layers[index].visible = not self.layers[index].visible

    def get_composited_image(self):
        visible_layers = [layer for layer in self.layers if layer.visible]

        if not visible_layers:
            return None

        base_image = visible_layers[0].image.copy()
        base_image = base_image.convertToFormat(QImage.Format_ARGB32)
        painter = QPainter(base_image)

        for layer in visible_layers[1:]:
            painter.drawImage(0, 0, layer.image)

        painter.end()
        return base_image

    def save_history(self):
        """Salva uma cópia das camadas atuais para permitir desfazer."""
        history_copy = []
        for layer in self.layers:
            cloned_image = layer.image.copy()
            cloned_layer = Layer(layer.name, cloned_image, layer.visible)
            history_copy.append(cloned_layer)
        self.history.append(history_copy)
        
    def undo(self):
        if self.history:
            self.layers = self.history.pop()
            return True
        return False

    def apply_blur(self, layer_index, kernel_size=5):
        if not self.layers:
            return
        if not (0 <= layer_index < len(self.layers)):
            raise IndexError("Índice da camada fora do intervalo.")
        self.save_history()
        layer = self.layers[layer_index]
        image = self.qimage_to_cv(layer.image)

        blurred = cv2.blur(image, (kernel_size, kernel_size))

        layer.image = self.cv_to_qimage(blurred)

    def apply_gaussian_blur(self, layer_index, kernel_size=5, sigma=0):
        if not self.layers:
            return
        if not (0 <= layer_index < len(self.layers)):
            raise IndexError("Índice da camada fora do intervalo.")
        if kernel_size <= 0 or kernel_size % 2 == 0:
            raise ValueError("O tamanho do kernel deve ser um número ímpar positivo.")
        self.save_history()
        print(f"Aplicando Gaussian Blur na camada {layer_index} com kernel_size={kernel_size} e sigma={sigma}")
        layer = self.layers[layer_index]
        image = self.qimage_to_cv(layer.image)

        gaussian_blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

        layer.image = self.cv_to_qimage(gaussian_blurred)
        
    def qimage_to_cv(self, qt_image):
        """ Converte QImage para um array NumPy compatível com OpenCV. """
        qt_image = qt_image.convertToFormat(QImage.Format_RGBA8888)
        width = qt_image.width()
        height = qt_image.height()
        ptr = qt_image.bits()
        ptr.setsize(qt_image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)

    def cv_to_qimage(self, cv_image):
        """ Converte um array NumPy (OpenCV) para QImage. """
        if cv_image.shape[2] == 4:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGBA)
            qt_image = QImage(
                cv_image.data,
                cv_image.shape[1],
                cv_image.shape[0],
                cv_image.strides[0],
                QImage.Format_RGBA8888
            )
        else:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            qt_image = QImage(
                cv_image.data,
                cv_image.shape[1],
                cv_image.shape[0],
                cv_image.strides[0],
                QImage.Format_RGB888
            )
        return qt_image.copy() 