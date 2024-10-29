from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt

class LayerListItem(QListWidgetItem):
    def __init__(self, name: str, visible: bool = True) -> None:
        super().__init__(name)
        self.setFlags(
            self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled
        )
        self.setCheckState(Qt.Checked if visible else Qt.Unchecked)
    def is_visible(self) -> bool:
        return self.checkState() == Qt.Checked