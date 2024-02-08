from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class LensListWidget:
    def __init__(self, frame, decryptFile, trainIdx, lensList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.trainIdx = trainIdx
        self.lensList = lensList
        self.reloadFunc = reloadFunc

        self.lensListLf = ttk.LabelFrame(self.frame, text=textSetting.textList["orgInfoEditor"]["lensInfoLabel"])
        self.lensListLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(self.lensListLf)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)

        self.txtFrame = ttk.Frame(scrollbarFrame.interior)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.lensCntNameLb = tkinter.Label(self.txtFrame, text=textSetting.textList["orgInfoEditor"]["lensCntLabel"], font=textSetting.textList["font6"], width=12, borderwidth=1, relief="solid")
        self.lensCntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varLensCnt = tkinter.IntVar()
        self.varLensCnt.set(len(self.lensList))
        self.lensCntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varLensCnt, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.lensCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.lensCntBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editLensCnt(self.varLensCnt.get()))
        self.lensCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.lensList)):
            self.txtFrame2 = ttk.Frame(scrollbarFrame.interior)
            self.txtFrame2.pack(anchor=tkinter.NW, pady=5)

            self.btnFrame = ttk.Frame(self.txtFrame2)
            self.btnFrame.pack(side=tkinter.LEFT, anchor=tkinter.NW)
            self.nameFrame = ttk.Frame(self.txtFrame2)
            self.nameFrame.pack(anchor=tkinter.NW)
            self.eleFrame = ttk.Frame(self.txtFrame2)
            self.eleFrame.pack(anchor=tkinter.NW)

            lensInfo = self.lensList[i]

            for j in range(len(lensInfo)):
                self.tempBtn = tkinter.Button(self.btnFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=partial(self.editLensList, i, lensInfo))
                self.tempBtn.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.nameLb = tkinter.Label(self.nameFrame, text=textSetting.textList["orgInfoEditor"]["lensNameLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
                self.nameLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)

                self.f1Lb = tkinter.Label(self.eleFrame, text=textSetting.textList["orgInfoEditor"]["lensF1Label"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
                self.f1Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.b1Lb = tkinter.Label(self.eleFrame, text=textSetting.textList["orgInfoEditor"]["lensB1Label"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
                self.b1Lb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)

                if j in [0, 1]:
                    self.varTemp = tkinter.StringVar()
                    self.varTemp.set(lensInfo[j])
                    self.temphTextLb = tkinter.Label(self.nameFrame, textvariable=self.varTemp, font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i, column=j + 1, sticky=tkinter.W + tkinter.E, ipadx=10)
                elif j in [2, 3]:
                    self.varTempF = tkinter.DoubleVar()
                    self.varTempF.set(round(float(lensInfo[j]), 3))
                    self.temphTextLb = tkinter.Label(self.eleFrame, textvariable=self.varTempF, width=7, font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i, column=j - 1, sticky=tkinter.W + tkinter.E)
                elif j == 4:
                    for k in range(len(lensInfo[j])):
                        self.varTemp = tkinter.IntVar()
                        self.varTemp.set(int(lensInfo[j][k]))
                        self.temphTextLb = tkinter.Label(self.eleFrame, textvariable=self.varTemp, width=7, font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                        self.temphTextLb.grid(row=i + 1, column=k + 1, sticky=tkinter.W + tkinter.E)

    def editLensCnt(self, val):
        result = EditLensCntWidget(self.frame, textSetting.textList["orgInfoEditor"]["lensEditCntLabel"], self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveLensCnt(self.trainIdx, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I65"])
            self.reloadFunc()

    def editLensList(self, i, valList):
        result = EditLensWidget(self.frame, textSetting.textList["orgInfoEditor"]["lensEditLabel"], self.decryptFile, valList)
        if result.reloadFlag:
            self.lensList[i] = result.resultValueList
            if not self.decryptFile.saveLensList(self.trainIdx, self.lensList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I66"])
            self.reloadFunc()


class EditLensCntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditLensCntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.pack()

        self.varLensCnt = tkinter.IntVar()
        self.varLensCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varLensCnt, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varLensCnt.get())
                    if res <= 0:
                        errorMsg = textSetting.textList["errorList"]["E61"].format(1)
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
                    self.resultValue = res
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E60"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)

            if self.resultValue < self.val:
                msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
                result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True


class EditLensWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, lensInfo):
        self.decryptFile = decryptFile
        self.lensInfo = lensInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditLensWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        lensInfoLbList = textSetting.textList["orgInfoEditor"]["lensInfoLabelList"]
        for i in range(len(self.lensInfo)):
            if i in [0, 1]:
                self.lensLb = ttk.Label(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
                self.lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varTemp = tkinter.StringVar()
                self.varTemp.set(self.lensInfo[i])
                self.varList.append(self.varTemp)
                self.lensEt = ttk.Entry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
                self.lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
            elif i in [2, 3]:
                self.lensLb = ttk.Label(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
                self.lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varTemp = tkinter.DoubleVar()
                self.varTemp.set(round(float(self.lensInfo[i]), 3))
                self.varList.append(self.varTemp)
                self.lensEt = ttk.Entry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
                self.lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
            elif i == 4:
                varList = []
                for j in range(len(self.lensInfo[i])):
                    self.lensLb = ttk.Label(master, text=lensInfoLbList[i + j], font=textSetting.textList["font2"])
                    self.lensLb.grid(row=i + j, column=0, sticky=tkinter.W + tkinter.E)
                    self.varTemp = tkinter.IntVar()
                    self.varTemp.set(self.lensInfo[i][j])
                    varList.append(self.varTemp)
                    self.lensEt = ttk.Entry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
                    self.lensEt.grid(row=i + j, column=1, sticky=tkinter.W + tkinter.E)
                self.varList.append(varList)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i in [0, 1]:
                            res = self.varList[i].get()
                        elif i in [2, 3]:
                            res = float(self.varList[i].get())
                        elif i == 4:
                            res = []
                            varList = self.varList[i]
                            for j in range(len(varList)):
                                var = int(varList[j].get())
                                res.append(var)
                        self.resultValueList.append(res)
                    return True
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E3"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)

    def apply(self):
        self.reloadFlag = True
