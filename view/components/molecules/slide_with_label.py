from PyQt5.QtWidgets import QVBoxLayout, QWidget
from atoms.slider import ValidatedSlider
from atoms.label import TextLabel
from typing import Callable, Optional

class SliderWithLabel(QWidget):
    def __init__(
        self, 
        min_val: int, 
        max_val: int, 
        step: int, 
        validation_fn: Optional[Callable[[int], bool]] = None, 
        label_text: str = "Valor:", 
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.label = TextLabel(label_text, self)
        layout.addWidget(self.label)

        self.slider = ValidatedSlider(min_val=min_val, max_val=max_val, step=step, validation_fn=validation_fn, parent=self)
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

    def update_label(self, value: int) -> None:
        self.label.setText(f"Valor: {value}")

    def get_value(self) -> int:
        return self.slider.value()
