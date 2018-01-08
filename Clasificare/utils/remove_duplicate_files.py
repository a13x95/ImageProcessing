
import os
import sys


def relative_files(path):
    dic = {}
    for root, dirnames, files in os.walk(path):
        relroot = os.path.relpath(root, path)
        for filename in files:
            if filename not in dic:
                dic[filename] = []
            dic[filename].append(os.path.join(root, filename))
    for key in dic:
        if len(dic[key]) > 1:
            for path in dic[key]:
                os.remove(path)


if __name__ == "__main__":
    directory = "../dataset/vgg16"
    relative_files(directory)
