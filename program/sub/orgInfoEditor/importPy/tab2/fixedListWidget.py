from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class FixedListWidget:
    def __init__(self, frame, trainIndex, decryptFile, text, elseList, ver, rootFrameAppearance, reloadWidget):
        self.frame = frame
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.ver = ver
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget

        elseLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=text)
        elseLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10)

        txtFrame = ttkCustomWidget.CustomTtkFrame(elseLf)
        txtFrame.pack(anchor=tkinter.NW, padx=10)
        self.varList = []

        for i in range(len(self.elseList)):
            colNum = 0
            if decryptFile.game == "LS" and ver == 1:
                varLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["orgInfoEditor"]["fixedListNumLabel"].format(i + 1), font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                varLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
                colNum += 1
            self.varList.append(tkinter.StringVar(value=self.elseList[i]))
            tempTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            tempTextLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
            colNum += 1
            tempBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVar, i, self.elseList[i]))
            tempBtn.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, elseInfo):
        result = EditFixedListWidget(self.frame.winfo_toplevel(), textSetting.textList["orgInfoEditor"]["valueModify"], self.decryptFile, elseInfo, self.ver, self.rootFrameAppearance)
        if result.reloadFlag:
            self.elseList[i] = result.resultValue
            if not self.decryptFile.saveElseList(self.trainIndex, self.ver, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])
            self.reloadWidget()


class EditFixedListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, val, ver, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = val
        self.ver = ver
        self.resultValue = None
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varTemp = tkinter.StringVar()
        self.varTemp.set(self.val)
        txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
        txtEt.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        self.resultValue = None
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    if self.decryptFile.game == "LS" and self.ver == 1:
                        self.resultValue = int(self.varTemp.get())
                    else:
                        self.resultValue = self.varTemp.get()
                    return True
                except Exception:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E3"])
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def apply(self):
        self.reloadFlag = True
