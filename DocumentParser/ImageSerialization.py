from PIL import Image, ImageOps
import sys

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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError(f'You need to provide at least 1 parameter but {len(sys.argv) - 1} were given')

    import os
    import json

    if not os.path.exists(sys.argv[1]):
        raise ValueError('You need to provide an existing path')
    if not os.path.isdir(sys.argv[1]):
        raise ValueError('The path does not point to a directory but to other type of file')

    with open('result.json', 'w') as output:
        output.write('[')

        first = True
        for files in os.listdir(sys.argv[1]):
            file_path = os.path.join(sys.argv[1], files)
            if os.path.isfile(file_path):
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    result = get_info_from_image(file_path)
                    print(f'>> finished analyzing file: {file_path}; started writing')
                    if first:
                        first = False
                        output.write(json.dumps(result, separators=(',', ':')))
                    else:
                        output.write(',' + json.dumps(result, separators=(',', ':')))
                    print(f'>> finished writing output')

        output.write(']')

    print('>> done parsing files')
    # print('>> starting writing to file')
    #
    # with open('result.json', 'w') as output:
    #     output.write(json.dumps(result, separators=(',', ':')) + '\n')

    print('>> finished writing results to file')
