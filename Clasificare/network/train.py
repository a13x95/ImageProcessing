import os

import numpy as np
from scipy.ndimage import imread
from Clasificare.network.model import build_model
import progressbar

_SHOULD_RESIZE_DATASET = False
_DATASET_SIZE = (512, 512)

_FILE_PATH = os.path.abspath(os.path.dirname(__file__))
_TRAIN_PATH = os.path.join(_FILE_PATH, './train')
_TEST_PATH = os.path.join(_FILE_PATH, './test')


def get_image_data(file):
    image = imread(file, mode="RGB")
    return np.array(image) / 255.


def read_data(dirpath,
              image_size=(128, 128),
              labels=2,
              create_labels=True,
              limit=None):

    files = os.listdir(dirpath)
    num_images = len(files)
    if limit is None:
        limit = num_images
    x_data = np.empty(shape=(limit, image_size[0], image_size[1], 3))
    y_data = np.empty(shape=(limit, labels))

    bar = progressbar.ProgressBar()
    for index, filename in bar(list(enumerate(files))[:limit]):
        file = os.path.join(dirpath, filename)
        if os.path.isfile(file):
            is_dog = 1.0
            if filename.find('cat') != -1:
                is_dog = 0

            image = get_image_data(file)
            x_data[index] = image
            if create_labels:
                y_data[index] = np.array([1. - is_dog, is_dog])

    if create_labels:
        return x_data, y_data
    return x_data


def run():
    x_train, y_train = read_data(_TRAIN_PATH)
    # test = read_data(_TEST_PATH)

    model = build_model(lr=0.5)

    model.fit(
        x=x_train,
        y=y_train,
        epochs=20,
        batch_size=300,
        verbose=True
    )

    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)


if __name__ == '__main__':
    run()
