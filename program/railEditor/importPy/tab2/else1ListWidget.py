from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class Else1ListWidget:
    def __init__(self, root, frame, decryptFile, else1List, rootFrameAppearance, reloadFunc):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.else1List = else1List
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        else1Lf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["else1Label"])
        else1Lf.pack(anchor=tkinter.NW, padx=10, pady=5)

        txtFrame = ttkCustomWidget.CustomTtkFrame(else1Lf)
        txtFrame.pack(anchor=tkinter.NW)

        self.varList = []
        self.varCnt = 0
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.varElse1 = tkinter.DoubleVar()
            self.varElse1.set(round(float(self.else1List[0]), 3))
            else1TextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varElse1, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            else1TextLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            else1Btn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVarList, 0, [self.else1List[0]]))
            else1Btn.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

            txtFrame2 = ttkCustomWidget.CustomTtkFrame(else1Lf)
            txtFrame2.pack(anchor=tkinter.NW, pady=5)

            for i in range(1, len(self.else1List)):
                else1Info = self.else1List[i]
                for j in range(len(else1Info)):
                    if j in [0, 1]:
                        varTemp = tkinter.IntVar()
                        varTemp.set(round(float(else1Info[j]), 3))
                    else:
                        varTemp = tkinter.IntVar()
                        varTemp.set(int(else1Info[j]))
                    self.varList.append(varTemp)
                    tempfTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, textvariable=self.varList[self.varCnt], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                    tempfTextLb.grid(row=i, column=j, sticky=tkinter.W + tkinter.E)
                    tempfBtn = ttkCustomWidget.CustomTtkButton(txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVarList, i, else1Info))
                    tempfBtn.grid(row=i, column=len(else1Info), sticky=tkinter.W + tkinter.E)
                    self.varCnt += 1
        else:
            txtFrame2 = ttkCustomWidget.CustomTtkFrame(else1Lf)
            txtFrame2.pack(anchor=tkinter.NW, pady=5)

            for i in range(len(self.else1List)):
                varTemp = tkinter.DoubleVar()
                varTemp.set(round(float(self.else1List[i]), 5))
                self.varList.append(varTemp)
                tempfTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, textvariable=self.varList[self.varCnt], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                tempfTextLb.grid(row=0, column=i, sticky=tkinter.W + tkinter.E)
                tempfBtn = ttkCustomWidget.CustomTtkButton(txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVarList2, self.else1List))
                tempfBtn.grid(row=0, column=len(self.else1List), sticky=tkinter.W + tkinter.E)
                self.varCnt += 1

    def editVarList(self, i, valList):
        result = EditElse1ListWidget(self.root, textSetting.textList["railEditor"]["editElse1Label"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            if i == 0:
                self.else1List[i] = result.resultValueList[0]
            else:
                self.else1List[i] = result.resultValueList
            if not self.decryptFile.saveElse1List(self.else1List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I75"])

            self.reloadFunc()

    def editVarList2(self, valList):
        result = EditElse1List2Widget(self.root, textSetting.textList["railEditor"]["editElse1Label"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.else1List = result.resultValueList
            if not self.decryptFile.saveElse1List(self.else1List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I75"])

            self.reloadFunc()


class EditElse1ListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, valList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.valList = valList
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.valList)):
            if i < 2:
                txtLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["editElse1F1Label"].format(i + 1), font=textSetting.textList["font2"])
                txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            else:
                txtLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["editElse1B1Label"].format(i - 1), font=textSetting.textList["font2"])
                txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)

            if i in [0, 1]:
                varTemp = tkinter.DoubleVar()
                varTemp.set(round(float(self.valList[i]), 3))
            else:
                varTemp = tkinter.IntVar()
                varTemp.set(int(self.valList[i]))
            self.varList.append(varTemp)
            self.txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            self.txtEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                for i in range(len(self.valList)):
                    try:
                        if i in [0, 1]:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())

                        if res < 0:
                            errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    except Exception:
                        errorMsg = textSetting.textList["errorList"]["E3"]
                        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                        return False
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class EditElse1List2Widget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, valList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.valList = valList
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.valList)):
            txtLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["editElse1F1Label"].format(i + 1), font=textSetting.textList["font2"])
            txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            varTemp = tkinter.DoubleVar()
            varTemp.set(round(float(self.valList[i]), 5))
            self.varList.append(varTemp)
            txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            txtEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                for i in range(len(self.valList)):
                    try:
                        res = float(self.varList[i].get())
                        self.resultValueList.append(res)
                    except Exception:
                        errorMsg = textSetting.textList["errorList"]["E3"]
                        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                        return False
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
