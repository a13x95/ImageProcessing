import os

import numpy as np
from scipy.ndimage import imread
from Clasificare.network.model import build_model
import progressbar

_SHOULD_RESIZE_DATASET = False
_DATASET_SIZE = (512, 512)

_FILE_PATH = os.path.abspath(os.path.dirname(__file__))
_TRAIN_PATH = os.path.join(_FILE_PATH, '../images_data/Pictures')
_TEST_PATH = os.path.join(_FILE_PATH, './test')


def get_image_data(file):
    image = imread(file, mode="RGB")
    return np.array(image) / 255.


def find_all_files(dirpath, recursive=False):
    files = []
    for name in os.listdir(dirpath):
        file = os.path.join(dirpath, name)
        if recursive and os.path.isdir(file):
            files.extend(find_all_files(file))

        if os.path.isfile(file):
            files.append(file)

    return files


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
              recursive=False):
    files = find_all_files(dirpath, recursive=recursive)
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
        return x_data, create_y_train(labels, labels_set, limit=limit)
    return x_data


def run():
    x_train, y_train = read_data(
        _TRAIN_PATH,
        lambda x: os.path.dirname(x),
        recursive=True
    )
    # test = read_data(_TEST_PATH)

    model = build_model(lr=0.05)

    model.fit(
        x=x_train,
        y=y_train,
        epochs=58,
        batch_size=5,
        verbose=True
    )

    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)


if __name__ == '__main__':
    run()
