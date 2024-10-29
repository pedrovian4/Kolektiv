from commands.command import Command
from managers.layer_manager import LayerManager
from PyQt5.QtGui import QImage

class RemoveLayerCommand(Command):
    def __init__(self, layer_manager: LayerManager, layer_index: int) -> None:
        self.layer_manager = layer_manager
        self.layer_index = layer_index
        self.removed_layer_name: str = ""
        self.removed_image: QImage = QImage()

    def execute(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        self.removed_layer_name = layer.name
        self.removed_image = layer.image
        self.layer_manager.delete_layer(self.layer_index)
        print(f"RemoveLayerCommand: Camada '{self.removed_layer_name}' removida do índice {self.layer_index}.")

    def undo(self) -> None:
        self.layer_manager.add_image_layer(self.removed_layer_name, self.removed_image)
        layers = self.layer_manager.get_layers()
        if len(layers) > self.layer_index + 1:
            layer = layers.pop()
            layers.insert(self.layer_index, layer)
        print(f"RemoveLayerCommand: Camada '{self.removed_layer_name}' restaurada no índice {self.layer_index}.")
