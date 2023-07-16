import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


class TrainCountWidget:
    def __init__(self, frame, decryptFile, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc

        self.txtFrame = tkinter.Frame(self.frame, padx=10, pady=5)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.trainCntLb = tkinter.Label(self.txtFrame, text="車両数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.trainCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varTrainCnt = tkinter.IntVar()
        self.varTrainCnt.set(self.decryptFile.trainCnt)
        self.trainCntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varTrainCnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.trainCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.trainCntBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editVar(self.varTrainCnt.get()))
        self.trainCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditTrainCountWidget(self.frame, "車両数変更", self.decryptFile, value)

        if result.reloadFlag:
            if not self.decryptFile.saveTrainCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="車両数情報を修正しました")

            self.reloadFunc()


class EditTrainCountWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.reloadFlag = False
        self.resultValue = 0
        super(EditTrainCountWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varTrainCnt = tkinter.IntVar()
        self.varTrainCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varTrainCnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varTrainCnt.get())
                    if res <= 0:
                        errorMsg = "1以上の数字で入力してください。"
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
