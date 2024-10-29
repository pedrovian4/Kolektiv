from typing import Callable
from processors.image_processor import ImageProcessor
from .controller_interface import Controller

class HistoryController(Controller):
    def __init__(self, processor: ImageProcessor, update_display: Callable[[], None]) -> None:
        self.processor = processor
        self.update_display = update_display

    def show(self) -> None:
        pass
    
    def undo_action(self) -> None:
        if self.processor.undo():
            self.update_display()
        else:
            self._show_no_action_message("desfazer")

    def redo_action(self) -> None:
        if self.processor.redo():
            self.update_display()
        else:
            self._show_no_action_message("refazer")

    def _show_no_action_message(self, action: str) -> None:
        print(f"Não há ações para {action}")
