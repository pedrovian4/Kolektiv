from PyQt5.QtWidgets import QSlider, QWidget
from PyQt5.QtCore import Qt
from typing import Callable, Optional

class ValidatedSlider(QSlider):
    def __init__(
        self,
        orientation: Qt.Orientation = Qt.Horizontal,
        min_val: int = 1,
        max_val: int = 99,
        step: int = 1,
        validation_fn: Optional[Callable[[int], bool]] = None,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(orientation, parent)
        self.setRange(min_val, max_val)
        self.setSingleStep(step)
        self.validation_fn = validation_fn or (lambda x: True)
        self.valueChanged.connect(self.validate_value)

    def validate_value(self, value: int) -> None:
        if not self.validation_fn(value):
            self.setValue(self.value() + self.singleStep())
