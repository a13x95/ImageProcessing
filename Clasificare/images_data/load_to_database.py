import json
import os

from PIL import Image
from bson import ObjectId
from pymongo import MongoClient


def get_info_from_image(path):
    img = Image.open(path)
    pixels = img.load()
    image_pixels_rgb = [
        (
            255 - int((pixels[width, height] * 0x00010101) / 10000),
            255 - int(((pixels[width, height] * 0x00010101) / 100) % 100),
            255 - int((pixels[width, height] * 0x00010101) % 100)
        )
        for height in range(0, img.size[1])
        for width in range(0, img.size[0])
    ] if isinstance(pixels[0, 0], int) else [
        (
            pixels[width, height][0],
            pixels[width, height][1],
            pixels[width, height][2]
        )
        for height in range(0, img.size[1])
        for width in range(0, img.size[0])
    ]
    return {
        'width': img.size[0],
        'height': img.size[1],
        'pixels': image_pixels_rgb
    }


if __name__ == "__main__":
    client = MongoClient("mongodb://mongodb0.example.net:27017")
    db = client['medical_database']

    directory = '/home/andrei/PycharmProjects/ImageProcessing/Clasificare/images_data/Pictures'
    for dir in os.listdir(directory):
        current_dir = os.path.join(directory, dir)
        if os.path.isdir(dir):
            collection = db['dir']
            for img in os.listdir(current_dir):
                if img.split('.')[-1] == 'jpg':
                    img_path = os.path.join(current_dir, img)

                    img = get_info_from_image(img_path)
                    id = ObjectId()

                    data = {'category': dir, 'height': img['height'], 'width': img['width'], 'pixels': img['pixels']}

                    json_data = json.dumps(data)
                    post_id = collection.insert_one(data).inserted_id

                    break
        break
