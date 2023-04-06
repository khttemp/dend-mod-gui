from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


class StationWidget:
    def __init__(self, frame, decryptFile, stationList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.stationList = stationList
        self.reloadFunc = reloadFunc

        self.stationLf = ttk.LabelFrame(self.frame, text="駅名標位置情報")
        self.stationLf.pack(anchor=tkinter.NW, padx=10, pady=5)

        self.txtFrame = ttk.Frame(self.stationLf)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.stationCntLb = tkinter.Label(self.txtFrame, text="駅名標位置数", font=("", 20), width=12, borderwidth=1, relief="solid")
        self.stationCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varStationCnt = tkinter.IntVar()
        self.varStationCnt.set(len(self.decryptFile.stationList))
        self.stationCntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varStationCnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.stationCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.stationCntBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editStationCnt(self.varStationCnt.get()))
        self.stationCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.txtFrame2 = ttk.Frame(self.stationLf)
        self.txtFrame2.pack(anchor=tkinter.NW)

        if len(self.decryptFile.stationList) > 0:
            self.constLb = tkinter.Label(self.txtFrame2, text="const0", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.constLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.ambLb = tkinter.Label(self.txtFrame2, text="AMB番号", font=("", 20), width=9, borderwidth=1, relief="solid")
            self.ambLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.ambChildLb = tkinter.Label(self.txtFrame2, text="AMB子番号", font=("", 20), width=10, borderwidth=1, relief="solid")
            self.ambChildLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
            self.eleLb = tkinter.Label(self.txtFrame2, text="ele", font=("", 20), width=7, borderwidth=1, relief="solid")
            self.eleLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)
            self.pngNumLb = tkinter.Label(self.txtFrame2, text="画像番号", font=("", 20), width=9, borderwidth=1, relief="solid")
            self.pngNumLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.decryptFile.stationList)):
            stationInfo = self.decryptFile.stationList[i]
            for j in range(len(stationInfo)):
                self.varStation = tkinter.IntVar()
                self.varStation.set(stationInfo[j])
                self.varStationLb = tkinter.Label(self.txtFrame2, textvariable=self.varStation, font=("", 20), borderwidth=1, relief="solid")
                self.varStationLb.grid(row=i + 1, column=j, sticky=tkinter.W + tkinter.E)
            self.varBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editStation, i, stationInfo))
            self.varBtn.grid(row=i + 1, column=len(stationInfo), sticky=tkinter.W + tkinter.E)

    def editStationCnt(self, val):
        result = EditStationCntWidget(self.frame, "駅名標数の変更", self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveStationCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名標数を修正しました")
            self.reloadFunc()

    def editStation(self, i, stationInfo):
        result = EditStationWidget(self.frame, "駅名標情報の変更", self.decryptFile, stationInfo)
        if result.reloadFlag:
            self.stationList[i] = result.resultValueList
            if not self.decryptFile.saveStation(self.stationList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名標情報を修正しました")
            self.reloadFunc()


class EditStationCntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditStationCntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varStationCnt = tkinter.IntVar()
        self.varStationCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varStationCnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varStationCnt.get())
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


class EditStationWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, stationInfo):
        self.decryptFile = decryptFile
        self.stationInfo = stationInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditStationWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        stationInfoLbList = ["const0", "AMB番号", "AMB子番号", "ele", "画像番号"]
        for i in range(len(self.stationInfo)):
            self.stationLb = ttk.Label(master, text=stationInfoLbList[i], font=("", 14))
            self.stationLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.varStation = tkinter.IntVar()
            self.varStation.set(self.stationInfo[i])
            self.varList.append(self.varStation)
            self.stationEt = ttk.Entry(master, textvariable=self.varStation, font=("", 14))
            self.stationEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        res = int(self.varList[i].get())
                        self.resultValueList.append(res)
                    return True
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
