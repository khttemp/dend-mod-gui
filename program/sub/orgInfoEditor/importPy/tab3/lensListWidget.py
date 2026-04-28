from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class LensListWidget:
    def __init__(self, frame, decryptFile, trainIdx, lensList, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.trainIdx = trainIdx
        self.lensList = lensList
        self.reloadFunc = reloadFunc
        self.rootFrameAppearance = rootFrameAppearance

        lensListLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["orgInfoEditor"]["lensInfoLabel"])
        lensListLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)
        scrollbarFrame = ScrollbarFrame(lensListLf, bgColor=rootFrameAppearance.bgColor)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)

        txtFrame = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame.pack(anchor=tkinter.NW, padx=10)

        lensCntNameLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["orgInfoEditor"]["lensCntLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=12, borderwidth=1, relief="solid")
        lensCntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varLensCnt = tkinter.IntVar()
        self.varLensCnt.set(len(self.lensList))
        lensCntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varLensCnt, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        lensCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        lensCntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editLensCnt(self.varLensCnt.get()))
        lensCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.varList = []
        varCnt = 0
        for i in range(len(self.lensList)):
            txtFrame2 = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
            txtFrame2.pack(anchor=tkinter.NW, padx=10, pady=5)

            btnFrame = ttkCustomWidget.CustomTtkFrame(txtFrame2)
            btnFrame.pack(side=tkinter.LEFT, anchor=tkinter.NW)
            nameFrame = ttkCustomWidget.CustomTtkFrame(txtFrame2)
            nameFrame.pack(anchor=tkinter.NW)
            eleFrame = ttkCustomWidget.CustomTtkFrame(txtFrame2)
            eleFrame.pack(anchor=tkinter.NW)

            lensInfo = self.lensList[i]
            for j in range(len(lensInfo)):
                tempBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editLensList, i, lensInfo))
                tempBtn.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                nameLb = ttkCustomWidget.CustomTtkLabel(nameFrame, text=textSetting.textList["orgInfoEditor"]["lensNameLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                nameLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)

                f1Lb = ttkCustomWidget.CustomTtkLabel(eleFrame, text=textSetting.textList["orgInfoEditor"]["lensF1Label"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                f1Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                b1Lb = ttkCustomWidget.CustomTtkLabel(eleFrame, text=textSetting.textList["orgInfoEditor"]["lensB1Label"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                b1Lb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)

                if j in [0, 1]:
                    self.varList.append(tkinter.StringVar(value=lensInfo[j]))
                    temphTextLb = ttkCustomWidget.CustomTtkLabel(nameFrame, textvariable=self.varList[varCnt], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                    temphTextLb.grid(row=i, column=j + 1, sticky=tkinter.W + tkinter.E, ipadx=10)
                    varCnt += 1
                elif j in [2, 3]:
                    self.varList.append(tkinter.DoubleVar(value=round(float(lensInfo[j]), 3)))
                    temphTextLb = ttkCustomWidget.CustomTtkLabel(eleFrame, textvariable=self.varList[varCnt], width=7, font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                    temphTextLb.grid(row=i, column=j - 1, sticky=tkinter.W + tkinter.E)
                    varCnt += 1
                elif j == 4:
                    for k in range(len(lensInfo[j])):
                        self.varList.append(tkinter.IntVar(value=int(lensInfo[j][k])))
                        temphTextLb = ttkCustomWidget.CustomTtkLabel(eleFrame, textvariable=self.varList[varCnt], width=7, font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                        temphTextLb.grid(row=i + 1, column=k + 1, sticky=tkinter.W + tkinter.E)
                        varCnt += 1

    def editLensCnt(self, val):
        result = EditLensCntWidget(self.frame, textSetting.textList["orgInfoEditor"]["lensEditCntLabel"], self.decryptFile, val, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveLensCnt(self.trainIdx, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I65"])
            self.reloadFunc()

    def editLensList(self, i, valList):
        result = EditLensWidget(self.frame, textSetting.textList["orgInfoEditor"]["lensEditLabel"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.lensList[i] = result.resultValueList
            if not self.decryptFile.saveLensList(self.trainIdx, self.lensList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I66"])
            self.reloadFunc()


class EditLensCntWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, val, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
        self.valLb.pack()

        self.varLensCnt = tkinter.IntVar()
        self.varLensCnt.set(self.val)
        self.valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varLensCnt, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()
        super().body(master)

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


class EditLensWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, lensInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.lensInfo = lensInfo
        self.varList = []
        self.varCnt = 0
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        lensInfoLbList = textSetting.textList["orgInfoEditor"]["lensInfoLabelList"]
        for i in range(len(self.lensInfo)):
            if i in [0, 1]:
                self.lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
                self.lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.StringVar(value=self.lensInfo[i]))
                self.lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                self.lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
            elif i in [2, 3]:
                self.lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
                self.lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.DoubleVar(value=round(float(self.lensInfo[i]), 3)))
                self.lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                self.lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
            elif i == 4:
                varList = []
                for j in range(len(self.lensInfo[i])):
                    self.lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i + j], font=textSetting.textList["font2"])
                    self.lensLb.grid(row=i + j, column=0, sticky=tkinter.W + tkinter.E)
                    varList.append(tkinter.IntVar(value=self.lensInfo[i][j]))
                    self.lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=varList[j], font=textSetting.textList["font2"])
                    self.lensEt.grid(row=i + j, column=1, sticky=tkinter.W + tkinter.E)
                    self.varCnt += 1
                self.varList.append(varList)
        super().body(master)

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
