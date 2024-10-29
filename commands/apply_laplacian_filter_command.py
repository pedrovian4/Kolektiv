from commands.command import Command
from managers.layer_manager import LayerManager
from PyQt5.QtGui import QImage
from strategies.laplacian_filter_stategy import LaplacianFilterStrategy

class ApplyLaplacianFilterCommand(Command):
    def __init__(self, layer_manager: LayerManager, layer_index: int, strategy: LaplacianFilterStrategy) -> None:
        self.layer_manager = layer_manager
        self.layer_index = layer_index
        self.strategy = strategy
        self.previous_image: QImage = QImage()

    def execute(self) -> None:
        layer = self.layer_manager.get_layer(self.layer_index)
        self.previous_image = layer.image.copy()
        laplacian_image = self.strategy.laplacian_filter(layer.image)
        self.layer_manager.set_layer_image(self.layer_index, laplacian_image)
        print(f"ApplyLaplacianFilterCommand: Filtro Laplaciano aplicado na camada '{layer.name}'.")

    def undo(self) -> None:
        self.layer_manager.set_layer_image(self.layer_index, self.previous_image)
        layer = self.layer_manager.get_layer(self.layer_index)
        print(f"ApplyLaplacianFilterCommand: Filtro Laplaciano desfeito na camada '{layer.name}'.")
