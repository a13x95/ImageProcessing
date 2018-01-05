# PRECONDITIONS
# first run "pip install PyMuPDF"
import urllib
import sys
from pdf_document_parser import pdf_document_parser
from ppt_document_parser import ppt_document_parser
from html_page_parser import html_page_parser


def url_is_alive(url):
    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

if __name__ == "__main__":
    if url_is_alive(sys.argv[1]):

