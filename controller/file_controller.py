from PyQt5.QtWidgets import QMessageBox, QFileDialog
from abstracts.image_handler_abstract import AbstractImageHandler
from controller.controller_interface import Controller
from typing import Callable, Optional, List
import os
from view.components.atoms.status_bar import CustomStatusBar
from view.main_window import MainWindow

class FileController(Controller):
    last_directory = None

    def __init__(self, processor: AbstractImageHandler, controller, update_display: Callable[[], None]) -> None:
        self.processor = processor
        self.main_controller = controller
        self.update_display = update_display

    def show(self) -> None:
        if not FileController.last_directory:
            FileController.last_directory = self.get_initial_directory()

    def load_image(self) -> None:
        file_paths = self.select_image_file()
        if file_paths:
            print(f"FileController: {len(file_paths)} imagens carregadas: {file_paths}")
            for file_path in file_paths:
                self._load_image_to_processor(file_path)

    def _load_image_to_processor(self, file_path: str) -> None:
        qt_image = self.processor.load_image(file_path)
        print(f"FileController: Imagem no QImage para '{file_path}': {qt_image}")
        if qt_image and not qt_image.isNull():
            self.main_controller.controllers["layers"].add_image_layer(file_path, qt_image)
            self.update_display()
            self.get_my_component().showMessage(f"Imagem carregada: {file_path}")
        else:
            QMessageBox.critical(self.get_main_window(), "Erro", f"Não foi possível carregar a imagem: {file_path}.")

    def save_image(self) -> None:
        if not self.processor.layers:
            QMessageBox.warning(self.get_main_window(), "Aviso", "Nenhuma imagem para salvar.")
            return

        file_path = self.select_save_file()
        if file_path:
            self._save_image_to_path(file_path)

    def _save_image_to_path(self, file_path: str) -> None:
        composited_image = self.processor.get_composited_image()
        if composited_image is None or composited_image.isNull():
            QMessageBox.warning(self.get_main_window(), "Aviso", "Não há imagem composta para salvar.")
            return

        success = self.processor.save_image(composited_image, file_path)
        if success:
            self.get_my_component().showMessage(f"Imagem salva: {file_path}")
        else:
            QMessageBox.critical(self.get_main_window(), "Erro", "Não foi possível salvar a imagem.")

    def select_image_file(self) -> Optional[List[str]]:
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.get_main_window(),
            "Abrir Imagens",
            FileController.last_directory or self.get_initial_directory(),
            "Arquivos de Imagem (*.png *.jpg *.bmp)"
        )
        if file_paths:
            self.set_last_directory(os.path.dirname(file_paths[0]))
            return file_paths
        return None

    def select_save_file(self) -> Optional[str]:
        file_path, _ = QFileDialog.getSaveFileName(
            self.get_main_window(),
            "Salvar Imagem",
            FileController.last_directory or self.get_initial_directory(),
            "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)"
        )
        if file_path:
            self.set_last_directory(os.path.dirname(file_path))
            return file_path
        return None

    def get_initial_directory(self) -> str:
        home_dir = os.path.expanduser("~")
        potential_dirs = [
            os.path.join(home_dir, "Pictures"),
            os.path.join(home_dir, "pictures"),
            os.path.join(home_dir, "Images"),
            os.path.join(home_dir, "images"),
            os.path.join(home_dir, "Imagens"),
            os.path.join(home_dir, "imagens"),
        ]

        for directory in potential_dirs:
            if os.path.isdir(directory):
                return directory

        return home_dir

    @staticmethod
    def set_last_directory(directory: str) -> None:
        if os.path.isdir(directory):
            FileController.last_directory = directory
    
    def get_main_window(self) -> MainWindow:
        return self.main_controller.window
    
    def get_my_component(self) -> CustomStatusBar:
        return self.get_main_window().main_layout.status_bar
