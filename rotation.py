from math import cos, pi, sin
from os.path import basename as get_file_name

from cv2 import imread, imshow
from imutils import rotate as best_case  # only used for comparison purposes
from numpy import uint8
from numpy import zeros as populated_array


class RotatedImage:  # abstract class
    ''' Represents a rotated image '''

    def __init__(self, image_path, degrees):
        self.image_path = image_path  # the file system path to the input image
        self.degrees = degrees  # the amount of degrees to rotate the image
        self.image = imread(image_path)  # the input image object
        if self.image is None:
            # raise an error if the input image could not be located given the file system path
            raise(OSError)

    def __str__(self):
        deg = 'degree' if self.degrees == -1 or self.degrees == 1 else 'degrees'
        return '%s rotated %s %s' % (get_file_name(self.image_path), self.degrees, deg)

    def _rotate(self):
        raise NotImplementedError

    def show(self):
        ''' Render a GUI window with the rotated image. '''
        imshow(str(self), self._rotate())


class BestCaseImage(RotatedImage):

    def __init__(self, image_path, degrees):
        super().__init__(image_path, degrees)

    def __str__(self):
        return super().__str__() + ' using an external library'

    def _rotate(self):
        return best_case(self.image, self.degrees)


class ForwardMappedImage(RotatedImage):
    ''' Represents a rotated image using forward mapping '''

    def __init__(self, image_path, degrees):
        super().__init__(image_path, degrees)

    def __str__(self):
        return super().__str__() + ' using forward mapping'

    def _rotate(self):
        ''' Rotate the image that the associated object represents.
        Note: this class method should be considered protected '''

        # define the width and height of the input image
        width, height = (len(self.image), len(self.image[0]))
        # convert degrees to radinas
        rad = (pi/180) * self.degrees

        # define the array to hold the new pixel coordinates of the rotated image
        new_image = populated_array((width, height, 3), uint8)

        # find new x/y coordinates
        for x in range(width):
            for y in range(height):
                new_x = round(x * cos(rad) - y * sin(rad))
                new_y = round(x * sin(rad) + y * cos(rad))
                if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                    continue
                else:
                    new_image[new_x, new_y] = self.image[x, y]

        # finally, return the new image
        return new_image


class BackwardMappedImage(RotatedImage):
    ''' Represents a rotated image using backward mapping '''

    def __init__(self, image_path, degrees):
        super().__init__(image_path, degrees)

    def __str__(self):
        return super().__str__() + ' using backward mapping'

    def _rotate(self):
        # define the width and height of the input image
        width, height = (len(self.image), len(self.image[0]))
        # convert degrees to radinas
        rad = 2 * pi - ((pi/180) * self.degrees)

        # define the array to hold the new pixel coordinates of the rotated image
        new_image = populated_array((width, height, 3), uint8)

        # find new x/y coordinates
        for x in range(width):
            for y in range(height):
                new_x = round(x * cos(rad) - y * sin(rad))
                new_y = round(x * sin(rad) + y * cos(rad))
                if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                    continue
                else:
                    new_image[x, y] = self.image[new_x, new_y]

        # finally, return the new image
        return new_image


class ImageCollection:

    def __init__(self, image_path, degrees):
        self.algorithms = [ForwardMappedImage(image_path, degrees),
                           BackwardMappedImage(image_path, degrees),
                           BestCaseImage(image_path, degrees)]

    def show(self):
        for algorithm in self.algorithms:
            algorithm.show()
