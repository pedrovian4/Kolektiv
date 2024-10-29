# controller/main_controller.py

from PyQt5.QtGui import QImage, QPixmap
from managers.simple_history_manager import SimpleHistoryHandler
from processors.image_processor import ImageProcessor
from view.main_window import MainWindow
from managers.layer_manager import LayerManager
from controller.layer_controller import LayerController
from controller.file_controller import FileController
from controller.blur_controller import BlurController
from managers.history_manager import HistoryManager

class MainController:
    def __init__(self):
        self.image_processor = ImageProcessor()
        
        history_handler = SimpleHistoryHandler()
        self.history_manager = HistoryManager(history_handler, self)
        
        self.blur_controller = BlurController(self.image_processor)
        self.layer_controller = LayerController(
            layer_manager=LayerManager(self.image_processor),
            controller=self,
            blur_controller=self.blur_controller,
            history_manager=self.history_manager,
        )
        self.file_controller = FileController(self.image_processor, self, self.update_display)
        
        self.controllers = {
            "layers": self.layer_controller,
            "file": self.file_controller,
            "blur": self.blur_controller
        }
        
        self.window = MainWindow(self)
        self.setup_connections()


    def setup_connections(self):
        self.window.main_layout.undo_action.triggered.connect(self.history_manager.undo_action)
        self.window.main_layout.redo_action.triggered.connect(self.history_manager.redo_action)

    def show_main_window(self):
        self.window.show()

    def update_display(self):
        composited_image = self.image_processor.get_composited_image()
        if composited_image:
            self.window.main_layout.image_label.set_image(composited_image)
        else:
            self.window.main_layout.image_label.clear()
