from cv2 import imread, imshow
import numpy as np
from math import *
from utils import get_file_name


class RotatedImage:
    ''' Represents a rotated image '''

    def __init__(self, image_path, degrees):
        self.image_path = image_path
        self.image_path_name = get_file_name(self.image_path)
        self.degrees = degrees
        self.image = imread(image_path)
        self.rotated_image = None
        if self.image is None:
            raise(OSError)

    def _rotate(self):  # TODO: the rotated image has holes
        ''' Rotate the image that the associated object represents.
        Note: this class method should be considered protected '''

        # define input variables
        img = self.image  # shorthand
        width, height = (len(img), len(img[0]))
        deg = (pi/180) * self.degrees  # converting degrees to radinas

        # define the array to hold the new pixel coordinates of the rotated image
        new_coordinates = np.zeros((width, height), dtype=tuple)

        # define the variables used to offset the final image
        smallest_new_x = None
        smallest_new_y = None
        largest_new_x = None
        largest_new_y = None

        # find new x/y coordinates
        for x in range(width):
            for y in range(height):
                # calculate new pixel coordinates using the formular for clockwise rotation
                new_x = round(x * cos(deg) + y * sin(deg))
                new_y = round(-x * sin(deg) + y * cos(deg))
                new_coordinates[x, y] = (new_x, new_y)

                # check for smallest/largest x/y, used to offset the final image
                if smallest_new_x is None or new_x < smallest_new_x:
                    smallest_new_x = new_x
                if largest_new_x is None or new_x > largest_new_x:
                    largest_new_x = new_x
                if smallest_new_y is None or new_y < smallest_new_y:
                    smallest_new_y = new_y
                if largest_new_y is None or new_y > largest_new_y:
                    largest_new_y = new_y

        # calculate the dimensions of the new image and define the translational offset
        new_width = abs(smallest_new_x - largest_new_x) + 1
        new_height = abs(smallest_new_y - largest_new_y) + 1
        x_offset = -smallest_new_x
        y_offset = -smallest_new_y

        # define the new image and fill it with black pixels
        new_image = np.zeros((new_width, new_height, 3), np.uint8)

        # insert pixels into new image
        for x in range(width):
            for y in range(height):
                new_x, new_y = new_coordinates[x, y]
                new_image[new_x + x_offset][new_y + y_offset] = img[x][y]

        # TODO: pixel interpolation

        # finally, return the new image
        return new_image

    def show(self):
        ''' Render a GUI window with the rotated image.
        Note: the rotated image is cached and must be cleared for a new rotated render to be generate '''

        # generate the rotated version of the image if it hasn't been doen already
        if self.rotated_image is None:  # caching
            self.rotated_image = self._rotate()

        # show the rotated image with the image file name as the window header
        imshow(self.image_path_name, self.rotated_image)
