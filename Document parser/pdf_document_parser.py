# first run "pip install PyMuPDF"
# then  run "python pdf_document_parser.py <pdf path>"

import sys
import re
import fitz

checkXObject = r"/Type(?= */XObject)"                           # finds "/Type/XObject"
checkImage = r"/Subtype(?= */Image)"                            # finds "/Subtype/Image"

if len(sys.argv) != 2:
    print("Usage: %s <wrong number of parameters>" % sys.argv[0])
    exit(0)

this_document = fitz.open(sys.argv[1])
all_image_count = 0
all_objects_count = this_document._getXrefLength()

for iterator in range(1, all_objects_count):                    # scan through all objects
    this_object = this_document._getObjectString(iterator)      # string defining the object

    is_XObject = re.search(checkXObject, this_object)           # tests for XObject
    is_Image = re.search(checkImage, this_object)               # tests for Image

    if not is_XObject or not is_Image:                          # not an image object if not both True
        continue

    all_image_count = all_image_count + 1
    png_image = fitz.Pixmap(this_document, iterator)            # make png from image

    if png_image.n < 4:                                         # can be saved as PNG
        png_image.writePNG("image_%s.png" % iterator)
    else:                                                       # must convert the CMYK first
        rgb_image = fitz.Pixmap(fitz.csRGB, png_image)
        rgb_image.writePNG("image_%s.png" % iterator)
        rgb_image = None

    png_image = None
