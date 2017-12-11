import json
import numpy
import os
import sys
from PIL import Image


def resize(image, desired_size_tuple=(550, 512)):
    height = image['height']
    width = image['width']
    pixels1D = image['pixels']
    pixels = [pixels1D[i * width:(i + 1) * width] for i in range(0, height)]
    pixels = numpy.array(pixels, dtype=numpy.uint8)
    new_image = Image.fromarray(pixels)
    new_image.thumbnail(desired_size_tuple, Image.ANTIALIAS)  # resize
    new_width = new_image.size[0]
    new_height = new_image.size[1]
    # get pixels from new image and padding with shite spaces
    pixels1D = new_image.load()
    pixels = [
        (
            pixels1D[width, height][0],
            pixels1D[width, height][1],
            pixels1D[width, height][2]
        )
        for height in range(0, new_height)
        for width in range(0, new_width)
    ]
    pixels = [pixels[i * new_width:(i + 1) * new_width] for i in range(0, new_height)]  # from new image
    desired_width, desired_height = desired_size_tuple
    if desired_width > new_width:
        # print(desired_width, " W> ", new_width)
        white_line_pixels = [(255, 255, 255)] * (desired_width - new_width)
        for i in range(new_height):
            pixels[i].extend(white_line_pixels)  # padding white spaces in the right side
    if desired_height > new_height:
        # print(desired_height, " H> ", new_height)
        white_line_pixels = [(255, 255, 255)] * desired_width
        for i in range(desired_height - new_height):
            pixels.append(white_line_pixels)  # padding white spaces at the bottom
    pixels = numpy.array(pixels, dtype=numpy.uint8)
    return Image.fromarray(pixels)  # remake image


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError(f'You need to provide at least 1 parameter but {len(sys.argv) - 1} were given')

    if not os.path.exists(sys.argv[1]):
        raise ValueError('You need to provide an existing path (to json)')
    if not os.path.isfile(sys.argv[1]):
        raise ValueError('The path does not point to a file (json)')

    file_name = sys.argv[1]
    images = json.load(open(file_name))
    if not os.path.exists("Images"):
        os.mkdir("Images")
    for counter, image in enumerate(images):
        resize(image)

        try:
            new_image = resize(image)
            new_image.save(os.path.join("Images", "{}.jpg".format(counter)))
            print(">> Created " + os.path.join("Images", "{}.jpg".format(counter)))
        except Exception as e:
            print("An error occurred")