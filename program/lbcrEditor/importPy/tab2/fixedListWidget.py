from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


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
                self.varLb = tkinter.Label(self.txtFrame, text="No.{0}".format(i + 1), font=("", 20), borderwidth=1, relief="solid")
                self.varLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
                colNum += 1
            elseInfo = self.elseList[i]
            self.varTemp = tkinter.StringVar()
            self.varTemp.set(elseInfo)
            self.tempTextLb = tkinter.Label(self.txtFrame, textvariable=self.varTemp, font=("", 20), borderwidth=1, relief="solid")
            self.tempTextLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
            colNum += 1
            self.tempBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=partial(self.editVar, i, elseInfo))
            self.tempBtn.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, elseInfo):
        resultValue = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=elseInfo)
        if resultValue:
            self.elseList[i] = resultValue
            if not self.decryptFile.saveElseList(self.trainIdx, self.ver, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="情報を修正しました")
            self.reloadFunc()
