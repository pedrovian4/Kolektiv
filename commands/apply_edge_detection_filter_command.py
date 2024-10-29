from commands.command import Command
from PyQt5.QtGui import QImage

class ApplyEdgeDetectionCommand(Command):
    def __init__(self, layer_manager, layer_index: int, strategy) -> None:
        self.layer_manager = layer_manager
        self.layer_index = layer_index
        self.strategy = strategy
        self.previous_image: QImage = QImage()

    def execute(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        self.previous_image = layer.image.copy()
        edged_image = self.strategy.detect_edges(layer.image)
        self.layer_manager.set_layer_image(self.layer_index, edged_image)
        print(f"ApplyEdgeDetectionCommand: Detecção de bordas aplicada na camada '{layer.name}'.")

    def undo(self) -> None:
        self.layer_manager.set_layer_image(self.layer_index, self.previous_image)
        layer = self.layer_manager.get_layer(self.layer_index)
        print(f"ApplyEdgeDetectionCommand: Detecção de bordas desfeita na camada '{layer.name}'.")
