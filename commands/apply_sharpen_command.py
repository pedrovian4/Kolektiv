from commands.command import Command
from managers.layer_manager import LayerManager
from strategies.sharpen_strategies import SharpenStrategy
from PyQt5.QtGui import QImage

class ApplySharpenCommand(Command):
    def __init__(self, layer_manager: LayerManager, layer_index: int, strategy: SharpenStrategy) -> None:
        self.layer_manager = layer_manager
        self.layer_index = layer_index
        self.strategy = strategy
        self.previous_image: QImage = QImage()

    def execute(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        self.previous_image = layer.image.copy()
        sharpened_image = self.strategy.sharpen(layer.image)
        self.layer_manager.set_layer_image(self.layer_index, sharpened_image)
        print(f"ApplySharpenCommand: Nitidez aplicada na camada '{layer.name}'.")

    def undo(self) -> None:
        self.layer_manager.set_layer_image(self.layer_index, self.previous_image)
        layer = self.layer_manager.get_layer(self.layer_index)
        print(f"ApplySharpenCommand: Nitidez desfeita na camada '{layer.name}'.")
