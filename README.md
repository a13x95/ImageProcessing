# ImageProcessing
Modul Inteligenta Artificiala
Fiecare responsabil de modul trebuie sa-si creeze un director unde isi vor desfasura activitatea membrii modulului.

Luati Git Bash si urmariti pasii:

* Creeaza un folder in care vei lucra

* Din Git Bash intra in folder

* Scrie in commander
```
git init #pentru crearea repositorului local in folder-ul vostru curent
git clone https://github.com/a13x95/ImageProcessing.git
git branch work #creeam un branch numit work
git checkout work #ne mutam pe branch-ul work si aici vom lucra de acuma incolo
```

* Pentru a adauga fisierele pe Github: (din branch-ul work)
```
git add . #adaugam tot din directorul nostru
git commit -m "Descriere a modificarilor" #aici git va face un pachet cu adaugarile noastre
git pull origin master #facem update la repository-ul local pe branch-ul master
git checkout master #schimbam branch-ul pe master
git merge work #combinam schimbarile noastre cu cele ale coechipierilor nostri. ATENTIE la merge conflicts!
git push origin master #adaugam modificarile noastre local si pe repository-ul oficial
git checkout work #schimbam inapoi pe branch-ul work si continuam sa facem schimbari
```	
Pasii sunt luati din repository-ul proiectului de la [Ingineria Programarii](https://github.com/fistinflame/IngineriaProgramarii/)


Project dependencies:
   - keras
   - python-resize-image
   - progressbar2
   - matplotlib
   - h5py
   - sklearn
   - pymongo
   - etc.
   
This dependencies can be installed manually or by running the following
command having requirements.txt in the current directory:
pip install -r requirements.txt