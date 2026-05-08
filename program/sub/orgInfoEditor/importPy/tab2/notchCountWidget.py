import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class NotchCountWidget(tkinter.Frame):
    def __init__(self, frame, trainIndex, notchNum, decryptFile, rootFrameAppearance, reloadWidget):
        super().__init__(frame)
        self.trainIndex = trainIndex
        self.notchNum = notchNum
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget

        notchCountFrame = ttkCustomWidget.CustomTtkFrame(self)
        notchCountFrame.pack(expand=True, fill=tkinter.BOTH)

        notchCountLb = ttkCustomWidget.CustomTtkLabel(notchCountFrame, text=textSetting.textList["orgInfoEditor"]["notchLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=8, borderwidth=1, relief="solid")
        notchCountLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        notchCountTextLb = ttkCustomWidget.CustomTtkLabel(notchCountFrame, text=self.notchNum, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        notchCountTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        notchCountBtn = ttkCustomWidget.CustomTtkButton(notchCountFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=self.editNotchCount)
        notchCountBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editNotchCount(self):
        if self.notchNum not in [4, 5, 12]:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E23"].format(self.notchNum))
            return

        result = EditNotchCountDialog(self.winfo_toplevel(), textSetting.textList["orgInfoEditor"]["editNotchLabel"], self.trainIndex, self.notchNum, self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadWidget()


class EditNotchCountDialog(CustomSimpleDialog):
    def __init__(self, master, title, trainIndex, notchNum, decryptFile, rootFrameAppearance):
        self.trainIndex = trainIndex
        self.notchNum = notchNum
        self.decryptFile = decryptFile
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        if self.notchNum == 4:
            notchIdx = 0
        elif self.notchNum == 5:
            notchIdx = 1
        elif self.notchNum == 12:
            notchIdx = 2

        self.notchLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I57"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
        self.notchLb.grid(row=0, column=0)
        notchList = textSetting.textList["orgInfoEditor"]["editNotchList"]
        self.notchCb = ttkCustomWidget.CustomTtkCombobox(master, width=12, value=notchList, state="readonly", font=textSetting.textList["font2"])
        self.notchCb.current(notchIdx)
        self.notchCb.grid(row=1, column=0)
        super().body(master)

    def validate(self):
        if self.decryptFile.game in ["LS", "BS"]:
            if self.notchCb.current() == 2:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E23"].format(12))
                return False

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I58"])
        if not result:
            return

        newNotchNum = -1
        notchIdx = self.notchCb.current()
        if notchIdx == 0:
            newNotchNum = 4
        elif notchIdx == 1:
            newNotchNum = 5
        elif notchIdx == 2:
            newNotchNum = 12

        if not self.decryptFile.saveNotchInfo(self.trainIndex, newNotchNum):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return False
        return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I59"])
        self.reloadFlag = True
