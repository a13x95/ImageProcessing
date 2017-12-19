import os
from keras import optimizers
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, regularizers, AveragePooling2D
from keras.models import Sequential, model_from_json
import numpy as np


def build_model(lr=0.01):
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
        optimizer=optimizers.RMSprop(lr=lr),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


_FILE_PATH = os.path.abspath(os.path.dirname(__file__))


def load_model(model="./model_medical.json",
               weights="./model_medical.h5"):
    model_path = os.path.join(_FILE_PATH, model)
    weights_path = os.path.join(_FILE_PATH, weights)

    # load json and create model
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(weights_path)

    return loaded_model


_LABELS = [
    "ANEURYSM",
    "ARTERIOVENOUS MALFORMATION",
    "BASIN",
    "BRAIN",
    "BRAIN TRAUMA",
    "CARDIOGENIC PULMONARY EDEMA",
    "CEREBRAL ABSCESS",
    "CHEST RADIOLOGY",
    "COMMON CAROTID OCCLUSION",
    "DEGENERATIVE DISEASE",
    "EYE",
    "FEMALE_GENITALS",
    "FETUS",
    "FOOT",
    "HAND",
    "HEAD",
    "HEART",
    "HORSESHOE KIDNEY",
    "HYPERPLASIA",
    "IDIOPATHIC",
    "KIDNEYS",
    "LEGS",
    "LONGITUDINAL PETROUS (TEMPORAL BONE) FRACTURE",
    "LUNGS",
    "MALE_GENITALS",
    "MITRAL STENOSIS",
    "MULTIPLE SCLEROSIS",
    "NECK",
    "NEUROFIBROMATOSIS TYPE 1",
    "PELVIC",
    "PULMONARY CANCER",
    "RUPTURED DERMOID INCLUSION CYST",
    "SPINE",
    "SURGICAL HEMORRHAGE"
]


def predict(image, model=None):
    if model is None:
        model = load_model("./model_medical.json", "./model_medical.h5")

    shape = image.shape
    single_instance_shape = (1, shape[0], shape[1], shape[2])
    y = model.predict(image.reshape(single_instance_shape))
    label = y[0].argmax()
    image.reshape(shape)

    return _LABELS[label]
