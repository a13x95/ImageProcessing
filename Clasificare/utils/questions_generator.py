import json
import numpy
import os
import sys
from PIL import Image
import random
"""parameter in command line: path to json (ca jsoanele lui Stefanus)"""
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError(f'You need to provide at least 1 parameter but {len(sys.argv) - 1} were given')

    if not os.path.exists(sys.argv[1]):
        raise ValueError('You need to provide an existing path (to json)')
    if not os.path.isfile(sys.argv[1]):
        raise ValueError('The path does not point to a file (json)')

    file_name = sys.argv[1]
    images = json.load(open(file_name))
    if not os.path.exists("QImages"):
        os.mkdir("QImages")

    annotations = []
    correct_answers = {}
    image_paths = []

    ANSWERS_PER_QUESTIONS = 3

    for counter, image in enumerate(images):
        height = image['height']
        width = image['width']
        pixels1D = image['pixels']
        annotation = image['adn']
        annotations.append(annotation)
        correct_answers[os.path.join("QImages", "{}.png".format(counter))] = annotation
        pixels = [pixels1D[i * width:(i + 1) * width] for i in range(0, height)]
        pixels = numpy.array(pixels, dtype=numpy.uint8)
        new_image = Image.fromarray(pixels)
        new_image.save(os.path.join("QImages", "{}.png".format(counter)))

    for image in correct_answers:
        question = {'question': 'What represents the image bellow?',
                    'path': image, 'correct': correct_answers[image]}
        answers = [x for x in annotations if x != correct_answers[image]]
        question['answers'] = random.sample(answers, ANSWERS_PER_QUESTIONS - 1)
        with open(os.path.join("QJeisoane", os.path.basename(image).split('.')[0] + ".json"), 'w') as outfile:
            json.dump(question, outfile)