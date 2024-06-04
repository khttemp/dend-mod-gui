import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class HurikoWidget():
    def __init__(self, root, cbIdx, i, perfCnt, frame, huriko, decryptFile, varList, btnList, defaultData, rootFrameAppearance):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData
        self.rootFrameAppearance = rootFrameAppearance

        self.hurikoNameLb = ttkCustomWidget.CustomTtkLabel(frame, text=self.decryptFile.trainHurikoNameList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.hurikoNameLb.grid(row=perfCnt + i, column=0, sticky=tkinter.NSEW)
        self.varHuriko = tkinter.IntVar()
        self.varHuriko.set(str(huriko[i]))
        self.varList.append(self.varHuriko)
        self.hurikoLb = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.varHuriko, font=textSetting.textList["font6"], anchor=tkinter.CENTER, relief="solid")
        self.hurikoLb.grid(row=perfCnt + i, column=1, sticky=tkinter.NSEW)
        self.hurikoBtn = ttkCustomWidget.CustomTtkButton(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar([self.hurikoNameLb, self.hurikoLb], self.varHuriko, self.varHuriko.get(), self.defaultData[self.cbIdx]["huriko"][i]), state="disabled")
        self.hurikoBtn.grid(row=perfCnt + i, column=2, sticky=tkinter.NSEW, padx=(0, 10))
        self.btnList.append(self.hurikoBtn)

        color = ""
        if self.defaultData[self.cbIdx]["huriko"][i] < huriko[i]:
            color = "red"
        elif self.defaultData[self.cbIdx]["huriko"][i] > huriko[i]:
            color = "blue"
        else:
            color = "black"
        self.hurikoNameLb.setFgColor(color)
        self.hurikoLb.setFgColor(color)

    def editVar(self, labelList, var, value, defaultValue, flag=True):
        EditHurikoVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], labelList, var, value, defaultValue, self.rootFrameAppearance)


class EditHurikoVarInfo(CustomSimpleDialog):
    def __init__(self, master, title, labelList, var, value, defaultValue, rootFrameAppearance):
        self.labelList = labelList
        self.var = var
        self.value = value
        self.defaultValue = defaultValue
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
                try:
                    result = int(result)
                    self.var.set(result)
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E60"]
                    mb.showerror(title=textSetting.textList["intError"], message=errorMsg)
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
