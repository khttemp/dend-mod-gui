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


root = None
config_ini_path = None
v_frameCheck = None
v_meshCheck = None
v_XYZCheck = None
v_mtrlCheck = None
v_modelNameMode = None
v_flagHexMode = None
v_ambReadMode = None
selectedProgram = None
maxMenubarLen = None
version = 0
onlineUpdateVer = 0
updateFlag = False
menubar = None
programFrame = None


def resource_path(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(os.path.abspath(os.path.dirname(__file__))))
    return os.path.join(bundle_dir, relative_path)


def clearProgramFrame():
    children = programFrame.winfo_children()
    for child in children:
        child.destroy()


def callProgram(programName):
    global root
    global selectedProgram
    global config_ini_path

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
        ssUnityProgram.call_ssUnity(root, programFrame, config_ini_path)
    elif selectedProgram == "rsRail":
        rsRailProgram.call_rsRail(root, programFrame)

    delete_OptionMenu()
    if selectedProgram == "smf":
        add_smfWriteOptionMenu()
    elif selectedProgram == "SSUnity":
        add_xlsxWriteOptionMenu()


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
            configRead.set(section, options, "0")

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
        configRead.read(config_ini_path, encoding="utf-8")

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


def add_xlsxWriteOptionMenu():
    global config_ini_path
    global v_modelNameMode
    global v_flagHexMode
    global v_ambReadMode
    global menubar
    global maxMenubarLen

    if not os.path.exists(config_ini_path):
        writeDefaultConfig()

    configRead = configparser.ConfigParser()
    configRead.read(config_ini_path, encoding="utf-8")

    readErrorFlag = False
    if configCheckOption("MODEL_NAME_MODE", "mode"):
        readErrorFlag = True
    if configCheckOption("FLAG_MODE", "mode"):
        readErrorFlag = True
    if configCheckOption("AMB_READ_MODE", "mode"):
        readErrorFlag = True

    if readErrorFlag:
        configRead.read(config_ini_path, encoding="utf-8")

    if menubar.entryconfig(tkinter.END) == menubar.entryconfig(maxMenubarLen):
        v_modelNameMode = tkinter.IntVar()
        v_modelNameMode.set(int(configRead.get("MODEL_NAME_MODE", "mode")))
        v_flagHexMode = tkinter.IntVar()
        v_flagHexMode.set(int(configRead.get("FLAG_MODE", "mode")))
        v_ambReadMode = tkinter.IntVar()
        v_ambReadMode.set(int(configRead.get("AMB_READ_MODE", "mode")))
        xlsxWriteOptionMenu = tkinter.Menu(menubar, tearoff=False)
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["model1"], variable=v_modelNameMode, value=0, command=writeXlsxConfig)
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["model2"], variable=v_modelNameMode, value=1, command=writeXlsxConfig)
        xlsxWriteOptionMenu.add_separator()
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["flag1"], variable=v_flagHexMode, value=0, command=writeXlsxConfig)
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["flag2"], variable=v_flagHexMode, value=1, command=writeXlsxConfig)
        xlsxWriteOptionMenu.add_separator()
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["ambRead1"], variable=v_ambReadMode, value=0, command=writeXlsxConfig)
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["ambRead2"], variable=v_ambReadMode, value=1, command=writeXlsxConfig)
        menubar.add_cascade(label=textSetting.textList["menu"]["SSUnity"]["name"], menu=xlsxWriteOptionMenu)


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

            config.add_section("MODEL_NAME_MODE")
            config.set("MODEL_NAME_MODE", "mode", 0)
            config.add_section("FLAG_MODE")
            config.set("FLAG_MODE", "mode", 0)
            config.add_section("AMB_READ_MODE")
            config.set("AMB_READ_MODE", "mode", 0)

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


def writeXlsxConfig():
    global v_modelNameMode
    global v_flagHexMode
    global v_ambReadMode
    global config_ini_path

    configRead = configparser.ConfigParser()
    configRead.read(config_ini_path, encoding="utf-8")

    configRead.set("MODEL_NAME_MODE", "mode", str(v_modelNameMode.get()))
    configRead.set("FLAG_MODE", "mode", str(v_flagHexMode.get()))
    configRead.set("AMB_READ_MODE", "mode", str(v_ambReadMode.get()))

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


def guiMain():
    global root
    global config_ini_path
    global v_frameCheck
    global v_meshCheck
    global v_XYZCheck
    global v_mtrlCheck
    global selectedProgram
    global maxMenubarLen
    global version
    global onlineUpdateVer
    global updateFlag
    global menubar
    global programFrame

    config_ini_path = "config.ini"
    if platform.system() == "Windows":
        config_ini_path = os.path.join(os.getenv("APPDATA"), "dend-mod-gui", "config.ini")

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


def execSaveRail(excelFile, railFile, quietFlag):
    if os.path.splitext(railFile)[1].lower() == ".den":
        return execSaveStageData(excelFile, railFile, quietFlag)

    import openpyxl
    import program.railEditor.dendDecrypt.RSdecrypt as dendRs
    import program.railEditor.dendDecrypt.CSdecrypt as dendCs
    import program.railEditor.dendDecrypt.BSdecrypt as dendBs
    import program.railEditor.dendDecrypt.LSdecrypt as dendLs
    from program.railEditor.importPy.excelWidget import ExcelWidget

    try:
        wb = openpyxl.load_workbook(excelFile, data_only=True)
        tabList = textSetting.textList["railEditor"]["railComboValue"]
        # ver
        ws = wb[tabList[0]]
        ver = ws.cell(1, 1).value

        oldVersionList = [
            "DEND_MAP_VER0100", "DEND_MAP_VER0101",
            "DEND_MAP_VER0102",
            "DEND_MAP_VER0110",
            "DEND_MAP_VER0300", "DEND_MAP_VER0400"
        ]

        if ver in oldVersionList:
            if ver == "DEND_MAP_VER0300" or ver == "DEND_MAP_VER0400":
                decryptFile = dendRs.RailDecrypt(railFile)
            elif ver == "DEND_MAP_VER0110":
                decryptFile = dendCs.RailDecrypt(railFile)
            elif ver == "DEND_MAP_VER0102":
                decryptFile = dendBs.RailDecrypt(railFile)
            elif ver == "DEND_MAP_VER0100" or ver == "DEND_MAP_VER0101":
                decryptFile = dendLs.RailDecrypt(railFile)
            excelWidget = ExcelWidget(decryptFile, None)

            if decryptFile.game == "LS":
                tabList = textSetting.textList["railEditor"]["railLsComboValue"]

            for tabName in tabList:
                if tabName not in wb.sheetnames:
                    errMsg = textSetting.textList["errorList"]["E95"].format(tabName)
                    mb.showerror(title=textSetting.textList["error"], message=errMsg)
                    return -3

            newByteArr = bytearray()

            if decryptFile.game == "LS":
                if not excelWidget.lsSave(wb, tabList, newByteArr):
                    if excelWidget.error == "":
                        errMsg = textSetting.textList["errorList"]["E14"]
                    else:
                        errMsg = excelWidget.error
                    mb.showerror(title=textSetting.textList["error"], message=errMsg)
                    return -4
            elif decryptFile.game == "BS":
                if not excelWidget.bsSave(wb, tabList, newByteArr):
                    if excelWidget.error == "":
                        errMsg = textSetting.textList["errorList"]["E14"]
                    else:
                        errMsg = excelWidget.error
                    mb.showerror(title=textSetting.textList["error"], message=errMsg)
                    return -4
            elif decryptFile.game == "CS":
                if not excelWidget.csSave(wb, tabList, newByteArr):
                    if excelWidget.error == "":
                        errMsg = textSetting.textList["errorList"]["E14"]
                    else:
                        errMsg = excelWidget.error
                    mb.showerror(title=textSetting.textList["error"], message=errMsg)
                    return -4
            elif decryptFile.game == "RS":
                if not excelWidget.rsSave(wb, tabList, newByteArr):
                    if excelWidget.error == "":
                        errMsg = textSetting.textList["errorList"]["E14"]
                    else:
                        errMsg = excelWidget.error
                    mb.showerror(title=textSetting.textList["error"], message=errMsg)
                    return -4
            w = open(decryptFile.filePath, "wb")
            w.write(newByteArr)
            w.close()
            if not quietFlag:
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I114"])
            return 0
    except Exception:
        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
        return -1


def execSaveStageData(stageDataFile, denFile, quietFlag):
    from program.ssUnity.SSDecrypt.denDecrypt import DenDecrypt
    from program.ssUnity.ssUnity import loadExcelAndMerge
    decryptFile = DenDecrypt(denFile)
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
        return -1
    if len(decryptFile.allList) == 1:
        dataName = decryptFile.allList[0][0]
        if dataName != "stagedata":
            errMsg = textSetting.textList["errorList"]["E105"] + denFile
            mb.showerror(title=textSetting.textList["error"], message=errMsg)
            return -5
        data = decryptFile.allList[0][-1]
        if os.path.splitext(stageDataFile)[1] == ".txt":
            with open(stageDataFile, "rb") as f:
                data.script = f.read()
        else:
            errMsgObj = {}
            if not loadExcelAndMerge(stageDataFile, data, errMsgObj):
                mb.showerror(title=textSetting.textList["error"], message=errMsgObj["message"])
                return -6
        data.save()
        with open(decryptFile.filePath, "wb") as w:
            w.write(decryptFile.env.file.save())
        if not quietFlag:
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
        return 0
    else:
        errMsg = textSetting.textList["errorList"]["E105"] + denFile
        mb.showerror(title=textSetting.textList["error"], message=errMsg)
        return -6


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        if sys.argv[1] in ["/saveRail", "/quietSaveRail", "/debugSaveRail"]:
            quietFlag = False
            debugFlag = False
            if sys.argv[1] == "/quietSaveRail":
                quietFlag = True
            elif sys.argv[1] == "/debugSaveRail":
                debugFlag = True
            excelFile = sys.argv[2]
            if not os.path.exists(excelFile):
                errMsg = textSetting.textList["errorList"]["E103"] + excelFile
                mb.showerror(title=textSetting.textList["error"], message=errMsg)
                sys.exit(-2)
            railFile = sys.argv[3]
            if os.path.splitext(railFile)[1].lower() == ".bin":
                if not os.path.exists(railFile):
                    w = open(railFile, "wb")
                    w.close()
            else:
                if not os.path.exists(railFile):
                    errMsg = textSetting.textList["errorList"]["E104"] + railFile
                    mb.showerror(title=textSetting.textList["error"], message=errMsg)
                    sys.exit(-2)
            if debugFlag:
                debugStr = "エクセルのパス\n{0}".format(os.path.abspath(excelFile))
                debugStr += "\n"
                debugStr += "ファイルのパス\n{0}".format(os.path.abspath(railFile))
                debugStr += "\nで確認しました。このまま実行しますか？"
                result = mb.askyesno(title=textSetting.textList["confirm"], message=debugStr)
                if not result:
                    sys.exit(0)
            sys.exit(execSaveRail(excelFile, railFile, quietFlag))
    guiMain()
