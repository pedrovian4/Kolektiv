# controller/layer_controller.py

import os
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from view.components.atoms.status_bar import CustomStatusBar
from view.components.organisms.layers_panel import LayersPanel
from view.main_window import MainWindow
from .controller_interface import Controller
from typing import Callable
from managers.layer_manager import LayerManager 
from controller.blur_controller import BlurController

class LayerController(Controller):
    def __init__(self, layer_manager: LayerManager, controller, blur_controller: BlurController) -> None:
        self.layer_manager = layer_manager
        self.main_controller = controller
        self.blur_controller = blur_controller

    def show(self) -> None:
        self.refresh_layers_panel()

    def add_image_layer(self, file_path: str, qt_image: QImage) -> None:
        layer_name = os.path.basename(file_path)
        print(f"LayerController: Adicionando camada '{layer_name}'")
        self.layer_manager.add_image_layer(file_path, qt_image)
        self.get_status_bar().showMessage(f"Camada adicionada: {layer_name}")
        self.get_layers_pannel().add_layer_to_list(layer_name, True)  
        self.refresh_layers_panel()
        self.main_controller.update_display()
   
    def delete_layer(self, index: int) -> None:
        try:
            removed_layer_name = self.layer_manager.delete_layer(index)
            self.get_status_bar().showMessage(f"Camada removida: {removed_layer_name}")
            self.refresh_layers_panel()
            self.main_controller.update_display()
        except IndexError:
            QMessageBox.warning(self.get_main_window(), "Erro", "Camada não encontrada")

    def toggle_layer_visibility(self, index: int) -> None:
        try:
            self.layer_manager.toggle_layer_visibility(index)
            layer = self.layer_manager.get_layer(index)
            item = self.get_layers_pannel().layers_list.item(index)
            if layer.visible:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.get_status_bar().showMessage(f"Visibilidade da camada '{layer.name}' alterada para {'Visível' if layer.visible else 'Oculto'}")
            self.refresh_layers_panel()
            self.main_controller.update_display()
        except IndexError:
            QMessageBox.warning(self.get_main_window(), "Erro", "Camada não encontrada")
                
    def reorder_layers(self, source: int, dest: int) -> None:
        try:
            self.layer_manager.reorder_layers(source, dest)
            self.refresh_layers_panel()
            self.main_controller.update_display()
        except IndexError:
            QMessageBox.warning(self.get_main_window(), "Erro", "Reordenação de camadas inválida")

    def set_layer_opacity(self, index: int, opacity: float) -> None:
        try:
            if not (0.0 <= opacity <= 1.0):
                raise ValueError("A opacidade deve estar entre 0.0 e 1.0.")

            layer = self.layer_manager.get_layer(index)
            layer.opacity = opacity
            self.refresh_layers_panel()
            self.get_status_bar().showMessage(f"Opacidade da camada '{layer.name}' alterada para {opacity * 100:.0f}%")
            self.main_controller.update_display()
        except IndexError:
            QMessageBox.warning(self.get_main_window(), "Erro", "Camada não encontrada")
        except ValueError as ve:
            QMessageBox.warning(self.get_main_window(), "Erro", str(ve))
    
    def confirm_layer_removal(self, layer_name: str) -> bool:
        reply = QMessageBox.question(
            self.get_main_window(),
            "Remover Camada",
            f"Tem certeza que deseja remover a camada '{layer_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def apply_blur(self, layer_index: int, blur_type: str, **kwargs) -> None:
        try:
            print(f"LayerController: Aplicando {blur_type} na camada {layer_index}")
            self.blur_controller.apply_blur_to_layer(layer_index, blur_type, **kwargs)
            layer = self.layer_manager.get_layer(layer_index)
            self.get_status_bar().showMessage(f"{blur_type.capitalize()} aplicado na camada '{layer.name}'")
            self.refresh_layers_panel()
            self.main_controller.update_display()
        except IndexError:
            QMessageBox.warning(self.get_main_window(), "Erro", "Camada não encontrada")
        except ValueError as ve:
            QMessageBox.warning(self.get_main_window(), "Erro", str(ve))

    def refresh_layers_panel(self) -> None:
        self.get_layers_pannel().clear_layers_list()
        for layer in self.layer_manager.get_layers():
            self.get_layers_pannel().add_layer_to_list(layer.name, layer.visible)

    def get_main_window(self) -> MainWindow:
        return self.main_controller.window
    
    def get_status_bar(self) -> CustomStatusBar:
        return self.get_main_window().main_layout.status_bar
    
    def get_layers_pannel(self) -> LayersPanel:
        return self.get_main_window().main_layout.layers_panel
