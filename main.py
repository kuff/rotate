import argparse  # for parsing user input and handling exceptions

from cv2 import destroyAllWindows, waitKey  # for cleanup and termination

from rotation import ImageCollection  # for managing rotated images


def main_loop():
    # parse program arguments
    parser = argparse.ArgumentParser(
        prog='rotate.py', description='Rotate an image.')
    parser.add_argument(
        'image', type=str, help='the image to be rotated')
    parser.add_argument(
        'degrees', type=int, help='the amount of degrees to rotate the image by')
    parser.add_argument(
        'x', type=int, help='the point of rotation on the x-axis')
    parser.add_argument(
        'y', type=int, help='the point of rotation on the y-axis')
    parser.add_argument(  # not a requirement
        '--clockwise', '--cw', action='store_true', help='rotate image clockwise (Default: counter-clockwise)')
    args = parser.parse_args()

    # create new image collection using provided program arguments
    image_collection = ImageCollection(
        args.image, args.degrees, args.x, args.y, args.clockwise)

    # process and show the rotated images
    print('Loading images...')
    image_collection.show()
    print('Images loaded in new windows. Press \'q\' on any of them to quit!')

    while True:
        # allow for keyboard interrupt
        if waitKey(1) & 0xFF == ord('q'):
            break  # breaks the loop, ending the program


if __name__ == "__main__":
    main_loop()
    destroyAllWindows()  # cleanup
