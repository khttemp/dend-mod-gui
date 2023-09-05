from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting


class FixedList2Widget:
    def __init__(self, frame, trainIdx, decryptFile, text, elseList, reloadFunc):
        self.frame = frame
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.reloadFunc = reloadFunc

        self.elseLf = ttk.LabelFrame(self.frame, text=text)
        self.elseLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10)

        self.txtFrame = ttk.Frame(self.elseLf)
        self.txtFrame.pack(anchor=tkinter.NW)

        for i in range(len(self.elseList)):
            elseInfo = self.elseList[i]
            self.varNum = tkinter.IntVar()
            self.varNum.set(elseInfo[0])
            self.varTemp = tkinter.StringVar()
            self.varTemp.set(elseInfo[1])
            self.tempNumLb = tkinter.Label(self.txtFrame, textvariable=self.varNum, width=5, font=textSetting.textList["font6"], borderwidth=1, relief="solid")
            self.tempNumLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E, ipadx=15)
            self.tempTextLb = tkinter.Label(self.txtFrame, textvariable=self.varTemp, font=textSetting.textList["font6"], borderwidth=1, relief="solid")
            self.tempTextLb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E, ipadx=15)
            self.tempBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=partial(self.editVar, i, elseInfo))
            self.tempBtn.grid(row=i, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, elseInfo):
        result = EditFixedList2Widget(self.frame, textSetting.textList["orgInfoEditor"]["fixedList2ModifyLabel"], self.decryptFile, elseInfo)
        if result.reloadFlag:
            self.elseList[i] = result.resultValueList
            if not self.decryptFile.saveElse2List(self.trainIdx, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])

            self.reloadFunc()


class EditFixedList2Widget(sd.Dialog):
    def __init__(self, master, title, decryptFile, valList):
        self.decryptFile = decryptFile
        self.valList = valList
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditFixedList2Widget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.valList)):
            if i == 0:
                self.txtLb = ttk.Label(master, text=textSetting.textList["orgInfoEditor"]["fixedList2NumLabel"], font=textSetting.textList["font2"])
                self.txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            else:
                self.txtLb = ttk.Label(master, text=textSetting.textList["orgInfoEditor"]["fixedList2NameLabel"], font=textSetting.textList["font2"])
                self.txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)

            if i == 0:
                self.varTemp = tkinter.IntVar()
            else:
                self.varTemp = tkinter.StringVar()
            self.varTemp.set(self.valList[i])
            self.varList.append(self.varTemp)
            self.txtEt = ttk.Entry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
            self.txtEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

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
