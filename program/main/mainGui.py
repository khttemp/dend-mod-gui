import os
import sys
from functools import partial

import program.main.mainProcess as mainProcess
import program.sub.textSetting as textSetting
import program.sub.errorLogClass as errorLogClass

import program.sub.comicscript.comicscriptGui as comicscriptGui
import program.sub.mdlBin.mdlBinGui as mdlBinGui
import program.sub.mdlinfo.mdlinfoGui as mdlinfoGui
import program.sub.orgInfoEditor.orgInfoEditorGui as orgInfoEditorGui
import program.sub.musicEditor.musicEditorGui as musicEditorGui
import program.sub.fvtMaker.fvtMakerGui as fvtMakerGui
import program.sub.railEditor.railEditorGui as railEditorGui
import program.sub.smf.smfGui as smfGui
import program.sub.ssUnity.ssUnityGui as ssUnityGui
import program.sub.rsRail.rsRailGui as rsRailGui
import program.sub.appearance.rootFrameWidget as rootFrameWidget

import configparser
import platform
import ctypes
import traceback
import tkinter
from tkinter import ttk
from tkinter import messagebox as mb

errObj = errorLogClass.ErrorLogObj()


class MainWindow(tkinter.Frame):
    def __init__(self, master, importDict):
        super().__init__(master)
        self.root = master
        self.rootFrameAppearance = None
        self.darkModeDllPath = None
        self.darkModeDll = None
        self.importDict = importDict

        self.selectedProgram = None
        self.selectedProgramFrame = None
        self.version = mainProcess.getUpdateVer(self.importDict["rootPath"])
        self.onlineVersion = mainProcess.getOnlineUpdateVer(self.importDict["configPath"])
        cmdJsonInfo = mainProcess.readCmdJsonInfo(self.importDict["rootPath"])
        self.importDict["cmdJsonInfo"] = cmdJsonInfo
        fvtInfo = mainProcess.readFvtInfo(self.importDict["rootPath"])
        self.importDict["fvtInfo"] = fvtInfo
        fvtImageInfo = mainProcess.readFvtImagePath(self.importDict["rootPath"])
        self.importDict["fvtImageInfo"] = fvtImageInfo

        self.checkConfig()
        self.drawMenu()

        self.readRootFrameAppearance()
        self.maxMenubarLen = self.menubar.index(tkinter.END)

        self.root.after(100, self.checkUpdate)

    def checkConfig(self):
        configPath = self.importDict["configPath"]
        if not os.path.exists(configPath):
            mainProcess.writeDefaultConfig(configPath)

    def drawMenu(self):
        self.root.title(textSetting.textList["app"]["title"].format(self.version))
        self.root.option_add("*font", textSetting.textList["defaultFont"])
        self.root.geometry("1024x768")

        self.style = ttk.Style(self.root)
        self.style.configure(".", font=textSetting.textList["defaultFont"])

        self.menubar = tkinter.Menu(self.root)

        self.v_prog = tkinter.IntVar()

        progmenu = tkinter.Menu(self.menubar, tearoff=False)
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["SSUnity"], value=-1, variable=self.v_prog, command=partial(self.callProgram, "SSUnity"))
        progmenu.add_separator()
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["orgInfoEditor"], value=1, variable=self.v_prog, command=partial(self.callProgram, "orgInfoEditor"))
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["mdlBin"], value=2, variable=self.v_prog, command=partial(self.callProgram, "mdlBin"))
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["mdlinfo"], value=3, variable=self.v_prog, command=partial(self.callProgram, "mdlinfo"))
        progmenu.add_separator()
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["comicscript"], value=4, variable=self.v_prog, command=partial(self.callProgram, "comicscript"))
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["musicEditor"], value=5, variable=self.v_prog, command=partial(self.callProgram, "musicEditor"))
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["fvtMaker"], value=6, variable=self.v_prog, command=partial(self.callProgram, "fvtMaker"))
        progmenu.add_separator()
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["railEditor"], value=7, variable=self.v_prog, command=partial(self.callProgram, "railEditor"))
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["rsRail"], value=8, variable=self.v_prog, command=partial(self.callProgram, "rsRail"))
        progmenu.add_separator()
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["smf"], value=9, variable=self.v_prog, command=partial(self.callProgram, "smf"))
        progmenu.add_separator()
        progmenu.add_command(label=textSetting.textList["menu"]["appearance"]["rootFrame"], command=self.editRootFrameAppearance)
        progmenu.add_radiobutton(label=textSetting.textList["menu"]["program"]["exit"], value=-2, variable=self.v_prog, command=sys.exit)

        filemenu = tkinter.Menu(self.menubar, tearoff=False)
        filemenu.add_command(label=textSetting.textList["menu"]["file"]["loadFile"], command=self.loadFile)

        self.menubar.add_cascade(label=textSetting.textList["menu"]["program"]["name"], menu=progmenu)
        self.menubar.add_cascade(label=textSetting.textList["menu"]["file"]["name"], menu=filemenu)

        self.root.config(menu=self.menubar)

    def checkUpdate(self):
        if self.onlineVersion == "":
            return
        if self.onlineVersion == self.version:
            return

        msg = textSetting.textList["update"]["message"].format(self.onlineVersion)
        result = mb.askyesno(title=textSetting.textList["update"]["title"], message=msg)
        if result:
            mainProcess.openReleases()

    def clearRootFrame(self):
        children = self.root.winfo_children()
        for idx, child in enumerate(children):
            # MainWindow, menu
            if idx <= 1:
                continue
            child.destroy()

    def readRootFrameAppearance(self):
        configPath = self.importDict["configPath"]
        mainProcess.configCheckOption(configPath, "ROOT_FRAME", "bg_color", "SystemButtonFace")
        mainProcess.configCheckOption(configPath, "ROOT_FRAME", "dark_mode")
        mainProcess.configCheckOption(configPath, "ROOT_FRAME", "theme", "vista")
        mainProcess.configCheckOption(configPath, "LABEL", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "LABELFRAME_LABEL", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "RADIO", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "TREEVIEW", "bg_color", "SystemWindow")
        mainProcess.configCheckOption(configPath, "TREEVIEW", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "TREEVIEW", "sel_bg_color", "SystemHighlight")
        mainProcess.configCheckOption(configPath, "TREEVIEW", "sel_fg_color", "SystemWindow")
        mainProcess.configCheckOption(configPath, "BUTTON", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "ENTRY", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "TREEVIEW", "field_bg_color", "SystemWindow")
        mainProcess.configCheckOption(configPath, "TREEVIEW_HEADER", "bg_color", "SystemButtonFace")
        mainProcess.configCheckOption(configPath, "TREEVIEW_HEADER", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "COMBOBOX", "bg_color", "SystemWindow")
        mainProcess.configCheckOption(configPath, "COMBOBOX", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(configPath, "COMBOBOX", "sel_bg_color", "SystemHighlight")
        mainProcess.configCheckOption(configPath, "COMBOBOX", "sel_fg_color", "SystemWindow")
        mainProcess.configCheckOption(configPath, "RADIO", "indicator_color", "SystemWindow")
        mainProcess.configCheckOption(configPath, "RADIO", "sel_indicator_color", "SystemWindowText")

        configRead = configparser.ConfigParser()
        configRead.read(configPath, encoding="utf-8")
        rootDarkModeFlag = int(configRead.get("ROOT_FRAME", "dark_mode")) > 0
        rootFrameBackgroundColor = configRead.get("ROOT_FRAME", "bg_color")
        self.root["bg"] = rootFrameBackgroundColor

        labelForegroundColor = configRead.get("LABEL", "fg_color")
        labelframeLabelForegroundColor = configRead.get("LABELFRAME_LABEL", "fg_color")
        radioForegroundColor = configRead.get("RADIO", "fg_color")

        treeviewBackgroundColor = configRead.get("TREEVIEW", "bg_color")
        treeviewForegroundColor = configRead.get("TREEVIEW", "fg_color")
        treeviewSelectedBackgroundColor = configRead.get("TREEVIEW", "sel_bg_color")
        treeviewSelectedForegroundColor = configRead.get("TREEVIEW", "sel_fg_color")

        buttonForegroundColor = configRead.get("BUTTON", "fg_color")
        entryForegroundColor = configRead.get("ENTRY", "fg_color")

        treeviewFieldBackgroundColor = configRead.get("TREEVIEW", "field_bg_color")
        treeviewHeaderBackgroundColor = configRead.get("TREEVIEW_HEADER", "bg_color")
        treeviewHeaderForegroundColor = configRead.get("TREEVIEW_HEADER", "fg_color")

        comboboxBackgroundColor = configRead.get("COMBOBOX", "bg_color")
        comboboxForegroundColor = configRead.get("COMBOBOX", "fg_color")
        comboboxSelectedBackgroundColor = configRead.get("COMBOBOX", "sel_bg_color")
        comboboxSelectedForegroundColor = configRead.get("COMBOBOX", "sel_fg_color")

        indicatorColor = configRead.get("RADIO", "indicator_color")
        indicatorSelectedColor = configRead.get("RADIO", "sel_indicator_color")

        if platform.system() == "Windows":
            try:
                if rootDarkModeFlag:
                    self.darkModeDllPath = mainProcess.dll_path(self.importDict["rootPath"], "tablacusdark64.dll")
                    self.darkModeDll = ctypes.CDLL(self.darkModeDllPath)
                    rootDarkModeFlag = True
            except Exception:
                rootDarkModeFlag = False
                errObj.write(traceback.format_exc())

        themeName = configRead.get("ROOT_FRAME", "theme")
        self.style.theme_use(themeName)

        self.style.configure("custom.TLabel", background=rootFrameBackgroundColor, foreground=labelForegroundColor)
        self.style.configure("custom.red.TLabel", background=rootFrameBackgroundColor, foreground="red")
        self.style.configure("custom.blue.TLabel", background=rootFrameBackgroundColor, foreground="blue")
        self.style.configure("custom.green.TLabel", background=rootFrameBackgroundColor, foreground="green")
        self.style.configure("custom.444444.TLabel", background=rootFrameBackgroundColor, foreground="#444444")
        self.style.configure("custom.TButton", background=rootFrameBackgroundColor, foreground=buttonForegroundColor)
        self.style.configure("custom.update.TButton", background=rootFrameBackgroundColor, foreground=buttonForegroundColor, font=textSetting.textList["font7"], width=5, disabledbackground=rootFrameBackgroundColor)
        self.style.configure("custom.listbox.TButton", background=rootFrameBackgroundColor, foreground=buttonForegroundColor, font=textSetting.textList["font2"], width=5)
        self.style.configure("custom.paste.TButton", background=rootFrameBackgroundColor, foreground=buttonForegroundColor, font=textSetting.textList["font2"], width=10)
        self.style.configure("custom.elsePerf.TButton", background=rootFrameBackgroundColor, foreground=buttonForegroundColor, font=textSetting.textList["font7"])
        self.style.configure("custom.TRadiobutton", background=rootFrameBackgroundColor, foreground=radioForegroundColor)
        self.style.configure("custom.TCheckbutton", background=rootFrameBackgroundColor, foreground=radioForegroundColor, font=textSetting.textList["font2"])
        self.style.configure("custom.railFlag.TCheckbutton", background=rootFrameBackgroundColor, foreground=radioForegroundColor)
        self.style.configure("custom.TLabelframe", background=rootFrameBackgroundColor)
        self.style.configure("custom.TLabelframe.Label", background=rootFrameBackgroundColor, foreground=labelframeLabelForegroundColor)
        self.style.configure("custom.TFrame", background=rootFrameBackgroundColor)
        self.style.configure("custom.TSeparator", background=rootFrameBackgroundColor)
        self.style.configure("custom.Treeview", background=treeviewBackgroundColor, foreground=treeviewForegroundColor, fieldbackground=treeviewFieldBackgroundColor)
        self.style.configure("custom.Treeview.Heading", background=treeviewHeaderBackgroundColor, foreground=treeviewHeaderForegroundColor)
        self.style.configure("custom.TMenubutton", background=rootFrameBackgroundColor, foreground=buttonForegroundColor)
        self.style.configure("custom.TSpinbox", fieldbackground=rootFrameBackgroundColor, foreground=buttonForegroundColor)
        self.style.map("custom.TRadiobutton", indicatorcolor=[("!selected", indicatorColor), ("selected", indicatorSelectedColor)])
        self.style.map("custom.TCheckbutton", indicatorcolor=[("!selected", indicatorColor), ("selected", indicatorSelectedColor)])
        self.style.map("custom.railFlag.TCheckbutton", indicatorcolor=[("!selected", indicatorColor), ("selected", indicatorSelectedColor)])
        self.style.map("custom.TEntry", background=[("!readonly", rootFrameBackgroundColor), ("readonly", rootFrameBackgroundColor)], fieldbackground=[("!readonly", rootFrameBackgroundColor), ("readonly", rootFrameBackgroundColor)], foreground=[("!readonly", entryForegroundColor), ("readonly", entryForegroundColor)])
        self.style.map("custom.Horizontal.TScrollbar", background=[("!disabled", rootFrameBackgroundColor), ("disabled", rootFrameBackgroundColor)])
        self.style.map("custom.Vertical.TScrollbar", background=[("!disabled", rootFrameBackgroundColor), ("disabled", rootFrameBackgroundColor)])
        self.style.map("custom.TCombobox", background=[("readonly", rootFrameBackgroundColor), ("disabled", rootFrameBackgroundColor)], fieldbackground=[("readonly", comboboxBackgroundColor), ("disabled", comboboxBackgroundColor)], foreground=[("readonly", comboboxForegroundColor), ("disabled", comboboxForegroundColor)])
        self.style.map("custom.Treeview", background=[("selected", treeviewSelectedBackgroundColor)], foreground=[("selected", treeviewSelectedForegroundColor)])
        self.root.option_add("*TCombobox*Listbox.background", comboboxBackgroundColor)
        self.root.option_add("*TCombobox*Listbox.foreground", comboboxForegroundColor)
        self.root.option_add("*TCombobox*Listbox.selectBackground", comboboxSelectedBackgroundColor)
        self.root.option_add("*TCombobox*Listbox.selectForeground", comboboxSelectedForegroundColor)

        self.rootFrameAppearance = rootFrameWidget.RootFrameAppearance(self.root, configPath, labelForegroundColor, rootFrameBackgroundColor, configRead)

    def editRootFrameAppearance(self):
        pass

    def callProgram(self, programName):
        self.clearRootFrame()

        self.selectedProgram = programName
        if self.selectedProgram == "orgInfoEditor":
            self.selectedProgramFrame = orgInfoEditorGui.OrgInfoEditorWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "mdlBin":
            self.selectedProgramFrame = mdlBinGui.MdlBinWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "mdlinfo":
            self.selectedProgramFrame = mdlinfoGui.MdlinfoWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "comicscript":
            self.selectedProgramFrame = comicscriptGui.ComicscriptWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "musicEditor":
            self.selectedProgramFrame = musicEditorGui.MusicEditorWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "fvtMaker":
            self.selectedProgramFrame = fvtMakerGui.FvtMakerWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "railEditor":
            self.selectedProgramFrame = railEditorGui.RailEditorWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "smf":
            self.selectedProgramFrame = smfGui.SmfWindow(self.root, self.importDict, self.rootFrameAppearance)
        elif self.selectedProgram == "SSUnity":
            self.selectedProgramFrame = ssUnityGui.SSUnityWindow(self.root, self.importDict)
        elif self.selectedProgram == "rsRail":
            self.selectedProgramFrame = rsRailGui.RsRailWindow(self.root, self.importDict)

        self.setConfigMenu(self.selectedProgram)

    def setConfigMenu(self, selectedProgram):
        if self.menubar.index(tkinter.END) > self.maxMenubarLen:
            self.menubar.delete(self.maxMenubarLen + 1)

        if selectedProgram in ["SSUnity", "railEditor"]:
            if self.menubar.entryconfig(tkinter.END) == self.menubar.entryconfig(self.maxMenubarLen):
                configMenu = self.addXlsxWriteOptionMenu()
                self.menubar.add_cascade(label=textSetting.textList["menu"]["SSUnity"]["name"], menu=configMenu)
        elif selectedProgram == "comicscript":
            if self.menubar.entryconfig(tkinter.END) == self.menubar.entryconfig(self.maxMenubarLen):
                configMenu = self.addComicscriptOptionMenu()
                self.menubar.add_cascade(label=textSetting.textList["menu"]["comicscript"]["name"], menu=configMenu)
        elif selectedProgram == "smf":
            if self.menubar.entryconfig(tkinter.END) == self.menubar.entryconfig(self.maxMenubarLen):
                configMenu = self.addSmfWriteOptionMenu()
                self.menubar.add_cascade(label=textSetting.textList["menu"]["smf"]["name"], menu=configMenu)

    def addXlsxWriteOptionMenu(self):
        configPath = self.importDict["configPath"]
        model, flag, amb = mainProcess.readXlsxWriteConfig(configPath)
        self.v_modelNameMode = tkinter.IntVar()
        self.v_modelNameMode.set(model)
        self.v_flagHexMode = tkinter.IntVar()
        self.v_flagHexMode.set(flag)
        self.v_ambReadMode = tkinter.IntVar()
        self.v_ambReadMode.set(amb)

        xlsxWriteOptionMenu = tkinter.Menu(self.menubar, tearoff=False)
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["model1"], variable=self.v_modelNameMode, value=0, command=partial(mainProcess.writeXlsxConfig, configPath, "model", 0))
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["model2"], variable=self.v_modelNameMode, value=1, command=partial(mainProcess.writeXlsxConfig, configPath, "model", 1))
        xlsxWriteOptionMenu.add_separator()
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["flag1"], variable=self.v_flagHexMode, value=0, command=partial(mainProcess.writeXlsxConfig, configPath, "flag", 0))
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["flag2"], variable=self.v_flagHexMode, value=1, command=partial(mainProcess.writeXlsxConfig, configPath, "flag", 1))
        xlsxWriteOptionMenu.add_separator()
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["ambRead1"], variable=self.v_ambReadMode, value=0, command=partial(mainProcess.writeXlsxConfig, configPath, "amb", 0))
        xlsxWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["SSUnity"]["write"]["ambRead2"], variable=self.v_ambReadMode, value=1, command=partial(mainProcess.writeXlsxConfig, configPath, "amb", 1))
        return xlsxWriteOptionMenu

    def addComicscriptOptionMenu(self):
        configPath = self.importDict["configPath"]
        game = mainProcess.readComicscriptConfig(configPath)

        self.v_comicscriptCheck = tkinter.IntVar()
        self.v_comicscriptCheck.set(game)

        comicscriptOptionMenu = tkinter.Menu(self.menubar, tearoff=False)
        for i in range(5):
            comicscriptOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["comicscript"]["gameList"][i], value=i, variable=self.v_comicscriptCheck, command=partial(mainProcess.writeComicscriptConfig, configPath, i))
        return comicscriptOptionMenu

    def addSmfWriteOptionMenu(self):
        configPath = self.importDict["configPath"]
        flagList, glb = mainProcess.readSmfWriteConfig(configPath)

        self.v_frameCheck = tkinter.IntVar()
        self.v_frameCheck.set(flagList[0])
        self.v_meshCheck = tkinter.IntVar()
        self.v_meshCheck.set(flagList[1])
        self.v_XYZCheck = tkinter.IntVar()
        self.v_XYZCheck.set(flagList[2])
        self.v_mtrlCheck = tkinter.IntVar()
        self.v_mtrlCheck.set(flagList[3])
        self.v_flagGlbMode = tkinter.IntVar()
        self.v_flagGlbMode.set(glb)

        smfWriteOptionMenu = tkinter.Menu(self.menubar, tearoff=False)
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt1"], variable=self.v_frameCheck, command=partial(mainProcess.writeSmfFlagConfig, self.v_frameCheck, configPath, "frame"))
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt2"], variable=self.v_meshCheck, command=partial(mainProcess.writeSmfFlagConfig, self.v_meshCheck, configPath, "mesh"))
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt3"], variable=self.v_XYZCheck, command=partial(mainProcess.writeSmfFlagConfig, self.v_XYZCheck, configPath, "xyz"))
        smfWriteOptionMenu.add_checkbutton(label=textSetting.textList["menu"]["smf"]["write"]["opt4"], variable=self.v_mtrlCheck, command=partial(mainProcess.writeSmfFlagConfig, self.v_mtrlCheck, configPath, "mtrl"))
        smfWriteOptionMenu.add_separator()
        smfWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["smf"]["glb"]["opt1"], variable=self.v_flagGlbMode, value=0, command=partial(mainProcess.writeGlbConfig, configPath, 0))
        smfWriteOptionMenu.add_radiobutton(label=textSetting.textList["menu"]["smf"]["glb"]["opt2"], variable=self.v_flagGlbMode, value=1, command=partial(mainProcess.writeGlbConfig, configPath, 1))

        return smfWriteOptionMenu

    def loadFile(self):
        if self.selectedProgram is None:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E1"])
            return

        if self.selectedProgram == "orgInfoEditor":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "mdlBin":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "mdlinfo":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "comicscript":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "musicEditor":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "fvtMaker":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "railEditor":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "smf":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "SSUnity":
            self.selectedProgramFrame.openFile()
        elif self.selectedProgram == "rsRail":
            self.selectedProgramFrame.openFile()


def guiMain(importDict):
    root = tkinter.Tk()
    window = MainWindow(root, importDict)
    importDict["window"] = window
    window.mainloop()
