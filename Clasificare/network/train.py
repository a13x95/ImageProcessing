import os
from collections import Counter

import numpy as np
from scipy.ndimage import imread
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt

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
        return x_data, create_y_train(labels, labels_set, limit=limit), labels_set
    return x_data


def build_confusion_matrix(named_labels,
                           conf_mat,
                           filename='confusion_matrix.png'):
    fig_size = plt.rcParams["figure.figsize"]
    plt.rcParams["figure.figsize"] = [14, 6]

    fig = plt.figure(1)
    fig.canvas.set_window_title('Confusion matrix')

    plt.rcParams["figure.figsize"] = fig_size

    conf_mat_norm = conf_mat / conf_mat.sum(axis=1)[:, None]

    conf_mat2 = np.around(conf_mat_norm, decimals=1)
    plt.imshow(conf_mat2, interpolation='nearest', aspect='equal')
    for x in range(len(named_labels)):
        for y in range(len(named_labels)):
            plt.annotate(str(conf_mat2[x][y]), xy=(y, x), ha='center', va='center', fontsize=5)

    plt.xticks(range(len(named_labels)),
               rotation=90,
               fontsize=6)

    plt.yticks(range(len(named_labels)),
               map(lambda e: "{0} #{1}".format(e[1], e[0]),
                   enumerate(named_labels)),
               fontsize=6)

    plt.title('Confusion matrix')
    plt.colorbar()
    plt.savefig(filename)

    return fig


def run_fold_validation(folds=4):
    x, y, named_labels = read_data(
        _TRAIN_PATH,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True
    )

    y_labeled = np.argmax(y, axis=1)
    labels = frozenset(y_labeled)
    no_labels = len(labels)
    skf = StratifiedKFold(n_splits=folds, shuffle=True)
    conf_mat = np.zeros((no_labels, no_labels))
    for i, (train_index, test_index) in enumerate(skf.split(X=x, y=y_labeled)):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_test_labels = y_labeled[test_index]

        model = build_model(lr=0.0005)

        model.fit(
            x=x_train,
            y=y_train,
            validation_data=(x_test, y_test),
            epochs=4,
            batch_size=70,
            verbose=True
        )

        y_predict = model.predict(x_test)
        y_predict_labels = np.argmax(y_predict, axis=1)
        cm = confusion_matrix(y_test_labels, y_predict_labels)
        conf_mat = conf_mat + cm

    build_confusion_matrix(named_labels, conf_mat)
    plt.show()


def run():
    x, y, named_labels = read_data(
        _TRAIN_PATH,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True
    )

    model = build_model(lr=0.0005)

    history = model.fit(
        x=x,
        y=y,
        epochs=100,
        batch_size=50,
        verbose=True
    )

    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    # confusion matrix
    y_labeled = np.argmax(y, axis=1)
    y_predict = model.predict(x)
    y_predict_labels = np.argmax(y_predict, axis=1)
    conf_mat = confusion_matrix(y_labeled, y_predict_labels)
    build_confusion_matrix(named_labels,
                           conf_mat,
                           filename='run_confusion_matrix.png')

    fig = plt.figure(2)
    fig.canvas.set_window_title('Training plots')

    # accuracy

    plt.subplot(211)
    plt.plot(history.history['acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train'], loc='upper left')

    # loss

    plt.subplot(212)
    plt.plot(history.history['loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train'], loc='upper left')
    plt.show()


if __name__ == '__main__':
    run()
