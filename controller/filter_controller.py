from controller.blur_controller import BlurController
from .controller_interface import Controller
from processors.image_processor import ImageProcessor
from view.main_window import MainWindow

class FilterController(Controller):
    def __init__(self, processor: ImageProcessor, main_window: MainWindow) -> None:
        self.processor = processor
        self.main_window = main_window
        self.blur_controller = BlurController(self.processor)

    def show(self) -> None:
        pass

    def apply_blur(self, layer_index: int, blur_type: str = "blur") -> None:
        kernel_size, sigma = self.get_blur_settings(blur_type)
        self.blur_controller.apply_blur(layer_index, blur_type, kernel_size, sigma)
        self.main_window.display_composited_image()
        self._show_blur_message(layer_index, blur_type, kernel_size)

    def get_blur_settings(self, blur_type: str) -> tuple:
        kernel_size = self.main_window.get_kernel_size()
        sigma = self.main_window.get_sigma() if blur_type == "gaussian" else 0.0
        return kernel_size, sigma

    def _show_blur_message(self, layer_index: int, blur_type: str, kernel_size: int) -> None:
        layer_name = self.processor.layers[layer_index].name
        self.main_window.status_bar.showMessage(
            f"Filtro de Blur '{blur_type}' aplicado na camada '{layer_name}' com kernel={kernel_size}."
        )
