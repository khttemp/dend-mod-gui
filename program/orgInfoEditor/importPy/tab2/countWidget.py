import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog, CustomAskstring

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


class CountWidget():
    def __init__(self, root, trainIdx, game, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        if self.game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
            index = self.decryptFile.indexList[self.trainIdx]
            notchNum = self.decryptFile.byteArr[index]

            modelInfo = self.decryptFile.trainModelList[self.trainIdx]

            self.countFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
            self.countFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=15, pady=5)

            self.notchLb = ttkCustomWidget.CustomTtkLabel(self.countFrame, text=textSetting.textList["orgInfoEditor"]["notchLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.notchLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.varNotch = tkinter.IntVar()
            self.varNotch.set(notchNum)
            self.notchTextLb = ttkCustomWidget.CustomTtkLabel(self.countFrame, textvariable=self.varNotch, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.notchTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.notchBtn = ttkCustomWidget.CustomTtkButton(self.countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editNotchVar())
            self.notchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

            self.henseiLb = ttkCustomWidget.CustomTtkLabel(self.countFrame, text=textSetting.textList["orgInfoEditor"]["csvOrgNumTitle"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.henseiLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
            self.varHensei = tkinter.IntVar()
            self.varHensei.set(modelInfo["mdlCnt"])
            self.henseiTextLb = ttkCustomWidget.CustomTtkLabel(self.countFrame, textvariable=self.varHensei, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.henseiTextLb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
            self.henseiBtn = ttkCustomWidget.CustomTtkButton(self.countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editHenseiVar(self.varHensei.get()))
            self.henseiBtn.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)

            self.colorLb = ttkCustomWidget.CustomTtkLabel(self.countFrame, text=textSetting.textList["orgInfoEditor"]["colorCnt"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.colorLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
            self.varColor = tkinter.IntVar()
            self.varColor.set(modelInfo["colorCnt"])
            self.colorTextLb = ttkCustomWidget.CustomTtkLabel(self.countFrame, textvariable=self.varColor, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.colorTextLb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)
            self.colorBtn = ttkCustomWidget.CustomTtkButton(self.countFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar(self.varColor.get()))
            self.colorBtn.grid(row=2, column=2, sticky=tkinter.W + tkinter.E)
        else:
            trainOrgInfo = self.decryptFile.trainInfoList[self.trainIdx]
            speedList = trainOrgInfo[0]
            notchNum = len(speedList) // self.notchContentCnt

            self.notchLb = ttkCustomWidget.CustomTtkLabel(self.frame, text=textSetting.textList["orgInfoEditor"]["notchLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.notchLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.varNotch = tkinter.IntVar()
            self.varNotch.set(notchNum)
            self.notchTextLb = ttkCustomWidget.CustomTtkLabel(self.frame, textvariable=self.varNotch, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            self.notchTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.notchBtn = ttkCustomWidget.CustomTtkButton(self.frame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editNotchVar())
            self.notchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editNotchVar(self):
        result = EditNotchInfo(self.root, textSetting.textList["orgInfoEditor"]["editNotchLabel"], self.trainIdx, self.game, self.decryptFile, self.notchContentCnt, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc()

    def editHenseiVar(self, value):
        resultObj = CustomAskstring(self.root, title=textSetting.textList["orgInfoEditor"]["valueModify"], prompt=textSetting.textList["infoList"]["I44"], initialvalue=value, bgColor=self.rootFrameAppearance.bgColor)
        resultValue = resultObj.result

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
        resultObj = CustomAskstring(self.root, title=textSetting.textList["orgInfoEditor"]["valueModify"], prompt=textSetting.textList["infoList"]["I44"], initialvalue=value, bgColor=self.rootFrameAppearance.bgColor)
        result = resultObj.result

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


class EditNotchInfo(CustomSimpleDialog):
    def __init__(self, master, title, trainIdx, game, decryptFile, notchContentCnt, rootFrameAppearance):
        self.trainIdx = trainIdx
        self.game = game
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

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

        self.notchLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["infoList"]["I57"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
        self.notchLb.grid(row=0, column=0)
        notchList = textSetting.textList["orgInfoEditor"]["editNotchList"]
        self.notchCb = ttkCustomWidget.CustomTtkCombobox(frame, width=12, value=notchList, state="readonly", font=textSetting.textList["font2"])
        self.notchCb.current(notchIdx)
        self.notchCb.grid(row=1, column=0)
        super().body(frame)

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
