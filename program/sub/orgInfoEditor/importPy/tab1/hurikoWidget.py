from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class HurikoWidget(tkinter.Frame):
    def __init__(self, frame, decryptFile, hurikoName, hurikoValue, defaultValue, rootFrameAppearance):
        super().__init__(frame)
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance

        hurikoFrame = ttkCustomWidget.CustomTtkFrame(self)
        hurikoFrame.pack(expand=True, fill=tkinter.BOTH)

        self.hurikoNameLb = ttkCustomWidget.CustomTtkLabel(hurikoFrame, text=hurikoName, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.hurikoNameLb.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.hurikoValue = hurikoValue
        self.varHuriko = tkinter.IntVar()
        self.varHuriko.set(self.hurikoValue)
        self.hurikoLb = ttkCustomWidget.CustomTtkLabel(hurikoFrame, textvariable=self.varHuriko, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.hurikoLb.grid(row=0, column=1, sticky=tkinter.NSEW)
        self.hurikoBtn = ttkCustomWidget.CustomTtkButton(hurikoFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVar, defaultValue), state="disabled")
        self.hurikoBtn.grid(row=0, column=2, sticky=tkinter.NSEW, padx=(0, 10))
        self.setLabelColor(self.hurikoNameLb, self.hurikoLb, hurikoValue, defaultValue)

        hurikoFrame.grid_columnconfigure(0, weight=4, uniform="perf")
        hurikoFrame.grid_columnconfigure(1, weight=1, uniform="perf")

    def setLabelColor(self, nameLabel, label, value, defaultValue):
        color = ""
        if value > defaultValue:
            color = "red"
        elif value < defaultValue:
            color = "blue"
        nameLabel.setFgColor(color)
        label.setFgColor(color)

    def editVar(self, defaultValue):
        result = EditHurikoVarInfo(self.winfo_toplevel(), textSetting.textList["orgInfoEditor"]["valueModify"], self.hurikoValue, defaultValue, self.rootFrameAppearance)
        if result.inputFlag:
            self.hurikoValue = result.resultValue
            self.varHuriko.set(self.hurikoValue)
            self.setLabelColor(self.hurikoNameLb, self.hurikoLb, self.hurikoValue, defaultValue)


class EditHurikoVarInfo(CustomSimpleDialog):
    def __init__(self, master, title, value, defaultValue, rootFrameAppearance):
        self.value = value
        self.defaultValue = defaultValue
        self.resultValue = None
        self.inputFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        self.defaultLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(self.defaultValue), font=textSetting.textList["font2"])
        self.defaultLb.pack()

        sep = ttkCustomWidget.CustomTtkSeparator(master, orient="horizontal")
        sep.pack(fill=tkinter.X, ipady=5)

        self.inputLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.inputLb.pack()

        self.v_val = tkinter.StringVar()
        self.v_val.set(self.value)
        self.inputEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_val, font=textSetting.textList["font2"])
        self.inputEt.pack()
        super().body(master)

    def validate(self):
        result = self.inputEt.get()
        if result:
            try:
                try:
                    self.resultValue = int(result)
                except ValueError:
                    mb.showerror(title=textSetting.textList["intError"], message=textSetting.textList["errorList"]["E60"])
                    return False
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        self.inputFlag = True
