from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from typing import Optional
from view.components.atoms.label import Label
from view.components.molecules.layer_list_item import LayerListItem
from view.components.organisms.layers_context_menu import LayersContextMenu

class LayersPanel(QWidget):
    def __init__(self, controller, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        label = Label("Camadas", self)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(label)

        self.setup_layers_list()
        layout.addWidget(self.layers_list)
        layout.addStretch()

        self.setLayout(layout)

    def setup_layers_list(self) -> None:
        self.layers_list = QListWidget(self)
        self.layers_list.setSelectionMode(QListWidget.SingleSelection)
        self.layers_list.setDragEnabled(True)
        self.layers_list.setAcceptDrops(True)
        self.layers_list.setDragDropMode(QListWidget.InternalMove)

        self.layers_list.model().rowsMoved.connect(self.on_layers_reordered)
        self.layers_list.itemChanged.connect(self.on_layer_visibility_changed)
        self.layers_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.layers_list.customContextMenuRequested.connect(self.open_context_menu)

    def add_layer_to_list(self, name: str, visible: bool = True) -> None:
        print(f"LayersPanel: Adicionando camada '{name}' com visibilidade {visible}.")
        item = LayerListItem(name, visible)
        self.layers_list.addItem(item)

    def clear_layers_list(self) -> None:
        print("LayersPanel: Limpando todas as camadas da interface.")
        self.layers_list.clear()

    def on_layer_visibility_changed(self, item: QListWidgetItem) -> None:
        index = self.layers_list.row(item)
        visible = item.checkState() == Qt.Checked
        print(f"LayersPanel: Camada '{item.text()}' visibilidade alterada para {visible}")
        self.controller.toggle_layer_visibility(index)

    def on_layers_reordered(self, source_parent, source_start: int, source_end: int, dest_parent, dest_row: int) -> None:
        print(f"LayersPanel: Camadas reordenadas de {source_start} para {dest_row}")
        self.controller.reorder_layers(source_start, dest_row)

    def open_context_menu(self, position) -> None:
        item = self.layers_list.itemAt(position)
        if item:
            context_menu = LayersContextMenu(self.controller, self)
            action = context_menu.exec_(self.layers_list.viewport().mapToGlobal(position))
            if action:
                context_menu.handle_action(action, item)
