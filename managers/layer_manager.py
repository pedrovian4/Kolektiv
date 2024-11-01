import os
from PyQt5.QtGui import QImage
from abstracts.image_handler_abstract import AbstractImageHandler
from entities.layer import Layer
from typing import List
from strategies.high_pass_filter_stategies import HighpassFilterStrategy
from strategies.laplacian_filter_stategy import LaplacianFilterStrategy
from strategies.sharpen_strategies import SharpenStrategy

class LayerManager:
    def __init__(self, image_handler: AbstractImageHandler) -> None:
        self.image_handler = image_handler

    def add_image_layer(self, file_path: str, qt_image: QImage) -> None:
        layer_name = os.path.basename(file_path)
        print(f"LayerManager: Adicionando camada '{layer_name}'")
        self.image_handler.add_layer(layer_name, qt_image)

    def delete_layer(self, index: int) -> str:
        if 0 <= index < len(self.image_handler.layers):
            removed_layer = self.image_handler.layers[index].name
            print(f"LayerManager: Removendo camada '{removed_layer}'")
            self.image_handler.remove_layer(index)
            return removed_layer
        else:
            print(f"LayerManager: Índice de camada inválido: {index}")
            raise IndexError

    def toggle_layer_visibility(self, index: int) -> None:
        print(f"LayerManager: Alternando visibilidade da camada no índice {index}")
        self.image_handler.toggle_layer_visibility(index)

    def reorder_layers(self, source: int, dest: int) -> None:
        print(f"LayerManager: Reordenando camadas de {source} para {dest}")
        self.image_handler.reorder_layers(source, dest)

    def get_layers(self) -> List[Layer]:
        return self.image_handler.layers

    def get_layer(self, index: int) -> Layer:
        if 0 <= index < len(self.image_handler.layers):
            return self.image_handler.layers[index]
        else:
            print(f"LayerManager: Índice de camada inválido ao obter camada: {index}")
            raise IndexError

    def apply_blur_to_layer(self, index: int, blur_type: str, kernel_size: int = 5, sigma: float = 1.0) -> None:
        if 0 <= index < len(self.image_handler.layers):
            self.image_handler.apply_blur_to_layer(index, blur_type, kernel_size, sigma)
        else:
            print(f"LayerManager: Índice de camada inválido ao aplicar blur: {index}")
            raise IndexError
    
    def set_layer_image(self, index: int, image: QImage) -> None:
        if 0 <= index < len(self.image_handler.layers):
            self.image_handler.layers[index].image = image
            print(f"LayerManager: Imagem da camada '{self.image_handler.layers[index].name}' atualizada.")
        else:
            print(f"LayerManager: Índice de camada inválido ao definir imagem: {index}")
            raise IndexError
        
    def apply_sharpen_to_layer(self, index: int, strategy: SharpenStrategy) -> None:
        if not (0 <= index < len(self.image_handler.layers)):
            print(f"LayerManager: Índice de camada inválido ao aplicar nitidez: {index}")
            raise IndexError

        layer = self.image_handler.layers[index]
        print(f"LayerManager: Aplicando nitidez usando {strategy.__class__.__name__} na camada '{layer.name}'")
        sharpened_image = strategy.sharpen(layer.image)
        self.set_layer_image(index, sharpened_image)
    def apply_highpass_filter_to_layer(self, index: int, strategy: HighpassFilterStrategy) -> None:
        if not (0 <= index < len(self.image_handler.layers)):
            print(f"LayerManager: Índice de camada inválido ao aplicar Highpass Filter: {index}")
            raise IndexError

        layer = self.image_handler.layers[index]
        print(f"LayerManager: Aplicando Highpass Filter usando {strategy.__class__.__name__} na camada '{layer.name}'")
        highpass_image = strategy.highpass_filter(layer.image)
        self.set_layer_image(index, highpass_image)
        
    def apply_laplacian_filter_to_layer(self, index: int, strategy: LaplacianFilterStrategy) -> None:
        if not (0 <= index < len(self.image_handler.layers)):
            print(f"LayerManager: Índice de camada inválido ao aplicar Filtro Laplaciano: {index}")
            raise IndexError("Índice de camada inválido")

        layer = self.image_handler.layers[index]
        print(f"LayerManager: Aplicando Filtro Laplaciano usando {strategy.__class__.__name__} na camada '{layer.name}'")
        laplacian_image = strategy.laplacian_filter(layer.image)
        self.set_layer_image(index, laplacian_image)
        
    def apply_edge_detection_filter_to_layer(self, index: int, strategy) -> None:
        if not (0 <= index < len(self.image_handler.layers)):
            print(f"LayerManager: Índice de camada inválido ao aplicar Filtro de Detecção de Bordas: {index}")
            raise IndexError("Índice de camada inválido")

        layer = self.image_handler.layers[index]
        print(f"LayerManager: Aplicando Filtro de Detecção de Bordas usando {strategy.__class__.__name__} na camada '{layer.name}'")
        edge_image = strategy.detect_edges(layer.image)
        self.set_layer_image(index, edge_image)