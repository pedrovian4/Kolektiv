from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSlider,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QComboBox
)
from PyQt5.QtCore import Qt
import cv2

class TransformSettingsDialog(QDialog):
    def __init__(self, parent=None, title="Configurar Transformação", transform_type="scale") -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.transform_type = transform_type.lower()
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        if self.transform_type == "scale":
            scale_x_label = QLabel("Fator de Escala X:", self)
            layout.addWidget(scale_x_label)
            self.scale_x_input = QLineEdit(self)
            self.scale_x_input.setText("1.0")
            layout.addWidget(self.scale_x_input)

            scale_y_label = QLabel("Fator de Escala Y:", self)
            layout.addWidget(scale_y_label)
            self.scale_y_input = QLineEdit(self)
            self.scale_y_input.setText("1.0")
            layout.addWidget(self.scale_y_input)

            interpolation_label = QLabel("Método de Interpolação:", self)
            layout.addWidget(interpolation_label)
            self.interpolation_combo = QComboBox(self)
            self.interpolation_combo.addItems([
                "INTER_NEAREST",
                "INTER_LINEAR",
                "INTER_CUBIC",
                "INTER_AREA",
                "INTER_LANCZOS4"
            ])
            self.interpolation_combo.setCurrentText("INTER_LINEAR")
            layout.addWidget(self.interpolation_combo)

        elif self.transform_type == "rotate":
            angle_label = QLabel("Ângulo de Rotação (graus):", self)
            layout.addWidget(angle_label)
            self.angle_input = QLineEdit(self)
            self.angle_input.setText("0.0")
            layout.addWidget(self.angle_input)

            scale_label = QLabel("Fator de Escala:", self)
            layout.addWidget(scale_label)
            self.scale_input = QLineEdit(self)
            self.scale_input.setText("1.0")
            layout.addWidget(self.scale_input)

            center_label = QLabel("Centro da Rotação (x, y) [Opcional]:", self)
            layout.addWidget(center_label)
            self.center_input = QLineEdit(self)
            self.center_input.setPlaceholderText("Ex: 100,200")
            layout.addWidget(self.center_input)

            interpolation_label = QLabel("Método de Interpolação:", self)
            layout.addWidget(interpolation_label)
            self.interpolation_combo = QComboBox(self)
            self.interpolation_combo.addItems([
                "INTER_NEAREST",
                "INTER_LINEAR",
                "INTER_CUBIC",
                "INTER_AREA",
                "INTER_LANCZOS4"
            ])
            self.interpolation_combo.setCurrentText("INTER_LINEAR")
            layout.addWidget(self.interpolation_combo)

        elif self.transform_type == "translate":
            shift_x_label = QLabel("Deslocamento X (pixels):", self)
            layout.addWidget(shift_x_label)
            self.shift_x_input = QLineEdit(self)
            self.shift_x_input.setText("0")
            layout.addWidget(self.shift_x_input)

            shift_y_label = QLabel("Deslocamento Y (pixels):", self)
            layout.addWidget(shift_y_label)
            self.shift_y_input = QLineEdit(self)
            self.shift_y_input.setText("0")
            layout.addWidget(self.shift_y_input)

            border_label = QLabel("Modo de Borda:", self)
            layout.addWidget(border_label)
            self.border_combo = QComboBox(self)
            self.border_combo.addItems([
                "BORDER_CONSTANT",
                "BORDER_REPLICATE",
                "BORDER_REFLECT",
                "BORDER_REFLECT_101",
                "BORDER_WRAP",
                "BORDER_REFLECT101",
                "BORDER_TRANSPARENT",
                "BORDER_ISOLATED"
            ])
            self.border_combo.setCurrentText("BORDER_CONSTANT")
            layout.addWidget(self.border_combo)

            self.border_value_label = QLabel("Valor da Borda (R, G, B, A):", self)
            layout.addWidget(self.border_value_label)
            self.border_value_input = QLineEdit(self)
            self.border_value_input.setPlaceholderText("Ex: 0,0,0,0")
            self.border_value_input.setText("0,0,0,0")
            layout.addWidget(self.border_value_input)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Confirmar", self)
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def get_values(self) -> dict:
        if self.transform_type == "scale":
            try:
                scale_x = float(self.scale_x_input.text())
                scale_y = float(self.scale_y_input.text())
                interpolation_str = self.interpolation_combo.currentText()
                interpolation = getattr(cv2, interpolation_str, cv2.INTER_LINEAR)
                return {
                    "scale_x": scale_x,
                    "scale_y": scale_y,
                    "interpolation": interpolation
                }
            except ValueError:
                return {
                    "scale_x": 1.0,
                    "scale_y": 1.0,
                    "interpolation": cv2.INTER_LINEAR
                }
        elif self.transform_type == "rotate":
            try:
                angle = float(self.angle_input.text())
                scale = float(self.scale_input.text())
                center_text = self.center_input.text()
                if center_text:
                    center = tuple(map(int, center_text.split(',')))
                else:
                    center = None
                interpolation_str = self.interpolation_combo.currentText()
                interpolation = getattr(cv2, interpolation_str, cv2.INTER_LINEAR)
                return {
                    "angle": angle,
                    "scale": scale,
                    "center": center,
                    "interpolation": interpolation
                }
            except ValueError:
                return {
                    "angle": 0.0,
                    "scale": 1.0,
                    "center": None,
                    "interpolation": cv2.INTER_LINEAR
                }
        elif self.transform_type == "translate":
            try:
                shift_x = int(self.shift_x_input.text())
                shift_y = int(self.shift_y_input.text())
                border_mode_str = self.border_combo.currentText()
                border_mode = getattr(cv2, border_mode_str, cv2.BORDER_CONSTANT)
                border_value_text = self.border_value_input.text()
                border_value = tuple(map(int, border_value_text.split(','))) if border_value_text else (0, 0, 0, 0)
                return {
                    "shift_x": shift_x,
                    "shift_y": shift_y,
                    "border_mode": border_mode,
                    "border_value": border_value
                }
            except ValueError:
                return {
                    "shift_x": 0,
                    "shift_y": 0,
                    "border_mode": cv2.BORDER_CONSTANT,
                    "border_value": (0, 0, 0, 0)
                }
