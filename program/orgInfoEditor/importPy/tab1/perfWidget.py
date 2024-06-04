import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class PerfWidget():
    def __init__(self, root, cbIdx, i, frame, perf, decryptFile, varList, btnList, defaultData, rootFrameAppearance):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData
        self.rootFrameAppearance = rootFrameAppearance

        self.perfNameLb = ttkCustomWidget.CustomTtkLabel(frame, text=self.decryptFile.trainPerfNameList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.perfNameLb.grid(row=i, column=0, sticky=tkinter.NSEW)
        self.varPerf = tkinter.DoubleVar()
        self.varPerf.set(str(perf[i]))
        self.varList.append(self.varPerf)
        self.perfLb = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.varPerf, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.perfLb.grid(row=i, column=1, sticky=tkinter.NSEW)
        self.perfBtn = ttkCustomWidget.CustomTtkButton(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar([self.perfNameLb, self.perfLb], self.varPerf, self.varPerf.get(), self.defaultData[self.cbIdx]["att"][i]), state="disabled")
        self.perfBtn.grid(row=i, column=2, sticky=tkinter.NSEW, padx=(0, 10))
        self.btnList.append(self.perfBtn)

        color = ""
        if self.defaultData[self.cbIdx]["att"][i] < perf[i]:
            color = "red"
        elif self.defaultData[self.cbIdx]["att"][i] > perf[i]:
            color = "blue"
        else:
            color = "black"
        self.perfNameLb.setFgColor(color)
        self.perfLb.setFgColor(color)

        frame.grid_columnconfigure(0, weight=10)
        frame.grid_columnconfigure(1, weight=1)

    def editVar(self, labelList, var, value, defaultValue, flag=False):
        EditPerfVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], labelList, var, value, defaultValue, self.rootFrameAppearance, flag)


class EditPerfVarInfo(CustomSimpleDialog):
    def __init__(self, master, title, labelList, var, value, defaultValue, rootFrameAppearance, flag=False):
        self.labelList = labelList
        self.var = var
        self.value = value
        self.defaultValue = defaultValue
        self.flag = flag
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, frame):
        self.defaultLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(self.defaultValue), font=textSetting.textList["font2"])
        self.defaultLb.pack()

        sep = ttkCustomWidget.CustomTtkSeparator(frame, orient="horizontal")
        sep.pack(fill=tkinter.X, ipady=5)

        self.inputLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.inputLb.pack()

        self.v_val = tkinter.StringVar()
        self.v_val.set(self.value)
        self.inputEt = ttkCustomWidget.CustomTtkEntry(frame, textvariable=self.v_val, font=textSetting.textList["font2"])
        self.inputEt.pack()
        super().body(frame)

    def validate(self):
        result = self.inputEt.get()
        if result:
            try:
                if self.flag:
                    try:
                        result = int(result)
                        if result < 0:
                            errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                            mb.showerror(title=textSetting.textList["intError"], message=errorMsg)
                            return False
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
