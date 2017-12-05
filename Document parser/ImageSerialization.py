from PIL import Image


def get_info_from_image(path):
    img = Image.open(path)
    pixels = img.load()
    pixels_dict = [
        {
            'red': pixels[i, j][0],
            'green': pixels[i, j][1],
            'blue': pixels[i, j][2]
        }
        for i in range(0, img.size[1])
        for j in range(0, img.size[0])]
    return {
        'width': img.size[0],
        'height': img.size[1],
        'pixels': pixels_dict
    }
