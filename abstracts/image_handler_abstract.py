from PyQt5.QtGui import QImage
from typing import Optional, List
from entities.layer import Layer
from abc import ABC, abstractmethod

class AbstractImageHandler(ABC):
    @abstractmethod
    def load_image(self, file_path: str) -> Optional[QImage]:
        pass

    @abstractmethod
    def save_image(self, image: QImage, file_path: str) -> bool:
        pass

    @abstractmethod
    def get_composited_image(self) -> Optional[QImage]:
        pass

    @abstractmethod
    def add_layer(self, name: str, image: QImage) -> None:
        pass

    @abstractmethod
    def remove_layer(self, index: int) -> None:
        pass

    @property
    @abstractmethod
    def layers(self) -> List[Layer]:
        pass
