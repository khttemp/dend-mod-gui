from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class Else2ListWidget:
    def __init__(self, frame, decryptFile, else2List, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else2List = else2List
        self.reloadFunc = reloadFunc

        self.eleLf = ttk.LabelFrame(self.frame, text="else2")
        self.eleLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(self.eleLf)

        self.txtFrame = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.else2CntNameLb = tkinter.Label(self.txtFrame, text="else2数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else2CntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varElse2Cnt = tkinter.IntVar()
        self.varElse2Cnt.set(len(self.else2List))
        self.else2CntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varElse2Cnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else2CntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.else2CntBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editElse2Cnt(self.varElse2Cnt.get()))
            self.else2CntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.txtFrame2 = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame2.pack(anchor=tkinter.NW, pady=5)

        for i in range(len(self.else2List)):
            else2Info = self.else2List[i]
            for j in range(len(else2Info)):
                if j in [2, 3, 4]:
                    self.varTempF = tkinter.DoubleVar()
                    self.varTempF.set(round(float(else2Info[j]), 3))
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempF, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=i, column=j, sticky=tkinter.W + tkinter.E)
                else:
                    self.varTempH = tkinter.IntVar()
                    self.varTempH.set(int(else2Info[j]))
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=i, column=j, sticky=tkinter.W + tkinter.E)
            self.tempBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse2List, i, else2Info))
            self.tempBtn.grid(row=i, column=len(else2Info), sticky=tkinter.W + tkinter.E)

    def editElse2Cnt(self, val):
        result = EditElse2CntWidget(self.frame, "else2数の変更", self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveElse2Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else2数を修正しました")
            self.reloadFunc()

    def editElse2List(self, i, valList):
        result = EditElse2ListWidget(self.frame, "else2の変更", self.decryptFile, valList)
        if result.reloadFlag:
            self.else2List[i] = result.resultValueList
            if not self.decryptFile.saveElse2List(self.else2List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else2の情報を修正しました")

            self.reloadFunc()


class EditElse2CntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditElse2CntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varElse2Cnt = tkinter.IntVar()
        self.varElse2Cnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varElse2Cnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varElse2Cnt.get())
                    if res < 0:
                        errorMsg = "0以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValue = res
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return False
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

            if self.resultValue < self.val:
                msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True


class EditElse2ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else2Info):
        self.decryptFile = decryptFile
        self.else2Info = else2Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse2ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        else2InfoLbList = ["e1", "e2", "f1", "f2", "f3", "e3"]
        for i in range(len(self.else2Info)):
            self.else2Lb = ttk.Label(master, text=else2InfoLbList[i], font=("", 14))
            self.else2Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i in [2, 3, 4]:
                self.varElse2 = tkinter.DoubleVar()
                self.varElse2.set(round(float(self.else2Info[i]), 3))
            else:
                self.varElse2 = tkinter.IntVar()
                self.varElse2.set(self.else2Info[i])
            self.varList.append(self.varElse2)
            self.else2Et = ttk.Entry(master, textvariable=self.varElse2, font=("", 14))
            self.else2Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
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
                    errorMsg = "数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return False
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
