from typing import List
from entities.layer import Layer
import copy

class HistoryProcessor:
    def __init__(self) -> None:
        self._history: List[List[Layer]] = []

    def save_state(self, layers: List[Layer]) -> None:
        self._history.append(copy.deepcopy(layers))

    def undo(self, layers: List[Layer]) -> List[Layer]:
        if self._history:
            return self._history.pop()
        return layers
