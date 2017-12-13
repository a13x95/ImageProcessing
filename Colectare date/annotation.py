from html.parser import HTMLParser
import os
import shutil


def get_content_by_category(category):
    return open(os.path.join("XML_annotations", category + ".xml")).read()


attributes = []
annotations = list(map(lambda x: x[:len(x) - 4], os.listdir("XML_annotations")))


class ParserXML(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attributes.append(attrs)


if not os.path.exists("TRAINING_SET"):
    os.mkdir("TRAINING_SET")


parser = ParserXML()
for key in annotations:
    print(">" * 5, key)
    counter = 0
    parser.feed(get_content_by_category(key))
    new_path = os.path.join("TRAINING_SET", key.upper())
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for attr in attributes:
        img_name = filter(lambda x: x[0] == 'src', attr)
        img_name = os.path.basename(list(img_name)[0][1])
        try:
            shutil.copy(os.path.join("TrainingImages", img_name), os.path.join(new_path, img_name))
            counter += 1
        except Exception:
            pass
    print("     Added {} images for {}".format(counter, key))
