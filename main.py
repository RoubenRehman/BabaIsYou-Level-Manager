#from os import walk
#from os.path import expanduser
import os
from tkinter import *

class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class InitWindow(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        self.pathLabel = Label(master, text="Enter your path to your steamapps folder")
        self.pathLabel.grid()

        self.pathEntry = Entry(master)
        self.pathEntry.grid()

        self.submitButton = Button(master, command=self.buttonClick, text="OK")
        self.submitButton.grid()

    def __del__(self):
        return self.path

    def buttonClick(self):
        self.path = self.pathEntry.get()
        print(self.path)

path = '/media/rouben/Volume/SteamGames/steamapps/common/Baba Is You/Data/Worlds/levels/'

files = []

# getting all files in directory
for (dirpath, dirnames, filenames) in os.walk(path):
    files.extend(filenames)

# filtering .ld-files and getting the level name form them
for f in files:
    if f.endswith('.ld'):
        with open(path+f) as level:
            level_name = level.read().split('[general]')[1].split('name=')[1].split('\n')[0]
            print(level_name)

def startup():
    HOME = os.path.expanduser("~")

    if not os.path.exists(os.path.join(HOME, 'BabaIsYouLevelManager')):
        #os.mkdir(os.path.join(HOME, 'BabaIsYouLevelManager'))
        init_window = InitWindow()
        m = init_window.mainloop()
        print(m)

startup()
