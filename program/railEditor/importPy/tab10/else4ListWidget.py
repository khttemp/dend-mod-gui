from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class Else4ListWidget:
    def __init__(self, frame, decryptFile, else4List, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else4List = else4List
        self.reloadFunc = reloadFunc

        self.elseLf = ttk.LabelFrame(self.frame, text="else4")
        self.elseLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(self.elseLf)

        self.txtFrame = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.else4CntNameLb = tkinter.Label(self.txtFrame, text="else4数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else4CntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varElse4Cnt = tkinter.IntVar()
        self.varElse4Cnt.set(len(self.else4List))
        self.else4CntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varElse4Cnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else4CntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game == "RS":
            self.else4CntBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editElse4Cnt(self.varElse4Cnt.get()))
            self.else4CntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.txtFrame2 = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame2.pack(anchor=tkinter.NW, pady=5)
        rowNum = 0

        for i in range(len(self.else4List)):
            else4Info = self.else4List[i]

            self.tempBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse4List, i, else4Info))
            self.tempBtn.grid(row=rowNum, column=0, sticky=tkinter.W + tkinter.E)

            self.varAmbNo = tkinter.IntVar()
            self.varAmbNo.set(int(else4Info[0]))
            self.ambNoTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varAmbNo, font=("", 20), width=7, borderwidth=1, relief="solid")
            self.ambNoTextLb.grid(row=rowNum, column=1, sticky=tkinter.W + tkinter.E)

            self.varPrevRail = tkinter.IntVar()
            self.varPrevRail.set(int(else4Info[1]))
            self.prevRailTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varPrevRail, font=("", 20), width=7, borderwidth=1, relief="solid")
            self.prevRailTextLb.grid(row=rowNum, column=2, sticky=tkinter.W + tkinter.E)

            rowNum += 1

            for j in range(6):
                self.varTemp = tkinter.DoubleVar()
                self.varTemp.set(float(else4Info[2 + j]))
                self.tempTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                self.tempTextLb.grid(row=rowNum, column=j + 1, sticky=tkinter.W + tkinter.E)
            rowNum += 1

    def editElse4Cnt(self, val):
        result = EditElse4CntWidget(self.frame, "else4数の変更", self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveElse4Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else4数を修正しました")
            self.reloadFunc()

    def editElse4List(self, i, valList):
        result = EditElse4ListWidget(self.frame, "else4の変更", self.decryptFile, valList)
        if result.reloadFlag:
            self.else4List[i] = result.resultValueList
            if not self.decryptFile.saveElse4List(self.else4List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else4情報を修正しました")
            self.reloadFunc()


class EditElse4CntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditElse4CntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varElse4Cnt = tkinter.IntVar()
        self.varElse4Cnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varElse4Cnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varElse4Cnt.get())
                    if res < 0:
                        errorMsg = "0以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValue = res
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

            if self.resultValue < self.val:
                msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True


class EditElse4ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else4Info):
        self.decryptFile = decryptFile
        self.else4Info = else4Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse4ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        else4InfoLbList = ["railNo", "prevRail", "f1", "f2", "f3", "f4", "f5", "f6"]
        for i in range(len(self.else4Info)):
            self.else4Lb = ttk.Label(master, text=else4InfoLbList[i], font=("", 14))
            self.else4Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i in [0, 1]:
                self.varElse4 = tkinter.IntVar()
                self.varElse4.set(self.else4Info[i])
            else:
                self.varElse4 = tkinter.DoubleVar()
                self.varElse4.set(self.else4Info[i])
            self.varList.append(self.varElse4)
            self.else4Et = ttk.Entry(master, textvariable=self.varElse4, font=("", 14))
            self.else4Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["BS", "CS"] and i == 0:
                self.else4Et["state"] = "disabled"
            elif self.decryptFile.game == "LS" and i in [0, 1]:
                self.else4Et["state"] = "disabled"

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i in [0, 1]:
                            res = int(self.varList[i].get())
                        else:
                            res = float(self.varList[i].get())
                        self.resultValueList.append(res)
                    return True
                except Exception:
                    errorMsg = "数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
