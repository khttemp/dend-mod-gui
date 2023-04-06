import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

LS = 0
BS = 1
CS = 2
RS = 3


class HurikoWidget():
    def __init__(self, root, cbIdx, i, perfCnt, frame, huriko, decryptFile, varList, btnList, defaultData):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData

        self.hurikoNameLb = tkinter.Label(frame, text=self.decryptFile.trainHurikoNameList[i], font=("", 20), width=24, borderwidth=1, relief="solid")
        self.hurikoNameLb.grid(row=perfCnt + i, column=0, sticky=tkinter.W + tkinter.E)
        self.varHuriko = tkinter.IntVar()
        self.varHuriko.set(str(huriko[i]))
        self.varList.append(self.varHuriko)
        self.hurikoLb = tkinter.Label(frame, textvariable=self.varHuriko, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.hurikoLb.grid(row=perfCnt + i, column=1, sticky=tkinter.W + tkinter.E)
        self.hurikoBtn = tkinter.Button(frame, text="修正", font=("", 14), command=lambda: self.editVar([self.hurikoNameLb, self.hurikoLb], self.varHuriko, self.varHuriko.get(), self.defaultData[self.cbIdx]["huriko"][i]), state="disabled")
        self.hurikoBtn.grid(row=perfCnt + i, column=2, sticky=tkinter.W + tkinter.E)
        self.btnList.append(self.hurikoBtn)

        color = ""
        if self.defaultData[self.cbIdx]["huriko"][i] < huriko[i]:
            color = "red"
        elif self.defaultData[self.cbIdx]["huriko"][i] > huriko[i]:
            color = "blue"
        else:
            color = "black"
        self.hurikoNameLb["fg"] = color
        self.hurikoLb["fg"] = color

    def editVar(self, labelList, var, value, defaultValue, flag=True):
        EditHurikoVarInfo(self.root, "値変更", labelList, var, value, defaultValue)


class EditHurikoVarInfo(sd.Dialog):
    def __init__(self, master, title, labelList, var, value, defaultValue):
        self.labelList = labelList
        self.var = var
        self.value = value
        self.defaultValue = defaultValue
        super(EditHurikoVarInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        self.defaultLb = tkinter.Label(frame, text="デフォルトの値＝" + str(self.defaultValue), font=("", 14))
        self.defaultLb.pack()

        sep = ttk.Separator(frame, orient='horizontal')
        sep.pack(fill=tkinter.X, ipady=5)

        self.inputLb = tkinter.Label(frame, text="値を入力してください", font=("", 14))
        self.inputLb.pack()

        v_val = tkinter.StringVar()
        v_val.set(self.value)
        self.inputEt = tkinter.Entry(frame, textvariable=v_val, font=("", 14))
        self.inputEt.pack()

    def validate(self):
        result = self.inputEt.get()
        if result:
            try:
                try:
                    result = int(result)
                    self.var.set(result)
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="整数エラー", message=errorMsg)
                    return False
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

            if self.defaultValue is not None:
                color = ""
                if self.defaultValue < result:
                    color = "red"
                elif self.defaultValue > result:
                    color = "blue"
                else:
                    color = "black"

                for label in self.labelList:
                    label["fg"] = color
            return True
