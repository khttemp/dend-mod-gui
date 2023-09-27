import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import program.textSetting as textSetting

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


class CountWidget():
    def __init__(self, root, trainIdx, game, frame, decryptFile, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.reloadFunc = reloadFunc

        if self.game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
            index = self.decryptFile.indexList[self.trainIdx]
            notchNum = self.decryptFile.byteArr[index]

            modelInfo = self.decryptFile.trainModelList[self.trainIdx]

            self.countFrame = ttk.Frame(self.frame)
            self.countFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=15, pady=5)

            self.notchLb = tkinter.Label(self.countFrame, text=textSetting.textList["orgInfoEditor"]["notchLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.notchLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.varNotch = tkinter.IntVar()
            self.varNotch.set(notchNum)
            self.notchTextLb = tkinter.Label(self.countFrame, textvariable=self.varNotch, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.notchTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.notchBtn = tkinter.Button(self.countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editNotchVar())
            self.notchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

            self.henseiLb = tkinter.Label(self.countFrame, text=textSetting.textList["orgInfoEditor"]["csvOrgNumTitle"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.henseiLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
            self.varHensei = tkinter.IntVar()
            self.varHensei.set(modelInfo["mdlCnt"])
            self.henseiTextLb = tkinter.Label(self.countFrame, textvariable=self.varHensei, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.henseiTextLb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
            self.henseiBtn = tkinter.Button(self.countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editHenseiVar(self.varHensei.get()))
            self.henseiBtn.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)

            self.colorLb = tkinter.Label(self.countFrame, text=textSetting.textList["orgInfoEditor"]["colorCnt"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.colorLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
            self.varColor = tkinter.IntVar()
            self.varColor.set(modelInfo["colorCnt"])
            self.colorTextLb = tkinter.Label(self.countFrame, textvariable=self.varColor, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.colorTextLb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)
            self.colorBtn = tkinter.Button(self.countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar(self.varColor.get()))
            self.colorBtn.grid(row=2, column=2, sticky=tkinter.W + tkinter.E)
        else:
            trainOrgInfo = self.decryptFile.trainInfoList[self.trainIdx]
            speedList = trainOrgInfo[0]
            notchNum = len(speedList) // self.notchContentCnt

            self.notchLb = tkinter.Label(self.frame, text=textSetting.textList["orgInfoEditor"]["notchLabel"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.notchLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.varNotch = tkinter.IntVar()
            self.varNotch.set(notchNum)
            self.notchTextLb = tkinter.Label(self.frame, textvariable=self.varNotch, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.notchTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.notchBtn = tkinter.Button(self.frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editNotchVar())
            self.notchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editNotchVar(self):
        result = EditNotchInfo(self.root, textSetting.textList["orgInfoEditor"]["editNotchLabel"], self.trainIdx, self.game, self.decryptFile, self.notchContentCnt)
        if result.reloadFlag:
            self.reloadFunc()

    def editHenseiVar(self, value):
        resultValue = sd.askstring(title=textSetting.textList["orgInfoEditor"]["valueModify"], prompt=textSetting.textList["infoList"]["I44"], initialvalue=value)

        if resultValue:
            try:
                try:
                    resultValue = int(resultValue)
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E60"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return

                if resultValue <= 0:
                    errorMsg = textSetting.textList["errorList"]["E61"].format(1)
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return

                if resultValue < value:
                    msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
                    result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
                    if not result:
                        return

                if not self.decryptFile.saveHenseiNum(self.trainIdx, resultValue):
                    self.decryptFile.printError()
                    errorMsg = textSetting.textList["errorList"]["E4"]
                    mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                    return False

                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I55"])
                self.reloadFunc()
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)

    def editVar(self, value):
        if self.game in [gameDefine.LS, gameDefine.BS]:
            if self.game == gameDefine.LS:
                errorMsg = textSetting.textList["errorList"]["E65"]
            else:
                errorMsg = textSetting.textList["errorList"]["E66"]
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return
        result = sd.askstring(title=textSetting.textList["orgInfoEditor"]["valueModify"], prompt=textSetting.textList["infoList"]["I44"], initialvalue=value)

        if result:
            try:
                try:
                    result = int(result)
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E60"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return

                if result < 0:
                    errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return

                if not self.decryptFile.saveColor(self.trainIdx, result):
                    self.decryptFile.printError()
                    errorMsg = textSetting.textList["errorList"]["E4"]
                    mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                    return False

                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I56"])
                self.reloadFunc()

            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)


class EditNotchInfo(sd.Dialog):
    def __init__(self, master, title, trainIdx, game, decryptFile, notchContentCnt):
        self.trainIdx = trainIdx
        self.game = game
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.reloadFlag = False
        super(EditNotchInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        if self.game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
            index = self.decryptFile.indexList[self.trainIdx]
            notchNum = self.decryptFile.byteArr[index]
        else:
            trainOrgInfo = self.decryptFile.trainInfoList[self.trainIdx]
            speedList = trainOrgInfo[0]
            notchNum = len(speedList) // self.notchContentCnt

        if notchNum == 4:
            notchIdx = 0
        elif notchNum == 5:
            notchIdx = 1
        elif notchNum == 12:
            notchIdx = 2

        self.notchLb = tkinter.Label(frame, text=textSetting.textList["infoList"]["I57"], font=textSetting.textList["font2"])
        self.notchLb.grid(row=0, column=0)
        notchList = textSetting.textList["orgInfoEditor"]["editNotchList"]
        self.notchCb = ttk.Combobox(frame, width=12, value=notchList, state="readonly", font=textSetting.textList["font2"])
        self.notchCb.current(notchIdx)
        self.notchCb.grid(row=1, column=0)

    def validate(self):
        if self.game in [gameDefine.LS, gameDefine.BS]:
            if self.notchCb.current() == 2:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E23"].format(12))
                return False
        warnMsg = textSetting.textList["infoList"]["I58"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            newNotchNum = -1
            notchIdx = self.notchCb.current()
            if notchIdx == 0:
                newNotchNum = 4
            elif notchIdx == 1:
                newNotchNum = 5
            elif notchIdx == 2:
                newNotchNum = 12

            if not self.decryptFile.saveNotchInfo(self.trainIdx, newNotchNum):
                self.decryptFile.printError()
                errorMsg = textSetting.textList["errorList"]["E4"]
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            else:
                return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I59"])
        self.reloadFlag = True
