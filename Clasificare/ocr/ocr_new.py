from PIL import Image
import sys
import cv2
import numpy as np

import codecs
import pyocr.builders


def remove_noise(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    for row in img:
        for i in range(0, len(row)):
            if row[i] > 195:
                row[i] = 255
            else:
                row[i] = 0

    cv2.imwrite("removed_noise.png", img)
    return 'removed_noise.png'


def ocr(imagePath):
    tools = pyocr.get_available_tools()
    builder = pyocr.builders.TextBuilder()

    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'libtesseract'

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[0]
    print("Will use lang '%s'" % (lang))

    txt = tool.image_to_string(
        Image.open(remove_noise(imagePath)),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )

    with codecs.open(imagePath + 'result.txt', 'w', encoding='utf-8') as file_descriptor:
        builder.write_file(file_descriptor, txt)


if __name__ == '__main__':
    for i in range(1, 9):
        ocr('tests/testImg' + str(i) + '.jpg')
