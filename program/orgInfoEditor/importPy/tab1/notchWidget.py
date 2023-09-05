import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import program.textSetting as textSetting


class NotchWidget():
    def __init__(self, root, cbIdx, i, notchCnt, frame, speed, decryptFile, notchContentCnt, varList, btnList, defaultData):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData

        self.notchNum = textSetting.textList["orgInfoEditor"]["notchLabel"] + str(i + 1)
        self.notchNumLb = tkinter.Label(frame, text=self.notchNum, font=textSetting.textList["font6"], width=14, borderwidth=1, relief="solid")
        self.notchNumLb.grid(rowspan=self.notchContentCnt, row=self.notchContentCnt * i, column=0, sticky=tkinter.N + tkinter.S)

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

        self.speedNameLb = tkinter.Label(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchSpeed"], font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
        self.speedNameLb.grid(row=self.notchContentCnt * i, column=1, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.varSpeed = tkinter.DoubleVar()
        self.varSpeed.set(str(speed[i]))

        self.varList.append(self.varSpeed)
        self.speedLb = tkinter.Label(frame, textvariable=self.varSpeed, font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
        self.speedLb.grid(row=self.notchContentCnt * i, column=2, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.speedBtn = tkinter.Button(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar([self.speedNameLb, self.speedLb], self.varSpeed, self.varSpeed.get(), speedDefaultValue), state="disabled")
        self.speedBtn.grid(row=self.notchContentCnt * i, column=3, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.btnList.append(self.speedBtn)

        self.speedNameLb["fg"] = color
        self.speedLb["fg"] = color

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

        self.tlkNameLb = tkinter.Label(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchTlk"], font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
        self.tlkNameLb.grid(row=self.notchContentCnt * i + 1, column=1, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.varTlk = tkinter.DoubleVar()
        self.varTlk.set(str(speed[notchCnt + i]))
        self.varList.append(self.varTlk)
        self.tlkLb = tkinter.Label(frame, textvariable=self.varTlk, font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
        self.tlkLb.grid(row=self.notchContentCnt * i + 1, column=2, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.tlkBtn = tkinter.Button(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar([self.tlkNameLb, self.tlkLb], self.varTlk, self.varTlk.get(), tlkDefaultValue), state="disabled")
        self.tlkBtn.grid(row=self.notchContentCnt * i + 1, column=3, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.btnList.append(self.tlkBtn)

        self.tlkNameLb["fg"] = color
        self.tlkLb["fg"] = color

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

            self.soundNameLb = tkinter.Label(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchSound"], font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
            self.soundNameLb.grid(row=self.notchContentCnt * i + 2, column=1, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            self.varSound = tkinter.IntVar()
            self.varSound.set(str(speed[notchCnt * 2 + i]))
            self.varList.append(self.varSound)
            self.soundLb = tkinter.Label(frame, textvariable=self.varSound, font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
            self.soundLb.grid(row=self.notchContentCnt * i + 2, column=2, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            self.soundBtn = tkinter.Button(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar([self.soundNameLb, self.soundLb], self.varSound, self.varSound.get(), soundDefaultValue, True), state="disabled")
            self.soundBtn.grid(row=self.notchContentCnt * i + 2, column=3, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            self.btnList.append(self.soundBtn)

            self.soundNameLb["fg"] = color
            self.soundLb["fg"] = color

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

            self.addNameLb = tkinter.Label(frame, text=textSetting.textList["orgInfoEditor"]["csvNotchAdd"], font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
            self.addNameLb.grid(row=self.notchContentCnt * i + 3, column=1, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            self.varAdd = tkinter.DoubleVar()
            self.varAdd.set(str(speed[notchCnt * 3 + i]))
            self.varList.append(self.varAdd)
            self.addLb = tkinter.Label(frame, textvariable=self.varAdd, font=textSetting.textList["font6"], width=5, borderwidth=1, relief="solid")
            self.addLb.grid(row=self.notchContentCnt * i + 3, column=2, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            self.addBtn = tkinter.Button(frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar([self.addNameLb, self.addLb], self.varAdd, self.varAdd.get(), addDefaultValue), state="disabled")
            self.addBtn.grid(row=self.notchContentCnt * i + 3, column=3, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            self.btnList.append(self.addBtn)

            self.addNameLb["fg"] = color
            self.addLb["fg"] = color

    def editVar(self, labelList, var, value, defaultValue, flag=False):
        EditNotchVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], labelList, var, value, defaultValue, flag)


class EditNotchVarInfo(sd.Dialog):
    def __init__(self, master, title, labelList, var, value, defaultValue, flag=False):
        self.labelList = labelList
        self.var = var
        self.value = value
        self.defaultValue = defaultValue
        self.flag = flag
        super(EditNotchVarInfo, self).__init__(parent=master, title=title)

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
