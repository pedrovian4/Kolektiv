# controller/blur_controller.py

from controller.controller_interface import Controller
from processors.image_processor import ImageProcessor
from strategies.blur_strategies import Blur, GaussianBlur, MedianBlur, BlurStrategy
from typing import Union, Optional
import numpy as np

class BlurController(Controller):
    def __init__(self, processor: ImageProcessor) -> None:
        super().__init__()
        self.processor = processor
        self.blur_strategies = {
            "blur": Blur(),
            "gaussian": GaussianBlur(),
            "median": MedianBlur()
        }
        
    def show(self) -> None:
        ...
    
    def apply_blur_to_layer(self, layer_index: int, blur_type: str, **kwargs) -> None:
        strategy: Optional[BlurStrategy] = self.blur_strategies.get(blur_type.lower())
        if not strategy:
            raise ValueError(f"Unknown blur type: {blur_type}")
        self.processor.apply_blur_to_layer(layer_index, strategy, **kwargs)
