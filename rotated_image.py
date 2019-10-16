from numpy import zeros as populated_array, uint8
from imutils import rotate_bound as best_case  # only used for comparison
from cv2 import imread, imshow
from utils import get_file_name  # local utility function
from math import sin, cos, pi


class RotatedImage:
    ''' Represents a rotated image '''

    def __init__(self, image_path, degrees):
        self.image_path = image_path  # the file system path to the input image
        self.image_path_name = get_file_name(self.image_path)
        self.degrees = degrees  # the amount of degrees to rotate the image
        self.image = imread(image_path)  # the input image object
        if self.image is None:
            # raise an error if the input image could not be located given the file system path
            raise(OSError)

    def _rotate(self):
        ''' Rotate (clockwise) the image that the associated object represents.
        Note: this class method should be considered protected '''

        # define input variables
        img = self.image  # shorthand
        # define the width and height of the input image
        width, height = (len(img), len(img[0]))
        rad = (pi/180) * self.degrees  # converting degrees to radinas

        # define the array to hold the new pixel coordinates of the rotated image
        new_coordinates = populated_array((width, height), dtype=tuple)

        # define the variables used to offset the final image
        smallest_new_x = None
        smallest_new_y = None
        largest_new_x = None
        largest_new_y = None

        # find new x/y coordinates
        for x in range(width):
            for y in range(height):
                # calculate new pixel coordinates using the formular for clockwise rotation
                new_x = round(x * cos(rad) + y * sin(rad))
                new_y = round(-x * sin(rad) + y * cos(rad))

                # save the new coordinates to a new array
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
        new_image = populated_array((new_width, new_height, 3), uint8)

        # insert pixels into new image
        for x in range(width):
            for y in range(height):
                new_x, new_y = new_coordinates[x, y]
                new_image[new_x + x_offset][new_y + y_offset] = img[x][y]

        # do pixel interpolation on leftover black pixels
        for x in range(1, new_width - 1):
            for y in range(1, new_height - 1):
                if all(value == 0 for value in new_image[x, y]):
                    # define the neighbors of the selected black pixel
                    pixel_up = new_image[x - 1, y]
                    pixel_down = new_image[x + 1, y]
                    pixel_left = new_image[x, y - 1]
                    pixel_right = new_image[x, y + 1]

                    # continue immidiately if all neigbor pixels are black aswell
                    if all(all(value == 0 for value in pixel) for pixel in [pixel_up, pixel_down, pixel_left, pixel_right]):
                        continue

                    # calculate the avarage of each RGB value
                    avarage_red = int(round((
                        float(pixel_up[0]) + float(pixel_down[0]) + float(pixel_left[0]) + float(pixel_right[0]))/4))
                    avarage_green = int(round((
                        float(pixel_up[1]) + float(pixel_down[1]) + float(pixel_left[1]) + float(pixel_right[1]))/4))
                    avarage_blue = int(round((
                        float(pixel_up[2]) + float(pixel_down[2]) + float(pixel_left[2]) + float(pixel_right[2]))/4))

                    # paste new RGB values into the black pixel
                    new_image[x, y, 0] = avarage_red
                    new_image[x, y, 1] = avarage_green
                    new_image[x, y, 2] = avarage_blue

        # finally, return the new image
        return new_image

    def show(self):
        ''' Render a GUI window with the rotated image. '''

        # show the rotated image using both the custom algorithm implemented above, as well as an external library method
        imshow('%s rotated %s degrees using custom algorithm' %
               (self.image_path_name, self.degrees), self._rotate())
        imshow('%s rotated %s degrees using external library (imutils.rotate_bounds)' % (self.image_path_name, self.degrees),
               best_case(self.image, self.degrees))
