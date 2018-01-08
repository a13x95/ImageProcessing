import os
from keras import optimizers, Model
from keras.layers import Dense, Flatten, Dropout, BatchNormalization
from keras.applications.vgg16 import VGG16
from keras.optimizers import SGD
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import confusion_matrix

from Clasificare.statistics.statistics import build_confusion_matrix
from Clasificare.utils.dataset_utils import read_data


def load_vgg_16(num_classes):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    x = Flatten()(base_model.output)
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = BatchNormalization()(x)
    predictions = Dense(num_classes, activation='softmax', use_bias=False)(x)

    # create graph of your new model
    head_model = Model(input=base_model.input, output=predictions)

    # compile the model
    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.4, nesterov=True)
    head_model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

    return head_model


_FILE_PATH = os.path.abspath(os.path.dirname(__file__))


def build_model(dataset):
    named_labels = dataset.named_labels

    model = load_vgg_16(len(named_labels))

    return model


def fit_model(model,
              x_train, y_train, y_train_labeled,
              x_test, y_test, y_test_labeled):
    return model.fit(
        x=x_train,
        y=y_train,
        epochs=22,
        validation_data=(x_test, y_test),
        batch_size=30,
        verbose=True
    )


def train_model(dataset_path="../../dataset/vgg16"):
    dataset = read_data(
        dataset_path,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True,
        shuffle=True
    )

    x = dataset.x
    y = dataset.y
    named_labels = dataset.named_labels

    model = build_model(dataset)

    history = model.fit(
        x=x,
        y=y,
        epochs=22,
        batch_size=30,
        validation_split=0.2,
        verbose=True
    )

    # serialize model to JSON
    model_json = model.to_json()
    with open("./trained_models/vgg16.json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model.save_weights("./trained_models/vgg16.h5")

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
    train_model()
