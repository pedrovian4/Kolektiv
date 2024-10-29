from PyQt5.QtWidgets import QAction
from atoms.icon_button import IconButton
from typing import Callable, Optional

class ToolbarButton(IconButton):
    def __init__(
        self,
        icon_path: str,
        text: str,
        parent,
        callback: Callable[[], None],
        tooltip: Optional[str] = None
    ) -> None:
        super().__init__(icon_path, text, parent, callback, tooltip)
