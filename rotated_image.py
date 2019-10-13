import cv2
import imutils  # should be phased out before final release!
import numpy
from utils import *


class RotatedImage:
    def __init__(self, image_path, rotation):
        self.image_path = image_path
        self.image_path_name = get_file_name(self.image_path)
        self.rotation = rotation
        self.rotated_image = None
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise(IOError)

    def _rotate(self):
        # TODO: use own algorithm
        return imutils.rotate_bound(self.image, self.rotation)

    def show(self):
        if self.rotated_image is None:  # caching
            self.rotated_image = self._rotate()
        cv2.imshow(self.image_path_name, self.rotated_image)
