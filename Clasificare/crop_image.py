import json
import numpy
import os
import sys
from PIL import Image

size = 300, 300
cropping_points = [(0, 0), (15, 40)]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError(f'You need to provide at least 1 parameter but {len(sys.argv) - 1} were given')

    if not os.path.exists(sys.argv[1]):
        raise ValueError('You need to provide an existing path (to json)')
    if not os.path.isfile(sys.argv[1]):
        raise ValueError('The path does not point to a file (json)')

    file_name = sys.argv[1]
    images = json.load(open(file_name))
    if not os.path.exists("CropImages"):
        os.mkdir("CropImages")
    for counter, image in enumerate(images):
        try:
            height = image['height']
            width = image['width']
            pixels1D = image['pixels']
            pixels = [pixels1D[i * width:(i + 1) * width] for i in range(0, height)]
            pixels = numpy.array(pixels, dtype=numpy.uint8)
            new_image = Image.fromarray(pixels).crop()
            for index, point in enumerate(cropping_points):
                new_image.crop((point[0], point[1], point[0] + size[0], point[1] + size[1])).save(os.path.join("CropImages", str(counter) + "." + str(index) + ".jpg"))
                print(">> Created " + "CropImages/" + str(counter) + "." + str(index) + ".jpg")
        except Exception:
            print("An error occurred")
