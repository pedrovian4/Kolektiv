# view/main_window.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import os
from typing import Optional
from view.components.organisms.main_toolbar import MainToolbar
from view.components.templates.main_layout import MainLayout

class MainWindow(QMainWindow):
    def __init__(self, controller, parent: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Kolektiv 🖼️")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon(os.path.join("icons", "app_icon.png")))
        self.main_layout = MainLayout(controller, self)
        self.setCentralWidget(self.main_layout)

        self.toolbar = MainToolbar (controller, self)
        self.addToolBar(self.toolbar)

        self.apply_styles()

    def apply_styles(self) -> None:
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QToolBar {
                background-color: #2E2E2E;
                border-bottom: 1px solid #3E3E3E;
            }
            QStatusBar {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QToolButton {
                background-color: transparent;
                border: none;
            }
            QToolButton:hover {
                background-color: #3E3E3E;
            }
        """)
    
    def update_layers_list(self) -> None:
        """Atualiza a lista de camadas na interface."""
        self.main_layout.layers_panel.refresh_layers()

    def display_composited_image(self) -> None:
        """Atualiza a imagem composta exibida na interface."""
        self.controller.update_display()