from math import cos, pi, sin  # for calculating image rotation
from os.path import basename as get_file_name  # name of image file

from cv2 import imread, imshow  # interpret and display images
# for populating 2d arrays of pixel values
from numpy import uint8
from numpy import zeros as populated_array


class RotatedImage:  # abstract class
    ''' Represents a rotated image '''

    def __init__(self, image_path, degrees, x, y, clockwise):
        self.image_path = image_path  # the file system path to the input image
        self.image = imread(image_path)  # the input image object
        if self.image is None:
            # raise an error if the input image could not be located given the file system path
            raise(OSError)
        self.degrees = degrees  # the amount of degrees to rotate the image
        self.point_of_rotation = (x, y)  # the specific point to rotate around
        self.clockwise = clockwise  # whether to rotate clockwise or counter-clockwise

    def __str__(self):
        # construct object string
        deg = 'degree' if self.degrees == -1 or self.degrees == 1 else 'degrees'
        return '%s rotated %s %s' % (get_file_name(self.image_path), self.degrees, deg)

    def _rotate(self):
        raise NotImplementedError

    def show(self):
        ''' Render a GUI window with the rotated image. '''
        imshow(str(self), self._rotate())


class ForwardMappedImage(RotatedImage):
    ''' Represents a rotated image using forward mapping '''

    def __init__(self, image_path, degrees, x, y, clockwise):
        super().__init__(image_path, degrees, x, y, clockwise)

    def __str__(self):
        return super().__str__() + ' using forward mapping'

    def _rotate(self):
        ''' Rotate the associated image using forward mapping.
        Note: this class method should be considered protected '''

        # define the width and height of the input image
        width, height = (len(self.image[0]),
                         len(self.image))
        # convert degrees to radians
        rad = (pi/180) * self.degrees
        # define image and point of rotation
        img = self.image
        por_x, por_y = self.point_of_rotation

        # define the array to hold the new pixel coordinates of the rotated image
        new_image = populated_array((height, width, 3), uint8)

        # find new x/y coordinates
        for x in range(width):
            for y in range(height):

                # center pixel around point of rotation, perform the rotation, and translate the pixel back
                new_x, new_y = (0, 0)
                if self.clockwise:  # rotate in either clockwise or counter-clockwise direction
                    new_x = round((x - por_x) * cos(rad) -
                                  (y - por_y) * sin(rad)) + por_x
                    new_y = round((x - por_x) * sin(rad) +
                                  (y - por_y) * cos(rad)) + por_y
                else:
                    new_x = round((x - por_x) * cos(rad) +
                                  (y - por_y) * sin(rad)) + por_x
                    new_y = round(-(x - por_x) * sin(rad) +
                                  (y - por_y) * cos(rad)) + por_y

                # ignore the pixel if it is outside the image frame, otherwise insert it into the rotated image
                if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                    continue
                else:
                    new_image[new_y, new_x] = img[y, x]

        # finally, return the new image
        return new_image


class BackwardMappedImage(RotatedImage):
    ''' Represents a rotated image using backward mapping '''

    def __init__(self, image_path, degrees, x, y, clockwise):
        super().__init__(image_path, degrees, x, y, clockwise)

    def __str__(self):
        return super().__str__() + ' using backward mapping'

    def _rotate(self):
        ''' Rotate the associated image using backward mapping.
        Note: this class method should be considered protected '''

        # define the width and height of the input image
        width, height = (len(self.image[0]),
                         len(self.image))
        # convert degrees to radians
        rad = 2 * pi - ((pi/180) * self.degrees)
        # define image and point of rotation
        img = self.image
        por_x, por_y = self.point_of_rotation

        # define the array to hold the new pixel coordinates of the rotated image
        new_image = populated_array((height, width, 3), uint8)

        # find new x/y coordinates
        for x in range(width):
            for y in range(height):

                # center pixel around point of rotation, perform the rotation, and translate the pixel back
                new_x, new_y = (0, 0)
                if self.clockwise:  # rotate in either clockwise or counter-clockwise direction
                    new_x = round((x - por_x) * cos(rad) -
                                  (y - por_y) * sin(rad)) + por_x
                    new_y = round((x - por_x) * sin(rad) +
                                  (y - por_y) * cos(rad)) + por_y
                else:
                    new_x = round((x - por_x) * cos(rad) +
                                  (y - por_y) * sin(rad)) + por_x
                    new_y = round(-(x - por_x) * sin(rad) +
                                  (y - por_y) * cos(rad)) + por_y

                # ignore the pixel if it is outside the image frame, otherwise insert it into the rotated image
                if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                    continue
                else:
                    new_image[y, x] = img[new_y, new_x]

        # finally, return the new image
        return new_image


class ImageCollection:

    def __init__(self, image_path, degrees, x, y, clockwise):
        self.algorithms = [ForwardMappedImage(image_path, degrees, x, y, clockwise),
                           BackwardMappedImage(image_path, degrees, x, y, clockwise)]

    def show(self):
        for algorithm in self.algorithms:
            algorithm.show()
