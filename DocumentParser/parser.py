# PRECONDITIONS
# first run "pip install PyMuPDF"
# second run "pip install PyPDF2"
import urllib
import sys
import os
import PyPDF2
from pdf_document_parser import pdf_document_parser
#from ppt_document_parser import ppt_document_parser
#from docx_document_parser import docx_document_parser
#from html_page_parser import html_page_parser


def url_is_alive(url):
    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

def file_is_pdf(fileName):
    try:
        PyPDF2.PdfFileReader(open(fileName, "rb"))
        return True
    except PyPDF2.utils.PdfReadError:
        #print("invalid PDF file")
        return False

def file_is_docx(fileName):
    if fileName.endswith(".doc") or fileName.endswith(".docx"):
        return True
    return False

def file_is_ppt(fileName):
    if fileName.endswith(".pptx") or fileName.endswith(".ppt") or fileName.endswith(".pps"):
        return True
    return False

if __name__ == "__main__":
    argv = sys.argv
    argv[0] = ""
    if len(argv) != 2:
        print("Usage: %s <wrong number of parameters>" % argv[0])
        exit(0)
    folder = argv[1]
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if os.path.isdir(file) == False:
                base=os.path.basename(file)
                argv[0] = os.path.splitext(base)[0] + "/"
                if file_is_pdf(file):
                    pdf_document_parser(argv)
                # elif file_is_docx(file):
                #     docx_document_parser(argv[1])
                # elif file_is_ppt(file):
                #     ppt_document_parser(argv)
    if file_is_pdf(argv[1]):
        pdf_document_parser(argv)
    # elif url_is_alive(argv[1]):
    #     html_page_parser(argv)
    # elif file_is_docx(argv[1]):
    #     docx_document_parser(argv[1])
    # elif file_is_ppt(argv[1]):
    #     ppt_document_parser(argv)
    

