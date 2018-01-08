#pip install beautifulsoup4
#run "python html_page_parser.py <link>" [EX] "python html_page_parser.py http://students.info.uaic.ro/"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import sys,os,json,ImageSerialization

def extractImageSrc(tag):
    data=list()
    src=tag.split("src=",1)[1].split("\"")[1]
    alt=tag.split("alt=",1)[1].split("\"")[1]
    data.append(src)
    data.append(alt)
    return data

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

def html_page_parser(argv):
    if len(argv) != 2:
        print("Usage: %s <wrong number of parameters>" % argv[0])
        exit(0)

    #get html source code in a file
    html = urllib2.urlopen(argv[1]).read().decode("utf-8")
    soup= BeautifulSoup(html,"html.parser")
    tags=soup.find_all('img')
    title=soup.find_all('title')

    imgLinks=list()
    caption=list()

    if len(tags)==0:
        print("This website doesn't contain any image in it's content!")
        exit(0)
    elif len(tags)>0:
        for element in tags:
                src=extractImageSrc(str(element))[0]
                alt=extractImageSrc(str(element))[1]
                if len(alt)<1:
                    title = str(title).split(">", 1)[1]
                    title = title.split("<", 1)[0]
                    alt=title
                if src.startswith("http"):
                    imgLinks.append(src)
                    caption.append(alt)
                else:
                    caption.append(alt)
                    imgLinks.append(checkAddress(argv[1])+src)

    #current_directory_path = os.path.dirname(os.path.realpath(__file__))
    current_directory_path = os.path.join('.', 'result')
    contor=0
    for i in imgLinks:
        filename="img"+str(contor)+getImgExtension(i)
        filepath = os.path.join('result', filename)
        contor+=1
        try:
            urllib2.urlretrieve(i, filepath)
        except:
            pass

    images_list=list()
    images_list=get_images(current_directory_path)

    finalResult=[]
    contor=0

    for i in images_list:
        result_json = ImageSerialization.get_info_from_image(i)
        result_json['caption']=caption[contor]
        finalResult.append(result_json)
        contor += 1

    file=open("%sresult.json" % argv[0],'w')
    file.write(json.dumps(finalResult, separators=(',', ':')) + '\n')
    file.close()

if __name__ == "__main__":
    argv = sys.argv
    html_page_parser(argv)