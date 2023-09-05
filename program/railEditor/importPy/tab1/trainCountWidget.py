import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting


class TrainCountWidget:
    def __init__(self, frame, decryptFile, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc

        self.txtFrame = tkinter.Frame(self.frame, padx=10, pady=5)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.trainCntLb = tkinter.Label(self.txtFrame, text=textSetting.textList["railEditor"]["trainCount"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.trainCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varTrainCnt = tkinter.IntVar()
        self.varTrainCnt.set(self.decryptFile.trainCnt)
        self.trainCntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varTrainCnt, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.trainCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.trainCntBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar(self.varTrainCnt.get()))
        self.trainCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditTrainCountWidget(self.frame, textSetting.textList["railEditor"]["editTrainCountLabel"], self.decryptFile, value)

        if result.reloadFlag:
            if not self.decryptFile.saveTrainCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I72"])

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

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.pack()

        self.varTrainCnt = tkinter.IntVar()
        self.varTrainCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varTrainCnt, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varTrainCnt.get())
                    if res <= 0:
                        errorMsg = textSetting.textList["errorList"]["E61"].format(1)
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
                    self.resultValue = res
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E60"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return False
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

            if self.resultValue < self.val:
                msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
                result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True
