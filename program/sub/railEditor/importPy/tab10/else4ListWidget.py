from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog

from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame


class Else4ListWidget:
    def __init__(self, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else4List = decryptFile.else4List
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        if self.decryptFile.game == "LSTrial":
            return

        if self.decryptFile.game == "LS" and self.decryptFile.ver != "DEND_MAP_VER0101":
            return

        elseLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["else4Label"])
        elseLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(elseLf, bgColor=rootFrameAppearance.bgColor)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)

        txtFrame = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame.pack(anchor=tkinter.NW)

        else4CntNameLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["railEditor"]["else4CntLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        else4CntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        else4CntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=len(self.else4List), font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        else4CntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game == "RS":
            else4CntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=self.editElse4Cnt)
            else4CntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        txtFrame2 = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame2.pack(anchor=tkinter.NW, pady=5)
        rowNum = 0
        colNum = 0

        for i in range(len(self.else4List)):
            else4Info = self.else4List[i]

            tempBtn = ttkCustomWidget.CustomTtkButton(txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editElse4List, i, else4Info))
            tempBtn.grid(row=rowNum, column=0, sticky=tkinter.W + tkinter.E)
            railNoTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=else4Info[0], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=15, borderwidth=1, relief="solid")
            railNoTextLb.grid(row=rowNum, column=1, sticky=tkinter.W + tkinter.E)
            prevRailTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=else4Info[1], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=15, borderwidth=1, relief="solid")
            prevRailTextLb.grid(row=rowNum, column=2, sticky=tkinter.W + tkinter.E)
            rowNum += 1

            for j in range(6):
                tempTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=else4Info[2 + j], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=15, borderwidth=1, relief="solid")
                tempTextLb.grid(row=rowNum, column=colNum + 1, sticky=tkinter.W + tkinter.E)
                colNum += 1
                if j % 3 == 2:
                    rowNum += 1
                    colNum = 0
            rowNum += 1

    def editElse4Cnt(self):
        result = EditElse4CntWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["editElse4CntLabel"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveElse4Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I93"])
            self.reloadFunc()

    def editElse4List(self, i, valList):
        result = EditElse4ListWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["editElse4Label"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.else4List[i] = result.resultValueList
            if not self.decryptFile.saveElse4List(self.else4List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I94"])
            self.reloadFunc()


class EditElse4CntWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.resultValue = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()

        self.varElse4Cnt = tkinter.IntVar()
        self.varElse4Cnt.set(len(self.decryptFile.else4List))
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varElse4Cnt, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

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

            if self.resultValue < len(self.decryptFile.else4List):
                msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
                result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True


class EditElse4ListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, else4Info, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.else4Info = else4Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        else4InfoLbList = textSetting.textList["railEditor"]["editElse4ElementLabelList"]
        for i in range(len(self.else4Info)):
            else4Lb = ttkCustomWidget.CustomTtkLabel(master, text=else4InfoLbList[i], font=textSetting.textList["font2"])
            else4Lb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            if i in [0, 1]:
                varElse4 = tkinter.IntVar()
                varElse4.set(self.else4Info[i])
            else:
                varElse4 = tkinter.DoubleVar()
                varElse4.set(self.else4Info[i])
            self.varList.append(varElse4)
            else4Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            else4Et.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["BS", "CS"]:
                if i == 0:
                    else4Et["state"] = "disabled"
            elif self.decryptFile.game == "LS":
                if i in [0, 1]:
                    else4Et["state"] = "disabled"
        super().body(master)

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
