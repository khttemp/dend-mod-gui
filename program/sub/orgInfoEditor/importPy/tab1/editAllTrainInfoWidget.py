import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class AllEdit(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.eleLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["perfElement"], width=5, font=textSetting.textList["font2"])
        self.eleLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S, padx=3)
        self.v_ele = tkinter.StringVar()
        self.eleCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_ele, width=24, font=textSetting.textList["font2"], value=self.decryptFile.trainPerfNameList, state="readonly")
        self.eleCb.grid(row=0, column=1, sticky=tkinter.N + tkinter.S, padx=3)
        self.v_ele.set(self.decryptFile.trainPerfNameList[0])

        self.allLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["perfAllTrainLabel"], width=5, font=textSetting.textList["font2"])
        self.allLb.grid(row=0, column=2, sticky=tkinter.N + tkinter.S, padx=3)

        self.v_num = tkinter.DoubleVar()
        self.v_num.set(1.0)
        self.numEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_num, width=6, font=textSetting.textList["font2"], justify="right")
        self.numEt.grid(row=0, column=3, sticky=tkinter.N + tkinter.S, padx=3)

        calcList = textSetting.textList["orgInfoEditor"]["perfCalcList"]
        self.v_ele2 = tkinter.StringVar()
        self.eleCb2 = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_ele2, font=textSetting.textList["font2"], width=8, value=calcList, state="readonly")
        self.v_ele2.set(calcList[0])

        self.eleCb2.grid(row=0, column=4, sticky=tkinter.N + tkinter.S, padx=3)
        super().body(master)

    def validate(self):
        try:
            result = float(self.v_num.get())
            if self.eleCb2.current() == 0:
                warnMsg = textSetting.textList["infoList"]["I52"]
            else:
                warnMsg = textSetting.textList["infoList"]["I53"]
            result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")

            if result:
                perfIndex = self.eleCb.current()
                num = self.v_num.get()

                if not self.decryptFile.saveAllEdit(perfIndex, num, self.eleCb2.current()):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return False
                return True
        except Exception:
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return False

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I54"])
        self.reloadFlag = True
