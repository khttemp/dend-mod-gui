from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting


class FixedListWidget:
    def __init__(self, frame, game, trainIdx, decryptFile, text, elseList, ver, reloadFunc):
        self.frame = frame
        self.game = game
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.ver = ver
        self.reloadFunc = reloadFunc

        self.elseLf = ttk.LabelFrame(self.frame, text=text)
        self.elseLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10)

        self.txtFrame = ttk.Frame(self.elseLf)
        self.txtFrame.pack(anchor=tkinter.NW)

        for i in range(len(self.elseList)):
            colNum = 0
            if self.game == 0 and ver == 1:
                self.varLb = tkinter.Label(self.txtFrame, text=textSetting.textList["orgInfoEditor"]["fixedListNumLabel"].format(i + 1), font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                self.varLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
                colNum += 1
            elseInfo = self.elseList[i]
            self.varTemp = tkinter.StringVar()
            self.varTemp.set(elseInfo)
            self.tempTextLb = tkinter.Label(self.txtFrame, textvariable=self.varTemp, font=textSetting.textList["font6"], borderwidth=1, relief="solid")
            self.tempTextLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
            colNum += 1
            self.tempBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=partial(self.editVar, i, elseInfo))
            self.tempBtn.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, elseInfo):
        resultValue = sd.askstring(title=textSetting.textList["orgInfoEditor"]["valueModify"], prompt=textSetting.textList["infoList"]["I44"], initialvalue=elseInfo)
        if resultValue:
            self.elseList[i] = resultValue
            if not self.decryptFile.saveElseList(self.trainIdx, self.ver, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])
            self.reloadFunc()
