from commands.command import Command
from managers.layer_manager import LayerManager
from strategies.blur_strategies import Blur, BlurStrategy, GaussianBlur, MedianBlur
from PyQt5.QtGui import QImage

class ApplyBlurCommand(Command):
    def __init__(self, layer_manager: LayerManager, layer_index: int, strategy: str, **kwargs) -> None:
        self.layer_manager = layer_manager
        self.layer_index = layer_index
        self.strategy = strategy
        self.kwargs = kwargs
        self.previous_image: QImage = QImage()


    def execute(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        self.previous_image = layer.image.copy()
        self.layer_manager.apply_blur_to_layer(self.layer_index, self.strategy, **self.kwargs)
        print(f"ApplyBlurCommand: Blur '{type(self.strategy).__name__}' aplicado na camada '{layer.name}'.")

    def undo(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        layer.image = self.previous_image
        print(f"ApplyBlurCommand: Blur desfeito na camada '{layer.name}'.")
