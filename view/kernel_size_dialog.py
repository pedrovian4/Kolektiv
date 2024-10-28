
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt

class KernelSizeDialog(QDialog):
    def __init__(self, parent=None, title="Selecionar Tamanho do Kernel", initial=5, min_val=1, max_val=99):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.kernel_size = initial

        layout = QVBoxLayout()

        self.label = QLabel(f"Tamanho do Kernel: {self.kernel_size}")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_val // 2)
        self.slider.setMaximum(max_val // 2)
        self.slider.setValue(self.kernel_size // 2)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        layout.addWidget(self.slider)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_slider_value_changed(self, value):
        self.kernel_size = 2 * value + 1
        self.label.setText(f"Tamanho do Kernel: {self.kernel_size}")

    def get_kernel_size(self):
        return self.kernel_size
