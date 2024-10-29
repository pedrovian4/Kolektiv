# view/components/molecules/edge_detection_settings_dialog.py

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

class EdgeDetectionSettingsDialog(QDialog):
    def __init__(self, parent=None, title="Configurar Detecção de Bordas", method="sobel") -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.method = method.lower()
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        if self.method == "sobel":
            dx_label = QLabel("Ordem da Derivada em X:", self)
            layout.addWidget(dx_label)
            self.dx_slider = QSlider(Qt.Horizontal, self)
            self.dx_slider.setRange(0, 2)
            self.dx_slider.setSingleStep(1)
            self.dx_slider.setValue(1)
            self.dx_slider.valueChanged.connect(self.update_dx)
            layout.addWidget(self.dx_slider)

            dy_label = QLabel("Ordem da Derivada em Y:", self)
            layout.addWidget(dy_label)
            self.dy_slider = QSlider(Qt.Horizontal, self)
            self.dy_slider.setRange(0, 2)
            self.dy_slider.setSingleStep(1)
            self.dy_slider.setValue(1)
            self.dy_slider.valueChanged.connect(self.update_dy)
            layout.addWidget(self.dy_slider)

            ksize_label = QLabel("Tamanho do Kernel (Ímpar):", self)
            layout.addWidget(ksize_label)
            self.ksize_slider = QSlider(Qt.Horizontal, self)
            self.ksize_slider.setRange(1, 31)
            self.ksize_slider.setSingleStep(2)
            self.ksize_slider.setValue(3)
            self.ksize_slider.valueChanged.connect(self.update_ksize)
            layout.addWidget(self.ksize_slider)

        elif self.method == "prewitt":
            axis_label = QLabel("Eixo de Detecção:", self)
            layout.addWidget(axis_label)
            self.axis_combo = QComboBox(self)
            self.axis_combo.addItems(["X", "Y", "Ambos"])
            self.axis_combo.currentTextChanged.connect(self.update_axis)
            layout.addWidget(self.axis_combo)

            ksize_label = QLabel("Tamanho do Kernel (Ímpar):", self)
            layout.addWidget(ksize_label)
            self.ksize_slider = QSlider(Qt.Horizontal, self)
            self.ksize_slider.setRange(1, 31)
            self.ksize_slider.setSingleStep(2)
            self.ksize_slider.setValue(3)
            self.ksize_slider.valueChanged.connect(self.update_ksize)
            layout.addWidget(self.ksize_slider)

        elif self.method == "canny":

            threshold1_label = QLabel("Limiar Inferior:", self)
            layout.addWidget(threshold1_label)
            self.threshold1_slider = QSlider(Qt.Horizontal, self)
            self.threshold1_slider.setRange(0, 500)
            self.threshold1_slider.setSingleStep(1)
            self.threshold1_slider.setValue(100)
            self.threshold1_slider.valueChanged.connect(self.update_threshold1)
            layout.addWidget(self.threshold1_slider)

            threshold2_label = QLabel("Limiar Superior:", self)
            layout.addWidget(threshold2_label)
            self.threshold2_slider = QSlider(Qt.Horizontal, self)
            self.threshold2_slider.setRange(0, 500)
            self.threshold2_slider.setSingleStep(1)
            self.threshold2_slider.setValue(200)
            self.threshold2_slider.valueChanged.connect(self.update_threshold2)
            layout.addWidget(self.threshold2_slider)

            aperture_label = QLabel("Tamanho da Janela de Apertura:", self)
            layout.addWidget(aperture_label)
            self.aperture_slider = QSlider(Qt.Horizontal, self)
            self.aperture_slider.setRange(3, 7)
            self.aperture_slider.setSingleStep(2)
            self.aperture_slider.setValue(3)
            self.aperture_slider.valueChanged.connect(self.update_aperture)
            layout.addWidget(self.aperture_slider)

            self.l2_checkbox = QComboBox(self)
            self.l2_checkbox.addItems(["False", "True"])
            self.l2_checkbox.setCurrentText("False")
            self.l2_checkbox.currentTextChanged.connect(self.update_l2)
            l2_label = QLabel("Gradiente L2:", self)
            layout.addWidget(l2_label)
            layout.addWidget(self.l2_checkbox)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Confirmar", self)
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def update_dx(self, value: int) -> None:
        self.dx = value
        print(f"EdgeDetectionSettingsDialog: Ordem da Derivada em X atualizada para {self.dx}")

    def update_dy(self, value: int) -> None:
        self.dy = value
        print(f"EdgeDetectionSettingsDialog: Ordem da Derivada em Y atualizada para {self.dy}")

    def update_ksize(self, value: int) -> None:
        self.ksize = value if value % 2 != 0 else value + 1
        self.ksize_slider.setValue(self.ksize)
        print(f"EdgeDetectionSettingsDialog: Tamanho do Kernel atualizado para {self.ksize}")

    def update_axis(self, text: str) -> None:
        self.axis = text.lower()
        print(f"EdgeDetectionSettingsDialog: Eixo de Detecção atualizado para {self.axis}")

    def update_threshold1(self, value: int) -> None:
        self.threshold1 = value
        print(f"EdgeDetectionSettingsDialog: Limiar Inferior atualizado para {self.threshold1}")

    def update_threshold2(self, value: int) -> None:
        self.threshold2 = value
        print(f"EdgeDetectionSettingsDialog: Limiar Superior atualizado para {self.threshold2}")

    def update_aperture(self, value: int) -> None:
        self.apertureSize = value
        print(f"EdgeDetectionSettingsDialog: Tamanho da Janela de Apertura atualizado para {self.apertureSize}")

    def update_l2(self, text: str) -> None:
        self.L2gradient = text.lower() == "true"
        print(f"EdgeDetectionSettingsDialog: Gradiente L2 atualizado para {self.L2gradient}")

    def get_values(self) -> dict:
        """
        Retorna os valores configurados com base no método selecionado.
        """
        if self.method == "sobel":
            return {
                "dx": getattr(self, 'dx', 1),
                "dy": getattr(self, 'dy', 1),
                "ksize": getattr(self, 'ksize', 3),
                "border_type": "BORDER_DEFAULT"
            }
        elif self.method == "prewitt":
            return {
                "axis": getattr(self, 'axis', 'both'),
                "ksize": getattr(self, 'ksize', 3),
                "border_type": "BORDER_DEFAULT"
            }
        elif self.method == "canny":
            return {
                "threshold1": getattr(self, 'threshold1', 100.0),
                "threshold2": getattr(self, 'threshold2', 200.0),
                "apertureSize": getattr(self, 'apertureSize', 3),
                "L2gradient": getattr(self, 'L2gradient', False)
            }
