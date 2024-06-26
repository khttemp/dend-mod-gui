import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class NotchWidget():
    def __init__(self, root, cbIdx, i, notchCnt, frame, speed, decryptFile, notchContentCnt, varList, btnList, defaultData, rootFrameAppearance):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData
        self.rootFrameAppearance = rootFrameAppearance

        self.notchNum = textSetting.textList["orgInfoEditor"]["notchLabel"] + str(i + 1)
        self.notchNumLb = ttkCustomWidget.CustomTtkLabel(frame, text=self.notchNum, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.notchNumLb.grid(rowspan=self.notchContentCnt, row=self.notchContentCnt * i, column=0, sticky=tkinter.NSEW)

        try:
            color = ""
            if self.defaultData[self.cbIdx]["notch"][i] < speed[i]:
                color = "red"
            elif self.defaultData[self.cbIdx]["notch"][i] > speed[i]:
                color = "blue"
            else:
                color = "black"
            speedDefaultValue = self.defaultData[self.cbIdx]["notch"][i]
        except Exception:
            color = "green"
            speedDefaultValue = None

        self.speedNameLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchSpeed"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.speedNameLb.grid(row=self.notchContentCnt * i, column=1, sticky=tkinter.NSEW)
        self.varSpeed = tkinter.DoubleVar()
        self.varSpeed.set(str(speed[i]))

        self.varList.append(self.varSpeed)
        self.speedLb = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.varSpeed, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.speedLb.grid(row=self.notchContentCnt * i, column=2, sticky=tkinter.NSEW)
        self.speedBtn = ttkCustomWidget.CustomTtkButton(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar([self.speedNameLb, self.speedLb], self.varSpeed, self.varSpeed.get(), "speed", i, speedDefaultValue), state="disabled")
        self.speedBtn.grid(row=self.notchContentCnt * i, column=3, sticky=tkinter.NSEW, padx=(0, 10))
        self.btnList.append(self.speedBtn)

        self.speedNameLb.setFgColor(color)
        self.speedLb.setFgColor(color)

        try:
            color = ""
            if self.defaultData[self.cbIdx]["tlk"][i] < speed[notchCnt + i]:
                color = "red"
            elif self.defaultData[self.cbIdx]["tlk"][i] > speed[notchCnt + i]:
                color = "blue"
            else:
                color = "black"
            tlkDefaultValue = self.defaultData[self.cbIdx]["tlk"][i]
        except Exception:
            color = "green"
            tlkDefaultValue = None

        self.tlkNameLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchTlk"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.tlkNameLb.grid(row=self.notchContentCnt * i + 1, column=1, sticky=tkinter.NSEW)
        self.varTlk = tkinter.DoubleVar()
        self.varTlk.set(str(speed[notchCnt + i]))
        self.varList.append(self.varTlk)
        self.tlkLb = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.varTlk, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.tlkLb.grid(row=self.notchContentCnt * i + 1, column=2, sticky=tkinter.NSEW)
        self.tlkBtn = ttkCustomWidget.CustomTtkButton(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar([self.tlkNameLb, self.tlkLb], self.varTlk, self.varTlk.get(), "tlk", i, tlkDefaultValue), state="disabled")
        self.tlkBtn.grid(row=self.notchContentCnt * i + 1, column=3, sticky=tkinter.NSEW, padx=(0, 10))
        self.btnList.append(self.tlkBtn)

        self.tlkNameLb.setFgColor(color)
        self.tlkLb.setFgColor(color)

        if self.notchContentCnt > 2:
            try:
                color = ""
                if self.defaultData[self.cbIdx]["soundNum"][i] < speed[notchCnt * 2 + i]:
                    color = "red"
                elif self.defaultData[self.cbIdx]["soundNum"][i] > speed[notchCnt * 2 + i]:
                    color = "blue"
                else:
                    color = "black"
                soundDefaultValue = self.defaultData[self.cbIdx]["soundNum"][i]
            except Exception:
                color = "green"
                soundDefaultValue = None

            self.soundNameLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchSound"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.soundNameLb.grid(row=self.notchContentCnt * i + 2, column=1, sticky=tkinter.NSEW)
            self.varSound = tkinter.IntVar()
            self.varSound.set(str(speed[notchCnt * 2 + i]))
            self.varList.append(self.varSound)
            self.soundLb = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.varSound, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.soundLb.grid(row=self.notchContentCnt * i + 2, column=2, sticky=tkinter.NSEW)
            self.soundBtn = ttkCustomWidget.CustomTtkButton(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar([self.soundNameLb, self.soundLb], self.varSound, self.varSound.get(), "sound", i, soundDefaultValue, True), state="disabled")
            self.soundBtn.grid(row=self.notchContentCnt * i + 2, column=3, sticky=tkinter.NSEW, padx=(0, 10))
            self.btnList.append(self.soundBtn)

            self.soundNameLb.setFgColor(color)
            self.soundLb.setFgColor(color)

            try:
                color = ""
                if self.defaultData[self.cbIdx]["add"][i] < speed[notchCnt * 3 + i]:
                    color = "red"
                elif self.defaultData[self.cbIdx]["add"][i] > speed[notchCnt * 3 + i]:
                    color = "blue"
                else:
                    color = "black"
                addDefaultValue = self.defaultData[self.cbIdx]["add"][i]
            except Exception:
                color = "green"
                addDefaultValue = None

            self.addNameLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchAdd"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.addNameLb.grid(row=self.notchContentCnt * i + 3, column=1, sticky=tkinter.NSEW)
            self.varAdd = tkinter.DoubleVar()
            self.varAdd.set(str(speed[notchCnt * 3 + i]))
            self.varList.append(self.varAdd)
            self.addLb = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.varAdd, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
            self.addLb.grid(row=self.notchContentCnt * i + 3, column=2, sticky=tkinter.NSEW)
            self.addBtn = ttkCustomWidget.CustomTtkButton(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar([self.addNameLb, self.addLb], self.varAdd, self.varAdd.get(), "add", i, addDefaultValue), state="disabled")
            self.addBtn.grid(row=self.notchContentCnt * i + 3, column=3, sticky=tkinter.NSEW, padx=(0, 10))
            self.btnList.append(self.addBtn)

            self.addNameLb.setFgColor(color)
            self.addLb.setFgColor(color)

        frame.grid_columnconfigure(0, weight=10)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

    def editVar(self, labelList, var, value, notchName, notchNum, defaultValue, flag=False):
        EditNotchVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], labelList, var, value, notchName, notchNum, defaultValue, self.rootFrameAppearance, flag)


class EditNotchVarInfo(CustomSimpleDialog):
    def __init__(self, master, title, labelList, var, value, notchName, notchNum, defaultValue, rootFrameAppearance, flag=False):
        self.labelList = labelList
        self.master = master
        self.var = var
        self.value = value
        self.notchName = notchName
        self.notchNum = notchNum
        self.defaultValue = defaultValue
        self.flag = flag
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, frame):
        self.defaultLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(self.defaultValue), font=textSetting.textList["font2"])
        self.defaultLb.pack()

        sep = ttkCustomWidget.CustomTtkSeparator(frame, orient="horizontal")
        sep.pack(fill=tkinter.X, ipady=5)

        self.v_calcMinSpeed = tkinter.DoubleVar()
        self.v_calcMinSpeed.set(0.0)
        if self.notchName == "tlk":
            calcMinSpeedLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["calcMinSpeedLabel"].format(self.notchNum, self.notchNum + 1), font=textSetting.textList["font2"])
            calcMinSpeedLb.pack()
            calcMinSpeedValue = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.v_calcMinSpeed, font=textSetting.textList["font2"])
            calcMinSpeedValue.pack()
            sep = ttkCustomWidget.CustomTtkSeparator(frame, orient="horizontal")
            sep.pack(fill=tkinter.X, ipady=5)

        self.inputLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.inputLb.pack()

        self.v_val = tkinter.StringVar()
        self.v_val.set(self.value)
        self.inputEt = ttkCustomWidget.CustomTtkEntry(frame, textvariable=self.v_val, font=textSetting.textList["font2"])
        self.inputEt.pack()
        if self.notchName == "tlk":
            self.inputEt.bind("<KeyRelease>", self.calcMinSpeedHandler)
            self.calcMinSpeed()
        super().body(frame)

    def calcMinSpeedHandler(self, event):
        self.calcMinSpeed()

    def calcMinSpeed(self):
        try:
            inputTlk = float(self.v_val.get())
        except Exception:
            inputTlk = float(self.value)

        notchPerfFrame = self.master.winfo_children()[1]
        perfLabelFrame = notchPerfFrame.winfo_children()[1]
        perfAllFrame = perfLabelFrame.winfo_children()[0]
        perfCanvas = perfAllFrame.winfo_children()[1]
        perfCanvasInFrame = perfCanvas.winfo_children()[0]

        weightIdx = -1
        noneTlkIdx = -1
        perfWidgetList = perfCanvasInFrame.winfo_children()
        for i in range(len(perfWidgetList) // 3):
            nameLabel = perfWidgetList[3 * i]
            if nameLabel["text"] == "Weight":
                weightIdx = i
            if nameLabel["text"] == "None_Tlk":
                noneTlkIdx = i

        weight = float(perfWidgetList[3 * weightIdx + 1]["text"])
        noneTlk = float(perfWidgetList[3 * noneTlkIdx + 1]["text"])
        minSpeed = ((weight - inputTlk) / noneTlk)
        if minSpeed < 0:
            minSpeed = 0
        minSpeed = round(minSpeed * 60 / 1.11, 3)
        self.v_calcMinSpeed.set(minSpeed)

    def validate(self):
        result = self.inputEt.get()
        if result:
            try:
                if self.flag:
                    try:
                        result = int(result)
                        self.var.set(result)
                    except Exception:
                        errorMsg = textSetting.textList["errorList"]["E60"]
                        mb.showerror(title=textSetting.textList["intError"], message=errorMsg)
                        return False
                else:
                    try:
                        result = float(result)
                        self.var.set(result)
                    except Exception:
                        errorMsg = textSetting.textList["errorList"]["E3"]
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
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
                    label.setFgColor(color)
            return True
