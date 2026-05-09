from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class FixedList2Widget:
    def __init__(self, frame, trainIndex, decryptFile, text, elseList, rootFrameAppearance, reloadWidget):
        self.frame = frame
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget

        elseLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=text)
        elseLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10)

        txtFrame = ttkCustomWidget.CustomTtkFrame(elseLf)
        txtFrame.pack(anchor=tkinter.NW, padx=10)
        self.varList = []

        for i in range(len(self.elseList)):
            varList = []
            elseInfo = self.elseList[i]
            varList.append(tkinter.IntVar(value=elseInfo[0]))
            varList.append(tkinter.StringVar(value=elseInfo[1]))
            self.varList.append(varList)
            tempNumLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=varList[0], width=5, font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            tempNumLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E, ipadx=15)
            tempTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=varList[1], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            tempTextLb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E, ipadx=15)
            tempBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVar, i, elseInfo))
            tempBtn.grid(row=i, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, elseInfo):
        result = EditFixedList2Widget(self.frame.winfo_toplevel(), textSetting.textList["orgInfoEditor"]["fixedList2ModifyLabel"], self.decryptFile, elseInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.elseList[i] = result.resultValueList
            if not self.decryptFile.saveElse2List(self.trainIndex, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])
            self.reloadWidget()


class EditFixedList2Widget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, valList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.valList = valList
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.valList)):
            if i == 0:
                txtLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["fixedList2NumLabel"], font=textSetting.textList["font2"])
                txtLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            else:
                txtLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["fixedList2NameLabel"], font=textSetting.textList["font2"])
                txtLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)

            if i == 0:
                self.varTemp = tkinter.IntVar()
            else:
                self.varTemp = tkinter.StringVar()
            self.varTemp.set(self.valList[i])
            self.varList.append(self.varTemp)
            txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
            txtEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                for i in range(len(self.valList)):
                    try:
                        if i == 0:
                            res = int(self.varList[i].get())
                            if res <= 0:
                                errorMsg = textSetting.textList["errorList"]["E61"].format(1)
                                mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                                return False
                        else:
                            res = self.varList[i].get()
                        self.resultValueList.append(res)
                    except Exception:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E3"])
                        return False
                return True
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def apply(self):
        self.reloadFlag = True
