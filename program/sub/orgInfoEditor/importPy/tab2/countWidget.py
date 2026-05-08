import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class CountWidget(tkinter.Frame):
    def __init__(self, frame, trainIndex, decryptFile, rootFrameAppearance, reloadWidget):
        super().__init__(frame)
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget

        self.modelInfo = self.decryptFile.trainModelList[self.trainIndex]

        countFrame = ttkCustomWidget.CustomTtkFrame(frame)
        countFrame.pack()

        henseiLb = ttkCustomWidget.CustomTtkLabel(countFrame, text=textSetting.textList["orgInfoEditor"]["csvOrgNumTitle"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=8, borderwidth=1, relief="solid")
        henseiLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        henseiTextLb = ttkCustomWidget.CustomTtkLabel(countFrame, text=self.modelInfo["mdlCnt"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        henseiTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        henseiBtn = ttkCustomWidget.CustomTtkButton(countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=self.editHenseiCount)
        henseiBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        colorLb = ttkCustomWidget.CustomTtkLabel(countFrame, text=textSetting.textList["orgInfoEditor"]["colorCnt"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=8, borderwidth=1, relief="solid")
        colorLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        colorTextLb = ttkCustomWidget.CustomTtkLabel(countFrame, text=self.modelInfo["colorCnt"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        colorTextLb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
        if decryptFile.game in ["CS", "RS"]:
            colorBtn = ttkCustomWidget.CustomTtkButton(countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=self.editColorCount)
            colorBtn.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)

        if decryptFile.game in ["LS", "BS"]:
            daishaCountText = textSetting.textList["orgInfoEditor"]["trackCnt"]
            daishaCountText = daishaCountText[:5] + "\n" + daishaCountText[5:]
            daishaLb = ttkCustomWidget.CustomTtkLabel(countFrame, text=daishaCountText, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=8, borderwidth=1, relief="solid")
            daishaLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
            daishaTextLb = ttkCustomWidget.CustomTtkLabel(countFrame, text=self.modelInfo["daishaCnt"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            daishaTextLb.grid(row=2, column=1, sticky=tkinter.NSEW)
            daishaBtn = ttkCustomWidget.CustomTtkButton(countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=self.editDaishaCount)
            daishaBtn.grid(row=2, column=2, sticky=tkinter.NSEW)

    def editHenseiCount(self):
        result = EditHenseiCountDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.trainIndex, self.modelInfo["mdlCnt"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadWidget()

    def editColorCount(self):
        result = EditColorCountDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.trainIndex, self.modelInfo["colorCnt"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadWidget()

    def editDaishaCount(self):
        result = EditDaishaCountDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.trainIndex, self.modelInfo["daishaCnt"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadWidget()


class EditHenseiCountDialog(CustomSimpleDialog):
    def __init__(self, master, title, trainIndex, henseiCount, decryptFile, rootFrameAppearance):
        self.trainIndex = trainIndex
        self.henseiCount = henseiCount
        self.decryptFile = decryptFile
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()
        self.varHenseiCount = tkinter.IntVar()
        self.varHenseiCount.set(self.henseiCount)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varHenseiCount, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

    def validate(self):
        try:
            try:
                resultValue = int(self.varHenseiCount.get())
            except Exception:
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E60"])
                return

            if resultValue <= 0:
                errorMsg = textSetting.textList["errorList"]["E61"].format(1)
                mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                return

            if resultValue < self.henseiCount:
                msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
                result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
                if not result:
                    return

            if not self.decryptFile.saveHenseiNum(self.trainIndex, resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I55"])
        self.reloadFlag = True


class EditColorCountDialog(CustomSimpleDialog):
    def __init__(self, master, title, trainIndex, colorCount, decryptFile, rootFrameAppearance):
        self.trainIndex = trainIndex
        self.colorCount = colorCount
        self.decryptFile = decryptFile
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()
        self.varColorCount = tkinter.IntVar()
        self.varColorCount.set(self.colorCount)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varColorCount, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

    def validate(self):
        try:
            try:
                resultValue = int(self.varColorCount.get())
            except Exception:
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E60"])
                return

            if resultValue < 0:
                errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                return

            if not self.decryptFile.saveColor(self.trainIndex, resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I56"])
        self.reloadFlag = True


class EditDaishaCountDialog(CustomSimpleDialog):
    def __init__(self, master, title, trainIndex, daishaCount, decryptFile, rootFrameAppearance):
        self.trainIndex = trainIndex
        self.daishaCount = daishaCount
        self.decryptFile = decryptFile
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()
        self.varDaishaCount = tkinter.IntVar()
        self.varDaishaCount.set(self.daishaCount)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varDaishaCount, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

    def validate(self):
        try:
            try:
                resultValue = int(self.varDaishaCount.get())
            except Exception:
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E60"])
                return

            if not self.decryptFile.saveDaishaCnt(self.trainIndex, resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])
        self.reloadFlag = True
