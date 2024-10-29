# view/components/molecules/sharpen_settings_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class SharpenSettingsDialog(QDialog):
    def __init__(self, parent=None, title="Configurar Nitidez") -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.kernel_size = 5
        self.sigma = 1.0
        self.amount = 1.0
        self.threshold = 0.0
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        kernel_label = QLabel("Tamanho do Kernel:", self)
        layout.addWidget(kernel_label)
        self.kernel_slider = QSlider(Qt.Horizontal, self)
        self.kernel_slider.setRange(1, 99)
        self.kernel_slider.setSingleStep(2)
        self.kernel_slider.setValue(self.kernel_size)
        self.kernel_slider.valueChanged.connect(self.update_kernel_size)
        layout.addWidget(self.kernel_slider)

        sigma_label = QLabel("Sigma:", self)
        layout.addWidget(sigma_label)
        self.sigma_slider = QSlider(Qt.Horizontal, self)
        self.sigma_slider.setRange(1, 100)
        self.sigma_slider.setSingleStep(1)
        self.sigma_slider.setValue(int(self.sigma * 10))
        self.sigma_slider.valueChanged.connect(self.update_sigma)
        layout.addWidget(self.sigma_slider)

        amount_label = QLabel("Quantidade:", self)
        layout.addWidget(amount_label)
        self.amount_slider = QSlider(Qt.Horizontal, self)
        self.amount_slider.setRange(1, 500)
        self.amount_slider.setSingleStep(1)
        self.amount_slider.setValue(int(self.amount * 100))
        self.amount_slider.valueChanged.connect(self.update_amount)
        layout.addWidget(self.amount_slider)

        threshold_label = QLabel("Limite:", self)
        layout.addWidget(threshold_label)
        self.threshold_slider = QSlider(Qt.Horizontal, self)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setSingleStep(1)
        self.threshold_slider.setValue(int(self.threshold))
        self.threshold_slider.valueChanged.connect(self.update_threshold)
        layout.addWidget(self.threshold_slider)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Confirmar", self)
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def update_kernel_size(self, value: int) -> None:
        self.kernel_size = value if value % 2 != 0 else value + 1
        print(f"SharpenSettingsDialog: Tamanho do Kernel atualizado para {self.kernel_size}")

    def update_sigma(self, value: int) -> None:
        self.sigma = value / 10.0
        print(f"SharpenSettingsDialog: Sigma atualizado para {self.sigma}")

    def update_amount(self, value: int) -> None:
        self.amount = value / 100.0
        print(f"SharpenSettingsDialog: Quantidade atualizada para {self.amount}")

    def update_threshold(self, value: int) -> None:
        self.threshold = value
        print(f"SharpenSettingsDialog: Limite atualizado para {self.threshold}")

    def get_values(self) -> tuple:
        return self.kernel_size, self.sigma, self.amount, self.threshold
