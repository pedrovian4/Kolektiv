from PyQt5.QtWidgets import QMenu, QWidget, QListWidgetItem, QDialog, QMessageBox
from view.components.molecules.blur_settings_dialog import BlurSettingsDialog
from view.components.molecules.edge_detection_dialog import EdgeDetectionSettingsDialog
from view.components.molecules.highpass_settings_dialog import HighpassSettingsDialog
from view.components.molecules.laplacian_dialog import LaplacianSettingsDialog
from view.components.molecules.sharpen_setting_dialog import SharpenSettingsDialog
from view.components.molecules.transform_dialog import TransformSettingsDialog

class LayersContextMenu(QMenu):
    def __init__(self, controller, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.parent_widget = parent
        self.create_actions()

    def create_actions(self) -> None:
        self.remove_action = self.addAction("Remover Camada")
        self.apply_blur_action = self.addAction("Aplicar Blur")
        self.apply_gaussian_blur_action = self.addAction("Aplicar Gaussian Blur")
        self.apply_median_blur_action = self.addAction("Aplicar Blur Mediano")
        self.apply_sharpen_action = self.addAction("Aplicar Nitidez")
        self.apply_highpass_filter_action = self.addAction("Aplicar filtro de alta passagem")
        self.apply_laplacian_filter_action = self.addAction("Aplicar filtro laplaciano")
        self.edge_detection_menu = self.addMenu("Detecção de Bordas")
        self.apply_sobel_action = self.edge_detection_menu.addAction("Sobel")
        self.apply_prewitt_action = self.edge_detection_menu.addAction("Prewitt")
        self.apply_canny_action = self.edge_detection_menu.addAction("Canny")

        self.transform_menu = self.addMenu("Transformações")
        self.apply_scale_action = self.transform_menu.addAction("Escala")
        self.apply_rotate_action = self.transform_menu.addAction("Rotação")
        self.apply_translate_action = self.transform_menu.addAction("Translação")

    def handle_action(self, action, item: QListWidgetItem) -> None:
        current_row = self.parent_widget.layers_list.row(item)
        layer_name = item.text()
        
        if action == self.remove_action:
            confirmed = self.show_confirm_dialog(layer_name)
            if confirmed:
                self.parent_widget.layers_list.takeItem(current_row)
                self.controller.delete_layer(current_row)
        elif action == self.apply_blur_action:
            dialog = BlurSettingsDialog(self, title="Blur")
            if dialog.exec_():
                values = dialog.get_values()
                if values == (None, None):
                    return
                kernel_size, sigma = values

                self.controller.apply_blur(layer_index=current_row, blur_type="blur", kernel_size=kernel_size)
        elif action == self.apply_gaussian_blur_action:
            dialog = BlurSettingsDialog(self, title="Blur Gaussiano", gaussian=True)
            if dialog.exec_() == QDialog.Accepted:
                values = dialog.get_values()
                if values == (None, None):
                    return
                kernel_size, sigma = values
                self.controller.apply_blur(layer_index=current_row, blur_type="gaussian", kernel_size=kernel_size, sigma=sigma)
        elif action == self.apply_median_blur_action:
            dialog = BlurSettingsDialog(self, title="Blur Mediano")
            if dialog.exec_():
                values = dialog.get_values()
                if values == (None, None):
                    return
                kernel_size, _ = values
                self.controller.apply_blur(layer_index=current_row, blur_type="median", kernel_size=kernel_size)
        elif action == self.apply_sharpen_action:
            dialog = SharpenSettingsDialog(self, title="Nitidez")
            if dialog.exec_():
                values = dialog.get_values()
                kernel_size, sigma, amount, threshold = values
                self.controller.apply_sharpen(
                    layer_index=current_row,
                    kernel_size=kernel_size,
                    sigma=sigma,
                    amount=amount,
                    threshold=threshold
                )
                
        elif action == self.apply_highpass_filter_action:
            dialog = HighpassSettingsDialog(self, title="Highpass Filter")
            if dialog.exec_():
                values = dialog.get_values()
                kernel_size, sigma, threshold = values
                self.controller.apply_highpass_filter(
                    layer_index=current_row,
                    kernel_size=kernel_size,
                    sigma=sigma,
                    threshold=threshold
                )
        elif action == self.apply_laplacian_filter_action:
            dialog = LaplacianSettingsDialog(self, title="Filtro Laplaciano")
            if dialog.exec_():
                kernel_size, scale, delta, border_type = dialog.get_values()
                self.controller.apply_laplacian_filter(
                    layer_index=current_row,
                    kernel_size=kernel_size,
                    scale=scale,
                    delta = delta,
                    border_type = border_type
                )
        elif action == self.apply_sobel_action:
            dialog = EdgeDetectionSettingsDialog(self, title="Sobel Edge Detection", method="sobel")
            if dialog.exec_():
                params = dialog.get_values()
                self.controller.apply_edge_detection(
                    layer_index=current_row,
                    method="sobel",
                    **params
                )
        elif action == self.apply_prewitt_action:
            dialog = EdgeDetectionSettingsDialog(self, title="Prewitt Edge Detection", method="prewitt")
            if dialog.exec_():
                params = dialog.get_values()
                self.controller.apply_edge_detection(
                    layer_index=current_row,
                    method="prewitt",
                    **params
                )
        elif action == self.apply_canny_action:
            dialog = EdgeDetectionSettingsDialog(self, title="Canny Edge Detection", method="canny")
            if dialog.exec_():
                params = dialog.get_values()
                self.controller.apply_edge_detection(
                    layer_index=current_row,
                    method="canny",
                    **params
                )
                
        elif action == self.apply_scale_action:
            dialog = TransformSettingsDialog(self, title="Escala", transform_type="scale")
            if dialog.exec_():
                params = dialog.get_values()
                self.controller.apply_transform(
                    layer_index=current_row,
                    transform_type="scale",
                    **params
                )
        elif action == self.apply_rotate_action:
            dialog = TransformSettingsDialog(self, title="Rotação", transform_type="rotate")
            if dialog.exec_():
                params = dialog.get_values()
                self.controller.apply_transform(
                    layer_index=current_row,
                    transform_type="rotate",
                    **params
                )
        elif action == self.apply_translate_action:
            dialog = TransformSettingsDialog(self, title="Translação", transform_type="translate")
            if dialog.exec_():
                params = dialog.get_values()
                self.controller.apply_transform(
                    layer_index=current_row,
                    transform_type="translate",
                    **params
                )
                
    def show_confirm_dialog(self, layer_name: str) -> bool:
        msg_box = QMessageBox(self.parent_widget)
        msg_box.setWindowTitle("Remover Camada")
        msg_box.setText(f"Tem certeza que deseja remover a camada '{layer_name}'?")
        msg_box.setIcon(QMessageBox.Question)

        sim_button = msg_box.addButton("Sim", QMessageBox.AcceptRole)
        nao_button = msg_box.addButton("Não", QMessageBox.RejectRole)

        msg_box.setDefaultButton(nao_button)

        msg_box.exec_()

        if msg_box.clickedButton() == sim_button:
            return True
        else:
            return False
