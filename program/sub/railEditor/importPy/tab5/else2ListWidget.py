from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog

from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame


class Else2ListWidget:
    def __init__(self, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else2List = decryptFile.else2List
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        if len(self.else2List) == 0:
            return

        eleLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["else2InfoLabel"])
        eleLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(eleLf, bgColor=rootFrameAppearance.bgColor)
        scrollbarFrame.pack(expand=True, fill=tkinter.BOTH)

        txtFrame = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame.pack(anchor=tkinter.NW, padx=5, pady=5)

        else2CntNameLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["railEditor"]["else2CntLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        else2CntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        else2CntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=len(self.else2List), font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        else2CntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        else2CntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=self.editElse2Cnt)
        else2CntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        txtFrame2 = ttkCustomWidget.CustomTtkFrame(scrollbarFrame.interior)
        txtFrame2.pack(anchor=tkinter.NW, padx=5, pady=5)

        for i in range(len(self.else2List)):
            else2Info = self.else2List[i]
            for j in range(len(else2Info)):
                if j in [2, 3, 4]:
                    else2Value = round(float(else2Info[j]), 3)
                else:
                    else2Value = else2Info[j]
                tempfTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=else2Value, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                tempfTextLb.grid(row=i, column=j, sticky=tkinter.W + tkinter.E)
            tempBtn = ttkCustomWidget.CustomTtkButton(txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editElse2List, i, else2Info))
            tempBtn.grid(row=i, column=len(else2Info), sticky=tkinter.W + tkinter.E)

    def editElse2Cnt(self):
        result = EditElse2CntWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["modifyElse2CntLabel"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveElse2Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I82"])
            self.reloadFunc()

    def editElse2List(self, i, valList):
        result = EditElse2ListWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["modifyElse2InfoLabel"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.else2List[i] = result.resultValueList
            if not self.decryptFile.saveElse2List(self.else2List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I83"])

            self.reloadFunc()


class EditElse2CntWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = len(self.decryptFile.else2List)
        self.resultValue = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()

        self.varElse2Cnt = tkinter.IntVar()
        self.varElse2Cnt.set(self.val)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varElse2Cnt, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

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


class EditElse2ListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, else2Info, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.else2Info = else2Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        else2InfoLbList = textSetting.textList["railEditor"]["editElse2LabelList"]
        for i in range(len(self.else2Info)):
            else2Lb = ttkCustomWidget.CustomTtkLabel(master, text=else2InfoLbList[i], font=textSetting.textList["font2"])
            else2Lb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            if i in [2, 3, 4]:
                varElse2 = tkinter.DoubleVar()
                varElse2.set(round(float(self.else2Info[i]), 3))
            else:
                varElse2 = tkinter.IntVar()
                varElse2.set(self.else2Info[i])
            self.varList.append(varElse2)
            else2Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            else2Et.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

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
