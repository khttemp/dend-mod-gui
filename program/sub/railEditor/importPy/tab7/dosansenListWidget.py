from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog

from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame


class DosansenListWidget:
    def __init__(self, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.dosansenList = decryptFile.dosansenList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        dosansenListLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["dosansenInfoLabel"], height=900)
        dosansenListLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(dosansenListLf, bgColor=rootFrameAppearance.bgColor)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)

        txtFrame = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame.pack(anchor=tkinter.NW)

        dosansenCntNameLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["railEditor"]["dosansenCntLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=12, borderwidth=1, relief="solid")
        dosansenCntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        dosansenCntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=len(self.dosansenList), font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        dosansenCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        dosansenCntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=self.editDosansenCnt)
        dosansenCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.dosansenList)):
            txtFrame2 = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
            txtFrame2.pack(anchor=tkinter.NW, pady=5, fill=tkinter.BOTH)

            dosansenInfo = self.dosansenList[i]
            tempBtn = ttkCustomWidget.CustomTtkButton(txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editDosansenList, i, dosansenInfo))
            tempBtn.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            startLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["dosansenStart"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            startLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            endLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["dosansenEnd"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            endLb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
            ele1Lb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["dosansenE1"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            ele1Lb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)
            endLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["dosansenAnime"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            endLb.grid(row=3, column=1, sticky=tkinter.W + tkinter.E)
            ele2Lb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["dosansenE2"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            ele2Lb.grid(row=4, column=1, sticky=tkinter.W + tkinter.E)
            f1Lb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["dosansenF1"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            f1Lb.grid(row=5, column=1, sticky=tkinter.W + tkinter.E)
            for j in range(len(dosansenInfo)):
                tempTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                if j in [0, 1, 2]:
                    dosansenValue = dosansenInfo[j]
                    tempTextLb.grid(row=0, column=2 + j, sticky=tkinter.W + tkinter.E)
                elif j in [3, 4, 5]:
                    dosansenValue = dosansenInfo[j]
                    tempTextLb.grid(row=1, column=j - 1, sticky=tkinter.W + tkinter.E)
                elif j == 6:
                    dosansenValue = dosansenInfo[j]
                    tempTextLb.grid(row=2, column=j - 4, sticky=tkinter.W + tkinter.E)
                elif j in [7, 8, 9, 10]:
                    dosansenValue = round(float(dosansenInfo[j]), 3)
                    tempTextLb.grid(row=3, column=j - 5, sticky=tkinter.W + tkinter.E)
                elif j == 11:
                    dosansenValue = dosansenInfo[j]
                    tempTextLb.grid(row=4, column=j - 9, sticky=tkinter.W + tkinter.E)
                elif j == 12:
                    dosansenValue = round(float(dosansenInfo[j]), 3)
                    tempTextLb.grid(row=5, column=j - 10, sticky=tkinter.W + tkinter.E)
                tempTextLb.configure(text=dosansenValue)

    def editDosansenCnt(self):
        result = EditDosansenCntWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["editDosansenCntLabel"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveDosansenCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["error"], message=textSetting.textList["infoList"]["I86"])
            self.reloadFunc()

    def editDosansenList(self, i, valList):
        result = EditDosansenWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["editDosansenInfoLabel"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.dosansenList[i] = result.resultValueList
            if not self.decryptFile.saveDosansenList(self.dosansenList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["error"], message=textSetting.textList["infoList"]["I87"])
            self.reloadFunc()


class EditDosansenCntWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = len(decryptFile.dosansenList)
        self.resultValue = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()

        self.varDosansenCnt = tkinter.IntVar()
        self.varDosansenCnt.set(self.val)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varDosansenCnt, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varDosansenCnt.get())
                    if res < 0:
                        errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
                    self.resultValue = res
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E60"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return False
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

            if self.resultValue < self.val:
                msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
                result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True


class EditDosansenWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, dosansenInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.dosansenInfo = dosansenInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        dosansenInfoLbList = textSetting.textList["railEditor"]["editDosansenLabelList"]
        for i in range(len(self.dosansenInfo)):
            stationLb = ttkCustomWidget.CustomTtkLabel(master, text=dosansenInfoLbList[i], font=textSetting.textList["font2"])
            stationLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i in [7, 8, 9, 10, 12]:
                varDosansen = tkinter.DoubleVar()
                varDosansen.set(round(float(self.dosansenInfo[i]), 3))
            else:
                varDosansen = tkinter.IntVar()
                varDosansen.set(self.dosansenInfo[i])
            self.varList.append(varDosansen)
            dosansenEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            dosansenEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i in [7, 8, 9, 10, 12]:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())
                        self.resultValueList.append(res)
                    return True
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E3"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return False
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
