from PyQt5 import QtWidgets, uic, QtGui
from zipfile import ZipFile as zp
import sys
import os
import random

class SetPathDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(SetPathDialog, self).__init__(*args, **kwargs)
        uic.loadUi('./GUI/SetPath.ui', self)

        # finding buttons
        self.browseButton = self.findChild(QtWidgets.QPushButton, 'BrowseButton')
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'ConfirmButton')

        # connection buttons
        self.browseButton.clicked.connect(self.browseButtonClicked)
        self.confirmButton.clicked.connect(self.confirmButtonClicked)

        # finding line edit
        self.steamPathEdit = self.findChild(QtWidgets.QLineEdit, 'SteamPath')

        self.steamPath = ""
        self.configPath = os.path.join(os.path.expanduser("~"), "BabaIsYouLevelManager/steampath.txt")

        self.show()

    def browseButtonClicked(self):
        self.steamPath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")) + "/common/Baba Is You/Data/Worlds/levels/"
        self.steamPathEdit.setText(self.steamPath)

    def confirmButtonClicked(self):
        # print(self.steamPath)
        if self.steamPathEdit.text() != "Set Path to your steamapps folder...":
            with open(self.configPath, "w") as config:
                config.write('STEAMPATH=' + self.steamPath + "\nSAVEPATH=")
            self.accept()


class LevelManager(QtWidgets.QMainWindow):
    def __init__(self):
        super(LevelManager, self).__init__()
        uic.loadUi('./GUI/MainWindow.ui', self)

        # finding Label
        self.statusLabel = self.findChild(QtWidgets.QLabel, 'StatusLabel')

        # finding SpinBox
        self.setExportNameSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'SetExportNameSpinbox')

        # finding buttons
        self.importButton = self.findChild(QtWidgets.QPushButton, 'ImportButton')
        self.exportButton = self.findChild(QtWidgets.QPushButton, 'ExportButton')
        self.exportSetNameButton = self.findChild(QtWidgets.QPushButton, 'ExportSetNameButton')
        self.refreshButton = self.findChild(QtWidgets.QPushButton, 'RefreshButton')
        self.steamPathButton = self.findChild(QtWidgets.QPushButton, 'SteamPathButton')
        self.savePathButton = self.findChild(QtWidgets.QPushButton, 'SavePathButton')

        # connecting buttons
        self.importButton.clicked.connect(self.importButtonClicked)
        self.exportButton.clicked.connect(self.exportButtonClicked)
        self.exportSetNameButton.clicked.connect(self.exportSetNameButtonClicked)
        self.refreshButton.clicked.connect(self.refreshButtonClicked)
        self.steamPathButton.clicked.connect(self.steamPathButtonClicked)
        self.savePathButton.clicked.connect(self.savePathButtonClicked)

        # finding level list
        self.levelList = self.findChild(QtWidgets.QListView, 'LevelList')
        self.levelList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # connection level list
        self.levelList.clicked.connect(self.levelListClicked)

        # getting and saving steampath from home dir
        self.HOME = os.path.expanduser("~")
        self.CONFIG = os.path.join(self.HOME, 'BabaIsYouLevelManager/steampath.txt')

        if not os.path.exists(os.path.join(self.HOME, 'BabaIsYouLevelManager')):
            os.mkdir(os.path.join(self.HOME, 'BabaIsYouLevelManager'))

        if not os.path.isfile(os.path.join(self.HOME, 'BabaIsYouLevelManager/steampath.txt')):
            setPathDialog = SetPathDialog(self)
            if not setPathDialog.exec_():
                sys.exit()

        # reading config file to get STEAMPATH and SAVEPATH
        with open(self.CONFIG, "r") as config:
            try:
                inRead = config.read()
                self.steamPath = inRead.split("STEAMPATH=")[1].split("\n")[0]
                #print(self.steamPath)
                self.savePath = inRead.split("SAVEPATH=")[1]    # returns an empyt string if no SAVEPATH is set yet
                self.getLevelNames()
            except:
                # displaying error message if config is not readable (e.g. STEAMPATH or SAVEPATH key faulty)
                self.displayErrorBox('Your configuration file seems faulty, check ' + str(self.CONFIG), exit=True)
                #error_dialog = QtWidgets.QErrorMessage()
                #error_dialog.showMessage('Your configuration file seems faulty, check the BabaIsYouLevelManager folder in your $HOME directory')

        # updating listView with level names
        # self.getLevelNames()

        self.selectedIndex = ""

        self.show()

    def getLevelNames(self):
        self.files = []
        self.levelNames = {}
        self.model = QtGui.QStandardItemModel()

        # getting all files in directory
        for (dirpath, dirnames, filenames) in os.walk(self.steamPath):
            self.files.extend(filenames)

        # filtering .ld-files and getting the level name form them
        for f in self.files:
            if f.endswith('.ld'):
                with open(self.steamPath+f) as level:
                    level_name = level.read().split('[general]')[1].split('name=')[1].split('\n')[0]
                    self.levelNames[level_name] = f.split(".")[0]

        self.levelList.setModel(self.model)

        # print(self.levelNames)

        for i in self.levelNames.keys():
            item = QtGui.QStandardItem(i)
            self.model.appendRow(item)

    def importButtonClicked(self):
        # get zip archive to open
        path = str(QtWidgets.QFileDialog.getOpenFileName(self, "Select level archive (zip format)")[0])
        self.getLevelNames()    # refresh levelList to be extra sure it's up to date
        try:
            zip = zp(path)
            import_name = zip.namelist()[0].split(".")[0]   # get filename of to be imported level
            filenamelist = [x.split(".")[0] for x in self.files if x.split(".")[1] in ["l", "ld", "ld.tmp", "png"]] # check if a level with that id already locally exists

            #print(import_name)
            #print(filenamelist)

            if not import_name in filenamelist: # if not, import
                zip.extractall(self.steamPath)

            else:   # else, rename files in the archive and try again
                nmbrs = [int(x.split("l")[0]) for x in filenamelist]
                import_name = str(random.choice(list(set(range(1, max(nmbrs)))-set(nmbrs)))) # get a new number that's not used as filename yet
                zipinfo = zip.infolist()

                #print(str(import_name))

                for info in zipinfo:
                    ending = info.filename.split(".")[1]
                    info.filename = import_name + "." + ending
                    zip.extract(member=info, path=self.steamPath)

            self.statusLabel.setText("Done importing!")

        except:
            self.displayErrorBox("Failed to open zip archive")
            self.statusLabel.setText("")

    def exportSetNameButtonClicked(self):
        self.exportLevel(fileName=str(int(self.setExportNameSpinBox.value())))

    def exportButtonClicked(self):
        self.exportLevel()

    def exportLevel(self, fileName = None):
        # if no SAVEPATH is set yet, do this now and save in config
        if not self.savePath:
            self.savePathButtonClicked()
            #self.savePath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory to export zip to"))
            #with open(self.CONFIG, "w") as config:
            #    config.write("STEAMPATH=" + self.steamPath + "\nSAVEPATH=" + self.savePath)

        # create zip object of clicked level files and save at SAVEPATH
        if self.selectedIndex:  # only if a level is selected in listView
            # catch if somehow selected name is not found in levelNames
            try:
                level = self.levelNames[self.selectedIndex]

                # getting files to zip
                filesToZip = [x for x in self.files if x.split(".")[0] == level]

                #print(filesToZip)

                # zipping files
                with zp(os.path.join(self.savePath, self.selectedIndex + ".zip"), "w") as zip:
                    for file in filesToZip:
                        if fileName:
                            zip.write(os.path.join(self.steamPath, file), arcname=fileName+'level.'+file.split(".", 1)[1])
                        else:
                            zip.write(os.path.join(self.steamPath, file), arcname=file)

                self.statusLabel.setText("Done exporting!")

            except:
                self.displayErrorBox("Couldn't find selected level in dataframe")
                self.statusLabel.setText("")

        else:
            self.displayErrorBox("Select a level first!")


    def refreshButtonClicked(self):
        self.getLevelNames()

    def steamPathButtonClicked(self):
        hold = self.steamPath
        get = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.steamPath = get + "/common/Baba Is You/Data/Worlds/levels/"
        #print(self.steamPath)

        if get:
            with open(self.CONFIG, "w") as config:
                config.write('STEAMPATH=' + self.steamPath + "\nSAVEPATH=" + self.savePath)
            self.statusLabel.setText("Steam Path updated")
        else:
            self.steamPath = hold

    def savePathButtonClicked(self):
        hold = self.savePath
        self.savePath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory to export zip to"))

        if self.savePath:
            with open(self.CONFIG, "w") as config:
                config.write("STEAMPATH=" + self.steamPath + "\nSAVEPATH=" + self.savePath)
            self.statusLabel.setText("Save Path updated")
        else:
            self.savePath = hold

    def levelListClicked(self, index):
        #print("Level List: " + index.data())
        self.selectedIndex = index.data()

    def displayErrorBox(self, title, exit = False):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(title)
        msg.setWindowTitle("Error")
        msg.exec_()
        if exit: sys.exit()

app = QtWidgets.QApplication(sys.argv)
window = LevelManager()
app.exec_()
