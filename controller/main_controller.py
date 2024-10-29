from controller.blur_controller import BlurController
from .controller_interface import Controller
from controller.file_controller import FileController
from controller.history_controller import HistoryController
from processors.history_processor import HistoryProcessor
from view.main_window import MainWindow
from processors.image_processor import ImageProcessor
from controller.layer_controller import LayerController
from managers.layer_manager import LayerManager
from PyQt5.QtGui import QImage
from typing import Optional

class MainController(Controller):
    def __init__(self) -> None:
        self.image_processor: ImageProcessor = ImageProcessor()
        self.history_processor: HistoryProcessor = HistoryProcessor()
        self.layer_manager = LayerManager(self.image_processor)
        
        self.blur_controller = BlurController(self.image_processor)
        self.layer_controller = LayerController(LayerManager(self.image_processor), self, self.blur_controller)
        self.file_controller = FileController(self.image_processor, self, self.update_display)
        

        self.controllers = {
            "layers": self.layer_controller,
            "file": self.file_controller,
            "blur": self.blur_controller
        }
        
        self.window: MainWindow = MainWindow(self)

    def show(self) -> None:
        self.window.show()
        for controller in self.controllers.values():
            controller.show()

    def update_display(self) -> None:
        qt_image: Optional[QImage] = self.image_processor.get_composited_image()
        if qt_image and not qt_image.isNull():
            print("MainController: Atualizando exibição da imagem.")
            self.window.main_layout.image_label.display_image(qt_image)
            self.window.main_layout.status_bar.showMessage("Imagem atualizada.")
        else:
            self.window.main_layout.image_label.clear_image()
            self.window.main_layout.status_bar.showMessage("Nenhuma imagem para exibir.")

    def toggle_layer_visibility(self, index: int) -> None:
        print(f"MainController: Alternando visibilidade da camada no índice {index}")
        self.controllers["layers"].toggle_layer_visibility(index)


    def on_layers_reordered(self, source: int, dest: int) -> None:
        print(f"MainController: Reordenando camadas de {source} para {dest}")
        self.controllers["layers"].reorder_layers(source, dest)

    def refresh_image(self) -> None:
        print("MainController: Atualizando imagem composta.")
        self.update_display()
