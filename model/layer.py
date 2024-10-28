from PyQt5.QtGui import QImage

class Layer:
    def __init__(self, name, image: QImage, visible=True):
        self.name = name
        self.image = image
        self.visible = visible
