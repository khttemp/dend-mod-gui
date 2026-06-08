from dataclasses import dataclass
from functools import partial
import platform
import ctypes, _ctypes
import traceback
import configparser
import tkinter
from tkinter import ttk
from tkinter import colorchooser
from tkinter import messagebox as mb

import program.main.mainProcess as mainProcess
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog
import program.sub.errorLogClass as errorLogClass

errObj = errorLogClass.ErrorLogObj()


@dataclass
class ConfigStyle:
    rootDarkModeFlag: bool = False
    themeName: str = ""
    labelForegroundColor: str = ""
    labelframeLabelForegroundColor: str = ""
    radioForegroundColor: str = ""
    treeviewBackgroundColor: str = ""
    treeviewForegroundColor: str = ""
    treeviewSelectedBackgroundColor: str = ""
    treeviewSelectedForegroundColor: str = ""
    buttonForegroundColor: str = ""
    entryForegroundColor: str = ""
    treeviewFieldBackgroundColor: str = ""
    treeviewHeaderBackgroundColor: str = ""
    treeviewHeaderForegroundColor: str = ""
    comboboxBackgroundColor: str = ""
    comboboxForegroundColor: str = ""
    comboboxSelectedBackgroundColor: str = ""
    comboboxSelectedForegroundColor: str = ""
    indicatorColor: str = ""
    indicatorSelectedColor: str = ""


class RootFrameAppearance:
    def __init__(self, root, importDict):
        self.root = root
        self.rootPath = importDict["rootPath"]
        self.configPath = importDict["configPath"]
        self.fgColor = ""
        self.bgColor = ""
        self.darkModeDll = None
        self.configStyle = ConfigStyle()

    def readRootFrameAppearance(self):
        mainProcess.configCheckOption(self.configPath, "ROOT_FRAME", "bg_color", "SystemButtonFace")
        mainProcess.configCheckOption(self.configPath, "ROOT_FRAME", "dark_mode")
        mainProcess.configCheckOption(self.configPath, "ROOT_FRAME", "theme", "vista")
        mainProcess.configCheckOption(self.configPath, "LABEL", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "LABELFRAME_LABEL", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "RADIO", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "TREEVIEW", "bg_color", "SystemWindow")
        mainProcess.configCheckOption(self.configPath, "TREEVIEW", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "TREEVIEW", "sel_bg_color", "SystemHighlight")
        mainProcess.configCheckOption(self.configPath, "TREEVIEW", "sel_fg_color", "SystemWindow")
        mainProcess.configCheckOption(self.configPath, "BUTTON", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "ENTRY", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "TREEVIEW", "field_bg_color", "SystemWindow")
        mainProcess.configCheckOption(self.configPath, "TREEVIEW_HEADER", "bg_color", "SystemButtonFace")
        mainProcess.configCheckOption(self.configPath, "TREEVIEW_HEADER", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "COMBOBOX", "bg_color", "SystemWindow")
        mainProcess.configCheckOption(self.configPath, "COMBOBOX", "fg_color", "SystemWindowText")
        mainProcess.configCheckOption(self.configPath, "COMBOBOX", "sel_bg_color", "SystemHighlight")
        mainProcess.configCheckOption(self.configPath, "COMBOBOX", "sel_fg_color", "SystemWindow")
        mainProcess.configCheckOption(self.configPath, "RADIO", "indicator_color", "SystemWindow")
        mainProcess.configCheckOption(self.configPath, "RADIO", "sel_indicator_color", "SystemWindowText")

        configRead = configparser.ConfigParser()
        configRead.read(self.configPath, encoding="utf-8")
        self.bgColor = configRead.get("ROOT_FRAME", "bg_color")
        self.root["bg"] = self.bgColor
        self.configStyle.rootDarkModeFlag = int(configRead.get("ROOT_FRAME", "dark_mode")) > 0
        self.configStyle.themeName = configRead.get("ROOT_FRAME", "theme")

        self.configStyle.labelForegroundColor = configRead.get("LABEL", "fg_color")
        self.fgColor = self.configStyle.labelForegroundColor
        self.configStyle.labelframeLabelForegroundColor = configRead.get("LABELFRAME_LABEL", "fg_color")
        self.configStyle.radioForegroundColor = configRead.get("RADIO", "fg_color")

        self.configStyle.treeviewBackgroundColor = configRead.get("TREEVIEW", "bg_color")
        self.configStyle.treeviewForegroundColor = configRead.get("TREEVIEW", "fg_color")
        self.configStyle.treeviewSelectedBackgroundColor = configRead.get("TREEVIEW", "sel_bg_color")
        self.configStyle.treeviewSelectedForegroundColor = configRead.get("TREEVIEW", "sel_fg_color")

        self.configStyle.buttonForegroundColor = configRead.get("BUTTON", "fg_color")
        self.configStyle.entryForegroundColor = configRead.get("ENTRY", "fg_color")

        self.configStyle.treeviewFieldBackgroundColor = configRead.get("TREEVIEW", "field_bg_color")
        self.configStyle.treeviewHeaderBackgroundColor = configRead.get("TREEVIEW_HEADER", "bg_color")
        self.configStyle.treeviewHeaderForegroundColor = configRead.get("TREEVIEW_HEADER", "fg_color")

        self.configStyle.comboboxBackgroundColor = configRead.get("COMBOBOX", "bg_color")
        self.configStyle.comboboxForegroundColor = configRead.get("COMBOBOX", "fg_color")
        self.configStyle.comboboxSelectedBackgroundColor = configRead.get("COMBOBOX", "sel_bg_color")
        self.configStyle.comboboxSelectedForegroundColor = configRead.get("COMBOBOX", "sel_fg_color")

        self.configStyle.indicatorColor = configRead.get("RADIO", "indicator_color")
        self.configStyle.indicatorSelectedColor = configRead.get("RADIO", "sel_indicator_color")

        if platform.system() == "Windows":
            try:
                if self.configStyle.rootDarkModeFlag:
                    darkModeDllPath = mainProcess.dll_path(self.rootPath, "tablacusdark64.dll")
                    self.darkModeDll = ctypes.CDLL(darkModeDllPath)
            except Exception:
                self.configStyle.rootDarkModeFlag = False
                errObj.write(traceback.format_exc())

    def editRootFrameAppearance(self):
        self.reloadFlag = False
        result = EditRootFrameAppearance(self.root, textSetting.textList["appearance"]["rootFrame"]["editRootFrameTitle"], self.bgColor, self.configStyle)
        if result.dirtyFlag and result.updateFlag:
            self.reloadFlag = True
            self.bgColor = result.bgColor
            currentDarkModeFlag = self.configStyle.rootDarkModeFlag
            newDarkModeFlag = int(result.v_darkModeFlag.get()) > 0
            self.configStyle.rootDarkModeFlag = newDarkModeFlag
            self.configStyle.themeName = result.v_themeName.get()
            self.configStyle.labelForegroundColor = result.configStyle.labelForegroundColor
            self.fgColor = result.configStyle.labelForegroundColor
            self.configStyle.radioForegroundColor = result.configStyle.radioForegroundColor
            self.configStyle.labelframeLabelForegroundColor = result.configStyle.labelframeLabelForegroundColor
            self.configStyle.treeviewBackgroundColor = result.configStyle.treeviewBackgroundColor
            self.configStyle.treeviewForegroundColor = result.configStyle.treeviewForegroundColor
            self.configStyle.treeviewSelectedBackgroundColor = result.configStyle.treeviewSelectedBackgroundColor
            self.configStyle.treeviewSelectedForegroundColor = result.configStyle.treeviewSelectedForegroundColor
            self.configStyle.buttonForegroundColor = result.configStyle.buttonForegroundColor
            self.configStyle.entryForegroundColor = result.configStyle.entryForegroundColor
            self.configStyle.treeviewFieldBackgroundColor = result.configStyle.treeviewFieldBackgroundColor
            self.configStyle.treeviewHeaderBackgroundColor = result.configStyle.treeviewHeaderBackgroundColor
            self.configStyle.treeviewHeaderForegroundColor = result.configStyle.treeviewHeaderForegroundColor
            self.configStyle.comboboxBackgroundColor = result.configStyle.comboboxBackgroundColor
            self.configStyle.comboboxForegroundColor = result.configStyle.comboboxForegroundColor
            self.configStyle.comboboxSelectedBackgroundColor = result.configStyle.comboboxSelectedBackgroundColor
            self.configStyle.comboboxSelectedForegroundColor = result.configStyle.comboboxSelectedForegroundColor
            self.configStyle.indicatorColor = result.configStyle.indicatorColor
            self.configStyle.indicatorSelectedColor = result.configStyle.indicatorSelectedColor

            if platform.system() == "Windows":
                try:
                    if currentDarkModeFlag != newDarkModeFlag:
                        if newDarkModeFlag:
                            darkModeDllPath = mainProcess.dll_path(self.rootPath, "tablacusdark64.dll")
                            self.darkModeDll = ctypes.CDLL(darkModeDllPath)
                        else:
                            _ctypes.FreeLibrary(self.darkModeDll._handle)
                            del self.darkModeDll
                            self.darkModeDll = None
                except Exception:
                    errObj.write(traceback.format_exc())

            mainProcess.writeConfigAppearance(self.configPath, self.bgColor, self.configStyle)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["appearance"]["success"])


class EditRootFrameAppearance(CustomSimpleDialog):
    def __init__(self, master, title, bgColor, configStyle):
        self.root = master
        self.bgColor = bgColor
        self.configStyle = configStyle
        self.v_darkModeFlag = None
        self.v_themeName = None
        self.dirtyFlag = False
        self.updateFlag = False
        super().__init__(master, title, bgColor)

    def readStyle(self):
        self.rfStyle.theme_use(self.v_themeName.get())
        self.rfStyle.configure("rootFramaWidget.TRadiobutton", background=self.bgColor, foreground=self.configStyle.radioForegroundColor)
        self.rfStyle.configure("rootFramaWidget.TButton", background=self.bgColor, foreground=self.configStyle.buttonForegroundColor)
        self.rfStyle.configure("rootFramaWidget.TLabel", background=self.bgColor, foreground=self.configStyle.labelForegroundColor)
        self.rfStyle.configure("rootFramaWidget.TFrame", background=self.bgColor, relief="solid")
        self.rfStyle.configure("rootFramaWidget.TSeparator", background=self.bgColor)

        self.rfStyle.map("rootFramaWidget.TCombobox", background=[("readonly", self.bgColor)], foreground=[("readonly", self.configStyle.comboboxForegroundColor)], fieldbackground=[("readonly", self.configStyle.comboboxBackgroundColor)], selectbackground=[("readonly", self.configStyle.comboboxSelectedBackgroundColor)], selectforeground=[("readonly", self.configStyle.comboboxSelectedForegroundColor)])
        self.rfStyle.map("rootFramaWidget.TRadiobutton", indicatorcolor=[("!selected", self.configStyle.indicatorColor), ("selected", self.configStyle.indicatorSelectedColor)])
        self.dialogMaster.option_add("*TCombobox*Listbox.background", self.configStyle.comboboxBackgroundColor)
        self.dialogMaster.option_add("*TCombobox*Listbox.foreground", self.configStyle.comboboxForegroundColor)
        self.dialogMaster.option_add("*TCombobox*Listbox.selectBackground", self.configStyle.comboboxSelectedBackgroundColor)
        self.dialogMaster.option_add("*TCombobox*Listbox.selectForeground", self.configStyle.comboboxSelectedForegroundColor)
        self.rfStyle.configure("rootFramaWidget.style.TFrame", background=self.bgColor)
        self.rfStyle.configure("rootFramaWidget.bgRootFrame.TFrame", background=self.bgColor)
        self.rfStyle.configure("rootFramaWidget.fgLabel.TFrame", background=self.configStyle.labelForegroundColor)
        self.rfStyle.configure("rootFramaWidget.fgLabelframe.TFrame", background=self.configStyle.labelframeLabelForegroundColor)
        self.rfStyle.configure("rootFramaWidget.fgRadio.TFrame", background=self.configStyle.radioForegroundColor)
        self.rfStyle.configure("rootFramaWidget.bgTreeview.TFrame", background=self.configStyle.treeviewBackgroundColor)
        self.rfStyle.configure("rootFramaWidget.fgTreeview.TFrame", background=self.configStyle.treeviewForegroundColor)
        self.rfStyle.configure("rootFramaWidget.bgSelTreeview.TFrame", background=self.configStyle.treeviewSelectedBackgroundColor)
        self.rfStyle.configure("rootFramaWidget.fgSelTreeview.TFrame", background=self.configStyle.treeviewSelectedForegroundColor)
        self.rfStyle.configure("rootFramaWidget.fgButton.TFrame", background=self.configStyle.buttonForegroundColor)
        self.rfStyle.configure("rootFramaWidget.fgEntry.TFrame", background=self.configStyle.entryForegroundColor)
        self.rfStyle.configure("rootFramaWidget.bgTreeviewField.TFrame", background=self.configStyle.treeviewFieldBackgroundColor)
        self.rfStyle.configure("rootFramaWidget.bgTreeviewHeader.TFrame", background=self.configStyle.treeviewHeaderBackgroundColor)
        self.rfStyle.configure("rootFramaWidget.fgTreeviewHeader.TFrame", background=self.configStyle.treeviewHeaderForegroundColor)
        self.rfStyle.configure("rootFramaWidget.bgCombobox.TFrame", background=self.configStyle.comboboxBackgroundColor)
        self.rfStyle.configure("rootFramaWidget.fgCombobox.TFrame", background=self.configStyle.comboboxForegroundColor)
        self.rfStyle.configure("rootFramaWidget.bgSelCombobox.TFrame", background=self.configStyle.comboboxSelectedBackgroundColor)
        self.rfStyle.configure("rootFramaWidget.fgSelCombobox.TFrame", background=self.configStyle.comboboxSelectedForegroundColor)
        self.rfStyle.configure("rootFramaWidget.bgRadiobutton.TFrame", background=self.configStyle.indicatorColor)
        self.rfStyle.configure("rootFramaWidget.bgSelRadiobutton.TFrame", background=self.configStyle.indicatorSelectedColor)

    def body(self, master):
        self.dialogMaster = master
        self.resizable(False, False)

        self.rfStyle = ttk.Style(master)
        self.v_themeName = tkinter.StringVar(value=self.configStyle.themeName)
        self.readStyle()

        darkModeSelectFrame = ttkCustomWidget.CustomTtkFrame(master, style="rootFramaWidget.TFrame")
        darkModeSelectFrame.pack(expand=True, fill=tkinter.BOTH, pady=(4, 0))
        darkModeSelectNameLb = ttkCustomWidget.CustomTtkLabel(darkModeSelectFrame, text=textSetting.textList["appearance"]["rootFrame"]["windowsDialogLabel"], font=textSetting.textList["font2"], anchor=tkinter.W, style="rootFramaWidget.TLabel")
        darkModeSelectNameLb.grid(columnspan=2, row=0, column=0, padx=4, pady=4, sticky=tkinter.EW)
        self.v_darkModeFlag = tkinter.IntVar(value=self.configStyle.rootDarkModeFlag)
        lightModeRadioBtn = ttkCustomWidget.CustomTtkRadiobutton(darkModeSelectFrame, text=textSetting.textList["appearance"]["rootFrame"]["lightModeRadioLabel"], value=0, variable=self.v_darkModeFlag, command=self.setDarkMode, style="rootFramaWidget.TRadiobutton")
        lightModeRadioBtn.grid(row=1, column=0, pady=8)
        darkModeRadioBtn = ttkCustomWidget.CustomTtkRadiobutton(darkModeSelectFrame, text=textSetting.textList["appearance"]["rootFrame"]["darkModeRadioLabel"], value=1, variable=self.v_darkModeFlag, command=self.setDarkMode, style="rootFramaWidget.TRadiobutton")
        darkModeRadioBtn.grid(row=1, column=1, pady=8)

        darkModeSelectFrame.grid_columnconfigure(0, weight=1)
        darkModeSelectFrame.grid_columnconfigure(1, weight=1)

        styleFrame1 = ttkCustomWidget.CustomTtkFrame(master, style="rootFramaWidget.style.TFrame")
        styleFrame1.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=(0, 4), pady=4)
        self.setWidgetColorList(styleFrame1, textSetting.textList["appearance"]["rootFrame"]["rootFrameLabel"], [textSetting.textList["appearance"]["rootFrame"]["tkThemeNameLabel"], textSetting.textList["appearance"]["rootFrame"]["bgColorLabel"]], ["rootTheme", "rootBg"])
        self.setWidgetColorList(styleFrame1, textSetting.textList["appearance"]["rootFrame"]["labelLabel"], [textSetting.textList["appearance"]["rootFrame"]["fgColorLabel"]], ["label"])
        self.setWidgetColorList(styleFrame1, textSetting.textList["appearance"]["rootFrame"]["labelFrameLabel"], [textSetting.textList["appearance"]["rootFrame"]["fgColorLabel"]], ["labelframe"])
        self.setWidgetColorList(styleFrame1, textSetting.textList["appearance"]["rootFrame"]["radiobuttonLabel"], [textSetting.textList["appearance"]["rootFrame"]["fgColorLabel"]], ["radio"])

        styleFrame2 = ttkCustomWidget.CustomTtkFrame(master, style="rootFramaWidget.style.TFrame")
        styleFrame2.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=(8, 4), pady=4)
        self.setWidgetColorList(styleFrame2, textSetting.textList["appearance"]["rootFrame"]["treeviewLabel"], [textSetting.textList["appearance"]["rootFrame"]["bgColorLabel"], textSetting.textList["appearance"]["rootFrame"]["fgColorLabel"], textSetting.textList["appearance"]["rootFrame"]["selectedBgColorLabel"], textSetting.textList["appearance"]["rootFrame"]["selectedFgColorLabel"]], ["treeviewBg", "treeviewFg", "treeviewSelectedBg", "treeviewSelectedFg"])

        styleFrame3 = ttkCustomWidget.CustomTtkFrame(master, style="rootFramaWidget.style.TFrame")
        styleFrame3.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=(16, 0), pady=4)
        self.setWidgetColorList(styleFrame3, textSetting.textList["appearance"]["rootFrame"]["buttonLabel"], [textSetting.textList["appearance"]["rootFrame"]["fgColorLabel"]], ["buttonFg"])
        self.setWidgetColorList(styleFrame3, textSetting.textList["appearance"]["rootFrame"]["entryLabel"], [textSetting.textList["appearance"]["rootFrame"]["fgColorLabel"]], ["entryFg"])
        self.setWidgetColorList(styleFrame3, textSetting.textList["appearance"]["rootFrame"]["treeviewThemeLabel"], [textSetting.textList["appearance"]["rootFrame"]["treeviewFieldBgLabel"], textSetting.textList["appearance"]["rootFrame"]["treeviewHeaderBgLabel"], textSetting.textList["appearance"]["rootFrame"]["treeviewHeaderFgLabel"]], ["treeviewFieldBg", "treeviewHeaderBg", "treeviewHeaderFg"])

        styleFrame4 = ttkCustomWidget.CustomTtkFrame(master, style="rootFramaWidget.style.TFrame")
        styleFrame4.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=(8, 0), pady=4)
        self.setWidgetColorList(styleFrame4, textSetting.textList["appearance"]["rootFrame"]["comboboxLabel"], [textSetting.textList["appearance"]["rootFrame"]["bgColorLabel"], textSetting.textList["appearance"]["rootFrame"]["fgColorLabel"], textSetting.textList["appearance"]["rootFrame"]["selectedBgColorLabel"], textSetting.textList["appearance"]["rootFrame"]["selectedFgColorLabel"]], ["comboboxBg", "comboboxFg", "comboboxSelectedBg", "comboboxSelectedFg"])
        self.setWidgetColorList(styleFrame4, textSetting.textList["appearance"]["rootFrame"]["radioThemeLabel"], [textSetting.textList["appearance"]["rootFrame"]["radioButtonColorLabel"], textSetting.textList["appearance"]["rootFrame"]["radioButtonSelColorLabel"]], ["radioButtonBg", "radioButtonSelBg"])

        super().body(master)

    def buttonbox(self):
        super().buttonbox("rootFramaWidget.TButton")

    def setDarkMode(self):
        self.dirtyFlag = True

    def setWidgetColorList(self, master, title, optionList, previewWidgetNameList):
        widgetFrame = ttkCustomWidget.CustomTtkFrame(master, style="rootFramaWidget.TFrame")
        widgetFrame.pack(fill=tkinter.BOTH, pady=(8, 0), ipadx=8)
        widgetNameLb = ttkCustomWidget.CustomTtkLabel(widgetFrame, text=title, font=textSetting.textList["font2"], anchor=tkinter.W, style="rootFramaWidget.TLabel")
        widgetNameLb.grid(columnspan=3, row=0, column=0, padx=4, pady=4, sticky=tkinter.EW)

        for i in range(len(optionList)):
            widgetColorNameLb = ttkCustomWidget.CustomTtkLabel(widgetFrame, text=optionList[i], font=textSetting.textList["defaultFont"], anchor=tkinter.W, style="rootFramaWidget.TLabel")
            widgetColorNameLb.grid(row=3*i+1, column=0, padx=4, pady=4, sticky=tkinter.NSEW)

            previewWidgetName = previewWidgetNameList[i]
            if previewWidgetName != "rootTheme":
                widgetColorPreviewFrame = ttkCustomWidget.CustomTtkFrame(widgetFrame, width=60, relief="groove")
                widgetColorPreviewFrame.grid(row=3*i+1, column=1, padx=(4, 0), pady=4, sticky=tkinter.NSEW)

                if previewWidgetName == "rootBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgRootFrame.TFrame")
                elif previewWidgetName == "label":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgLabel.TFrame")
                elif previewWidgetName == "radio":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgRadio.TFrame")
                elif previewWidgetName == "labelframe":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgLabelframe.TFrame")
                elif previewWidgetName == "treeviewBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgTreeview.TFrame")
                elif previewWidgetName == "treeviewFg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgTreeview.TFrame")
                elif previewWidgetName == "treeviewSelectedBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgSelTreeview.TFrame")
                elif previewWidgetName == "treeviewSelectedFg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgSelTreeview.TFrame")
                elif previewWidgetName == "buttonFg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgButton.TFrame")
                elif previewWidgetName == "entryFg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgEntry.TFrame")
                elif previewWidgetName == "treeviewFieldBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgTreeviewField.TFrame")
                elif previewWidgetName == "treeviewHeaderBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgTreeviewHeader.TFrame")
                elif previewWidgetName == "treeviewHeaderFg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgTreeviewHeader.TFrame")
                elif previewWidgetName == "comboboxBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgCombobox.TFrame")
                elif previewWidgetName == "comboboxFg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgCombobox.TFrame")
                elif previewWidgetName == "comboboxSelectedBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgSelCombobox.TFrame")
                elif previewWidgetName == "comboboxSelectedFg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.fgSelCombobox.TFrame")
                elif previewWidgetName == "radioButtonBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgRadiobutton.TFrame")
                elif previewWidgetName == "radioButtonSelBg":
                    widgetColorPreviewFrame.configure(style="rootFramaWidget.bgSelRadiobutton.TFrame")

                widgetColorBtn = ttkCustomWidget.CustomTtkButton(widgetFrame, text=textSetting.textList["appearance"]["rootFrame"]["colorEditButtonLabel"], style="rootFramaWidget.TButton")
                widgetColorBtn.grid(row=3*i+1, column=2, padx=4, pady=4, sticky=tkinter.NSEW)
                widgetColorBtn.configure(command=partial(self.setColorChoose, previewWidgetName))

                widgetColorDefaultBtn = ttkCustomWidget.CustomTtkButton(widgetFrame, text=textSetting.textList["appearance"]["rootFrame"]["colorDefaultButtonLabel"], style="rootFramaWidget.TButton")
                widgetColorDefaultBtn.grid(columnspan=3, row=3*i+2, column=0, padx=4, pady=4, sticky=tkinter.NSEW)
                widgetColorDefaultBtn.configure(command=partial(self.setDefaultColor, previewWidgetName))
            else:
                widgetCombobox = ttkCustomWidget.CustomTtkCombobox(widgetFrame, values=self.rfStyle.theme_names(), textvariable=self.v_themeName, state="readonly", style="rootFramaWidget.TCombobox")
                widgetCombobox.grid(columnspan=2, row=3*i+1, column=1, padx=4, pady=4, sticky=tkinter.NSEW)
                widgetCombobox.set(self.rfStyle.theme_use())
                widgetCombobox.bind("<<ComboboxSelected>>", lambda e: self.selectTheme())

            if i < len(optionList)-1:
                separator = ttkCustomWidget.CustomTtkSeparator(widgetFrame, orient="horizontal", style="rootFramaWidget.TSeparator")
                separator.grid(columnspan=3, row=3*i+3, column=0, padx=4, pady=4, sticky=tkinter.EW)

        widgetFrame.grid_columnconfigure(0, weight=1)
        widgetFrame.grid_columnconfigure(1, weight=1)
        widgetFrame.grid_columnconfigure(2, weight=1)

    def selectTheme(self):
        self.dirtyFlag = True

    def setColor(self, color, widgetName):
        if widgetName == "rootBg":
            self.bgColor = color
            self.rfStyle.configure("rootFramaWidget.TRadiobutton", background=self.bgColor)
            self.rfStyle.configure("rootFramaWidget.TButton", background=self.bgColor)
            self.rfStyle.configure("rootFramaWidget.TLabel", background=self.bgColor)
            self.rfStyle.configure("rootFramaWidget.TFrame", background=self.bgColor)
            self.rfStyle.configure("rootFramaWidget.TSeparator", background=self.bgColor)
            self.rfStyle.configure("rootFramaWidget.bgRootFrame.TFrame", background=self.bgColor)
            self.rfStyle.configure("rootFramaWidget.style.TFrame", background=self.bgColor)
            self.rfStyle.map("rootFramaWidget.TCombobox", background=[("readonly", self.bgColor)])

            for child in self.children.values():
                child["bg"] = self.bgColor
            self["bg"] = self.bgColor
        elif widgetName == "label":
            self.configStyle.labelForegroundColor = color
            self.rfStyle.configure("rootFramaWidget.TLabel", foreground=self.configStyle.labelForegroundColor)
            self.rfStyle.configure("rootFramaWidget.fgLabel.TFrame", background=self.configStyle.labelForegroundColor)
        elif widgetName == "radio":
            self.configStyle.radioForegroundColor = color
            self.rfStyle.configure("rootFramaWidget.TRadiobutton", foreground=self.configStyle.radioForegroundColor)
            self.rfStyle.configure("rootFramaWidget.fgRadio.TFrame", background=self.configStyle.radioForegroundColor)
        elif widgetName == "labelframe":
            self.configStyle.labelframeLabelForegroundColor = color
            self.rfStyle.configure("rootFramaWidget.fgLabelframe.TFrame", background=self.configStyle.labelframeLabelForegroundColor)
        elif widgetName == "treeviewBg":
            self.configStyle.treeviewBackgroundColor = color
            self.rfStyle.configure("rootFramaWidget.bgTreeview.TFrame", background=self.configStyle.treeviewBackgroundColor)
        elif widgetName == "treeviewFg":
            self.configStyle.treeviewForegroundColor = color
            self.rfStyle.configure("rootFramaWidget.fgTreeview.TFrame", background=self.configStyle.treeviewForegroundColor)
        elif widgetName == "treeviewSelectedBg":
            self.configStyle.treeviewSelectedBackgroundColor = color
            self.rfStyle.configure("rootFramaWidget.bgSelTreeview.TFrame", background=self.configStyle.treeviewSelectedBackgroundColor)
        elif widgetName == "treeviewSelectedFg":
            self.configStyle.treeviewSelectedForegroundColor = color
            self.rfStyle.configure("rootFramaWidget.fgSelTreeview.TFrame", background=self.configStyle.treeviewSelectedForegroundColor)
        elif widgetName == "buttonFg":
            self.configStyle.buttonForegroundColor = color
            self.rfStyle.configure("rootFramaWidget.TButton", foreground=self.configStyle.buttonForegroundColor)
            self.rfStyle.configure("rootFramaWidget.fgButton.TFrame", background=self.configStyle.buttonForegroundColor)
        elif widgetName == "entryFg":
            self.configStyle.entryForegroundColor = color
            self.rfStyle.configure("rootFramaWidget.fgEntry.TFrame", background=self.configStyle.entryForegroundColor)
        elif widgetName == "treeviewFieldBg":
            self.configStyle.treeviewFieldBackgroundColor = color
            self.rfStyle.configure(style="rootFramaWidget.bgTreeviewField.TFrame", background=self.configStyle.treeviewFieldBackgroundColor)
        elif widgetName == "treeviewHeaderBg":
            self.configStyle.treeviewHeaderBackgroundColor = color
            self.rfStyle.configure(style="rootFramaWidget.bgTreeviewHeader.TFrame", background=self.configStyle.treeviewHeaderBackgroundColor)
        elif widgetName == "treeviewHeaderFg":
            self.configStyle.treeviewHeaderForegroundColor = color
            self.rfStyle.configure(style="rootFramaWidget.fgTreeviewHeader.TFrame", background=self.configStyle.treeviewHeaderForegroundColor)
        elif widgetName == "comboboxBg":
            self.configStyle.comboboxBackgroundColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", fieldbackground=[("readonly", self.configStyle.comboboxBackgroundColor)])
            self.rfStyle.configure("rootFramaWidget.bgCombobox.TFrame", background=self.configStyle.comboboxBackgroundColor)
        elif widgetName == "comboboxFg":
            self.configStyle.comboboxForegroundColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", foreground=[("readonly", self.configStyle.comboboxForegroundColor)])
            self.rfStyle.configure("rootFramaWidget.fgCombobox.TFrame", background=self.configStyle.comboboxForegroundColor)
        elif widgetName == "comboboxSelectedBg":
            self.configStyle.comboboxSelectedBackgroundColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", selectbackground=[("readonly", self.configStyle.comboboxSelectedBackgroundColor)])
            self.rfStyle.configure("rootFramaWidget.bgSelCombobox.TFrame", background=self.configStyle.comboboxSelectedBackgroundColor)
        elif widgetName == "comboboxSelectedFg":
            self.configStyle.comboboxSelectedForegroundColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", selectforeground=[("readonly", self.configStyle.comboboxSelectedForegroundColor)])
            self.rfStyle.configure("rootFramaWidget.fgSelCombobox.TFrame", background=self.configStyle.comboboxSelectedForegroundColor)
        elif widgetName == "radioButtonBg":
            self.configStyle.indicatorColor = color
            self.rfStyle.map("rootFramaWidget.TRadiobutton", indicatorcolor=[("!selected", self.configStyle.indicatorColor), ("selected", self.configStyle.indicatorSelectedColor)])
            self.rfStyle.configure("rootFramaWidget.bgRadiobutton.TFrame", background=self.configStyle.indicatorColor)
        elif widgetName == "radioButtonSelBg":
            self.configStyle.indicatorSelectedColor = color
            self.rfStyle.map("rootFramaWidget.TRadiobutton", indicatorcolor=[("!selected", self.configStyle.indicatorColor), ("selected", self.configStyle.indicatorSelectedColor)])
            self.rfStyle.configure("rootFramaWidget.bgSelRadiobutton.TFrame", background=self.configStyle.indicatorSelectedColor)

    def setColorChoose(self, widgetName):
        if widgetName == "rootBg":
            askcolor = self.bgColor
        elif widgetName == "label":
            askcolor = self.configStyle.labelForegroundColor
        elif widgetName == "radio":
            askcolor = self.configStyle.radioForegroundColor
        elif widgetName == "labelframe":
            askcolor = self.configStyle.labelframeLabelForegroundColor
        elif widgetName == "treeviewBg":
            askcolor = self.configStyle.treeviewBackgroundColor
        elif widgetName == "treeviewFg":
            askcolor = self.configStyle.treeviewForegroundColor
        elif widgetName == "treeviewSelectedBg":
            askcolor = self.configStyle.treeviewSelectedBackgroundColor
        elif widgetName == "treeviewSelectedFg":
            askcolor = self.configStyle.treeviewSelectedForegroundColor
        elif widgetName == "buttonFg":
            askcolor = self.configStyle.buttonForegroundColor
        elif widgetName == "entryFg":
            askcolor = self.configStyle.entryForegroundColor
        elif widgetName == "treeviewFieldBg":
            askcolor = self.configStyle.treeviewFieldBackgroundColor
        elif widgetName == "treeviewHeaderBg":
            askcolor = self.configStyle.treeviewHeaderBackgroundColor
        elif widgetName == "treeviewHeaderFg":
            askcolor = self.configStyle.treeviewHeaderForegroundColor
        elif widgetName == "comboboxBg":
            askcolor = self.configStyle.comboboxBackgroundColor
        elif widgetName == "comboboxFg":
            askcolor = self.configStyle.comboboxForegroundColor
        elif widgetName == "comboboxSelectedBg":
            askcolor = self.configStyle.comboboxSelectedBackgroundColor
        elif widgetName == "comboboxSelectedFg":
            askcolor = self.configStyle.comboboxSelectedForegroundColor
        elif widgetName == "radioButtonBg":
            askcolor = self.configStyle.indicatorColor
        elif widgetName == "radioButtonSelBg":
            askcolor = self.configStyle.indicatorSelectedColor
        result = colorchooser.askcolor(askcolor, parent=self)
        if result is not None:
            if len(result) >= 2 and result[1] is not None:
                self.dirtyFlag = True
                self.setColor(result[1], widgetName)

    def setDefaultColor(self, widgetName):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["appearance"]["rootFrame"]["askColorSetDefault"], parent=self)
        if result:
            self.dirtyFlag = True
            if widgetName == "rootBg" or widgetName == "treeviewHeaderBg":
                self.setColor("SystemButtonFace", widgetName)
            elif widgetName == "treeviewBg" or widgetName == "comboboxBg" or widgetName == "treeviewFieldBg" or widgetName == "radioButtonBg":
                self.setColor("SystemWindow", widgetName)
            elif widgetName == "treeviewSelectedBg" or widgetName == "comboboxSelectedBg":
                self.setColor("SystemHighlight", widgetName)
            elif widgetName == "treeviewSelectedFg" or widgetName == "comboboxSelectedFg":
                self.setColor("SystemWindow", widgetName)
            else:
                self.setColor("SystemWindowText", widgetName)

    def validate(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["appearance"]["updateConfirm"], parent=self)
            if result:
                self.updateFlag = True
                return True
        else:
            return True

    def apply(self):
        return True
