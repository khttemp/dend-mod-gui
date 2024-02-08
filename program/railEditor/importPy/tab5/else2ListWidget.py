from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class Else2ListWidget:
    def __init__(self, frame, decryptFile, else2List, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else2List = else2List
        self.reloadFunc = reloadFunc

        self.eleLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["else2InfoLabel"])
        self.eleLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(self.eleLf)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)

        self.txtFrame = ttk.Frame(scrollbarFrame.interior)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.else2CntNameLb = tkinter.Label(self.txtFrame, text=textSetting.textList["railEditor"]["else2CntLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.else2CntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varElse2Cnt = tkinter.IntVar()
        self.varElse2Cnt.set(len(self.else2List))
        self.else2CntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varElse2Cnt, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.else2CntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.else2CntBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editElse2Cnt(self.varElse2Cnt.get()))
            self.else2CntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.txtFrame2 = ttk.Frame(scrollbarFrame.interior)
        self.txtFrame2.pack(anchor=tkinter.NW, pady=5)

        for i in range(len(self.else2List)):
            else2Info = self.else2List[i]
            for j in range(len(else2Info)):
                if j in [2, 3, 4]:
                    self.varTempF = tkinter.DoubleVar()
                    self.varTempF.set(round(float(else2Info[j]), 3))
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempF, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=i, column=j, sticky=tkinter.W + tkinter.E)
                else:
                    self.varTempH = tkinter.IntVar()
                    self.varTempH.set(int(else2Info[j]))
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=i, column=j, sticky=tkinter.W + tkinter.E)
            self.tempBtn = tkinter.Button(self.txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=partial(self.editElse2List, i, else2Info))
            self.tempBtn.grid(row=i, column=len(else2Info), sticky=tkinter.W + tkinter.E)

    def editElse2Cnt(self, val):
        result = EditElse2CntWidget(self.frame, textSetting.textList["railEditor"]["modifyElse2CntLabel"], self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveElse2Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I82"])
            self.reloadFunc()

    def editElse2List(self, i, valList):
        result = EditElse2ListWidget(self.frame, textSetting.textList["railEditor"]["modifyElse2InfoLabel"], self.decryptFile, valList)
        if result.reloadFlag:
            self.else2List[i] = result.resultValueList
            if not self.decryptFile.saveElse2List(self.else2List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I83"])

            self.reloadFunc()


class EditElse2CntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditElse2CntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.pack()

        self.varElse2Cnt = tkinter.IntVar()
        self.varElse2Cnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varElse2Cnt, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varElse2Cnt.get())
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


class EditElse2ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else2Info):
        self.decryptFile = decryptFile
        self.else2Info = else2Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse2ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        else2InfoLbList = textSetting.textList["railEditor"]["editElse2LabelList"]
        for i in range(len(self.else2Info)):
            self.else2Lb = ttk.Label(master, text=else2InfoLbList[i], font=textSetting.textList["font2"])
            self.else2Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i in [2, 3, 4]:
                self.varElse2 = tkinter.DoubleVar()
                self.varElse2.set(round(float(self.else2Info[i]), 3))
            else:
                self.varElse2 = tkinter.IntVar()
                self.varElse2.set(self.else2Info[i])
            self.varList.append(self.varElse2)
            self.else2Et = ttk.Entry(master, textvariable=self.varElse2, font=textSetting.textList["font2"])
            self.else2Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i in [2, 3, 4]:
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
