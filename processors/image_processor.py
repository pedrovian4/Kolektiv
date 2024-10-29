# managers/image_processor.py

from abstracts.image_handler_abstract import AbstractImageHandler
from entities.layer import Layer
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import Qt
from typing import List, Optional
import cv2
import numpy as np
from strategies.blur_strategies import BlurStrategy

class ImageProcessor(AbstractImageHandler):
    def __init__(self) -> None:
        self._layers: List[Layer] = []

    def load_image(self, file_path: str) -> Optional[QImage]:
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            print(f"Erro ao carregar a imagem: {file_path}")
            return None

        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
            bytes_per_line = 4 * image.shape[1]
            q_image = QImage(image.data, image.shape[1], image.shape[0], bytes_per_line, QImage.Format_RGBA8888)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            bytes_per_line = 3 * image.shape[1]
            q_image = QImage(image.data, image.shape[1], image.shape[0], bytes_per_line, QImage.Format_RGB888)

        return q_image.copy()

    def save_image(self, image: QImage, file_path: str) -> bool:
        if image.isNull():
            print("Imagem vazia. Não pode ser salva.")
            return False

        image = image.convertToFormat(QImage.Format_RGBA8888)
        width = image.width()
        height = image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)
        success = cv2.imwrite(file_path, arr)
        if not success:
            print(f"Erro ao salvar a imagem: {file_path}")
        return success

    def get_composited_image(self) -> Optional[QImage]:
        if not self._layers:
            print("Nenhuma camada para compor.")
            return None

        base_layer = QImage(self._layers[0].image.size(), QImage.Format_RGBA8888)
        base_layer.fill(Qt.transparent)

        for layer in self._layers:
            if layer.visible:
                base_layer = self.composite_images(base_layer, layer.image, layer.opacity)

        return base_layer

    def composite_images(self, base: QImage, overlay: QImage, opacity: float = 1.0) -> QImage:
        if base.size() != overlay.size():
            overlay = overlay.scaled(base.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        result = QImage(base)
        painter = QPainter(result)
        painter.setOpacity(opacity)
        painter.drawImage(0, 0, overlay)
        painter.end()
        return result

    def add_layer(self, name: str, image: QImage) -> None:
        self._layers.append(Layer(name, image))
        print(f"ImageProcessor: Camada adicionada '{name}'")

    def remove_layer(self, index: int) -> None:
        if 0 <= index < len(self._layers):
            removed_layer = self._layers[index].name
            del self._layers[index]
            print(f"ImageProcessor: Camada removida '{removed_layer}'")
        else:
            print(f"ImageProcessor: Índice de camada inválido ao remover: {index}")
            raise IndexError("Índice de camada inválido")

    def toggle_layer_visibility(self, index: int) -> None:
        if 0 <= index < len(self._layers):
            self._layers[index].visible = not self._layers[index].visible
            print(f"ImageProcessor: Visibilidade da camada '{self._layers[index].name}' alterada para {self._layers[index].visible}")
        else:
            print(f"ImageProcessor: Índice de camada inválido ao alternar visibilidade: {index}")
            raise IndexError("Índice de camada inválido")

    def reorder_layers(self, source: int, dest: int) -> None:
        if 0 <= source < len(self._layers) and 0 <= dest <= len(self._layers):
            layer = self._layers.pop(source)
            self._layers.insert(dest, layer)
            print(f"ImageProcessor: Camada '{layer.name}' movida de {source} para {dest}")
        else:
            print(f"ImageProcessor: Índices de reordenação inválidos: {source} para {dest}")
            raise IndexError("Índices de reordenação inválidos")

    @property
    def layers(self) -> List[Layer]:
        return self._layers

    def get_layer(self, index: int) -> Layer:
        if 0 <= index < len(self._layers):
            return self._layers[index]
        else:
            print(f"ImageProcessor: Índice de camada inválido ao obter camada: {index}")
            raise IndexError("Índice de camada inválido")

    def apply_blur_to_layer(self, index: int, blur_type: str, kernel_size: int = 5, sigma: float = 1.0) -> None:
        if not (0 <= index < len(self._layers)):
            print(f"ImageProcessor: Índice de camada inválido ao aplicar blur: {index}")
            raise IndexError("Índice de camada inválido")

        layer = self._layers[index]
        print(f"ImageProcessor: Aplicando {blur_type} na camada '{layer.name}'")

        np_image = self.qimage_to_numpy(layer.image)

        if blur_type == "blur":
            blurred_np = cv2.blur(np_image, (kernel_size, kernel_size))
        elif blur_type == "gaussian":
            blurred_np = cv2.GaussianBlur(np_image, (kernel_size, kernel_size), sigma)
        elif blur_type == "median":
            blurred_np = cv2.medianBlur(np_image, kernel_size)
        else:
            raise ValueError(f"Tipo de blur desconhecido: {blur_type}")

        blurred_qimage = self.numpy_to_qimage(blurred_np)

        layer.image = blurred_qimage
        print(f"ImageProcessor: Blur aplicado na camada '{layer.name}'")

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
