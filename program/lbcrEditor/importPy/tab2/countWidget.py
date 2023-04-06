import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

LS = 0
BS = 1
CS = 2
RS = 3


class CountWidget():
    def __init__(self, root, trainIdx, game, frame, decryptFile, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.reloadFunc = reloadFunc

        index = self.decryptFile.indexList[self.trainIdx]
        notchNum = self.decryptFile.byteArr[index]

        modelInfo = self.decryptFile.trainModelList[self.trainIdx]

        self.countFrame = ttk.Frame(self.frame)
        self.countFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=15, pady=5)

        self.notchLb = tkinter.Label(self.countFrame, text="ノッチ", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.notchLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varNotch = tkinter.IntVar()
        self.varNotch.set(notchNum)
        self.notchTextLb = tkinter.Label(self.countFrame, textvariable=self.varNotch, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.notchTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.notchBtn = tkinter.Button(self.countFrame, text="修正", font=("", 14), command=lambda: self.editNotchVar(self.varNotch, self.varNotch.get()))
        self.notchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.henseiLb = tkinter.Label(self.countFrame, text="編成数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.henseiLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.varHensei = tkinter.IntVar()
        self.varHensei.set(modelInfo["mdlCnt"])
        self.henseiTextLb = tkinter.Label(self.countFrame, textvariable=self.varHensei, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.henseiTextLb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
        self.henseiBtn = tkinter.Button(self.countFrame, text="修正", font=("", 14), command=lambda: self.editHenseiVar(self.varHensei, self.varHensei.get()))
        self.henseiBtn.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)

        self.colorLb = tkinter.Label(self.countFrame, text="カラー数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.colorLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
        self.varColor = tkinter.IntVar()
        self.varColor.set(modelInfo["colorCnt"])
        self.colorTextLb = tkinter.Label(self.countFrame, textvariable=self.varColor, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.colorTextLb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)
        self.colorBtn = tkinter.Button(self.countFrame, text="修正", font=("", 14), command=lambda: self.editVar(self.varColor, self.varColor.get()))
        self.colorBtn.grid(row=2, column=2, sticky=tkinter.W + tkinter.E)

    def editNotchVar(self, var, value):
        result = EditNotchInfo(self.root, "ノッチ情報修正", self.trainIdx, self.game, self.decryptFile, self.notchContentCnt)
        if result.reloadFlag:
            self.reloadFunc()

    def editHenseiVar(self, var, value):
        resultValue = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if resultValue:
            try:
                try:
                    resultValue = int(resultValue)
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return

                if resultValue <= 0:
                    errorMsg = "1以上の数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return

                if resultValue < value:
                    msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                    result = mb.askokcancel(title="警告", message=msg, icon="warning")
                    if not result:
                        return

                if not self.decryptFile.saveHenseiNum(self.trainIdx, resultValue):
                    self.decryptFile.printError()
                    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False

                mb.showinfo(title="成功", message="編成数を修正しました")
                self.reloadFunc()
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def editVar(self, var, value):
        if self.game in [LS, BS]:
            if self.game == LS:
                errorMsg = "LSはカラー数修正をサポートしません"
            else:
                errorMsg = "BSカラー修正はCSVで行ってください"
            mb.showerror(title="エラー", message=errorMsg)
            return
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if result:
            try:
                try:
                    result = int(result)
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return

                if result < 0:
                    errorMsg = "0以上の数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return

                if not self.decryptFile.saveColor(self.trainIdx, result):
                    self.decryptFile.printError()
                    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False

                mb.showinfo(title="成功", message="カラー数を修正しました")
                self.reloadFunc()

            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)


class EditNotchInfo(sd.Dialog):
    def __init__(self, master, title, trainIdx, game, decryptFile, notchContentCnt):
        self.trainIdx = trainIdx
        self.game = game
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.reloadFlag = False
        super(EditNotchInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        index = self.decryptFile.indexList[self.trainIdx]
        notchNum = self.decryptFile.byteArr[index]

        if notchNum == 4:
            notchIdx = 0
        elif notchNum == 5:
            notchIdx = 1
        elif notchNum == 12:
            notchIdx = 2

        self.notchLb = tkinter.Label(frame, text="ノッチ情報を修正してください")
        self.notchLb.grid(row=0, column=0)
        notchList = ["４ノッチ", "５ノッチ", "１２ノッチ"]
        self.notchCb = ttk.Combobox(frame, width=12, value=notchList, state="readonly")
        self.notchCb.current(notchIdx)
        self.notchCb.grid(row=1, column=0)

    def validate(self):
        if self.game <= BS:
            if self.notchCb.current() == 2:
                mb.showerror(title="エラー", message="12ノッチを対応できません")
                return False
        warnMsg = "ノッチ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            newNotchNum = -1
            notchIdx = self.notchCb.current()
            if notchIdx == 0:
                newNotchNum = 4
            elif notchIdx == 1:
                newNotchNum = 5
            elif notchIdx == 2:
                newNotchNum = 12

            if not self.decryptFile.saveNotchInfo(self.trainIdx, newNotchNum):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            else:
                return True

    def apply(self):
        mb.showinfo(title="成功", message="ノッチ数を変更しました")
        self.reloadFlag = True
