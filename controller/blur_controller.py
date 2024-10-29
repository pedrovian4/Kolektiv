# controller/blur_controller.py

from controller.controller_interface import Controller
from processors.image_processor import ImageProcessor
from strategies.blur_strategies import Blur, GaussianBlur, MedianBlur, BlurStrategy
from typing import Union, Optional
import numpy as np

class BlurController(Controller):
    def __init__(self, processor: ImageProcessor) -> None:
        super().__init__()
    def show(self) -> None:
        ...