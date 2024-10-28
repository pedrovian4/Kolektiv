import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QDialog
from view.main_window import MainWindow
from model.image_processor import ImageProcessor
from view.kernel_size_dialog import KernelSizeDialog


class MainController:
    def __init__(self):
        self.window = MainWindow(self)
        self.processor = ImageProcessor()
        self.image = None

    def show(self):
        self.window.show()

    def load_image(self):
        initial_dir = self.get_initial_directory()

        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Abrir Imagem",
            initial_dir,
            "Arquivos de Imagem (*.png *.jpg *.bmp)"
        )

        if file_path:
            qt_image = self.processor.load_image(file_path)
            if qt_image is not None:
                layer_name = os.path.basename(file_path)
                self.processor.add_layer(layer_name, qt_image)
                self.update_layers_list()
                self.display_composited_image()
                self.window.status_bar.showMessage(f"Imagem carregada: {file_path}")
            else:
                QMessageBox.critical(self.window, "Erro", "Não foi possível carregar a imagem selecionada.")

    def get_initial_directory(self):
        home_dir = os.path.expanduser("~")
        images_dir = os.path.join(home_dir, "images")
        imagens_dir = os.path.join(home_dir, "imagens")

        if os.path.isdir(images_dir):
            return images_dir
        elif os.path.isdir(imagens_dir):
            return imagens_dir
        else:
            return home_dir

    def display_composited_image(self):
        qt_image = self.processor.get_composited_image()
        if qt_image is not None:
            self.window.display_image(qt_image)
        else:
            self.window.clear_image()

    def update_layers_list(self):
        self.window.clear_layers_list()
        for layer in reversed(self.processor.layers):
            self.window.add_layer_to_list(layer.name, layer.visible)

    def move_layer_up(self, index):
        real_index = len(self.processor.layers) - 1 - index
        self.processor.move_layer_up(real_index)
        self.update_layers_list()
        self.display_composited_image()

    def move_layer_down(self, index):
        real_index = len(self.processor.layers) - 1 - index
        self.processor.move_layer_down(real_index)
        self.update_layers_list()
        self.display_composited_image()

    def toggle_layer_visibility(self, index):
        real_index = len(self.processor.layers) - 1 - index
        self.processor.toggle_layer_visibility(real_index)
        self.update_layers_list()
        self.display_composited_image()

    def save_image(self):
        if self.processor.layers:
            initial_dir = self.get_initial_directory()
            file_path, _ = QFileDialog.getSaveFileName(
                self.window,
                "Salvar Imagem",
                initial_dir,
                "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)"
            )
            if file_path:
                composited_image = self.processor.get_composited_image()
                success = self.processor.save_image(composited_image, file_path)
                if success:
                    self.window.status_bar.showMessage(f"Imagem salva: {file_path}")
                else:
                    QMessageBox.critical(self.window, "Erro", "Não foi possível salvar a imagem.")
        else:
            QMessageBox.warning(self.window, "Aviso", "Nenhuma imagem para salvar.")
    
    def reorder_layers(self, source_index, dest_index):
        source_real_index = len(self.processor.layers) - 1 - source_index
        dest_real_index = len(self.processor.layers) - 1 - dest_index

        layer = self.processor.layers.pop(source_real_index)
        self.processor.layers.insert(dest_real_index, layer)
        self.update_layers_list()
    
    def display_composited_image(self):
        qt_image = self.processor.get_composited_image()
        if qt_image is not None:
            self.window.display_image(qt_image)
        else:
            self.window.clear_image()

    def delete_layer(self, index):
        if 0 <= index < len(self.processor.layers):
            removed_layer = self.processor.layers[index].name  
            self.processor.remove_layer(index)
            self.update_layers_list()
            self.display_composited_image()
            self.window.status_bar.showMessage(f"Camada removida: {removed_layer}")
        else:
            QMessageBox.warning(self.window, "Erro", "Índice da camada inválido.")

    def apply_blur(self, layer_index=None):
        if layer_index is None:
            layer_index = len(self.processor.layers) - 1

        dialog = KernelSizeDialog(
            self.window,
            title="Aplicar Blur",
            initial=5,
            min_val=1,
            max_val=99
        )
        result = dialog.exec_()

        if result == QDialog.Accepted:
            kernel_size = dialog.get_kernel_size()
            print(f"Aplicando Blur com kernel_size={kernel_size}")
            try:
                self.processor.apply_blur(layer_index=layer_index, kernel_size=kernel_size)
                self.update_layers_list()
                self.display_composited_image()
                layer_name = self.processor.layers[layer_index].name
                self.window.status_bar.showMessage(f"Filtro de Blur aplicado na camada '{layer_name}' com kernel size={kernel_size}.")
            except IndexError as e:
                QMessageBox.critical(self.window, "Erro", str(e))
            except ValueError as ve:
                QMessageBox.critical(self.window, "Erro de Valor", str(ve))
    
    def apply_median_blur(self, layer_index=None):
        if layer_index is None:
            layer_index = len(self.processor.layers) - 1

        dialog = KernelSizeDialog(
            self.window,
            title="Aplicar Blur Mediano",
            initial=5,
            min_val=1,
            max_val=99
        )
        result = dialog.exec_()

        if result == QDialog.Accepted:
            kernel_size = dialog.get_kernel_size()
            print(f"Aplicando Blur com kernel_size={kernel_size}")
            try:
                self.processor.apply_blur(layer_index=layer_index, kernel_size=kernel_size)
                self.update_layers_list()
                self.display_composited_image()
                layer_name = self.processor.layers[layer_index].name
                self.window.status_bar.showMessage(f"Filtro de Blur aplicado na camada '{layer_name}' com kernel size={kernel_size}.")
            except IndexError as e:
                QMessageBox.critical(self.window, "Erro", str(e))
            except ValueError as ve:
                QMessageBox.critical(self.window, "Erro de Valor", str(ve))

    def apply_gaussian_blur(self, layer_index=None):
        if layer_index is None:
            layer_index = len(self.processor.layers) - 1

        dialog = KernelSizeDialog(
            self.window,
            title="Aplicar Gaussian Blur",
            initial=5,
            min_val=1,
            max_val=99
        )
        result = dialog.exec_()

        if result == QDialog.Accepted:
            kernel_size = dialog.get_kernel_size()
            sigma, ok_sigma = QInputDialog.getDouble(
                self.window,
                "Aplicar Gaussian Blur",
                "Valor de Sigma:",
                value=0.0,
                min=0.0,
                max=100.0,
                decimals=2
            )
            if ok_sigma:
                print(f"Aplicando Gaussian Blur com kernel_size={kernel_size} e sigma={sigma}")  # Debug
                try:
                    self.processor.apply_gaussian_blur(layer_index=layer_index, kernel_size=kernel_size, sigma=sigma)
                    self.update_layers_list()
                    self.display_composited_image()
                    layer_name = self.processor.layers[layer_index].name
                    self.window.status_bar.showMessage(f"Filtro de Gaussian Blur aplicado na camada '{layer_name}' com kernel size={kernel_size} e sigma={sigma}.")
                except IndexError as e:
                    QMessageBox.critical(self.window, "Erro", str(e))
                except ValueError as ve:
                    QMessageBox.critical(self.window, "Erro de Valor", str(ve))
                    
    def undo_action(self):
        success = self.processor.undo()
        if success:
            self.update_layers_list()
            self.display_composited_image()
            self.window.status_bar.showMessage("Última ação desfeita.")
        else:
            QMessageBox.information(self.window, "Desfazer", "Não há ações para desfazer.")

    def on_layers_reordered(self, source_index, dest_index):
        """
        Lida com a reorganização das camadas quando o usuário arrasta e solta na lista de camadas.
        """
        self.reorder_layers(source_index, dest_index)
        self.display_composited_image()