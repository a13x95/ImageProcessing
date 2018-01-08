import zipfile, os, sys, shutil
from os import path
import xml.etree.ElementTree as ET
import ImageSerialization
import DatabaseConnection


namespaces = {'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
              'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
              'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
              'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
              'v': 'urn:schemas-microsoft-com:vml'}


def getText(paragraph):
    nextText = ""
    for text in paragraph.findall('.//w:t', namespaces):
        nextText += text.text
    return nextText


def saveImage(path, picName):
    pic = os.path.basename(picName)

    if not os.path.exists("result"):
        os.mkdir("result")

    newpath = os.path.join("result", pic)

    fout = open(newpath, 'w')
    fout.close()

    with open(path, 'rb') as fin:
        with open(newpath, 'ab') as fout:
            buff = fin.read(128)
            while buff:
                fout.write(buff)
                buff = fin.read(128)


def getInfo(filepath):
    parentDir = os.path.dirname(filepath)
    dictRels = dict()

    docName = os.path.basename(filepath)

    relsFilePath = os.path.join(parentDir, "word", "_rels", "document.xml.rels")
    tree = ET.parse(relsFilePath)
    root = tree.getroot()
    for child in root:
        if 'image' in child.attrib['Type']:
            dictRels[child.attrib['Id']] = child.attrib['Target']

    finalArray = []

    docFilePath = os.path.join(parentDir, "word", "document.xml")

    tree = ET.parse(docFilePath)
    root = tree.getroot()


    paragraphsList = root.findall('.//w:p', namespaces)
    numParagraphs = len(paragraphsList)

    for paragraphIndex in range(0, numParagraphs):
        e = paragraphsList[paragraphIndex]
        if e.findall('.//w:drawing', namespaces) != []:
            for pic in e.findall('.//w:drawing/wp:anchor/a:graphic/a:graphicData/pic:pic', namespaces):

                for item in pic.findall('pic:blipFill/a:blip', namespaces):
                    for key, value in item.attrib.items():
                        if 'embed' in key:
                            image = value
                            break

                newpath = os.path.join('.', 'word', dictRels[image])
                dictNew = ImageSerialization.get_info_from_image(newpath)
                del dictNew['pixels']

                saveImage(newpath, dictRels[image])

                for item in pic.findall('.//pic:nvPicPr/pic:cNvPr', namespaces):
                    if 'title' in item.attrib:
                        dictNew['caption'] = item.attrib['title']
                    elif 'descr' in item.attrib:
                        dictNew['caption'] = item.attrib['descr']
                    else:
                        paragraphs = [paragraph for paragraph in root.findall(".//w:p", namespaces) if paragraph.get(
                            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rsidP') == e.get(
                            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rsidP')]
                        for paragraph in paragraphs:
                            if paragraph.findall('.//w:t', namespaces) != []:
                                dictNew['caption'] = getText(paragraph)
                                break

                dictNew['text'] = ""

                if paragraphIndex > 0:
                    prevParagraph = paragraphsList[paragraphIndex - 1]
                    dictNew['text'] += getText(prevParagraph)

                if paragraphIndex < numParagraphs - 1:
                    nextParagraph = paragraphsList[paragraphIndex + 1]
                    dictNew['text'] += getText(nextParagraph)

                dictNew['position'] = str(paragraphIndex) + "/" + str(numParagraphs)
                dictNew['document'] = docName

                db = DatabaseConnection.DatabaseConnection()
                db.insert_entry(dictNew)

                finalArray.append(dictNew)

            for pic in e.findall('.//w:drawing/wp:inline/a:graphic/a:graphicData/pic:pic', namespaces):
                for item in pic.findall('.//pic:blipFill/a:blip', namespaces):
                    for key, value in item.attrib.items():
                        if 'embed' in key:
                            image = value
                            break

                newpath = os.path.join('.', 'word', dictRels[image])

                dictNew = ImageSerialization.get_info_from_image(newpath)
                del dictNew['pixels']

                saveImage(newpath, dictRels[image])

                for item in pic.findall('.//pic:nvPicPr/pic:cNvPr', namespaces):
                    if 'title' in item.attrib:
                        dictNew['caption'] = item.attrib['title']
                    elif 'descr' in item.attrib:
                        dictNew['caption'] = item.attrib['descr']
                    else:
                        paragraphs = [paragraph for paragraph in root.findall(".//w:p", namespaces) if paragraph.get(
                            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rsidP') == e.get(
                            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rsidP')]
                        for paragraph in paragraphs:
                            if paragraph.findall('.//w:t', namespaces) != []:
                                dictNew['caption'] = getText(paragraph)
                                break

                dictNew['text'] = ""

                if paragraphIndex > 0:
                    prevParagraph = paragraphsList[paragraphIndex - 1]
                    dictNew['text'] += getText(prevParagraph)

                if paragraphIndex < numParagraphs - 1:
                    nextParagraph = paragraphsList[paragraphIndex + 1]
                    dictNew['text'] += getText(nextParagraph)

                dictNew['position'] = str(paragraphIndex) + "/" + str(numParagraphs)
                dictNew['document'] = docName

                db = DatabaseConnection.DatabaseConnection()
                db.insert_entry(dictNew)

                finalArray.append(dictNew)
        if e.findall('.//w:pict', namespaces) != []:
            for pic in e.findall('.//w:pict/v:shape/v:imagedata', namespaces):
                for key, value in pic.attrib.items():
                    if 'id' in key:
                        image = value
                        break

                newpath = os.path.join('.', 'word', dictRels[image])

                dictNew = ImageSerialization.get_info_from_image(newpath)
                del dictNew['pixels']

                dictNew = {}
                saveImage(newpath, dictRels[image])

                if 'title' in pic.attrib:
                    dictNew['caption'] = item.attrib['title']
                elif 'descr' in pic.attrib:
                    dictNew['caption'] = item.attrib['descr']
                else:
                    paragraphs = [paragraph for paragraph in root.findall(".//w:p", namespaces) if paragraph.get(
                        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rsidP') == e.get(
                        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rsidP')]
                    for paragraph in paragraphs:
                        if paragraph.findall('.//w:t', namespaces) != []:
                            dictNew['caption'] = getText(paragraph)
                            break

                dictNew['text'] = ""

                if paragraphIndex > 0:
                    prevParagraph = paragraphsList[paragraphIndex - 1]
                    dictNew['text'] += getText(prevParagraph)

                if paragraphIndex < numParagraphs - 1:
                    nextParagraph = paragraphsList[paragraphIndex + 1]
                    dictNew['text'] += getText(nextParagraph)

                dictNew['position'] = str(paragraphIndex) + "/" + str(numParagraphs)
                dictNew['document'] = docName

                db = DatabaseConnection.DatabaseConnection()
                db.insert_entry(dictNew)

                finalArray.append(dictNew)

    return finalArray


def convert(filepath):
    from win32com import client

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


def docx_document_parser(argv):
    filepath = argv
    if filepath.endswith(".doc"):
        convert(filepath)
    else:
        extractImages(filepath)

if __name__ == '__main__':
    argv = sys.argv
    docx_document_parser(argv)
