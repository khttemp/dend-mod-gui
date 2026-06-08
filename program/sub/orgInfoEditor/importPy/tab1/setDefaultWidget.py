import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class SetDefaultEdit(CustomSimpleDialog):
    def __init__(self, master, title, trainIndex, decryptFile, defaultData, rootFrameAppearance):
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.defaultData = defaultData
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        self.copySrcCb = ttkCustomWidget.CustomTtkCombobox(master, width=12, font=textSetting.textList["font2"], value=self.decryptFile.trainNameList, state="readonly")
        self.copySrcCb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S, padx=3)
        if self.decryptFile.game in ["SS"]:
            self.copySrcCb.bind("<<ComboboxSelected>>", lambda e: self.selectTrain())

        self.v_infoNotch = tkinter.IntVar()
        self.v_infoNotch.set(0)
        self.infoNotchCb = ttkCustomWidget.CustomTtkCheckbutton(master, text=textSetting.textList["orgInfoEditor"]["notchLabel"], variable=self.v_infoNotch)
        self.infoNotchCb.grid(row=0, column=1, sticky=tkinter.W, padx=3)

        self.v_infoPerf = tkinter.IntVar()
        self.v_infoPerf.set(0)
        self.infoPerfCb = ttkCustomWidget.CustomTtkCheckbutton(master, text=textSetting.textList["orgInfoEditor"]["perfLabel"], variable=self.v_infoPerf)
        self.infoPerfCb.grid(row=1, column=1, sticky=tkinter.W, padx=3)

        if self.decryptFile.game in ["SS"]:
            self.addNewGameCheckBox(master)
        self.infoDefLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["setDefaultLabel"], font=textSetting.textList["font2"])
        self.infoDefLb.grid(row=0, column=2, sticky=tkinter.N + tkinter.S, padx=3)

        self.copySrcCb.current(self.trainIndex)
        super().body(master)

    def addNewGameCheckBox(self, master):
        self.v_infoRain = tkinter.IntVar()
        self.v_infoRain.set(0)
        self.infoRainCb = ttkCustomWidget.CustomTtkCheckbutton(master, text=textSetting.textList["orgInfoEditor"]["SSRainLfLabel"], variable=self.v_infoRain)
        self.infoRainCb.grid(row=2, column=1, sticky=tkinter.W, padx=3)

        self.v_infoCarb = tkinter.IntVar()
        self.v_infoCarb.set(0)
        self.infoCarbCb = ttkCustomWidget.CustomTtkCheckbutton(master, text=textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"], variable=self.v_infoCarb)
        self.infoCarbCb.grid(row=3, column=1, sticky=tkinter.W, padx=3)

        self.v_infoOther = tkinter.IntVar()
        self.v_infoOther.set(0)
        self.infoOtherCb = ttkCustomWidget.CustomTtkCheckbutton(master, text=textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"], variable=self.v_infoOther)
        self.infoOtherCb.grid(row=4, column=1, sticky=tkinter.W, padx=3)

        self.v_infoHuriko = tkinter.IntVar()
        self.v_infoHuriko.set(0)
        self.v_hurikoText = tkinter.StringVar()
        self.v_hurikoText.set(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
        self.infoHurikoCb = ttkCustomWidget.CustomTtkCheckbutton(master, textvariable=self.v_hurikoText, variable=self.v_infoHuriko)
        self.infoHurikoCb.grid(row=5, column=1, sticky=tkinter.W, padx=3)

        self.v_infoOneWheel = tkinter.IntVar()
        self.v_infoOneWheel.set(0)
        self.v_oneWheelText = tkinter.StringVar()
        self.v_oneWheelText.set(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        self.infoOneWheelCb = ttkCustomWidget.CustomTtkCheckbutton(master, textvariable=self.v_oneWheelText, variable=self.v_infoOneWheel)
        self.infoOneWheelCb.grid(row=6, column=1, sticky=tkinter.W, padx=3)

    def selectTrain(self):
        # Mu2000, JR2000, H2300
        if self.copySrcCb.current() in [12, 19, 25]:
            self.v_hurikoText.set(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
        else:
            self.v_hurikoText.set(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"] + textSetting.textList["orgInfoEditor"]["setDeleteLabel"])

        # K800, K80
        if self.copySrcCb.current() in [27, 29]:
            self.v_oneWheelText.set(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        else:
            self.v_oneWheelText.set(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"] + textSetting.textList["orgInfoEditor"]["setDeleteLabel"])

    def validate(self):
        if self.decryptFile.game in ["RS", "CS", "BS", "LS"]:
            checkStatusList = [
                self.v_infoNotch.get(),
                self.v_infoPerf.get()
            ]
            ret = False
            for checkStatus in checkStatusList:
                ret |= checkStatus
            if not ret:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E62"])
                return False

            srcIdx = self.copySrcCb.current()
            srcIndex = self.decryptFile.indexList[srcIdx]
            srcNotchNum = self.decryptFile.byteArr[srcIndex]
            distData = self.defaultData[srcIdx]
            distNotchNum = len(distData["notch"])

            srcSpeed = None
            srcPerf = None
            srcHuriko = None

            trainOrgInfo = self.decryptFile.trainInfoList[srcIdx]
            srcSpeed = trainOrgInfo[0]
            srcPerf = trainOrgInfo[1]
            if len(trainOrgInfo) > 2:
                srcHuriko = trainOrgInfo[2]
            srcList = [srcIndex, srcNotchNum, srcSpeed, srcPerf, srcHuriko]
        else:
            checkStatusList = [
                self.v_infoNotch.get(),
                self.v_infoPerf.get(),
                self.v_infoRain.get(),
                self.v_infoCarb.get(),
                self.v_infoOther.get(),
                self.v_infoHuriko.get(),
                self.v_infoOneWheel.get(),
            ]
            ret = False
            for checkStatus in checkStatusList:
                ret |= checkStatus
            if not ret:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E62"])
                return False

            srcIdx = self.copySrcCb.current()
            trainOrgInfo = self.decryptFile.trainInfoList[srcIdx]
            srcSpeed = trainOrgInfo[0]
            srcNotchNum = len(srcSpeed) // self.decryptFile.notchContentCnt

            distData = self.defaultData[srcIdx]
            distNotchNum = len(distData["notch"])

            srcList = [
                srcIdx,
                srcNotchNum,
            ]

        warnMsg = ""
        if self.v_infoNotch.get() == 1:
            if srcNotchNum > distNotchNum:
                warnMsg += textSetting.textList["infoList"]["I45"].format(self.decryptFile.trainNameList[srcIdx], distNotchNum)
            elif srcNotchNum < distNotchNum:
                warnMsg += textSetting.textList["infoList"]["I45"].format(self.decryptFile.trainNameList[srcIdx], srcNotchNum)

        if self.v_infoNotch.get() == 1:
            warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["notchLabel"])
        if self.v_infoPerf.get() == 1:
            warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["perfLabel"])

        if self.decryptFile.game in ["SS"]:
            if self.v_infoRain.get() == 1:
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSRainLfLabel"])
            if self.v_infoCarb.get() == 1:
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"])
            if self.v_infoOther.get() == 1:
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"])
            if self.v_infoHuriko.get() == 1:
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
            if self.v_infoOneWheel.get() == 1:
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        warnMsg += textSetting.textList["infoList"]["I46"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

        if result:
            if not self.decryptFile.setDefaultTrainInfo(srcList, distData, checkStatusList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I47"])
        self.reloadFlag = True
