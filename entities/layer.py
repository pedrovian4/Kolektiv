from PyQt5.QtGui import QImage
from typing import Any

class Layer:
    def __init__(self, name: str, image: QImage, visible: bool = True, opacity: float = 1.0) -> None:
        self.name = name
        self.image = image
        self.visible = visible
        self.opacity = opacity