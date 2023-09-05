from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting


class RailPosWidget:
    def __init__(self, frame, title, num, decryptFile, trainList, reloadFunc):
        self.frame = frame
        self.title = title
        self.railBtnList = []
        self.num = num
        self.decryptFile = decryptFile
        self.trainList = trainList
        self.reloadFunc = reloadFunc

        self.railPosLf = ttk.LabelFrame(self.frame, text=title)
        self.railPosLf.pack()

        self.playHeaderLb = tkinter.Label(self.railPosLf, text=textSetting.textList["railEditor"]["railPosPlayerLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.playHeaderLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.railNoHeaderLb = tkinter.Label(self.railPosLf, text=textSetting.textList["railEditor"]["railPosRailNoLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.railNoHeaderLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.railPosHeaderLb = tkinter.Label(self.railPosLf, text=textSetting.textList["railEditor"]["railPosRailPosLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.railPosHeaderLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        self.b1HeaderLb = tkinter.Label(self.railPosLf, text=textSetting.textList["railEditor"]["railPosB1Label"], font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
        self.b1HeaderLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)
        self.f1HeaderLb = tkinter.Label(self.railPosLf, text=textSetting.textList["railEditor"]["railPosF1Label"], font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
        self.f1HeaderLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.trainList)):
            trainInfo = self.trainList[i]
            self.playLb = tkinter.Label(self.railPosLf, text=textSetting.textList["railEditor"]["railPosPlayerNameLabel"].format(i + 1), font=textSetting.textList["font6"], borderwidth=1, relief="solid")
            self.playLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            for j in range(len(trainInfo)):
                self.valLb = tkinter.Label(self.railPosLf, text=trainInfo[j], font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                self.valLb.grid(row=i + 1, column=j + 1, sticky=tkinter.W + tkinter.E)

            self.railBtn = tkinter.Button(self.railPosLf, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=partial(self.editVar, i, trainInfo))
            self.railBtn.grid(row=i + 1, column=len(trainInfo) + 1, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, trainInfo):
        result = EditRailPosWidget(self.frame, self.title + textSetting.textList["railEditor"]["commonModifyLabel"], self.decryptFile, trainInfo)

        if result.reloadFlag:
            self.trainList[i] = result.resultValueList
            if not self.decryptFile.saveRailPos(self.num, self.trainList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=self.title + textSetting.textList["infoList"]["I61"])

            self.reloadFunc()


class EditRailPosWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, trainInfo):
        self.decryptFile = decryptFile
        self.trainInfo = trainInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditRailPosWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        trainInfoLbList = textSetting.textList["railEditor"]["editRailPosLabelList"]
        for i in range(len(self.trainInfo)):
            self.railLb = ttk.Label(master, text=trainInfoLbList[i], font=textSetting.textList["font2"])
            self.railLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            if i == 3:
                self.varRail = tkinter.DoubleVar()
                self.varRail.set(self.trainInfo[i])
            else:
                self.varRail = tkinter.IntVar()
                self.varRail.set(self.trainInfo[i])
            self.varList.append(self.varRail)
            self.railEt = ttk.Entry(master, textvariable=self.varRail, font=textSetting.textList["font2"])
            self.railEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i == 3:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())
                            if res < 0:
                                errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                                mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                                return False
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
