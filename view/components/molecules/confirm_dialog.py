from PyQt5.QtWidgets import QMessageBox, QWidget
from typing import Optional

class ConfirmationDialog:
    @staticmethod
    def ask(parent: QWidget, title: str, message: str) -> bool:
        reply = QMessageBox.question(
            parent,
            title,
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes
