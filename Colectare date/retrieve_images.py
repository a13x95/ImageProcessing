import urllib.request, os
url_pattern = "https://medpix.nlm.nih.gov/images/cow/synpic"
if not os.path.exists("TrainingImages"):
    os.mkdir("TrainingImages")
counter = 0
while counter < 100000:
    url = url_pattern + str(counter) + ".jpg"
    file_name = os.path.join("TrainingImages", "synpic" + str(counter) + ".jpg")
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
    counter += 1