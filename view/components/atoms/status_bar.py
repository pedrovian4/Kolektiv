from PyQt5.QtWidgets import QStatusBar, QWidget
from typing import Optional

class CustomStatusBar(QStatusBar):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("""
            QStatusBar {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-size: 14px;
            }
        """)
