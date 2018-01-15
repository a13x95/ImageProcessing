#pip install beautifulsoup4
#run "python html_page_parser.py <link>" [EX] "python html_page_parser.py https://en.wikipedia.org/wiki/Bone_fracture"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import sys,os,json,ImageSerialization,DatabaseConnection

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

GlobalContor=0

def html_page_parser(argv):
    # get html source code in a file
    html = urllib2.urlopen(argv).read().decode("utf-8")
    soup = BeautifulSoup(html, "html5lib")
    tags = soup.find_all('img')
    # title=soup.find_all('title')
    title = soup.title.string
    imgLinks = list()
    caption = list()
    if len(tags)==0:
        print("This website doesn't contain any image in it's content!")
        exit(0)
    elif len(tags)>0:
        for element in tags:
            try:
                src = extractImageSrc(str(element))[0]
                alt = extractImageSrc(str(element))[1]
            except IndexError:
                pass
            if src.endswith((".jpg", ".png", ".jpeg", ".gif", ".svg")):
                if len(alt) < 1:
                    alt = title
                if src.startswith("http") or src.startswith("www."):
                    imgLinks.append(src)
                    caption.append(alt)
                elif src.startswith("//upload."):
                    imgLinks.append("https:" + src)
                    caption.append(alt)
                else:
                    caption.append(alt)
                    imgLinks.append(checkAddress(argv[1]) + src)

    current_directory_path = os.path.dirname(os.path.realpath(__file__))
    current_directory_path = os.path.join(current_directory_path, 'result')
    global GlobalContor
    for i in imgLinks:
        filename="HtmlImg"+str(GlobalContor)+getImgExtension(i)
        filepath = os.path.join('result', filename)
        GlobalContor+=1
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

    db = DatabaseConnection.DatabaseConnection()
    db.insert_entry(finalResult)
    #file=open("%sresult.json" % argv[0],'w')
    #file.write(json.dumps(finalResult, separators=(',', ':')) + '\n')
    #file.close()

def readLinksFromFile(pathFile):
    if os.path.isfile(pathFile):
        try:
            f = open(pathFile, "r")
        except:
            print("unable to open fisier for reading")
        lines=f.readlines()
        for i in lines:
            if i:
                try:
                    html_page_parser(i)
                except:
                    pass

if __name__ == "__main__":
    #argv = sys.argv
    if not os.path.exists("result"):
        os.mkdir("result")
    readLinksFromFile(sys.argv[1]) #"D:\Facultate\ImageProcessing\DocumentParser\html_links.txt"