from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class TailListWidget:
    def __init__(self, frame, decryptFile, trainIdx, tailList, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.trainIdx = trainIdx
        self.tailSmfList = tailList[0]
        self.tailElseList = tailList[1]
        self.lensList = tailList[2]
        self.reloadFunc = reloadFunc
        self.rootFrameAppearance = rootFrameAppearance

        tailListLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["orgInfoEditor"]["tailInfoLabel"])
        tailListLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)
        scrollbarFrame = ScrollbarFrame(tailListLf, False, bgColor=self.rootFrameAppearance.bgColor)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)
        txtFrame = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame.pack(anchor=tkinter.NW, padx=10)

        tailCntNameLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["orgInfoEditor"]["tailCntLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=12, borderwidth=1, relief="solid")
        tailCntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varTailCnt = tkinter.IntVar()
        self.varTailCnt.set(len(self.tailSmfList))
        tailCntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varTailCnt, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        tailCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        tailCntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editTailCnt(self.varTailCnt.get()))
        tailCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        txtFrame1 = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame1.pack(anchor=tkinter.NW, padx=10, pady=5)

        btnFrame = ttkCustomWidget.CustomTtkFrame(txtFrame1)
        btnFrame.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        smfFrame = ttkCustomWidget.CustomTtkFrame(txtFrame1)
        smfFrame.pack(anchor=tkinter.NW)
        elseFrame = ttkCustomWidget.CustomTtkFrame(txtFrame1)
        elseFrame.pack(anchor=tkinter.NW)

        smfElseBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editTailSmfElse(self.tailSmfList, self.tailElseList))
        smfElseBtn.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        tailSmfNameLb = ttkCustomWidget.CustomTtkLabel(smfFrame, text=textSetting.textList["orgInfoEditor"]["tailNameLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        tailSmfNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.tailSmfVarList = []
        for i in range(len(self.tailSmfList)):
            self.tailSmfVarList.append(tkinter.StringVar(value=self.tailSmfList[i]))
            tempTextLb = ttkCustomWidget.CustomTtkLabel(smfFrame, textvariable=self.tailSmfVarList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            tempTextLb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E, ipadx=10)

        tailElseLb = ttkCustomWidget.CustomTtkLabel(elseFrame, text=textSetting.textList["orgInfoEditor"]["tailElseLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        tailElseLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.tailElseVarList = []
        for i in range(len(self.tailElseList)):
            self.tailElseVarList.append(tkinter.IntVar(value=self.tailElseList[i]))
            tempTextLb = ttkCustomWidget.CustomTtkLabel(elseFrame, textvariable=self.tailElseVarList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            tempTextLb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        self.lensVarList = []
        self.lensVarCnt = 0
        for i in range(len(self.lensList)):
            txtFrame2 = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
            txtFrame2.pack(anchor=tkinter.NW, padx=10, pady=5)

            btnFrame2 = ttkCustomWidget.CustomTtkFrame(txtFrame2)
            btnFrame2.pack(side=tkinter.LEFT, anchor=tkinter.NW)
            nameFrame = ttkCustomWidget.CustomTtkFrame(txtFrame2)
            nameFrame.pack(anchor=tkinter.NW)
            eleFrame = ttkCustomWidget.CustomTtkFrame(txtFrame2)
            eleFrame.pack(anchor=tkinter.NW)

            lensInfo = self.lensList[i]
            for j in range(len(lensInfo)):
                tempBtn = ttkCustomWidget.CustomTtkButton(btnFrame2, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editLensList, i, lensInfo))
                tempBtn.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                nameLb = ttkCustomWidget.CustomTtkLabel(nameFrame, text=textSetting.textList["orgInfoEditor"]["tailNameLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                nameLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                f1Lb = ttkCustomWidget.CustomTtkLabel(eleFrame, text=textSetting.textList["orgInfoEditor"]["tailF1Label"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                f1Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                b1Lb = ttkCustomWidget.CustomTtkLabel(eleFrame, text=textSetting.textList["orgInfoEditor"]["tailB1Label"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                b1Lb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)

                if j in [0, 1]:
                    self.lensVarList.append(tkinter.StringVar(value=lensInfo[j]))
                    temphTextLb = ttkCustomWidget.CustomTtkLabel(nameFrame, textvariable=self.lensVarList[self.lensVarCnt], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                    temphTextLb.grid(row=i, column=j + 1, sticky=tkinter.W + tkinter.E, ipadx=10)
                    self.lensVarCnt += 1
                elif j in [2, 3]:
                    self.lensVarList.append(tkinter.DoubleVar(value=round(float(lensInfo[j]), 3)))
                    temphTextLb = ttkCustomWidget.CustomTtkLabel(eleFrame, textvariable=self.lensVarList[self.lensVarCnt], width=7, font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                    temphTextLb.grid(row=i, column=j - 1, sticky=tkinter.W + tkinter.E)
                    self.lensVarCnt += 1
                elif j == 4:
                    for k in range(len(lensInfo[j])):
                        self.lensVarList.append(tkinter.IntVar(value=int(lensInfo[j][k])))
                        temphTextLb = ttkCustomWidget.CustomTtkLabel(eleFrame, textvariable=self.lensVarList[self.lensVarCnt], width=7, font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                        temphTextLb.grid(row=i + 1, column=k + 1, sticky=tkinter.W + tkinter.E)
                        self.lensVarCnt += 1

    def editTailCnt(self, val):
        result = EditTailCntWidget(self.frame, textSetting.textList["orgInfoEditor"]["tailEditCntLabel"], self.decryptFile, val, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveTailCnt(self.trainIdx, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I67"])
            self.reloadFunc()

    def editTailSmfElse(self, smfList, elseList):
        result = EditTailSmfElseWidget(self.frame, textSetting.textList["orgInfoEditor"]["tailEditLabel"], self.decryptFile, smfList, elseList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveTailSmfElse(self.trainIdx, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I68"])
            self.reloadFunc()

    def editLensList(self, i, valList):
        result = EditLensWidget(self.frame, textSetting.textList["orgInfoEditor"]["lensEditLabel"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.lensList[i] = result.resultValueList
            if not self.decryptFile.saveTailLensList(self.trainIdx, self.lensList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I66"])
            self.reloadFunc()


class EditTailCntWidget(CustomSimpleDialog):
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


class EditTailSmfElseWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, smfList, elseList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.smfList = smfList
        self.elseList = elseList
        self.smfNameVarList = []
        self.elseVarList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        for i in range(len(self.smfList)):
            smfNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["tailSmfNameLabel"].format(i + 1), font=textSetting.textList["font2"])
            smfNameLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.smfNameVarList.append(tkinter.StringVar(value=self.smfList[i]))
            smfNameEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.smfNameVarList[i], font=textSetting.textList["font2"])
            smfNameEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.elseList)):
            elseLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["tailSmfElseLabel"].format(i + 1), font=textSetting.textList["font2"])
            elseLb.grid(row=len(self.smfList) + i, column=0, sticky=tkinter.W + tkinter.E)
            self.elseVarList.append(tkinter.IntVar(value=int(self.elseList[i])))
            elseEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.elseVarList[i], font=textSetting.textList["font2"])
            elseEt.grid(row=len(self.smfList) + i, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.smfNameVarList)):
                        res = self.smfNameVarList[i].get()
                        self.resultValueList.append(res)

                    for i in range(len(self.elseVarList)):
                        res = int(self.elseVarList[i].get())
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
                lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
                lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.StringVar(value=self.lensInfo[i]))
                lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
            elif i in [2, 3]:
                lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
                lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.DoubleVar(value=round(float(self.lensInfo[i]), 3)))
                lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
            elif i == 4:
                varList = []
                for j in range(len(self.lensInfo[i])):
                    lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i + j], font=textSetting.textList["font2"])
                    lensLb.grid(row=i + j, column=0, sticky=tkinter.W + tkinter.E)
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
