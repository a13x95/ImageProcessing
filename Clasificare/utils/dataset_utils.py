import os

import random
import numpy as np
from PIL import Image
from resizeimage import resizeimage
import progressbar
from scipy.ndimage import imread


def find_all_files(dirpath, recursive=False):
    files = []
    for name in os.listdir(dirpath):
        file = os.path.join(dirpath, name)
        if recursive and os.path.isdir(file):
            files.extend(find_all_files(file))

        if os.path.isfile(file):
            files.append(file)

    return files


def get_image_data(file):
    image = imread(file, mode="RGB")
    return np.array(image) / 255.


def create_y_train(labels, labels_set, limit=None):
    if limit is None:
        limit = len(labels)

    for idx, key in enumerate(labels_set):
        labels_set[key] = idx

    num_labels = len(labels_set)
    y_data = np.empty(shape=(limit, num_labels))
    for idx, label in enumerate(labels[:limit]):
        label_pos = labels_set[label]
        y_data[idx] = np.array(
            [
                0. if idx != label_pos else 1.0
                for idx in range(num_labels)
            ]
        )

    return y_data


def read_data(dirpath,
              label_function=os.path.basename,
              image_size=(128, 128),
              create_labels=True,
              limit=None,
              recursive=False,
              shuffle=False):
    files = find_all_files(dirpath, recursive=recursive)
    if shuffle:
        random.shuffle(files)

    num_images = len(files)
    if limit is None:
        limit = num_images
    x_data = np.empty(shape=(limit, image_size[0], image_size[1], 3))
    labels = []
    labels_set = {}

    bar = progressbar.ProgressBar()
    for index, file in bar(list(enumerate(files[:limit]))):
        if os.path.isfile(file):
            label = label_function(file)
            image = get_image_data(file)
            x_data[index] = image
            if create_labels:
                labels.append(label)
                labels_set[label] = 1

    if create_labels:
        return x_data, create_y_train(labels, labels_set, limit=limit), labels_set
    return x_data


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
    resize_dir_images(os.path.join(_FILE_PATH, '../dataset'), recursive=True)
