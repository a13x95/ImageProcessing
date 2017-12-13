#pip install beautifulsoup4
#run "python html_page_parser.py <link>" [EX] "python html_page_parser.py http://students.info.uaic.ro/"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import sys,os,json,ImageSerialization

def extractImageSrc(tag):
    src=tag.split("src=",1)[1].split("\"")[1]
    return src

def checkAddress(link):
    if link.endswith(".html"):
        str1=link[::-1].split("/",1)[1] #reverse string and split after first "/"
        str2=str1[::-1]
        str2+="/"
        return str2
    else:
        return link

def get_images(folder):
    images_list = list()
    if os.path.isdir(folder) is True:
        for filename in os.listdir(folder):
            caleFile = os.path.join(folder, filename)
            if os.path.isfile(caleFile)is True:
                if filename.endswith((".jpg",".png",".jpeg",".gif",".svg")):
                    images_list.append(caleFile)
    return images_list

def getImgExtension(imgExt):
    imgExt=imgExt[::-1]
    extension=""
    for i in imgExt:
        if i != '.':
            extension+=i
        elif i == '.':
            extension+=i
            extension=extension[::-1]
            break
    return extension

if len(sys.argv) != 2:
    print("Usage: %s <wrong number of parameters>" % sys.argv[0])
    exit(0)

#get html source code in a file
html = urllib2.urlopen(sys.argv[1]).read().decode("utf-8")
soup= BeautifulSoup(html,"html5lib")
tags=soup.find_all('img')

imgLinks=list()
if len(tags)==0:
    print("This website doesn't contain any image in it's content!")
    exit(0)
elif len(tags)>0:
    for element in tags:
            src=extractImageSrc(str(element))
            if src.startswith("http"):
                imgLinks.append(src)
            else:
                imgLinks.append(checkAddress(sys.argv[1])+src)

current_directory_path = os.path.dirname(os.path.realpath(__file__))
contor=0
for i in imgLinks:
    extension=getImgExtension(i)
    filename="img"+str(contor)+extension
    contor+=1
    try:
        urllib2.urlretrieve(i, filename)
    except:
        pass

images_list=list()
images_list=get_images(current_directory_path)

result_json=[]
for i in images_list:
    print(i)
    result_json.append(ImageSerialization.get_info_from_image(i))
    with open('result.json', 'w') as output:
        output.write(json.dumps(result_json, separators=(',', ':')) + '\n')