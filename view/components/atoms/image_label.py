from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from typing import Optional

class ImageLabel(QLabel):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("image_label")
        self.setMinimumSize(800, 600)

    def display_image(self, image: QImage) -> None:
        pixmap = QPixmap.fromImage(image)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

    def clear_image(self) -> None:
        self.clear()

    def set_image(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(pixmap)

