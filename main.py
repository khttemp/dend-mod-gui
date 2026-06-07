import os
import sys
import platform

import program.main.mainGui as mainGui


importDict = {
    "configPath": "config.ini",
    "window": None
}

if getattr(sys, "frozen", False):
    importDict["rootPath"] = os.path.join(os.path.abspath(os.path.dirname(sys.executable)), "_internal", "data")
else:
    importDict["rootPath"] = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows":
    importDict["configPath"] = os.path.join(os.getenv("APPDATA"), "dend-mod-gui", "config.ini")

if __name__ == "__main__":
    mainGui.guiMain(importDict)
