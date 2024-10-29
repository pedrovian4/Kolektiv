from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSlider,
    QPushButton,
    QHBoxLayout,
    QComboBox
)
from PyQt5.QtCore import Qt

class LaplacianSettingsDialog(QDialog):
    def __init__(self, parent=None, title="Configurar Filtro Laplaciano") -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.kernel_size = 3
        self.scale = 1.0
        self.delta = 0.0
        self.border_type = 'BORDER_DEFAULT'
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        kernel_label = QLabel("Tamanho do Kernel (Ímpar):", self)
        layout.addWidget(kernel_label)
        self.kernel_slider = QSlider(Qt.Horizontal, self)
        self.kernel_slider.setRange(1, 99)
        self.kernel_slider.setSingleStep(2)
        self.kernel_slider.setValue(self.kernel_size)
        self.kernel_slider.valueChanged.connect(self.update_kernel_size)
        layout.addWidget(self.kernel_slider)

        scale_label = QLabel("Escala:", self)
        layout.addWidget(scale_label)
        self.scale_slider = QSlider(Qt.Horizontal, self)
        self.scale_slider.setRange(1, 100)
        self.scale_slider.setSingleStep(1)
        self.scale_slider.setValue(int(self.scale * 10))
        self.scale_slider.valueChanged.connect(self.update_scale)
        layout.addWidget(self.scale_slider)

        delta_label = QLabel("Delta:", self)
        layout.addWidget(delta_label)
        self.delta_slider = QSlider(Qt.Horizontal, self)
        self.delta_slider.setRange(0, 255)
        self.delta_slider.setSingleStep(1)
        self.delta_slider.setValue(int(self.delta))
        self.delta_slider.valueChanged.connect(self.update_delta)
        layout.addWidget(self.delta_slider)

        border_label = QLabel("Tipo de Borda:", self)
        layout.addWidget(border_label)
        self.border_combo = QComboBox(self)
        self.border_types = {
            "Constante": "BORDER_CONSTANT",
            "Replicar": "BORDER_REPLICATE",
            "Refletir": "BORDER_REFLECT",
            "Refletir 101": "BORDER_REFLECT_101",
            "Wrap": "BORDER_WRAP"
        }
        for name in self.border_types.keys():
            self.border_combo.addItem(name)
        self.border_combo.setCurrentText("Refletir")
        self.border_combo.currentTextChanged.connect(self.update_border_type)
        layout.addWidget(self.border_combo)

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
        self.kernel_slider.setValue(self.kernel_size)
        print(f"LaplacianSettingsDialog: Tamanho do Kernel atualizado para {self.kernel_size}")

    def update_scale(self, value: int) -> None:
        self.scale = value / 10.0
        print(f"LaplacianSettingsDialog: Escala atualizada para {self.scale}")

    def update_delta(self, value: int) -> None:
        self.delta = value
        print(f"LaplacianSettingsDialog: Delta atualizado para {self.delta}")

    def update_border_type(self, text: str) -> None:
        self.border_type = self.border_types.get(text, "BORDER_DEFAULT")
        print(f"LaplacianSettingsDialog: Tipo de Borda atualizado para {self.border_type}")

    def get_values(self) -> tuple:
        return self.kernel_size, self.scale, self.delta, self.border_type
