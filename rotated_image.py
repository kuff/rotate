import cv2
import imutils
from utils import *


class RotatedImage:
    def __init__(self, image_path, rotation):
        self.image_path = image_path
        self.image_path_name = get_file_name(self.image_path)
        self.rotation = rotation
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise(IOError)

    def _rotate(self, rotation):
        # TODO: use own algorithm
        return imutils.rotate_bound(self.image, rotation)

    def show(self):
        cv2.imshow(self.image_path_name, self._rotate(self.rotation))
