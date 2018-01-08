import numpy as np
from keras.models import model_from_json
from skimage.transform import resize

from Clasificare.models.consts import LABELS


def predict(image, model):
    """
    Computes the probabilities for each label, given an image.

    :param image: The image to classify. Must be in the format (x, y, 3)
    :param model: The model to use for classification.
    :return: A mapping from labels to probabilities.
    """
    norm_image = image / 255.
    model_input_shape = tuple(map(int, model.input.shape[1:]))

    resized_image = resize(norm_image, output_shape=model_input_shape) * 255.

    image_x = np.expand_dims(resized_image, axis=0)
    probabilities = model.predict(image_x)

    stats = {}
    for idx in range(probabilities.shape[1]):
        stats[LABELS[idx]] = probabilities[0, idx]

    return stats


def load_model(model_file="./model_medical.json",
               weights_file="./model_medical.h5"):

    # load json and create model
    json_file = open(model_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(weights_file)

    return loaded_model
