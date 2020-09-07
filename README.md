# Level Manager for Baba Is You
A fan-made level manager to import and export custom Baba Is You levels.

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://opensource.org/licenses/MIT)  [![Python](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org)

#### [Blog Post](https://roubenrehman.github.io/posts/2020/09/06/Baba-Is-You-Fan-Made-Level-Manager.html)

## Introduction

[Baba is You](https://store.steampowered.com/app/736260/Baba_Is_You/) is a popular puzzle game available for Steam and Nintendo Switch. It does **not** officially feature a level editor, although an experimental version of a possible level editor can be manually activated by following [this](https://steamcommunity.com/sharedfiles/filedetails/?id=1686041344) tutorial. This project can be used to easily import and export levels to be able to share them with your friends.

## Usage

### Starting the Software
To start the Level Manager, first install all requirements:
```bash
pip install -r requirements.txt
```
Run the script using:
```bash
python MainWindow.py
```

Binaries for Linux and Windows will be available soon.

### On first Startup
On first startup, the Level Manager asks you to set PATH to your steamapps folder in which Baba is You is installed. The PATH is saved in BabaIsYouLevelManager/steampath.txt under your $HOME directory. It will be loaded automatically from that point on and can be changed by clicking the 'Set Steam Path' button.

If the PATH to the steamapps/ folder is set correctly, the Level Manager should display a list of all custom levels.

### Exporting
To export a level, click on it in the list and hit the "Export" button. On the first time, the Manager asks you to set an Export Path to which the level should be exported. This path is also saved in the BabaIsYouLevelManager/steampath.txt for later use and can be changed with the 'Set Export Path' button. The level is exported as a .zip file containing the files `<lvl name>.l`, `<lvl name>.ld`, `<lvl name>.ld.tmp` and `<lvl name>.png`. This zip archive can now be shared.

### Importing
To import a level, click the "Import" button. A Folder Dialog will open, choose the .zip file of the level to be imported. The Level Manager extracts the contents of this archive to the Baba is You custom levels folder. To avoid overwriting already existing levels, it first checks if the file names of the to-be-imported level is already taken. If this is the case, the Manager automatically uses a different `<number>level` filename. No existing levels should be overwritten that way.





# Disclaimer

I do not own any rights regarding the original Baba is You game, all rights lie with the author(s) of the game. This project is fan-made and only intended to be used as a rough alternative until the official level editor and its level-sharing mechanic is released.
