from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class Else4ListWidget:
    def __init__(self, frame, decryptFile, else4List, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else4List = else4List
        self.reloadFunc = reloadFunc

        self.elseLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["else4Label"])
        self.elseLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(self.elseLf)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)

        self.txtFrame = ttk.Frame(scrollbarFrame.interior)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.else4CntNameLb = tkinter.Label(self.txtFrame, text=textSetting.textList["railEditor"]["else4CntLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.else4CntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varElse4Cnt = tkinter.IntVar()
        self.varElse4Cnt.set(len(self.else4List))
        self.else4CntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varElse4Cnt, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.else4CntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game == "RS":
            self.else4CntBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editElse4Cnt(self.varElse4Cnt.get()))
            self.else4CntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.txtFrame2 = ttk.Frame(scrollbarFrame.interior)
        self.txtFrame2.pack(anchor=tkinter.NW, pady=5)
        rowNum = 0

        for i in range(len(self.else4List)):
            else4Info = self.else4List[i]

            self.tempBtn = tkinter.Button(self.txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=partial(self.editElse4List, i, else4Info))
            self.tempBtn.grid(row=rowNum, column=0, sticky=tkinter.W + tkinter.E)

            self.varAmbNo = tkinter.IntVar()
            self.varAmbNo.set(int(else4Info[0]))
            self.ambNoTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varAmbNo, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.ambNoTextLb.grid(row=rowNum, column=1, sticky=tkinter.W + tkinter.E)

            self.varPrevRail = tkinter.IntVar()
            self.varPrevRail.set(int(else4Info[1]))
            self.prevRailTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varPrevRail, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.prevRailTextLb.grid(row=rowNum, column=2, sticky=tkinter.W + tkinter.E)

            rowNum += 1

            for j in range(6):
                self.varTemp = tkinter.DoubleVar()
                self.varTemp.set(float(else4Info[2 + j]))
                self.tempTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
                self.tempTextLb.grid(row=rowNum, column=j + 1, sticky=tkinter.W + tkinter.E)
            rowNum += 1

    def editElse4Cnt(self, val):
        result = EditElse4CntWidget(self.frame, textSetting.textList["railEditor"]["editElse4CntLabel"], self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveElse4Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I93"])
            self.reloadFunc()

    def editElse4List(self, i, valList):
        result = EditElse4ListWidget(self.frame, textSetting.textList["railEditor"]["editElse4Label"], self.decryptFile, valList)
        if result.reloadFlag:
            self.else4List[i] = result.resultValueList
            if not self.decryptFile.saveElse4List(self.else4List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I94"])
            self.reloadFunc()


class EditElse4CntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditElse4CntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.pack()

        self.varElse4Cnt = tkinter.IntVar()
        self.varElse4Cnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varElse4Cnt, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varElse4Cnt.get())
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


class EditElse4ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else4Info):
        self.decryptFile = decryptFile
        self.else4Info = else4Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse4ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        else4InfoLbList = textSetting.textList["railEditor"]["editElse4ElementLabelList"]
        for i in range(len(self.else4Info)):
            self.else4Lb = ttk.Label(master, text=else4InfoLbList[i], font=textSetting.textList["font2"])
            self.else4Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i in [0, 1]:
                self.varElse4 = tkinter.IntVar()
                self.varElse4.set(self.else4Info[i])
            else:
                self.varElse4 = tkinter.DoubleVar()
                self.varElse4.set(self.else4Info[i])
            self.varList.append(self.varElse4)
            self.else4Et = ttk.Entry(master, textvariable=self.varElse4, font=textSetting.textList["font2"])
            self.else4Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["BS", "CS"] and i == 0:
                self.else4Et["state"] = "disabled"
            elif self.decryptFile.game == "LS" and i in [0, 1]:
                self.else4Et["state"] = "disabled"

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i in [0, 1]:
                            res = int(self.varList[i].get())
                        else:
                            res = float(self.varList[i].get())
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
