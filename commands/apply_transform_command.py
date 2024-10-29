from commands.command import Command
from PyQt5.QtGui import QImage

class ApplyTransformCommand(Command):
    def __init__(self, layer_manager, layer_index: int, strategy) -> None:
        self.layer_manager = layer_manager
        self.layer_index = layer_index
        self.strategy = strategy
        self.previous_image: QImage = QImage()

    def execute(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        self.previous_image = layer.image.copy()
        transformed_image = self.strategy.transform(layer.image)
        self.layer_manager.set_layer_image(self.layer_index, transformed_image)
        print(f"ApplyTransformCommand: Transformação aplicada na camada '{layer.name}'.")

    def undo(self) -> None:
        self.layer_manager.set_layer_image(self.layer_index, self.previous_image)
        layer = self.layer_manager.get_layer(self.layer_index)
        print(f"ApplyTransformCommand: Transformação desfeita na camada '{layer.name}'.")
