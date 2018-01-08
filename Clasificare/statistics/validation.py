from functools import reduce
from operator import mul

from sklearn.model_selection import StratifiedKFold
from tensorflow import confusion_matrix
import numpy as np
from Clasificare.statistics.statistics import build_confusion_matrix
import matplotlib.pyplot as plt


def kfold_validation(dataset,
                     build_model_method,
                     fit_model_method,
                     confusion_matrix_file=None,
                     folds=4):
    x = dataset.x
    y = dataset.y
    named_labels = dataset.named_labels

    y_labeled = np.argmax(y, axis=1)
    labels = frozenset(y_labeled)
    no_labels = len(labels)
    skf = StratifiedKFold(n_splits=folds, shuffle=True)
    conf_mat = np.zeros((no_labels, no_labels))
    for i, (train_index, test_index) in enumerate(skf.split(X=x, y=y_labeled)):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_test_labels = y_labeled[test_index]
        y_train_labels = y_labeled[train_index]

        print("Fitting model for iteration %s" % (i + 1))
        model = build_model_method(dataset)
        fit_model_method(
            model,
            x_train,
            y_train,
            y_train_labels,
            x_test,
            y_test,
            y_test_labels
        )

        y_predict_labels = np.argmax(model.predict(x_test), axis=1)
        cm = confusion_matrix(y_test_labels, y_predict_labels)
        conf_mat = conf_mat + cm
        del x_train, y_train, x_test, y_test

    filename = confusion_matrix_file
    if confusion_matrix_file is None:
        filename = 'validation_confusion_matrix_{0}_folds.png'.format(folds)
    build_confusion_matrix(
        named_labels,
        conf_mat,
        filename=filename
    )
    plt.show()
