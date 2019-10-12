import cv2
from utils import *
from rotated_image import *


def main_loop():
    # TODO: cool splash screen

    # request import image from user
    image_path = input(
        'Please provide a path to the image you want rotated: ')

    # remember file input image name
    image_file_name = get_file_name(image_path)

    # request desired rotation in degrees
    desired_rotation = input(
        'Please specify the desired rotation of ' + image_file_name + ': ')

    try:
        rotated_image = RotatedImage(image_path, int(desired_rotation))
    except():
        print(image_file_name + ' and/or ' + desired_rotation +
              ' does not appear to be valid inputs! Try again:')
        return main_loop()

    while True:
        # draw the next frame of the slick animation
        rotated_image.show()

        # allow for keyboard interrupt
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # breaks the loop, ending the program


if __name__ == "__main__":
    main_loop()
    cv2.destroyAllWindows()
