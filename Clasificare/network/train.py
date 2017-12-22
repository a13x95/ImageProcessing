import os
from collections import Counter

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
from Clasificare.network.model import build_model, predict

from Clasificare.utils.dataset_utils import read_data


_SHOULD_RESIZE_DATASET = False
_DATASET_SIZE = (512, 512)

_FILE_PATH = os.path.abspath(os.path.dirname(__file__))
_TRAIN_PATH = os.path.join(_FILE_PATH, './train')
_TEST_PATH = os.path.join(_FILE_PATH, './test')


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


def get_class_weights(y, smooth_factor=0):
    """
    Returns the weights for each class based on the frequencies of the samples
    :param smooth_factor: factor that smooths extremely uneven weights
    :param y: list of true labels (the labels must be hashable)
    :return: dictionary with the weight for each class
    """
    counter = Counter(y)

    if smooth_factor > 0:
        p = max(counter.values()) * smooth_factor
        for k in counter.keys():
            counter[k] += p

    majority = max(counter.values())

    return {cls: float(majority / count) for cls, count in counter.items()}


def kfold_validation(folds=4):
    x, y, named_labels = read_data(
        _TRAIN_PATH,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True,
        shuffle=True
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
        y_train_labeled = y_labeled[train_index]

        model = build_model(lr=0.0006)

        model.fit(
            x=x_train,
            y=y_train,
            validation_data=(x_test, y_test),
            epochs=60,
            batch_size=30,
            verbose=True
        )

        y_predict = model.predict(x_test)
        y_predict_labels = np.argmax(y_predict, axis=1)
        cm = confusion_matrix(y_test_labels, y_predict_labels)
        conf_mat = conf_mat + cm

    filename = 'validation_confusion_matrix_{0}_folds.png'.format(folds)
    build_confusion_matrix(
        named_labels,
        conf_mat,
        filename=filename
    )
    plt.show()


def run():
    x, y, named_labels = read_data(
        _TRAIN_PATH,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True
    )

    model = build_model(lr=0.0006)

    history = model.fit(
        x=x,
        y=y,
        epochs=60,
        batch_size=30,
        verbose=True
    )

    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model.save_weights("model.h5")

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


def test():
    x, y, named_labels = read_data(
        _TRAIN_PATH,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True,
        limit=10
    )

    print(predict(x[0]))


if __name__ == '__main__':
    test()
