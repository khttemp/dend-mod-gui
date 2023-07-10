from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class DosansenListWidget:
    def __init__(self, frame, decryptFile, dosansenList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.dosansenList = dosansenList
        self.reloadFunc = reloadFunc

        self.dosansenListLf = ttk.LabelFrame(self.frame, text="土讃線情報", height=900)
        self.dosansenListLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(self.dosansenListLf)

        self.txtFrame = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.dosansenCntNameLb = tkinter.Label(self.txtFrame, text="土讃線情報数", font=("", 20), width=12, borderwidth=1, relief="solid")
        self.dosansenCntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varDosansenCnt = tkinter.IntVar()
        self.varDosansenCnt.set(len(self.dosansenList))
        self.dosansenCntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varDosansenCnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.dosansenCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.dosansenCntBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editDosansenCnt(self.varDosansenCnt.get()))
        self.dosansenCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.dosansenList)):
            self.txtFrame2 = ttk.Frame(scrollbarFrame.frame)
            self.txtFrame2.pack(anchor=tkinter.NW, pady=5, fill=tkinter.BOTH)

            dosansenInfo = self.dosansenList[i]
            self.tempBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editDosansenList, i, dosansenInfo))
            self.tempBtn.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.startLb = tkinter.Label(self.txtFrame2, text="始め", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.startLb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
            self.endLb = tkinter.Label(self.txtFrame2, text="着地", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.endLb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.ele1Lb = tkinter.Label(self.txtFrame2, text="e1", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.ele1Lb.grid(row=i + 2, column=1, sticky=tkinter.W + tkinter.E)
            self.endLb = tkinter.Label(self.txtFrame2, text="anime", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.endLb.grid(row=i + 3, column=1, sticky=tkinter.W + tkinter.E)
            self.ele2Lb = tkinter.Label(self.txtFrame2, text="e2", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.ele2Lb.grid(row=i + 4, column=1, sticky=tkinter.W + tkinter.E)
            self.f1Lb = tkinter.Label(self.txtFrame2, text="f1", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.f1Lb.grid(row=i + 5, column=1, sticky=tkinter.W + tkinter.E)
            for j in range(len(dosansenInfo)):
                if j in [0, 1, 2]:
                    self.varTempH = tkinter.IntVar()
                    self.varTempH.set(int(dosansenInfo[j]))
                    self.temphTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i, column=2 + j, sticky=tkinter.W + tkinter.E)
                elif j in [3, 4, 5]:
                    self.varTempH = tkinter.IntVar()
                    self.varTempH.set(int(dosansenInfo[j]))
                    self.temphTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i + 1, column=j - 1, sticky=tkinter.W + tkinter.E)
                elif j == 6:
                    self.varTempH = tkinter.IntVar()
                    self.varTempH.set(int(dosansenInfo[j]))
                    self.temphTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i + 2, column=j - 4, sticky=tkinter.W + tkinter.E)
                elif j in [7, 8, 9, 10]:
                    self.varTempH = tkinter.DoubleVar()
                    self.varTempH.set(round(float(dosansenInfo[j]), 3))
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=i + 3, column=j - 5, sticky=tkinter.W + tkinter.E)
                elif j == 11:
                    self.varTempH = tkinter.IntVar()
                    self.varTempH.set(int(dosansenInfo[j]))
                    self.temphTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i + 4, column=j - 9, sticky=tkinter.W + tkinter.E)
                elif j == 12:
                    self.varTempH = tkinter.DoubleVar()
                    self.varTempH.set(round(float(dosansenInfo[j]), 3))
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTempH, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=i + 5, column=j - 10, sticky=tkinter.W + tkinter.E)

    def editDosansenCnt(self, val):
        result = EditDosansenCntWidget(self.frame, "土讃線情報数の変更", self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveDosansenCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="土讃線情報数を修正しました")
            self.reloadFunc()

    def editDosansenList(self, i, valList):
        result = EditDosansenWidget(self.frame, "土讃線情報の変更", self.decryptFile, valList)
        if result.reloadFlag:
            self.dosansenList[i] = result.resultValueList
            if not self.decryptFile.saveDosansenList(self.dosansenList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="土讃線情報を修正しました")
            self.reloadFunc()


class EditDosansenCntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditDosansenCntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varDosansenCnt = tkinter.IntVar()
        self.varDosansenCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varDosansenCnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varDosansenCnt.get())
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


class EditDosansenWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, dosansenInfo):
        self.decryptFile = decryptFile
        self.dosansenInfo = dosansenInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditDosansenWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        dosansenInfoLbList = [
            "始めレールNo",
            "始めレールPos(from)",
            "始めレールPos(to)",
            "着地レールNo",
            "着地レールPos(from)",
            "着地レールPos(to)",
            "e1",
            "anime_f1",
            "anime_f2",
            "anime_f3",
            "anime_f4",
            "e2",
            "f1"
        ]
        for i in range(len(self.dosansenInfo)):
            self.stationLb = ttk.Label(master, text=dosansenInfoLbList[i], font=("", 14))
            self.stationLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i in [7, 8, 9, 10, 12]:
                self.varDosansen = tkinter.DoubleVar()
                self.varDosansen.set(round(float(self.dosansenInfo[i]), 3))
            else:
                self.varDosansen = tkinter.IntVar()
                self.varDosansen.set(self.dosansenInfo[i])
            self.varList.append(self.varDosansen)
            self.dosansenEt = ttk.Entry(master, textvariable=self.varDosansen, font=("", 14))
            self.dosansenEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i in [7, 8, 9, 10, 12]:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())
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
