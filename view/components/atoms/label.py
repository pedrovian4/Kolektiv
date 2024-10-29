from PyQt5.QtWidgets import QLabel, QWidget
from typing import Optional

class Label(QLabel):
    def __init__(self, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setStyleSheet("color: #FFFFFF; font-weight: bold;")