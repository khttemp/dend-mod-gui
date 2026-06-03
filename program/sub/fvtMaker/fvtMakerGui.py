import copy
import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame
from program.sub.fvtMaker.importPy.tableWidget import CsvWidget, DescWidget
from program.sub.fvtMaker.importPy.fvtConvert import FvtConvert

import program.sub.fvtMaker.fvtMakerProcess as fvtMakerProcess


class FvtMakerWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict, rootFrameAppearance):
        super().__init__(master)
        self.importDict = importDict
        self.rootFrameAppearance = rootFrameAppearance
        self.fvtConvertFile = None
        self.LS = 1
        self.BS = 2
        self.CS = 3
        self.RS = 4

        headerFrame = ttkCustomWidget.CustomTtkFrame(master)
        headerFrame.pack(fill=tkinter.X, padx=40, pady=25)

        self.v_radio = tkinter.IntVar()
        self.v_radio.set(-1)

        lsRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Lightning Stage", command=self.radioButtonTrigger, variable=self.v_radio, value=self.LS)
        lsRb.grid(row=0, column=0, padx=10)

        bsRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Burning Stage", command=self.radioButtonTrigger, variable=self.v_radio, value=self.BS)
        bsRb.grid(row=0, column=1, padx=10)

        csRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Climax Stage", command=self.radioButtonTrigger, variable=self.v_radio, value=self.CS)
        csRb.grid(row=0, column=2, padx=10)

        rsRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Rising Stage", command=self.radioButtonTrigger, variable=self.v_radio, value=self.RS)
        rsRb.grid(row=0, column=3, padx=10)

        headerFrame.grid_columnconfigure(0, weight=1)
        headerFrame.grid_columnconfigure(1, weight=1)
        headerFrame.grid_columnconfigure(2, weight=1)
        headerFrame.grid_columnconfigure(3, weight=1)

        bodyFrame = ttkCustomWidget.CustomTtkFrame(master)
        bodyFrame.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))

        self.csvLf = ttkCustomWidget.CustomTtkLabelFrame(bodyFrame, text=textSetting.textList["fvtMaker"]["csvLfLabel"])
        self.csvLf.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.descLf = ttkCustomWidget.CustomTtkLabelFrame(bodyFrame, text=textSetting.textList["fvtMaker"]["howWrite"])
        self.descLf.grid(row=1, column=0, sticky=tkinter.NSEW)

        bodyFrame.grid_rowconfigure(0, weight=3)
        bodyFrame.grid_rowconfigure(1, weight=7)
        bodyFrame.grid_columnconfigure(0, weight=1)

    def radioButtonTrigger(self):
        self.deleteWidget()
        self.createWidget()

    def deleteWidget(self):
        children = self.csvLf.winfo_children()
        for child in children:
            child.destroy()

        children = self.descLf.winfo_children()
        for child in children:
            child.destroy()

    def createWidget(self):
        game = self.v_radio.get()
        if game == self.LS:
            fvtInfo = self.importDict["fvtInfo"]["LS"]
        elif game == self.BS:
            fvtInfo = self.importDict["fvtInfo"]["BS"]
        elif game == self.CS:
            fvtInfo = self.importDict["fvtInfo"]["CS"]
        else:
            fvtInfo = self.importDict["fvtInfo"]["RS"]

        headerList, dataList = fvtMakerProcess.getCsvInfo(game, copy.deepcopy(fvtInfo))

        frame = ScrollbarFrame(self.csvLf, True, bgColor=self.rootFrameAppearance.bgColor)
        frame.pack(expand=True, fill=tkinter.BOTH)
        csvWidget = CsvWidget(frame.interior, headerList, dataList)
        csvWidget.pack()

        frame2 = ScrollbarFrame(self.descLf, True, bgColor=self.rootFrameAppearance.bgColor)
        frame2.pack(expand=True, fill=tkinter.BOTH)
        descWidget = DescWidget(frame2.interior, self.importDict["fvtImageInfo"], game, self.rootFrameAppearance)
        descWidget.pack()

    def openFile(self):
        game = self.v_radio.get()
        if game == -1:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E13"])
            return

        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["fvtMaker"]["fileType"], "*.csv")])
        if not file_path:
            return

        del self.fvtConvertFile
        self.fvtConvertFile = FvtConvert(file_path, game)
        if not self.fvtConvertFile.open():
            self.fvtConvertFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E124"])
            return

        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I13"], icon="warning")
        if result:
            if not self.fvtConvertFile.write():
                self.fvtConvertFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I14"])
