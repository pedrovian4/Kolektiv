from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class BlurSettingsDialog(QDialog):
    def __init__(self, parent=None, title="Configurar Blur", gaussian = False) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.kernel_size = 5
        self.sigma = 1.0
        self.gaussian = gaussian
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        intensity_label = QLabel("Intensidade (Kernel):", self)
        layout.addWidget(intensity_label)
        self.intensity_slider = QSlider(Qt.Horizontal, self)
        self.intensity_slider.setRange(1, 99)
        self.intensity_slider.setSingleStep(2)
        self.intensity_slider.setValue(self.kernel_size)
        self.intensity_slider.valueChanged.connect(self.update_kernel_size)
        layout.addWidget(self.intensity_slider)

        if(self.gaussian):
            sharpness_label = QLabel("Nitidez (Sigma):", self)
            layout.addWidget(sharpness_label)
            self.sharpness_slider = QSlider(Qt.Horizontal, self)
            self.sharpness_slider.setRange(0, 100)
            self.sharpness_slider.setSingleStep(1)
            self.sharpness_slider.setValue(int(self.sigma * 10))
            self.sharpness_slider.valueChanged.connect(self.update_sigma)
            layout.addWidget(self.sharpness_slider)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Confirmar", self)
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def update_kernel_size(self, value: int) -> None:
        """Atualiza o tamanho do kernel baseado no valor do slider."""
        self.kernel_size = value if value % 2 != 0 else value + 1

    def update_sigma(self, value: int) -> None:
        """Atualiza o sigma baseado no valor do slider."""
        self.sigma = value / 10.0

    def get_values(self) -> tuple:
        """Retorna os valores configurados de kernel size e sigma."""
        return self.kernel_size, self.sigma
