import zipfile
import os
import sys
from win32com import client
from os import path

def convert(filepath):
    try:
        word = client.DispatchEx("Word.Application")
        folder = path.dirname(filepath)
        files = path.basename(filepath)
        new_name = files.replace(".doc", r".docx")
        in_file_path = path.join(folder, files)
        in_file = path.abspath(in_file_path)
        new_file_path = path.join(folder, new_name)
        new_file = path.abspath(new_file_path)
        doc = word.Documents.Open(in_file)
        doc.SaveAs(new_file, FileFormat=16)
        doc.Close()
        extractImages(new_file)
        os.remove(new_file)
    except Exception as e:
        print(e)
    finally:
        word.Quit()


def extractImages(filepath):
    z = zipfile.ZipFile(filepath)
    all_files = z.namelist()

    images = filter(lambda f : f.startswith('word/media'), all_files)

    for item in images:
        z.extract(item, r'.')

if len(sys.argv) != 2:
    print("Wrong number of parameters")
    exit(0)

filepath = sys.argv[1]

if filepath.endswith(".doc"):
    convert(filepath)
else:
    extractImages(filepath)