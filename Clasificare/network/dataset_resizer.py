import os
from PIL import Image
from resizeimage import resizeimage
import progressbar

from Clasificare.network.train import find_all_files


def force_resize_inplace(image_path, new_width, new_height):
    with open(image_path, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(
                image,
                [new_width, new_height],
                validate=False)
            cover.save(image_path, image.format)


def resize_dir_images(dirpath,
                      new_width=128,
                      new_height=128,
                      recursive=False):
    files = find_all_files(dirpath, recursive=recursive)

    bar = progressbar.ProgressBar()
    for file in bar(files):
        force_resize_inplace(file, new_width, new_height)


_FILE_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    resize_dir_images(os.path.join(_FILE_PATH, './train'), recursive=True)
