import urllib.request, os
import _thread
url_pattern = "https://medpix.nlm.nih.gov/images/cow/synpic"
if not os.path.exists("TrainingImages"):
    os.mkdir("TrainingImages")


def download(bottom_limit, upper_limit):
    while bottom_limit < upper_limit:
        url = url_pattern + str(int(bottom_limit)) + ".jpg"
        file_name = os.path.join("TrainingImages", "synpic" + str(int(bottom_limit)) + ".jpg")
        try:
            urllib.request.urlretrieve(url, file_name)
            if os.path.getsize(file_name) == 6168:  # size of invalid image from medpix
                os.remove(file_name)
                print("Failed: {}".format(file_name))
            else:
                pass
                print("Downloaded: {}".format(file_name))
        except:
            print("Failed: {}".format(file_name))
        bottom_limit += 1


size = 100000
threads_no = 50
for i in range(threads_no):
    _thread.start_new_thread(download, (i*size/threads_no, i*size/threads_no + size/threads_no))

while 1:
    pass
