from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from typing import Callable, Optional

class IconButton(QAction):
    def __init__(
        self,
        icon_path: str,
        text: str,
        parent,
        callback: Callable[[], None],
        tooltip: Optional[str] = None
    ) -> None:
        super().__init__(QIcon(icon_path), text, parent)
        self.setStatusTip(tooltip or text)
        self.triggered.connect(callback)
