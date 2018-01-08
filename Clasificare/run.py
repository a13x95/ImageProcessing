import sys
import os

from scipy.ndimage import imread
from Clasificare.models.neural_network.utils import load_model, predict


if __name__ == '__main__':
    file = sys.argv[1]
    image = imread(file, mode='RGB')

    model = load_model(
        model_file='./models/trained_models/vgg16.json',
        weights_file='./models/trained_models/vgg16.h5'
    )

    print(predict(image, model))
