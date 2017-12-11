import zipfile
import os
import sys
import win32com
from win32com import client

def PPT_convertor(filepath):
    try:
        Application = win32com.client.Dispatch("PowerPoint.Application")
        Application.Visible = True
        if filepath.endswith(".ppt"):
            new_filepath = filepath.replace(".ppt", r".pptx")
        elif filepath.endswith(".pps"):
            new_filepath = filepath.replace(".pps", r".pptx")
        Presentation = Application.Presentations.Open(filepath)
        Presentation.Saveas(new_filepath)
        Presentation.Close()
        return new_filepath
    except Exception as e:
        print(e)
    finally:
        Application.Quit()

def PPTX_extractImages(filepath):

    if zipfile.is_zipfile(filepath):

        z = zipfile.ZipFile(filepath)
        images = list()
        for file in z.namelist():
            path, name = os.path.split(file)
            if path == "ppt/media":
                images.append(file)
        for img in images:
            z.extract(img,r'.')

if len(sys.argv) > 2:
    print("Wrong number of parameters")
    exit(0)

filepath = sys.argv[1]

if filepath.endswith(".pptx"):
    PPTX_extractImages(filepath)

elif filepath.endswith(".ppt") or filepath.endswith(".pps"):

    new_filepath = PPT_convertor(filepath)
    PPTX_extractImages(new_filepath)
    os.remove(new_filepath)



