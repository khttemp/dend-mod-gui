from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class NotchWidget(tkinter.Frame):
    def __init__(self, root, frame, notchIndex, decryptFile, notchCnt, speed, defaultData, rootFrameAppearance):
        super().__init__(frame)
        self.root = root
        self.notchIndex = notchIndex
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance

        notchFrame = ttkCustomWidget.CustomTtkFrame(self)
        notchFrame.pack(expand=True, fill=tkinter.BOTH)

        rowSpanNum = decryptFile.notchContentCnt
        self.notchNum = textSetting.textList["orgInfoEditor"]["notchLabel"] + str(notchIndex + 1)
        self.notchNumLb = ttkCustomWidget.CustomTtkLabel(notchFrame, text=self.notchNum, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.notchNumLb.grid(rowspan=rowSpanNum, row=0, column=0, sticky=tkinter.NSEW)

        self.speedValue = speed[notchIndex]
        if notchIndex >= len(defaultData["notch"]):
            speedDefaultValue = None
        else:
            speedDefaultValue = defaultData["notch"][notchIndex]

        self.speedNameLb = ttkCustomWidget.CustomTtkLabel(notchFrame, text=textSetting.textList["orgInfoEditor"]["csvNotchSpeed"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.speedNameLb.grid(row=0, column=1, sticky=tkinter.NSEW)
        self.varSpeed = tkinter.DoubleVar()
        self.varSpeed.set(self.speedValue)

        self.speedLb = ttkCustomWidget.CustomTtkLabel(notchFrame, textvariable=self.varSpeed, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.speedLb.grid(row=0, column=2, sticky=tkinter.NSEW)
        self.speedBtn = ttkCustomWidget.CustomTtkButton(notchFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editSpeedVar, speedDefaultValue), state="disabled")
        self.speedBtn.grid(row=0, column=3, sticky=tkinter.NSEW, padx=(0, 10))
        self.setLabelColor(self.speedNameLb, self.speedLb, self.speedValue, speedDefaultValue)

        self.tlkValue = speed[notchCnt + notchIndex]
        if notchIndex >= len(defaultData["tlk"]):
            tlkDefaultValue = None
        else:
            tlkDefaultValue = defaultData["tlk"][notchIndex]

        self.tlkNameLb = ttkCustomWidget.CustomTtkLabel(notchFrame, text=textSetting.textList["orgInfoEditor"]["csvNotchTlk"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.tlkNameLb.grid(row=1, column=1, sticky=tkinter.NSEW)
        self.varTlk = tkinter.DoubleVar()
        self.varTlk.set(self.tlkValue)
        self.tlkLb = ttkCustomWidget.CustomTtkLabel(notchFrame, textvariable=self.varTlk, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.tlkLb.grid(row=1, column=2, sticky=tkinter.NSEW)
        self.tlkBtn = ttkCustomWidget.CustomTtkButton(notchFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editTlkVar, tlkDefaultValue), state="disabled")
        self.tlkBtn.grid(row=1, column=3, sticky=tkinter.NSEW, padx=(0, 10))
        self.setLabelColor(self.tlkNameLb, self.tlkLb, self.tlkValue, tlkDefaultValue)

        if decryptFile.notchContentCnt > 2:
            self.soundValue = speed[notchCnt*2 + notchIndex]
            if notchIndex >= len(defaultData["soundNum"]):
                soundDefaultValue = None
            else:
                soundDefaultValue = defaultData["soundNum"][notchIndex]

            self.soundNameLb = ttkCustomWidget.CustomTtkLabel(notchFrame, text=textSetting.textList["orgInfoEditor"]["csvNotchSound"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.soundNameLb.grid(row=2, column=1, sticky=tkinter.NSEW)
            self.varSound = tkinter.IntVar()
            self.varSound.set(self.soundValue)
            self.soundLb = ttkCustomWidget.CustomTtkLabel(notchFrame, textvariable=self.varSound, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.soundLb.grid(row=2, column=2, sticky=tkinter.NSEW)
            self.soundBtn = ttkCustomWidget.CustomTtkButton(notchFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editSoundVar, soundDefaultValue), state="disabled")
            self.soundBtn.grid(row=2, column=3, sticky=tkinter.NSEW, padx=(0, 10))
            self.setLabelColor(self.soundNameLb, self.soundLb, self.soundValue, soundDefaultValue)

            self.addValue = speed[notchCnt*3 + notchIndex]
            if notchIndex >= len(defaultData["add"]):
                addDefaultValue = None
            else:
                addDefaultValue = defaultData["add"][notchIndex]

            self.addNameLb = ttkCustomWidget.CustomTtkLabel(notchFrame, text=textSetting.textList["orgInfoEditor"]["csvNotchAdd"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.addNameLb.grid(row=3, column=1, sticky=tkinter.NSEW)
            self.varAdd = tkinter.DoubleVar()
            self.varAdd.set(self.addValue)
            self.addLb = ttkCustomWidget.CustomTtkLabel(notchFrame, textvariable=self.varAdd, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.addLb.grid(row=3, column=2, sticky=tkinter.NSEW)
            self.addBtn = ttkCustomWidget.CustomTtkButton(notchFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editAddVar, addDefaultValue), state="disabled")
            self.addBtn.grid(row=3, column=3, sticky=tkinter.NSEW, padx=(0, 10))
            self.setLabelColor(self.addNameLb, self.addLb, self.addValue, addDefaultValue)

        notchFrame.grid_columnconfigure(0, weight=3, uniform="notch")
        notchFrame.grid_columnconfigure(1, weight=2, uniform="notch")
        notchFrame.grid_columnconfigure(2, weight=2, uniform="notch")

    def setLabelColor(self, nameLabel, label, value, defaultValue):
        if defaultValue is None:
            color = "green"
        else:
            if value > defaultValue:
                color = "red"
            elif value < defaultValue:
                color = "blue"
            else:
                color = ""
        nameLabel.setFgColor(color)
        label.setFgColor(color)

    def editSpeedVar(self, defaultValue):
        result = EditNotchVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], self.speedValue, defaultValue, self.rootFrameAppearance)
        if result.inputFlag:
            self.speedValue = result.resultValue
            self.varSpeed.set(self.speedValue)
            self.setLabelColor(self.speedNameLb, self.speedLb, self.speedValue, defaultValue)

    def editTlkVar(self, defaultValue):
        tabFrame = self.root.master.winfo_children()[4]
        notchPerfFrame = tabFrame.winfo_children()[2]
        perfLf = notchPerfFrame.winfo_children()[1]
        scrollbarframe = perfLf.winfo_children()[0]
        canvas = scrollbarframe.winfo_children()[1]
        interior = canvas.winfo_children()[0]

        noneTlkIndex = self.decryptFile.trainPerfNameList.index("None_Tlk")
        noneTlkWidget = interior.winfo_children()[noneTlkIndex]
        noneTlkWidgetFrame = noneTlkWidget.winfo_children()[0]
        noneTlkWidgetLabel = noneTlkWidgetFrame.winfo_children()[1]
        noneTlkValue = noneTlkWidgetLabel.getvar(noneTlkWidgetLabel.cget("textvariable"))
        weightIndex = self.decryptFile.trainPerfNameList.index("Weight")
        weightWidget = interior.winfo_children()[weightIndex]
        weightWidgetFrame = weightWidget.winfo_children()[0]
        weightWidgetLabel = weightWidgetFrame.winfo_children()[1]
        weightValue = weightWidgetLabel.getvar(weightWidgetLabel.cget("textvariable"))

        result = EditNotchVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], self.tlkValue, defaultValue, self.rootFrameAppearance, calcFlag=True, notchIndex=self.notchIndex, noneTlkValue=noneTlkValue, weightValue=weightValue)
        if result.inputFlag:
            self.tlkValue = result.resultValue
            self.varTlk.set(self.tlkValue)
            self.setLabelColor(self.tlkNameLb, self.tlkLb, self.tlkValue, defaultValue)

    def editSoundVar(self, defaultValue):
        result = EditNotchVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], self.soundValue, defaultValue, self.rootFrameAppearance, isSound=True)
        if result.inputFlag:
            self.soundValue = result.resultValue
            self.varSound.set(self.soundValue)
            self.setLabelColor(self.soundNameLb, self.soundLb, self.soundValue, defaultValue)

    def editAddVar(self, defaultValue):
        result = EditNotchVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], self.addValue, defaultValue, self.rootFrameAppearance)
        if result.inputFlag:
            self.addValue = result.resultValue
            self.varAdd.set(self.addValue)
            self.setLabelColor(self.addNameLb, self.addLb, self.addValue, defaultValue)


class EditNotchVarInfo(CustomSimpleDialog):
    def __init__(self, master, title, value, defaultValue, rootFrameAppearance, isSound=False, calcFlag=False, notchIndex=None, noneTlkValue=None, weightValue=None):
        self.master = master
        self.value = value
        self.defaultValue = defaultValue
        self.isSound = isSound
        self.calcFlag = calcFlag
        self.notchIndex = notchIndex
        self.noneTlkValue = noneTlkValue
        self.weightValue = weightValue
        self.resultValue = None
        self.inputFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        self.defaultLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(self.defaultValue), font=textSetting.textList["font2"])
        self.defaultLb.pack()

        sep = ttkCustomWidget.CustomTtkSeparator(master, orient="horizontal")
        sep.pack(fill=tkinter.X, ipady=5)

        self.v_calcMinSpeed = tkinter.DoubleVar()
        self.v_calcMinSpeed.set(0.0)
        if self.calcFlag:
            calcMinSpeedLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["calcMinSpeedLabel"].format(self.notchIndex, self.notchIndex + 1), font=textSetting.textList["font2"])
            calcMinSpeedLb.pack()
            calcMinSpeedValue = ttkCustomWidget.CustomTtkLabel(master, textvariable=self.v_calcMinSpeed, font=textSetting.textList["font2"])
            calcMinSpeedValue.pack()
            sep = ttkCustomWidget.CustomTtkSeparator(master, orient="horizontal")
            sep.pack(fill=tkinter.X, ipady=5)

        self.inputLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.inputLb.pack()

        self.v_val = tkinter.StringVar()
        self.v_val.set(self.value)
        self.inputEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_val, font=textSetting.textList["font2"])
        self.inputEt.pack()
        if self.calcFlag:
            self.inputEt.bind("<KeyRelease>", self.calcMinSpeedHandler)
            self.calcMinSpeed()
        super().body(master)

    def calcMinSpeedHandler(self, event):
        self.calcMinSpeed()

    def calcMinSpeed(self):
        try:
            inputTlk = float(self.v_val.get())
        except ValueError:
            inputTlk = float(self.value)

        minSpeed = ((self.weightValue - inputTlk) / self.noneTlkValue)
        if minSpeed < 0:
            minSpeed = 0
        minSpeed = round(minSpeed * 60 / 1.11, 3)
        self.v_calcMinSpeed.set(minSpeed)

    def validate(self):
        result = self.inputEt.get()
        if result:
            try:
                if self.isSound:
                    try:
                        self.resultValue = int(result)
                    except ValueError:
                        mb.showerror(title=textSetting.textList["intError"], message=textSetting.textList["errorList"]["E60"])
                        return False
                else:
                    try:
                        self.resultValue = float(result)
                    except ValueError:
                        mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                        return False
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        self.inputFlag = True
