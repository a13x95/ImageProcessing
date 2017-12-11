import zipfile, os, sys, json, shutil
from win32com import client
from os import path
import xml.etree.ElementTree as ET
import ImageSerialization

def getInfo(filepath):
    parentDir = os.path.dirname(filepath)
    dictRels = dict()

    relsFilePath = os.path.join(parentDir, "word", "_rels", "document.xml.rels")
    tree = ET.parse(relsFilePath)
    root = tree.getroot()
    for child in root:
        if 'image' in child.attrib['Type']:
            dictRels[child.attrib['Id']] = child.attrib['Target']

    finalArray = []

    docFilePath = os.path.join(parentDir, "word", "document.xml")

    namespaces = {'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
                  'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                  'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                  'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'}

    tree = ET.parse(docFilePath)
    root = tree.getroot()

    for e in root.findall('.//w:drawing/wp:anchor/a:graphic/a:graphicData/pic:pic', namespaces):
        for item in e.findall('.//pic:blipFill/a:blip', namespaces):
            for key, value in item.attrib.items():
                if 'embed' in key:
                    image = value
                    break

        newpath = os.path.join('.', 'word', dictRels[image])
        dictNou = ImageSerialization.get_info_from_image(newpath)

        for item in e.findall('.//pic:nvPicPr/pic:cNvPr', namespaces):
            if 'descr' in item.attrib:
                dictNou['caption'] = item.attrib['descr']

        dictNou['document'] = os.path.basename(filepath)

        finalArray.append(dictNou)

    return finalArray


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

    images = filter(lambda f : f.startswith('word'), all_files)

    for item in images:
        z.extract(item, r'.')

    result = getInfo(filepath)
    shutil.rmtree('./word')

    with open('result.json', 'w') as output:
        output.write(json.dumps(result, separators=(',', ':')) + '\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Wrong number of parameters")
        exit(0)

    filepath = sys.argv[1]

    if filepath.endswith(".doc"):
        convert(filepath)
    else:
        extractImages(filepath)