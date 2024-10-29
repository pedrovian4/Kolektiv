from PyQt5.QtWidgets import QMenu, QWidget, QListWidgetItem, QDialog
from view.components.molecules.blur_settings_dialog import BlurSettingsDialog

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

    def handle_action(self, action, item: QListWidgetItem) -> None:
        current_row = self.parent_widget.layers_list.row(item)
        layer_name = item.text()
        

        if action == self.remove_action:
            confirmed = self.controller.confirm_layer_removal(layer_name)
            if confirmed:
                self.parent_widget.layers_list.takeItem(current_row)
                self.controller.delete_layer(current_row)
        elif action == self.apply_blur_action:
            dialog = BlurSettingsDialog(self, title="Blur", gaussian=False)
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
            dialog = BlurSettingsDialog(self, title="Blur Mediano", gaussian=False)
            if dialog.exec_():
                values = dialog.get_values()
                if values == (None, None):
                    return
                kernel_size, sigma = values
                self.controller.apply_blur(layer_index=current_row, blur_type="median", kernel_size=kernel_size)
