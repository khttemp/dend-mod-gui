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

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb

errObj = errorLogClass.ErrorLogObj()


class MainWindow(tkinter.Frame):
    def __init__(self, master, importDict):
        super().__init__(master)
        self.root = master
        self.rootFrameAppearance = rootFrameWidget.RootFrameAppearance(master, importDict)
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
        self.rootFrameAppearance.readRootFrameAppearance()
        self.setConfigStyle()

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
        progmenu.add_command(label=textSetting.textList["menu"]["appearance"]["rootFrame"], command=self.rootFrameAppearance.editRootFrameAppearance)
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

    def setConfigStyle(self):
        self.style.theme_use(self.rootFrameAppearance.configStyle.themeName)
        self.style.configure("custom.TLabel", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.labelForegroundColor)
        self.style.configure("custom.red.TLabel", background=self.rootFrameAppearance.bgColor, foreground="red")
        self.style.configure("custom.blue.TLabel", background=self.rootFrameAppearance.bgColor, foreground="blue")
        self.style.configure("custom.green.TLabel", background=self.rootFrameAppearance.bgColor, foreground="green")
        self.style.configure("custom.444444.TLabel", background=self.rootFrameAppearance.bgColor, foreground="#444444")
        self.style.configure("custom.TButton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.buttonForegroundColor)
        self.style.configure("custom.update.TButton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.buttonForegroundColor, font=textSetting.textList["font7"], width=5, disabledbackground=self.rootFrameAppearance.bgColor)
        self.style.configure("custom.listbox.TButton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.buttonForegroundColor, font=textSetting.textList["font2"], width=5)
        self.style.configure("custom.paste.TButton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.buttonForegroundColor, font=textSetting.textList["font2"], width=10)
        self.style.configure("custom.elsePerf.TButton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.buttonForegroundColor, font=textSetting.textList["font7"])
        self.style.configure("custom.TRadiobutton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.radioForegroundColor)
        self.style.configure("custom.TCheckbutton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.radioForegroundColor, font=textSetting.textList["font2"])
        self.style.configure("custom.railFlag.TCheckbutton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.radioForegroundColor)
        self.style.configure("custom.TLabelframe", background=self.rootFrameAppearance.bgColor)
        self.style.configure("custom.TLabelframe.Label", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.labelframeLabelForegroundColor)
        self.style.configure("custom.TFrame", background=self.rootFrameAppearance.bgColor)
        self.style.configure("custom.TSeparator", background=self.rootFrameAppearance.bgColor)
        self.style.configure("custom.Treeview", background=self.rootFrameAppearance.configStyle.treeviewBackgroundColor, foreground=self.rootFrameAppearance.configStyle.treeviewForegroundColor, fieldbackground=self.rootFrameAppearance.configStyle.treeviewFieldBackgroundColor)
        self.style.configure("custom.Treeview.Heading", background=self.rootFrameAppearance.configStyle.treeviewHeaderBackgroundColor, foreground=self.rootFrameAppearance.configStyle.treeviewHeaderForegroundColor)
        self.style.configure("custom.TMenubutton", background=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.buttonForegroundColor)
        self.style.configure("custom.TSpinbox", fieldbackground=self.rootFrameAppearance.bgColor, foreground=self.rootFrameAppearance.configStyle.buttonForegroundColor)
        self.style.map("custom.TRadiobutton", indicatorcolor=[("!selected", self.rootFrameAppearance.configStyle.indicatorColor), ("selected", self.rootFrameAppearance.configStyle.indicatorSelectedColor)])
        self.style.map("custom.TCheckbutton", indicatorcolor=[("!selected", self.rootFrameAppearance.configStyle.indicatorColor), ("selected", self.rootFrameAppearance.configStyle.indicatorSelectedColor)])
        self.style.map("custom.railFlag.TCheckbutton", indicatorcolor=[("!selected", self.rootFrameAppearance.configStyle.indicatorColor), ("selected", self.rootFrameAppearance.configStyle.indicatorSelectedColor)])
        self.style.map("custom.TEntry", background=[("!readonly", self.rootFrameAppearance.bgColor), ("readonly", self.rootFrameAppearance.bgColor)], fieldbackground=[("!readonly", self.rootFrameAppearance.bgColor), ("readonly", self.rootFrameAppearance.bgColor)], foreground=[("!readonly", self.rootFrameAppearance.configStyle.entryForegroundColor), ("readonly", self.rootFrameAppearance.configStyle.entryForegroundColor)])
        self.style.map("custom.Horizontal.TScrollbar", background=[("!disabled", self.rootFrameAppearance.bgColor), ("disabled", self.rootFrameAppearance.bgColor)])
        self.style.map("custom.Vertical.TScrollbar", background=[("!disabled", self.rootFrameAppearance.bgColor), ("disabled", self.rootFrameAppearance.bgColor)])
        self.style.map("custom.TCombobox", background=[("readonly", self.rootFrameAppearance.bgColor), ("disabled", self.rootFrameAppearance.bgColor)], fieldbackground=[("readonly", self.rootFrameAppearance.configStyle.comboboxBackgroundColor), ("disabled", self.rootFrameAppearance.configStyle.comboboxBackgroundColor)], foreground=[("readonly", self.rootFrameAppearance.configStyle.comboboxForegroundColor), ("disabled", self.rootFrameAppearance.configStyle.comboboxForegroundColor)])
        self.style.map("custom.Treeview", background=[("selected", self.rootFrameAppearance.configStyle.treeviewSelectedBackgroundColor)], foreground=[("selected", self.rootFrameAppearance.configStyle.treeviewSelectedForegroundColor)])
        self.root.option_add("*TCombobox*Listbox.background", self.rootFrameAppearance.configStyle.comboboxBackgroundColor)
        self.root.option_add("*TCombobox*Listbox.foreground", self.rootFrameAppearance.configStyle.comboboxForegroundColor)
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.rootFrameAppearance.configStyle.comboboxSelectedBackgroundColor)
        self.root.option_add("*TCombobox*Listbox.selectForeground", self.rootFrameAppearance.configStyle.comboboxSelectedForegroundColor)

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
