from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog, CustomAskstring


class FixedList2Widget:
    def __init__(self, frame, trainIdx, decryptFile, text, elseList, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

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
        result = EditFixedList2Widget(self.frame, textSetting.textList["orgInfoEditor"]["fixedList2ModifyLabel"], self.decryptFile, elseInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.elseList[i] = result.resultValueList
            if not self.decryptFile.saveElse2List(self.trainIdx, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])

            self.reloadFunc()


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
                txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            else:
                txtLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["fixedList2NameLabel"], font=textSetting.textList["font2"])
                txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)

            if i == 0:
                self.varTemp = tkinter.IntVar()
            else:
                self.varTemp = tkinter.StringVar()
            self.varTemp.set(self.valList[i])
            self.varList.append(self.varTemp)
            txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
            txtEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
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
                        errorMsg = textSetting.textList["errorList"]["E3"]
                        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)

    def apply(self):
        self.reloadFlag = True
