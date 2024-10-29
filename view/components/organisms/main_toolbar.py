# view/components/organisms/main_toolbar.py

from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from typing import Callable

class MainToolbar(QToolBar):
    def __init__(self, controller, parent) -> None:
        super().__init__("Ferramentas", parent)
        self.setIconSize(QSize(24, 24))
        self.controller = controller

        self.create_actions()

    def create_actions(self) -> None:
        open_icon = QIcon("icons/open.png")
        open_action = self.addAction(open_icon, "Abrir Imagem")
        open_action.setStatusTip("Abrir uma imagem")
        open_action.triggered.connect(self.controller.controllers["file"].load_image)

        save_icon = QIcon("icons/save.png")
        save_action = self.addAction(save_icon, "Salvar Imagem")
        save_action.setStatusTip("Salvar a imagem atual")
        save_action.triggered.connect(self.controller.controllers["file"].save_image)
