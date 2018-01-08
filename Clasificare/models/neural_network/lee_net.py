import os
from keras import optimizers
from keras.layers import Dense, Conv2D, Flatten, Dropout, AveragePooling2D
from keras.models import Sequential
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import confusion_matrix
from Clasificare.statistics.statistics import build_confusion_matrix


def build_model(dataset):
    # Network input shape is 128 x 128 RGB
    model = Sequential()

    # ## 1nd conv + relu + pool: 128x128x3 -> 128x128x3 -> 32x32x64
    model.add(
        Conv2D(
            filters=32,
            kernel_size=(5, 5),
            input_shape=(128, 128, 3),
            padding="same",
            data_format='channels_last',
            activation='relu')
    )
    model.add(
        AveragePooling2D(
            pool_size=(4, 4))
    )
    # ## END ## #

    # ## 2nd conv + relu + pool: 32x32x64 -> 32x32x128 -> 16x16x128
    model.add(
        Conv2D(
            filters=128,
            kernel_size=(5, 5),
            input_shape=(32, 32, 32),
            strides=(2, 2),
            padding="same",
            data_format='channels_last',
            activation='relu')
    )
    model.add(
        AveragePooling2D(
            pool_size=(2, 2))
    )
    # ## END ## #

    # ## 3rd conv + relu + pool: 8x8x128 -> 8x8x256 -> 4x4x256
    model.add(
        Conv2D(
            filters=256,
            kernel_size=(3, 3),
            input_shape=(8, 8, 128),
            padding="same",
            data_format='channels_last',
            activation='relu')
    )
    model.add(
        AveragePooling2D(
            pool_size=(2, 2))
    )
    # ## END ## #

    # ## 4th conv + relu + pool: 4x4x256 -> 4x4x512 -> 2x2x512
    model.add(
        Conv2D(
            filters=512,
            kernel_size=(3, 3),
            input_shape=(4, 4, 256),
            padding="same",
            data_format='channels_last',
            activation='relu')
    )
    model.add(
        AveragePooling2D(
            pool_size=(2, 2))
    )
    # ## END ## #

    # ## 5th conv + relu + pool: 2x2x512 -> 2x2x1024 -> 1x1x1024
    model.add(
        Conv2D(
            filters=1024,
            kernel_size=(3, 3),
            input_shape=(2, 2, 512),
            padding="same",
            data_format='channels_last',
            activation='relu')
    )
    model.add(
        AveragePooling2D(
            pool_size=(2, 2))
    )
    # ## END ## #

    # flatten: 1x1x1024 -> 1024
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(
        Dense(units=100,
              activation='relu'
              )
    )
    model.add(Dropout(0.6))

    model.add(
        Dense(units=34,
              activation='softmax')
    )
    model.compile(
        optimizer=optimizers.RMSprop(lr=0.0006),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


_FILE_PATH = os.path.abspath(os.path.dirname(__file__))


def fit_model(model,
              x_train, y_train, y_train_labeled,
              x_test, y_test, y_test_labeled):
    return model.fit(
        x=x_train,
        y=y_train,
        epochs=60,
        validation_data=(x_test, y_test),
        batch_size=30,
        verbose=True
    )


def train_model(dataset):
    x = dataset.x
    y = dataset.y
    named_labels = dataset.named_labels

    model = build_model(dataset)

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
