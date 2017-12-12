import requests
import eventlet
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.request import urlopen, Request
import os
import json

eventlet.monkey_patch()


def read_file(file_name):
    with open(file_name) as f:
        data = f.read().split('\n')
    return data


def get_extension(file_name):
    return file_name.split('.')[-1]


def gather_images(keyword_param, x_dim, y_dim, start_search):
    def get_soup(url, header):
        return BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')

    query = keyword_param
    query = query.split()
    query = '+'.join(query)
    url = "https://www.google.co.in/search?q=" + query + "&start=" + str(start_search) + "&num=1000&source=lnms&tbm=isch"
    print(url)

    # add the directory for your image here
    dir = "Pictures"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 "
                      "Safari/537.36 "
    }

    soup = get_soup(url, header)

    actual_images = []  # contains the link for Large original images, type of  image
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        actual_images.append((link, type))

    print("there are total", len(actual_images), "images")

    if not os.path.exists(dir):
        os.mkdir(dir)
    dir = os.path.join(dir, query.split()[0])

    if not os.path.exists(dir):
        os.mkdir(dir)

    for i, (img, type) in enumerate(actual_images):
        try:
            print(str(i))

            with eventlet.Timeout(2, False):
                response = requests.get(img)
            if response is None:
                print('Timed-out')
                continue

            img = Image.open(BytesIO(response.content)).convert('RGB')
            img = img.resize((x_dim, y_dim), Image.ANTIALIAS)
            img.save(os.path.join(dir, str(i) + ".jpg"), "JPEG",
                     quality=80, optimize=True, progressive=True)

        except Exception as e:
            print("could not load : " + img)
            print(e)


def gather_multi_images(keyword_param, x_dim, y_dim, no_images):
    i = 0
    while i <= no_images:
        gather_images(keyword_param, x_dim, y_dim, i)
        i += 100


if __name__ == "__main__":
    keywords = read_file('keywords')
    for keyword in keywords:
        if keyword:
            gather_images(keyword, 128, 128, 5)
