import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import program.textSetting as textSetting


class PerfWidget():
    def __init__(self, root, cbIdx, i, frame, perf, decryptFile, varList, btnList, defaultData):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData

        self.perfNameLb = tkinter.Label(frame, text=self.decryptFile.trainPerfNameList[i], font=textSetting.textList["font6"], width=27, borderwidth=1, relief="solid")
        self.perfNameLb.grid(row=i, column=0, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.varPerf = tkinter.DoubleVar()
        self.varPerf.set(str(perf[i]))
        self.varList.append(self.varPerf)
        self.perfLb = tkinter.Label(frame, textvariable=self.varPerf, font=textSetting.textList["font6"], width=10, borderwidth=1, relief="solid")
        self.perfLb.grid(row=i, column=1, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.perfBtn = tkinter.Button(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar([self.perfNameLb, self.perfLb], self.varPerf, self.varPerf.get(), self.defaultData[self.cbIdx]["att"][i]), state="disabled")
        self.perfBtn.grid(row=i, column=2, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.btnList.append(self.perfBtn)

        color = ""
        if self.defaultData[self.cbIdx]["att"][i] < perf[i]:
            color = "red"
        elif self.defaultData[self.cbIdx]["att"][i] > perf[i]:
            color = "blue"
        else:
            color = "black"
        self.perfNameLb["fg"] = color
        self.perfLb["fg"] = color

    def editVar(self, labelList, var, value, defaultValue, flag=False):
        EditPerfVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], labelList, var, value, defaultValue, flag)


class EditPerfVarInfo(sd.Dialog):
    def __init__(self, master, title, labelList, var, value, defaultValue, flag=False):
        self.labelList = labelList
        self.var = var
        self.value = value
        self.defaultValue = defaultValue
        self.flag = flag
        super(EditPerfVarInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        self.defaultLb = tkinter.Label(frame, text=textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(self.defaultValue), font=textSetting.textList["font2"])
        self.defaultLb.pack()

        sep = ttk.Separator(frame, orient="horizontal")
        sep.pack(fill=tkinter.X, ipady=5)

        self.inputLb = tkinter.Label(frame, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.inputLb.pack()

        v_val = tkinter.StringVar()
        v_val.set(self.value)
        self.inputEt = tkinter.Entry(frame, textvariable=v_val, font=textSetting.textList["font2"])
        self.inputEt.pack()

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
                    label["fg"] = color
            return True
