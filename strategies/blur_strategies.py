import cv2


class BlurStrategy:
    def apply(self, image, **kwargs):
        raise NotImplementedError

class Blur(BlurStrategy):
    def apply(self, image, kernel_size=5, **kwargs):
        return cv2.blur(image, (kernel_size, kernel_size))

class GaussianBlur(BlurStrategy):
    def apply(self, image, kernel_size=5, sigma=0, **kwargs):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

class MedianBlur(BlurStrategy):
    def apply(self, image, kernel_size=5, **kwargs):
        return cv2.medianBlur(image, kernel_size)