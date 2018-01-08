"""
install PyQt5: python -m pip install pyqt5
run: python start_ui.py
obs: add documents in UI folder (works for pdf and docs) and select UI folder (on "browse" button click)
"""

from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication, QPushButton, QLabel, QListView)
import sys
import os
import threading


class UI_(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.directory_name_label = None
        self.directory_result_label = None
        self.browse_folder_button = None
        self.statusBar()

        self.browse_folder_button = QPushButton('Browse', self)
        self.browse_folder_button.setToolTip('This is an example button')
        self.browse_folder_button.move(10, 10)
        self.browse_folder_button.clicked.connect(self.showDialog)

        self.directory_name_label = QLabel(self)
        self.directory_name_label.move(150, 10)
        self.directory_name_label.resize(400, 40)

        self.directory_result_label = QLabel(self)
        self.directory_result_label.move(150, 40)
        self.directory_result_label.resize(400, 40)

        #self.list_view = QListView(self)
        #self.list_view.move(500, 20)

        self.setGeometry(500, 500, 1000, 300)
        self.setWindowTitle('AI')
        self.show()

    def initUI(self):
        pass


    def execute_command(self, fname):
        os.system("python ../DocumentParser/parser.py " + fname)
        self.directory_result_label.setText("{} images in {}".format(len(os.listdir("Result")), "Result"))

    def showDialog(self):
        fname = str(QFileDialog.getExistingDirectory(self, "Select Directory", ".."))
        self.directory_name_label.setText(fname)
        t = threading.Thread(target=self.execute_command, args=(fname,))
        t.start()
        self.directory_result_label.setText("Working ...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI_()
    sys.exit(app.exec_())
