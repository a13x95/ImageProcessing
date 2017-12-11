from keras import optimizers
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, regularizers
from keras.models import Sequential


def build_model(lr=0.01):
    # Network input shape is 256 x 256 RGB
    model = Sequential()

    # ## 1nd conv + relu + pool: 128x128x3 -> 128x128x3 -> 32x32x64
    model.add(
        Conv2D(
            filters=64,
            kernel_size=(5, 5),
            input_shape=(128, 128, 3),
            padding="same",
            data_format='channels_last',
            activation='relu')
    )
    model.add(
        MaxPooling2D(
            pool_size=(4, 4))
    )
    # ## END ## #

    # ## 2nd conv + relu + pool: 32x32x64 -> 32x32x128 -> 16x16x128
    model.add(
        Conv2D(
            filters=128,
            kernel_size=(3, 3),
            input_shape=(32, 32, 64),
            padding="same",
            data_format='channels_last',
            activation='relu')
    )
    model.add(
        MaxPooling2D(
            pool_size=(4, 4))
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
        MaxPooling2D(
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
        MaxPooling2D(
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
        MaxPooling2D(
            pool_size=(2, 2))
    )
    # ## END ## #

    # flatten: 1x1x1024 -> 1024
    model.add(Flatten())

    model.add(
        Dense(units=100,
              activation='relu',
              kernel_regularizer=regularizers.l2(0.001),
              input_dim=1024))
    model.add(Dropout(0.3))
    model.add(Dense(units=2, activation='softmax'))
    model.compile(
        optimizer=optimizers.SGD(lr=lr),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model
