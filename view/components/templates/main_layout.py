# view/main_window.py

from typing import Optional
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QMenuBar, QAction
from PyQt5.QtCore import Qt
from view.components.atoms.image_label import ImageLabel
from view.components.atoms.status_bar import CustomStatusBar
from view.components.organisms.layers_panel import LayersPanel

class MainLayout(QWidget):
    def __init__(self, controller, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.menu_bar = QMenuBar(self)
        self.setup_menus()
        main_layout.addWidget(self.menu_bar)

        splitter = QSplitter(Qt.Horizontal, self)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #1E1E1E;
            }
        """)
        
        self.image_label = ImageLabel(self)
        splitter.addWidget(self.image_label)

        self.layers_panel = LayersPanel(self.controller.controllers['layers'], self)
        splitter.addWidget(self.layers_panel)

        splitter.setSizes([950, 250]) 

        main_layout.addWidget(splitter)

        self.status_bar = CustomStatusBar(self)
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)
        self.apply_styles()

    def setup_menus(self) -> None:
        edit_menu = self.menu_bar.addMenu("Editar")

        self.undo_action = QAction("Desfazer", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setEnabled(False)
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("Refazer", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)


    def apply_styles(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
            }
            QLabel#image_label {
                background-color: #2E2E2E;
                border: none;
            }
            QListWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                border: none;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #3E3E3E;
            }
            QListWidget::item:selected {
                background-color: #3E3E3E;
            }
            QLabel {
                color: #FFFFFF;
            }
            QMenuBar {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #3E3E3E;
            }
            QMenu {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QMenu::item:selected {
                background-color: #3E3E3E;
            }
        """)
    def refresh_layers(self) -> None:
        self.clear_layers_list()
        for layer in self.layer_controller.layer_manager.get_layers():
            self.add_layer_to_list(layer.name, layer.visible)