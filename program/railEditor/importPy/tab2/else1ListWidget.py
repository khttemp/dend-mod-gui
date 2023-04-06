from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


class Else1ListWidget:
    def __init__(self, frame, decryptFile, else1List, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else1List = else1List
        self.reloadFunc = reloadFunc

        self.else1Lf = ttk.LabelFrame(self.frame, text="else1")
        self.else1Lf.pack(anchor=tkinter.NW, padx=10)

        self.txtFrame = ttk.Frame(self.else1Lf)
        self.txtFrame.pack(anchor=tkinter.NW)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.varElse1 = tkinter.DoubleVar()
            self.varElse1.set(round(float(self.else1List[0]), 3))
            self.else1TextLb = tkinter.Label(self.txtFrame, textvariable=self.varElse1, font=("", 20), width=7, borderwidth=1, relief="solid")
            self.else1TextLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.else1Btn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=partial(self.editVarList, 0, [self.else1List[0]]))
            self.else1Btn.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

            self.txtFrame2 = ttk.Frame(self.else1Lf)
            self.txtFrame2.pack(anchor=tkinter.NW, pady=5)

            for i in range(1, len(self.else1List)):
                else1Info = self.else1List[i]
                for j in range(len(else1Info)):
                    if j in [0, 1]:
                        self.varTemp = tkinter.IntVar()
                        self.varTemp.set(round(float(else1Info[j]), 3))
                    else:
                        self.varTemp = tkinter.IntVar()
                        self.varTemp.set(int(else1Info[j]))
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=i, column=j, sticky=tkinter.W + tkinter.E)
                    self.tempfBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editVarList, i, else1Info))
                    self.tempfBtn.grid(row=i, column=len(else1Info), sticky=tkinter.W + tkinter.E)
        else:
            self.txtFrame2 = ttk.Frame(self.else1Lf)
            self.txtFrame2.pack(anchor=tkinter.NW, pady=5)

            for i in range(len(self.else1List)):
                self.varTemp = tkinter.DoubleVar()
                self.varTemp.set(round(float(self.else1List[i]), 5))
                self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                self.tempfTextLb.grid(row=0, column=i, sticky=tkinter.W + tkinter.E)
                self.tempfBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editVarList2, self.else1List))
                self.tempfBtn.grid(row=0, column=len(self.else1List), sticky=tkinter.W + tkinter.E)

    def editVarList(self, i, valList):
        result = EditElse1ListWidget(self.frame, "else1の変更", self.decryptFile, valList)
        if result.reloadFlag:
            if i == 0:
                self.else1List[i] = result.resultValueList[0]
            else:
                self.else1List[i] = result.resultValueList
            if not self.decryptFile.saveElse1List(self.else1List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else1の情報を修正しました")

            self.reloadFunc()

    def editVarList2(self, valList):
        result = EditElse1List2Widget(self.frame, "else1の変更", self.decryptFile, valList)
        if result.reloadFlag:
            self.else1List = result.resultValueList
            if not self.decryptFile.saveElse1List(self.else1List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else1の情報を修正しました")

            self.reloadFunc()


class EditElse1ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, valList):
        self.decryptFile = decryptFile
        self.valList = valList
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse1ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.valList)):
            if i < 2:
                self.txtLb = ttk.Label(master, text="f{0}".format(i + 1), font=("", 14))
                self.txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            else:
                self.txtLb = ttk.Label(master, text="b{0}".format(i - 1), font=("", 14))
                self.txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)

            if i in [0, 1]:
                self.varTemp = tkinter.DoubleVar()
                self.varTemp.set(round(float(self.valList[i]), 3))
            else:
                self.varTemp = tkinter.IntVar()
                self.varTemp.set(int(self.valList[i]))
            self.varList.append(self.varTemp)
            self.txtEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
            self.txtEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                for i in range(len(self.valList)):
                    try:
                        if i in [0, 1]:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())

                        if res < 0:
                            errorMsg = "0以上の数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    except Exception:
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="エラー", message=errorMsg)
                return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True


class EditElse1List2Widget(sd.Dialog):
    def __init__(self, master, title, decryptFile, valList):
        self.decryptFile = decryptFile
        self.valList = valList
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse1List2Widget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.valList)):
            self.txtLb = ttk.Label(master, text="f{0}".format(i + 1), font=("", 14))
            self.txtLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.varTemp = tkinter.DoubleVar()
            self.varTemp.set(round(float(self.valList[i]), 5))
            self.varList.append(self.varTemp)
            self.txtEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
            self.txtEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                for i in range(len(self.valList)):
                    try:
                        res = float(self.varList[i].get())
                        self.resultValueList.append(res)
                    except Exception:
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="エラー", message=errorMsg)
                return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
