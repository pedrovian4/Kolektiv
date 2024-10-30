from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton, QHBoxLayout, QStyledItemDelegate, QStyle, QStyleOptionButton
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt5.QtGui import QIcon, QPainter
from typing import Optional, List
from view.components.atoms.label import Label

class LayerModel(QAbstractListModel):
    def __init__(self, layers: List[dict],controller,parent=None):
        super().__init__(parent)
        self.layers = layers
        self.controller = controller

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.layers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.layers):
            return None
        layer = self.layers[index.row()]
        if role == Qt.DisplayRole:
            return layer['name']
        if role == Qt.CheckStateRole:
            return Qt.Checked if layer['visible'] else Qt.Unchecked

    def setData(self, index, value, role=Qt.EditRole) -> bool:
        if not index.isValid():
            return False
        if role == Qt.CheckStateRole:
            visible = value == Qt.Checked
            self.layers[index.row()]['visible'] = visible
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            self.controller.toggle_layer_visibility(index.row())
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable

    def addLayer(self, name: str, visible: bool = True) -> None:
        self.beginInsertRows(QModelIndex(), len(self.layers), len(self.layers))
        self.layers.append({'name': name, 'visible': visible})
        self.endInsertRows()

    def removeLayer(self, row: int) -> None:
        if 0 <= row < len(self.layers):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.layers[row]
            self.endRemoveRows()


class LayerDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionButton, index: QModelIndex) -> None:
        super().paint(painter, option, index)
        layer_visible = index.data(Qt.CheckStateRole) == Qt.Checked
        icon = QIcon("icons/eye-open.png" if layer_visible else "icons/eye-closed.png")
        icon_rect = option.rect.adjusted(option.rect.width() - 30, 5, -5, -5)
        icon.paint(painter, icon_rect)

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease:
            new_visibility = not (index.data(Qt.CheckStateRole) == Qt.Checked)
            model.setData(index, Qt.Checked if new_visibility else Qt.Unchecked, Qt.CheckStateRole)
            model.controller.toggle_layer_visibility(index.row())
        return super().editorEvent(event, model, option, index)



class LayersPanel(QWidget):
    def __init__(self, controller, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.layers = []
        self.model = LayerModel(self.layers, controller)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        label = Label("Pilha", self)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(label)

        self.layers_list = QListView(self)
        self.layers_list.setModel(self.model)
        self.layers_list.setItemDelegate(LayerDelegate())
        self.layers_list.setSelectionMode(QListView.SingleSelection)
        layout.addWidget(self.layers_list)

        buttons_layout = QHBoxLayout()
        
        """         
            add_button = QPushButton()
            add_button.setIcon(QIcon("icons/circle-plus.png"))
            add_button.setToolTip("Adicionar camada")
            add_button.clicked.connect(lambda: self.model.addLayer("Nova Camada"))
         """
        delete_button = QPushButton()
        delete_button.setIcon(QIcon("icons/x.png"))
        delete_button.setToolTip("Deletar camada")
        delete_button.clicked.connect(self.delete_selected_layer)

        buttons_layout.addWidget(delete_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def delete_selected_layer(self):
        index = self.layers_list.currentIndex()
        if index.isValid():
            self.controller.delete_layer(index.row()) 
