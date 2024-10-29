from commands.command import Command
from managers.layer_manager import LayerManager
from PyQt5.QtGui import QImage

class AddLayerCommand(Command):
    def __init__(self, layer_manager: LayerManager, layer_name: str, image: QImage) -> None:
        self.layer_manager = layer_manager
        self.layer_name = layer_name
        self.image = image
        self.layer_index: int = -1

    def execute(self) -> None:
        self.layer_manager.add_image_layer(self.layer_name, self.image)
        self.layer_index = len(self.layer_manager.get_layers()) - 1
        print(f"AddLayerCommand: Camada '{self.layer_name}' adicionada no índice {self.layer_index}.")

    def undo(self) -> None:
        if self.layer_index != -1:
            self.layer_manager.delete_layer(self.layer_index)
            print(f"AddLayerCommand: Camada '{self.layer_name}' removida do índice {self.layer_index}.")
