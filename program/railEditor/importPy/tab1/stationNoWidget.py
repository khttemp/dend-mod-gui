import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting


class StationNoWidget:
    def __init__(self, frame, decryptFile, stationNo, num, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.stationNo = stationNo
        self.num = num
        self.reloadFunc = reloadFunc

        self.txtFrame = tkinter.Frame(self.frame, padx=1, pady=5)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.stationNoLb = tkinter.Label(self.txtFrame, text=textSetting.textList["railEditor"]["stationNo"], font=textSetting.textList["font6"], width=12, borderwidth=1, relief="solid")
        self.stationNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varStationNo = tkinter.IntVar()
        self.varStationNo.set(self.stationNo)
        self.stationNoTextLb = tkinter.Label(self.txtFrame, textvariable=self.varStationNo, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.stationNoTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.stationNoBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar(self.varStationNo.get()))
        self.stationNoBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditStationNoWidget(self.frame, textSetting.textList["railEditor"]["editStationNoLabel"], self.decryptFile, value)

        if result.reloadFlag:
            if not self.decryptFile.saveStationNo(self.num, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I72"])

            self.reloadFunc()


class EditStationNoWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.reloadFlag = False
        self.resultValue = 0
        super(EditStationNoWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.pack()

        self.varStationNo = tkinter.IntVar()
        self.varStationNo.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varStationNo, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varStationNo.get())
                    if res < 0:
                        errorMsg = textSetting.textList["errorList"]["E61"].format(0)
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

            return True

    def apply(self):
        self.reloadFlag = True
