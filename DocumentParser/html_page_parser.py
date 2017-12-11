#run "python html_page_parser.py <link>" [EX] "python html_page_parser.py http://students.info.uaic.ro/"
from html.parser import HTMLParser
import urllib.request as urllib2
import ImageSerialization
import sys
import os
import json

if len(sys.argv) != 2:
    print("Usage: %s <wrong number of parameters>" % sys.argv[0])
    exit(0)

current_directory_path = os.path.dirname(os.path.realpath(__file__))

#Save html source code in a file
html = urllib2.urlopen(sys.argv[1]).read().decode("utf-8")
f=open("htmlFile.txt","w")
f.write(html)
f.close()

class MyHTMLParser(HTMLParser): #scrap start tags from html source code and search for <img> tag
    lsStartTags = list()
    def handle_starttag(self, startTag, attrs): #HTML Parser Methods
       self.lsStartTags.append(startTag)
parser=MyHTMLParser()
parser.feed(html) #geting all start tags into lsStartTags

def extractImgLocationFromTag(tag):
    location=""
    for i in range(len(tag)-1):
        if tag[i] is "\"" or tag[i] is "\'":
            i+=1
            while(tag[i] is not "\"" and tag[i] is not "\'"):
                location+=tag[i]
                i+=1
            break
    return location

counterImages=0
for tag in parser.lsStartTags:
    if tag == 'img' or tag=='IMG': #check if my list contains an image tag
        counterImages+=1

imgLinks=list()
if (counterImages is 0):
    print("This website: ",sys.argv[1]," does not contain any images along it's content!")
elif (counterImages>0):
    f=open("htmlFile.txt","r")
    line=f.readline()
    while line:
        fullLocation=sys.argv[1]
        if "<img " in line or "<IMG " in line:
            fullLocation+=extractImgLocationFromTag(line)
            imgLinks.append(fullLocation)
        line=f.readline()
    f.close()

for i in range(len(imgLinks)-1):
    filename="img"+str(i)+".jpg"
    urllib2.urlretrieve(imgLinks[i],filename)

def get_images(folder):
    images_list = list()
    if os.path.isdir(folder) is True:
        for filename in os.listdir(folder):
            caleFile = os.path.join(folder, filename)
            if os.path.isfile(caleFile)is True:
                if filename.endswith((".jpg",".png",".jpeg")):
                    images_list.append(caleFile)
    return images_list

images_list=list()
images_list=get_images(current_directory_path)
result_json=[]
for i in range(0,3):
    print(images_list[i])
    result_json.append(ImageSerialization.get_info_from_image(images_list[i]))
    with open('result.json', 'w') as output:
        output.write(json.dumps(result_json, separators=(',', ':')) + '\n')
