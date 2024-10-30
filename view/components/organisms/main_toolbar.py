from PyQt5.QtWidgets import QToolBar, QWidget, QSizePolicy
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

class MainToolbar(QToolBar):
    def __init__(self, controller, parent) -> None:
        super().__init__("Ferramentas", parent)
        self.setIconSize(QSize(16, 16))
        self.controller = controller

        self.create_actions()

    def create_actions(self) -> None:
        self.add_spacing()

        open_icon = QIcon("icons/open.png")
        self.open_action = self.addAction(open_icon, "Abrir Imagem")
        self.open_action.triggered.connect(self.controller.controllers["file"].load_image)

        save_icon = QIcon("icons/save.png")
        self.save_action = self.addAction(save_icon, "Salvar Imagem")
        self.save_action.triggered.connect(self.controller.controllers["file"].save_image)

        self.add_spacing()

        undo_icon = QIcon("icons/undo.png")
        self.undo_action = self.addAction(undo_icon, "Desfazer")
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self.controller.history_manager.undo_action)

        redo_icon = QIcon("icons/redo.png")
        self.redo_action = self.addAction(redo_icon, "Refazer")
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(self.controller.history_manager.redo_action)

        self.add_spacing()

        cut_icon = QIcon("icons/scissors.png")
        self.cut_action = self.addAction(cut_icon, "Corta imagem")
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(lambda: print("Cortar ação ativada"))

        copy_icon = QIcon("icons/copy.png")
        self.copy_action = self.addAction(copy_icon, "Copiar imagem")
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(lambda: print("Copiar ação ativada"))

        paste_icon = QIcon("icons/paste.png")
        self.paste_action = self.addAction(paste_icon, "Colar Imagem")
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(lambda: print("Colar ação ativada"))

        self.add_spacing()

        rotate_ccw_icon = QIcon("icons/rotate-ccw.png")
        self.rotate_ccw_action = self.addAction(rotate_ccw_icon, "Girar imagem sentido Anti-horário")
        self.rotate_ccw_action.setShortcut("Ctrl+CCW")
        self.rotate_ccw_action.triggered.connect(lambda: print("Girar imagens no sentido Anti-horario"))

        rotate_cw_icon = QIcon("icons/rotate-cw.png")
        self.rotate_cw_action = self.addAction(rotate_cw_icon, "Girar imagem sentido horário")
        self.rotate_cw_action.setShortcut("Ctrl+CW")
        self.rotate_cw_action.triggered.connect(lambda: print("Girar imagens no sentido horario"))

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

        help_icon = QIcon("icons/circle-help.png")
        self.help_action = self.addAction(help_icon, "Precisando de ajuda?")
        self.help_action.triggered.connect(lambda: print("Abrir ferramentas de ajuda"))

    def add_spacing(self):
        spacer = QWidget()
        spacer.setFixedWidth(5)
        self.addWidget(spacer)
