import os
import platform
import requests
import webbrowser
import datetime
import sys
import codecs
import configparser
import tkinter
from tkinter import ttk

from tkinter import messagebox as mb

import program.textSetting as textSetting
import program.comicscript.comicscript as comicscriptProgram
import program.mdlBin.mdlBin as mdlBinProgram
import program.mdlinfo.mdlinfo as mdlinfoProgram
import program.orgInfoEditor.orgInfoEditor as orgInfoEditorProgram
import program.musicEditor.musicEditor as musicEditorProgram
import program.fvtMaker.fvtMaker as fvtMakerProgram
import program.railEditor.railEditor as railEditorProgram
import program.smf.smf as smfProgram
import program.ssUnity.ssUnity as ssUnityProgram
import program.rsRail.rsRail as rsRailProgram


def resource_path(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(os.path.abspath(os.path.dirname(__file__))))
    return os.path.join(bundle_dir, relative_path)


def clearProgramFrame():
    children = programFrame.winfo_children()
    for child in children:
        child.destroy()


def callProgram(programName):
    global selectedProgram

    clearProgramFrame()
    selectedProgram = programName
    if selectedProgram == "orgInfoEditor":
        orgInfoEditorProgram.call_orgInfoEditor(root, programFrame)
    elif selectedProgram == "mdlBin":
        mdlBinProgram.call_mdlBin(root, programFrame)
    elif selectedProgram == "mdlinfo":
        mdlinfoProgram.call_mdlinfo(root, programFrame)
    elif selectedProgram == "comicscript":
        comicscriptProgram.call_comicscript(root, programFrame)
    elif selectedProgram == "musicEditor":
        musicEditorProgram.call_musicEditor(root, programFrame)
    elif selectedProgram == "fvtMaker":
        fvtMakerProgram.call_fvtMaker(root, programFrame)
    elif selectedProgram == "railEditor":
        railEditorProgram.call_railEditor(root, programFrame)
    elif selectedProgram == "smf":
        smfProgram.call_smf(root, programFrame)
    elif selectedProgram == "SSUnity":
        ssUnityProgram.call_ssUnity(root, programFrame)
    elif selectedProgram == "rsRail":
        rsRailProgram.call_rsRail(root, programFrame)

    delete_OptionMenu()
    if selectedProgram == "smf":
        add_smfWriteOptionMenu()


def loadFile():
    global v_frameCheck
    global v_meshCheck
    global v_XYZCheck
    global v_mtrlCheck
    global selectedProgram

    if selectedProgram == "orgInfoEditor":
        orgInfoEditorProgram.openFile()
    elif selectedProgram == "mdlBin":
        mdlBinProgram.openFile()
    elif selectedProgram == "mdlinfo":
        mdlinfoProgram.openFile()
    elif selectedProgram == "comicscript":
        comicscriptProgram.openFile()
    elif selectedProgram == "musicEditor":
        musicEditorProgram.openFile()
    elif selectedProgram == "fvtMaker":
        fvtMakerProgram.openFile()
    elif selectedProgram == "railEditor":
        railEditorProgram.openFile()
    elif selectedProgram == "smf":
        smfProgram.openFile(v_frameCheck.get(), v_meshCheck.get(), v_XYZCheck.get(), v_mtrlCheck.get())
    elif selectedProgram == "SSUnity":
        ssUnityProgram.openFile()
    elif selectedProgram == "rsRail":
        rsRailProgram.openFile()
    else:
        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E1"])


def configCheckOption(section, options):
    global config_ini_path

    configRead = configparser.ConfigParser()
    configRead.read(config_ini_path, encoding="utf-8")

    if not configRead.has_option(section, options):
        if not configRead.has_section(section):
            configRead.add_section(section)

        if section == "UPDATE":
            configRead.set(section, options, "2000/01/01")
        else:
            configRead.set(section, options, "0")

        try:
            f = codecs.open(config_ini_path, "w", "utf-8", "strict")
            configRead.write(f)
            f.close()
        except PermissionError:
            pass

        return True
    return False


def add_smfWriteOptionMenu():
    global config_ini_path
    global v_frameCheck
    global v_meshCheck
    global v_XYZCheck
    global v_mtrlCheck
    global menubar
    global maxMenubarLen

    if not os.path.exists(config_ini_path):
        writeDefaultConfig()

    configRead = configparser.ConfigParser()
    configRead.read(config_ini_path, encoding="utf-8")

    readErrorFlag = False
    if configCheckOption("SMF_FRAME", "mode"):
        readErrorFlag = True
    if configCheckOption("SMF_MESH", "mode"):
        readErrorFlag = True
    if configCheckOption("SMF_XYZ", "mode"):
        readErrorFlag = True
    if configCheckOption("SMF_MTRL", "mode"):
        readErrorFlag = True

    if readErrorFlag:
        try:
            f = codecs.open(config_ini_path, "w", "utf-8", "strict")
            configRead.write(f)
            f.close()
        except PermissionError:
            pass

    if menubar.entryconfig(tkinter.END) == menubar.entryconfig(maxMenubarLen):
        v_frameCheck = tkinter.IntVar()
        v_frameCheck.set(int(configRead.get("SMF_FRAME", "mode")))
        v_meshCheck = tkinter.IntVar()
        v_meshCheck.set(int(configRead.get("SMF_MESH", "mode")))
        v_XYZCheck = tkinter.IntVar()
        v_XYZCheck.set(int(configRead.get("SMF_XYZ", "mode")))
        v_mtrlCheck = tkinter.IntVar()
        v_mtrlCheck.set(int(configRead.get("SMF_MTRL", "mode")))
        smfWriteOptionMenu = tkinter.Menu(menubar, tearoff=False)
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt1"], variable=v_frameCheck, command=writeSmfConfig)
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt2"], variable=v_meshCheck, command=writeSmfConfig)
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt3"], variable=v_XYZCheck, command=writeSmfConfig)
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt4"], variable=v_mtrlCheck, command=writeSmfConfig)
        menubar.add_cascade(label=textSetting.textList["menu"]["smf"]["name"], menu=smfWriteOptionMenu)


def delete_OptionMenu():
    global menubar
    global maxMenubarLen

    if menubar.index(tkinter.END) > maxMenubarLen:
        menubar.delete(maxMenubarLen + 1)


def writeDefaultConfig():
    global config_ini_path
    global version

    if platform.system() == "Windows":
        try:
            config_ini_folder = os.path.dirname(config_ini_path)
            if not os.path.exists(config_ini_folder):
                os.makedirs(config_ini_folder)

            config = configparser.RawConfigParser()
            config.add_section("SMF_FRAME")
            config.set("SMF_FRAME", "mode", 0)
            config.add_section("SMF_MESH")
            config.set("SMF_MESH", "mode", 0)
            config.add_section("SMF_XYZ")
            config.set("SMF_XYZ", "mode", 0)
            config.add_section("SMF_MTRL")
            config.set("SMF_MTRL", "mode", 0)

            config.add_section("UPDATE")
            config.set("UPDATE", "time", "2000/01/01")

            f = codecs.open(config_ini_path, "w", "utf-8", "strict")
            config.write(f)
            f.close()
        except PermissionError:
            pass


def writeSmfConfig():
    global v_frameCheck
    global v_meshCheck
    global v_XYZCheck
    global v_mtrlCheck
    global config_ini_path

    configRead = configparser.ConfigParser()
    configRead.read(config_ini_path, encoding="utf-8")

    configRead.set("SMF_FRAME", "mode", str(v_frameCheck.get()))
    configRead.set("SMF_MESH", "mode", str(v_meshCheck.get()))
    configRead.set("SMF_XYZ", "mode", str(v_XYZCheck.get()))
    configRead.set("SMF_MTRL", "mode", str(v_mtrlCheck.get()))

    try:
        f = codecs.open(config_ini_path, "w", "utf-8", "strict")
        configRead.write(f)
        f.close()
    except PermissionError:
        pass


def getUpdateVer():
    global version
    global onlineUpdateVer
    global updateFlag

    path = resource_path("ver.txt")
    f = codecs.open(path, "r", "utf-8", "ignore")
    line = f.read()
    f.close()
    version = line.strip()

    try:
        url = "https://raw.githubusercontent.com/khttemp/dend-mod-gui/main/ver.txt"
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            onlineUpdateVer = response.text

            if (version != onlineUpdateVer):
                configCheckOption("UPDATE", "time")

                configRead = configparser.ConfigParser()
                configRead.read(config_ini_path, encoding="utf-8")

                localDateStr = configRead.get("UPDATE", "time")
                localDate = datetime.datetime.strptime(localDateStr, "%Y/%m/%d").date()
                currentDate = datetime.datetime.now().date()
                if (localDate - currentDate).days < 0:
                    updateFlag = True
    except Exception:
        pass


def confirmUpdate():
    global onlineUpdateVer
    global updateFlag

    if updateFlag:
        msg = textSetting.textList["update"]["message"].format(onlineUpdateVer)
        result = mb.askyesno(title=textSetting.textList["update"]["title"], message=msg)
        if result == tkinter.YES:
            webbrowser.open_new("https://github.com/khttemp/dend-mod-gui/releases")

        try:
            configRead = configparser.ConfigParser()
            configRead.read(config_ini_path, encoding="utf-8")

            currentTime = datetime.datetime.now()
            currentDate = datetime.datetime.strftime(currentTime, "%Y/%m/%d")
            configRead.set("UPDATE", "time", currentDate)

            f = codecs.open(config_ini_path, "w", "utf-8", "strict")
            configRead.write(f)
            f.close()
        except PermissionError:
            pass


config_ini_path = "config.ini"
if platform.system() == "Windows":
    config_ini_path = os.path.join(os.getenv("APPDATA"), "dend-mod-gui", "config.ini")
v_frameCheck = None
v_meshCheck = None
v_XYZCheck = None
v_mtrlCheck = None
selectedProgram = None

maxMenubarLen = None
version = 0
onlineUpdateVer = 0
updateFlag = False

getUpdateVer()

root = tkinter.Tk()
root.title(textSetting.textList["app"]["title"].format(version))
root.option_add("*font", textSetting.textList["defaultFont"])
root.geometry("1024x768")

style = ttk.Style()
style.configure(".", font=textSetting.textList["defaultFont"])

menubar = tkinter.Menu(root)

v_prog = tkinter.IntVar()

progmenu = tkinter.Menu(menubar, tearoff=False)
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["SSUnity"], value=-1, variable=v_prog, command=lambda: callProgram("SSUnity"))
progmenu.add_separator()
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["orgInfoEditor"], value=1, variable=v_prog, command=lambda: callProgram("orgInfoEditor"))
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["mdlBin"], value=2, variable=v_prog, command=lambda: callProgram("mdlBin"))
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["mdlinfo"], value=3, variable=v_prog, command=lambda: callProgram("mdlinfo"))
progmenu.add_separator()
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["comicscript"], value=4, variable=v_prog, command=lambda: callProgram("comicscript"))
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["musicEditor"], value=5, variable=v_prog, command=lambda: callProgram("musicEditor"))
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["fvtMaker"], value=6, variable=v_prog, command=lambda: callProgram("fvtMaker"))
progmenu.add_separator()
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["railEditor"], value=7, variable=v_prog, command=lambda: callProgram("railEditor"))
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["rsRail"], value=8, variable=v_prog, command=lambda: callProgram("rsRail"))
progmenu.add_separator()
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["smf"], value=9, variable=v_prog, command=lambda: callProgram("smf"))
progmenu.add_separator()
progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["exit"], value=-2, variable=v_prog, command=sys.exit)

filemenu = tkinter.Menu(menubar, tearoff=False)
filemenu.add_command(label=textSetting.textList["menu"]["file"]["loadFile"], command=loadFile)

menubar.add_cascade(label=textSetting.textList["menu"]["program"]["name"], menu=progmenu)
menubar.add_cascade(label=textSetting.textList["menu"]["file"]["name"], menu=filemenu)

root.config(menu=menubar)

programFrame = ttk.Frame(root)
programFrame.pack(fill=tkinter.BOTH, expand=True)

if not os.path.exists(config_ini_path):
    writeDefaultConfig()

maxMenubarLen = menubar.index(tkinter.END)

root.after(100, confirmUpdate)
root.mainloop()
