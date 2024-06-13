import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class TrainCountWidget:
    def __init__(self, root, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        txtFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        txtFrame.pack(anchor=tkinter.NW, padx=10, pady=5)

        trainCntLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["railEditor"]["trainCount"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        trainCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varTrainCnt = tkinter.IntVar()
        self.varTrainCnt.set(self.decryptFile.trainCnt)
        if not (self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag):
            trainCntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varTrainCnt, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            trainCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            trainCntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar(self.varTrainCnt.get()))
            trainCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        else:
            trainCntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=self.varTrainCnt.get(), font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            trainCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditTrainCountWidget(self.root, textSetting.textList["railEditor"]["editTrainCountLabel"], self.decryptFile, value, self.rootFrameAppearance)

        if result.reloadFlag:
            if not self.decryptFile.saveTrainCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I72"])

            self.reloadFunc()


class EditTrainCountWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, val, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = val
        self.reloadFlag = False
        self.resultValue = 0
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()

        self.varTrainCnt = tkinter.IntVar()
        self.varTrainCnt.set(self.val)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varTrainCnt, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

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
