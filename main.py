import os
import platform

import program.main.mainGui as mainGui


importDict = {
    "rootPath": os.path.abspath(os.path.dirname(__file__)),
    "configPath": "config.ini",
    "window": None
}

if platform.system() == "Windows":
    importDict["configPath"] = os.path.join(os.getenv("APPDATA"), "dend-mod-gui", "config.ini")

if __name__ == "__main__":
    mainGui.guiMain(importDict)
