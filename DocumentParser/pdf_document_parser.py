# first run "pip install PyMuPDF"
# then  run "python pdf_document_parser.py <pdf path>"

import sys
import re
import fitz

import sys
sys.path.append('../CollectedDataDump')
import DatabaseConnection

def pdf_document_parser(argv):
    checkXObject = r"/Type(?= */XObject)"                          
    checkImage = r"/Subtype(?= */Image)"                            

    if len(argv) != 2:
        print("Usage: %s <wrong number of parameters>" % argv[0])
        exit(0)

    this_document = fitz.open(argv[1])
    all_image_count = 0

    results = []

    for each_page in range(len(this_document)):
        image_list = this_document.getPageImageList(each_page)

        current_page = this_document.loadPage(each_page)
        current_page_text = current_page.getText(output = 'txt') 

        for each_image in image_list:
            this_object = each_image[0]
            pixels = fitz.Pixmap(this_document, this_object)
            all_image_count = all_image_count + 1

            if pixels.n < 4:      
                pixels.writePNG("%simage_%s.png" % (argv[0], all_image_count))
            else:                                              
                rgb_image = fitz.Pixmap(fitz.csRGB, pixels)
                rgb_image.writePNG("%simage_%s.png" % (argv[0], all_image_count))
                rgb_image = None

            pixels = None

            result = {
                "path" : "%simage_%s.png" % (argv[0], all_image_count),
                "text" : current_page_text,
                "page": each_page
            }

            results.append(result)
    
    database = DatabaseConnection()
    database.insert_entry(results)


if __name__ == "__main__":
    argv = sys.argv
    argv[0] = ""
    pdf_document_parser(argv)