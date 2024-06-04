from functools import partial
import codecs
import configparser
import tkinter
from tkinter import ttk
from tkinter import colorchooser
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class RootFrameAppearance:
    def __init__(self, root, iniPath, labelFgColor, bgColor, readColorConfigRead):
        self.root = root
        self.iniPath = iniPath
        self.fgColor = labelFgColor
        self.bgColor = bgColor
        self.readColorConfigRead = readColorConfigRead
        self.reloadFlag = False

    def editRootFrameAppearance(self):
        self.reloadFlag = False
        result = EditRootFrameAppearance(self.root, textSetting.textList["appearance"]["rootFrame"]["editRootFrameTitle"], self.bgColor, self.readColorConfigRead)
        if result.dirtyFlag and result.updateFlag:
            self.reloadFlag = True
            self.bgColor = result.bgColor
            self.labelFgColor = result.labelFgColor
            self.radioFgColor = result.radioFgColor
            self.labelframeFgColor = result.labelframeFgColor
            self.treeviewBgColor = result.treeviewBgColor
            self.treeviewFgColor = result.treeviewFgColor
            self.treeviewSelBgColor = result.treeviewSelBgColor
            self.treeviewSelFgColor = result.treeviewSelFgColor
            self.darkModeFlag = int(result.v_darkModeFlag.get())
            self.themeName = result.v_themeName.get()
            self.buttonFgColor = result.buttonFgColor
            self.entryFgColor = result.entryFgColor
            self.treeviewFieldBgColor = result.treeviewFieldBgColor
            self.treeviewHeaderBgColor = result.treeviewHeaderBgColor
            self.treeviewHeaderFgColor = result.treeviewHeaderFgColor
            self.comboboxBgColor = result.comboboxBgColor
            self.comboboxFgColor = result.comboboxFgColor
            self.comboboxSelBgColor = result.comboboxSelBgColor
            self.comboboxSelFgColor = result.comboboxSelFgColor
            self.indicatorColor = result.indicatorColor
            self.indicatorSelColor = result.indicatorSelColor

            try:
                configRead = configparser.ConfigParser()
                configRead.read(self.iniPath, encoding="utf-8")

                configRead.set("ROOT_FRAME", "bg_color", self.bgColor)
                configRead.set("ROOT_FRAME", "dark_mode", str(self.darkModeFlag))
                configRead.set("ROOT_FRAME", "theme", self.themeName)
                configRead.set("LABEL", "fg_color", self.labelFgColor)
                configRead.set("LABELFRAME_LABEL", "fg_color", self.labelframeFgColor)
                configRead.set("RADIO", "fg_color", self.labelFgColor)
                configRead.set("TREEVIEW", "bg_color", self.treeviewBgColor)
                configRead.set("TREEVIEW", "fg_color", self.treeviewFgColor)
                configRead.set("TREEVIEW", "sel_bg_color", self.treeviewSelBgColor)
                configRead.set("TREEVIEW", "sel_fg_color", self.treeviewSelFgColor)
                configRead.set("BUTTON", "fg_color", self.buttonFgColor)
                configRead.set("ENTRY", "fg_color", self.entryFgColor)
                configRead.set("TREEVIEW", "field_bg_color", self.treeviewFieldBgColor)
                configRead.set("TREEVIEW_HEADER", "bg_color", self.treeviewHeaderBgColor)
                configRead.set("TREEVIEW_HEADER", "fg_color", self.treeviewHeaderFgColor)
                configRead.set("COMBOBOX", "bg_color", self.comboboxBgColor)
                configRead.set("COMBOBOX", "fg_color", self.comboboxFgColor)
                configRead.set("COMBOBOX", "sel_bg_color", self.comboboxSelBgColor)
                configRead.set("COMBOBOX", "sel_fg_color", self.comboboxSelFgColor)
                configRead.set("COMBOBOX", "indicator_color", self.indicatorColor)
                configRead.set("COMBOBOX", "sel_indicator_color", self.indicatorSelColor)

                f = codecs.open(self.iniPath, "w", "utf-8", "strict")
                configRead.write(f)
                f.close()

                self.readColorConfigRead = configRead
            except PermissionError:
                pass


class EditRootFrameAppearance(CustomSimpleDialog):
    def __init__(self, master, title, bgColor, readColorConfigRead):
        self.root = master
        self.readColorConfigRead = readColorConfigRead
        self.v_darkModeFlag = None
        self.v_themeName = None
        self.selectColorFlag = False
        self.dirtyFlag = False
        self.updateFlag = False
        super().__init__(master, title, bgColor)

    def body(self, master):
        self.dialogMaster = master
        self.resizable(False, False)

        self.themeName = self.readColorConfigRead.get("ROOT_FRAME", "theme")
        self.darkModeFlag = int(self.readColorConfigRead.get("ROOT_FRAME", "dark_mode"))
        self.labelFgColor = self.readColorConfigRead.get("LABEL", "fg_color")
        self.labelframeFgColor = self.readColorConfigRead.get("LABELFRAME_LABEL", "fg_color")
        self.radioFgColor = self.readColorConfigRead.get("RADIO", "fg_color")
        self.treeviewBgColor = self.readColorConfigRead.get("TREEVIEW", "bg_color")
        self.treeviewFgColor = self.readColorConfigRead.get("TREEVIEW", "fg_color")
        self.treeviewSelBgColor = self.readColorConfigRead.get("TREEVIEW", "sel_bg_color")
        self.treeviewSelFgColor = self.readColorConfigRead.get("TREEVIEW", "sel_fg_color")
        self.buttonFgColor = self.readColorConfigRead.get("BUTTON", "fg_color")
        self.entryFgColor = self.readColorConfigRead.get("ENTRY", "fg_color")
        self.treeviewFieldBgColor = self.readColorConfigRead.get("TREEVIEW", "field_bg_color")
        self.treeviewHeaderBgColor = self.readColorConfigRead.get("TREEVIEW_HEADER", "bg_color")
        self.treeviewHeaderFgColor = self.readColorConfigRead.get("TREEVIEW_HEADER", "fg_color")
        self.comboboxBgColor = self.readColorConfigRead.get("COMBOBOX", "bg_color")
        self.comboboxFgColor = self.readColorConfigRead.get("COMBOBOX", "fg_color")
        self.comboboxSelBgColor = self.readColorConfigRead.get("COMBOBOX", "sel_bg_color")
        self.comboboxSelFgColor = self.readColorConfigRead.get("COMBOBOX", "sel_fg_color")
        self.indicatorColor = self.readColorConfigRead.get("RADIO", "indicator_color")
        self.indicatorSelColor = self.readColorConfigRead.get("RADIO", "sel_indicator_color")

        self.rfStyle = ttk.Style(master)
        self.v_themeName = tkinter.StringVar(value=self.themeName)
        self.readStyle()

        darkModeSelectFrame = ttkCustomWidget.CustomTtkFrame(master, style="rootFramaWidget.TFrame")
        darkModeSelectFrame.pack(expand=True, fill=tkinter.BOTH, pady=(4, 0))
        darkModeSelectNameLb = ttkCustomWidget.CustomTtkLabel(darkModeSelectFrame, text=textSetting.textList["appearance"]["rootFrame"]["windowsDialogLabel"], font=textSetting.textList["font2"], anchor=tkinter.W, style="rootFramaWidget.TLabel")
        darkModeSelectNameLb.grid(columnspan=2, row=0, column=0, padx=4, pady=4, sticky=tkinter.EW)
        self.v_darkModeFlag = tkinter.IntVar(value=self.darkModeFlag)
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

    def readStyle(self):
        self.rfStyle.theme_use(self.v_themeName.get())
        self.rfStyle.configure("rootFramaWidget.TRadiobutton", background=self.bgColor, foreground=self.radioFgColor)
        self.rfStyle.configure("rootFramaWidget.TButton", background=self.bgColor, foreground=self.buttonFgColor)
        self.rfStyle.configure("rootFramaWidget.TLabel", background=self.bgColor, foreground=self.labelFgColor)
        self.rfStyle.configure("rootFramaWidget.TFrame", background=self.bgColor, relief="solid")
        self.rfStyle.configure("rootFramaWidget.TSeparator", background=self.bgColor)

        self.rfStyle.map("rootFramaWidget.TCombobox", background=[("readonly", self.bgColor)], foreground=[("readonly", self.comboboxFgColor)], fieldbackground=[("readonly", self.comboboxBgColor)], selectbackground=[("readonly", self.comboboxSelBgColor)], selectforeground=[("readonly", self.comboboxSelFgColor)])
        self.rfStyle.map("rootFramaWidget.TRadiobutton", indicatorcolor=[("!selected", self.indicatorColor), ("selected", self.indicatorSelColor)])
        self.dialogMaster.option_add("*TCombobox*Listbox.background", self.comboboxBgColor)
        self.dialogMaster.option_add("*TCombobox*Listbox.foreground", self.comboboxFgColor)
        self.dialogMaster.option_add("*TCombobox*Listbox.selectBackground", self.comboboxSelBgColor)
        self.dialogMaster.option_add("*TCombobox*Listbox.selectForeground", self.comboboxSelFgColor)
        self.rfStyle.configure("rootFramaWidget.style.TFrame", background=self.bgColor)
        self.rfStyle.configure("rootFramaWidget.bgRootFrame.TFrame", background=self.bgColor)
        self.rfStyle.configure("rootFramaWidget.fgLabel.TFrame", background=self.labelFgColor)
        self.rfStyle.configure("rootFramaWidget.fgLabelframe.TFrame", background=self.labelframeFgColor)
        self.rfStyle.configure("rootFramaWidget.fgRadio.TFrame", background=self.radioFgColor)
        self.rfStyle.configure("rootFramaWidget.bgTreeview.TFrame", background=self.treeviewBgColor)
        self.rfStyle.configure("rootFramaWidget.fgTreeview.TFrame", background=self.treeviewFgColor)
        self.rfStyle.configure("rootFramaWidget.bgSelTreeview.TFrame", background=self.treeviewSelBgColor)
        self.rfStyle.configure("rootFramaWidget.fgSelTreeview.TFrame", background=self.treeviewSelFgColor)
        self.rfStyle.configure("rootFramaWidget.fgButton.TFrame", background=self.buttonFgColor)
        self.rfStyle.configure("rootFramaWidget.fgEntry.TFrame", background=self.entryFgColor)
        self.rfStyle.configure("rootFramaWidget.bgTreeviewField.TFrame", background=self.treeviewFieldBgColor)
        self.rfStyle.configure("rootFramaWidget.bgTreeviewHeader.TFrame", background=self.treeviewHeaderBgColor)
        self.rfStyle.configure("rootFramaWidget.fgTreeviewHeader.TFrame", background=self.treeviewHeaderFgColor)
        self.rfStyle.configure("rootFramaWidget.bgCombobox.TFrame", background=self.comboboxBgColor)
        self.rfStyle.configure("rootFramaWidget.fgCombobox.TFrame", background=self.comboboxFgColor)
        self.rfStyle.configure("rootFramaWidget.bgSelCombobox.TFrame", background=self.comboboxSelBgColor)
        self.rfStyle.configure("rootFramaWidget.fgSelCombobox.TFrame", background=self.comboboxSelFgColor)
        self.rfStyle.configure("rootFramaWidget.bgRadiobutton.TFrame", background=self.indicatorColor)
        self.rfStyle.configure("rootFramaWidget.bgSelRadiobutton.TFrame", background=self.indicatorSelColor)

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
            self.labelFgColor = color
            self.rfStyle.configure("rootFramaWidget.TLabel", foreground=self.labelFgColor)
            self.rfStyle.configure("rootFramaWidget.fgLabel.TFrame", background=self.labelFgColor)
        elif widgetName == "radio":
            self.radioFgColor = color
            self.rfStyle.configure("rootFramaWidget.TRadiobutton", foreground=self.radioFgColor)
            self.rfStyle.configure("rootFramaWidget.fgRadio.TFrame", background=self.radioFgColor)
        elif widgetName == "labelframe":
            self.labelframeFgColor = color
            self.rfStyle.configure("rootFramaWidget.fgLabelframe.TFrame", background=self.labelframeFgColor)
        elif widgetName == "treeviewBg":
            self.treeviewBgColor = color
            self.rfStyle.configure("rootFramaWidget.bgTreeview.TFrame", background=self.treeviewBgColor)
        elif widgetName == "treeviewFg":
            self.treeviewFgColor = color
            self.rfStyle.configure("rootFramaWidget.fgTreeview.TFrame", background=self.treeviewFgColor)
        elif widgetName == "treeviewSelectedBg":
            self.treeviewSelBgColor = color
            self.rfStyle.configure("rootFramaWidget.bgSelTreeview.TFrame", background=self.treeviewSelBgColor)
        elif widgetName == "treeviewSelectedFg":
            self.treeviewSelFgColor = color
            self.rfStyle.configure("rootFramaWidget.fgSelTreeview.TFrame", background=self.treeviewSelFgColor)
        elif widgetName == "buttonFg":
            self.buttonFgColor = color
            self.rfStyle.configure("rootFramaWidget.TButton", foreground=self.buttonFgColor)
            self.rfStyle.configure("rootFramaWidget.fgButton.TFrame", background=self.buttonFgColor)
        elif widgetName == "entryFg":
            self.entryFgColor = color
            self.rfStyle.configure("rootFramaWidget.fgEntry.TFrame", background=self.entryFgColor)
        elif widgetName == "treeviewFieldBg":
            self.treeviewFieldBgColor = color
            self.rfStyle.configure(style="rootFramaWidget.bgTreeviewField.TFrame", background=self.treeviewFieldBgColor)
        elif widgetName == "treeviewHeaderBg":
            self.treeviewHeaderBgColor = color
            self.rfStyle.configure(style="rootFramaWidget.bgTreeviewHeader.TFrame", background=self.treeviewHeaderBgColor)
        elif widgetName == "treeviewHeaderFg":
            self.treeviewHeaderFgColor = color
            self.rfStyle.configure(style="rootFramaWidget.fgTreeviewHeader.TFrame", background=self.treeviewHeaderFgColor)
        elif widgetName == "comboboxBg":
            self.comboboxBgColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", fieldbackground=[("readonly", self.comboboxBgColor)])
            self.rfStyle.configure("rootFramaWidget.bgCombobox.TFrame", background=self.comboboxBgColor)
        elif widgetName == "comboboxFg":
            self.comboboxFgColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", foreground=[("readonly", self.comboboxFgColor)])
            self.rfStyle.configure("rootFramaWidget.fgCombobox.TFrame", background=self.comboboxFgColor)
        elif widgetName == "comboboxSelectedBg":
            self.comboboxSelBgColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", selectbackground=[("readonly", self.comboboxSelBgColor)])
            self.rfStyle.configure("rootFramaWidget.bgSelCombobox.TFrame", background=self.comboboxSelBgColor)
        elif widgetName == "comboboxSelectedFg":
            self.comboboxSelFgColor = color
            self.rfStyle.map("rootFramaWidget.TCombobox", selectforeground=[("readonly", self.comboboxSelFgColor)])
            self.rfStyle.configure("rootFramaWidget.fgSelCombobox.TFrame", background=self.comboboxSelFgColor)
        elif widgetName == "radioButtonBg":
            self.indicatorColor = color
            self.rfStyle.map("rootFramaWidget.TRadiobutton", indicatorcolor=[("!selected", self.indicatorColor), ("selected", self.indicatorSelColor)])
            self.rfStyle.configure("rootFramaWidget.bgRadiobutton.TFrame", background=self.indicatorColor)
        elif widgetName == "radioButtonSelBg":
            self.indicatorSelColor = color
            self.rfStyle.map("rootFramaWidget.TRadiobutton", indicatorcolor=[("!selected", self.indicatorColor), ("selected", self.indicatorSelColor)])
            self.rfStyle.configure("rootFramaWidget.bgSelRadiobutton.TFrame", background=self.indicatorSelColor)

    def setColorChoose(self, widgetName):
        if widgetName == "rootBg":
            askcolor = self.bgColor
        elif widgetName == "label":
            askcolor = self.labelFgColor
        elif widgetName == "radio":
            askcolor = self.radioFgColor
        elif widgetName == "labelframe":
            askcolor = self.labelframeFgColor
        elif widgetName == "treeviewBg":
            askcolor = self.treeviewBgColor
        elif widgetName == "treeviewFg":
            askcolor = self.treeviewFgColor
        elif widgetName == "treeviewSelectedBg":
            askcolor = self.treeviewSelBgColor
        elif widgetName == "treeviewSelectedFg":
            askcolor = self.treeviewSelFgColor
        elif widgetName == "buttonFg":
            askcolor = self.buttonFgColor
        elif widgetName == "entryFg":
            askcolor = self.entryFgColor
        elif widgetName == "treeviewFieldBg":
            askcolor = self.treeviewFieldBgColor
        elif widgetName == "treeviewHeaderBg":
            askcolor = self.treeviewHeaderBgColor
        elif widgetName == "treeviewHeaderFg":
            askcolor = self.treeviewHeaderFgColor
        elif widgetName == "comboboxBg":
            askcolor = self.comboboxBgColor
        elif widgetName == "comboboxFg":
            askcolor = self.comboboxFgColor
        elif widgetName == "comboboxSelectedBg":
            askcolor = self.comboboxSelBgColor
        elif widgetName == "comboboxSelectedFg":
            askcolor = self.comboboxSelFgColor
        elif widgetName == "radioButtonBg":
            askcolor = self.indicatorColor
        elif widgetName == "radioButtonSelBg":
            askcolor = self.indicatorSelColor
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
