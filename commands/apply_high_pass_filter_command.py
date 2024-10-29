from commands.command import Command
from managers.layer_manager import LayerManager
from PyQt5.QtGui import QImage
from strategies.high_pass_filter_stategies import HighpassFilterStrategy

class ApplyHighpassFilterCommand(Command):
    def __init__(self, layer_manager: LayerManager, layer_index: int, strategy: HighpassFilterStrategy) -> None:
        self.layer_manager = layer_manager
        self.layer_index = layer_index
        self.strategy = strategy
        self.previous_image: QImage = QImage()

    def execute(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        self.previous_image = layer.image.copy()
        highpass_image = self.strategy.highpass_filter(layer.image)
        self.layer_manager.set_layer_image(self.layer_index, highpass_image)
        print(f"ApplyHighpassFilterCommand: Highpass Filter aplicado na camada '{layer.name}'.")

    def undo(self) -> None:
        self.layer_manager.set_layer_image(self.layer_index, self.previous_image)
        layer = self.layer_manager.get_layer(self.layer_index)
        print(f"ApplyHighpassFilterCommand: Highpass Filter desfeito na camada '{layer.name}'.")
