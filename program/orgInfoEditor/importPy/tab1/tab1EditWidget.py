import codecs
import tkinter
import traceback
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


def setDefault(tabFrame, decryptFile, game, trainIdx, defaultData, rootFrameAppearance, reloadFunc):
    result = SetDefaultEdit(tabFrame, textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"], decryptFile, game, trainIdx, defaultData, rootFrameAppearance)
    if result.reloadFlag:
        reloadFunc()


class SetDefaultEdit(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, game, trainIdx, defaultData, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.game = game
        self.trainIdx = trainIdx
        self.defaultData = defaultData
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.copySrcCb = ttkCustomWidget.CustomTtkCombobox(master, width=12, font=textSetting.textList["font2"], value=self.decryptFile.trainNameList, state="readonly")
        self.copySrcCb.bind("<<ComboboxSelected>>", lambda e: self.selectTrain())
        self.copySrcCb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S, padx=3)
        self.copySrcCb.current(self.trainIdx)

        self.v_infoNotch = tkinter.IntVar()
        self.v_infoNotch.set(0)
        self.infoNotchCb = ttkCustomWidget.CustomTtkCheckbutton(master, text=textSetting.textList["orgInfoEditor"]["notchLabel"], variable=self.v_infoNotch)
        self.infoNotchCb.grid(row=0, column=1, sticky=tkinter.W, padx=3)

        self.v_infoPerf = tkinter.IntVar()
        self.v_infoPerf.set(0)
        self.infoPerfCb = ttkCustomWidget.CustomTtkCheckbutton(master, text=textSetting.textList["orgInfoEditor"]["perfLabel"], variable=self.v_infoPerf)
        self.infoPerfCb.grid(row=1, column=1, sticky=tkinter.W, padx=3)

        if self.game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
            self.infoDefLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["setDefaultLabel"], font=textSetting.textList["font2"])
            self.infoDefLb.grid(row=1, column=2, sticky=tkinter.N + tkinter.S, padx=3)
        else:
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

            self.infoDefLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["setDefaultLabel"], font=textSetting.textList["font2"])
            self.infoDefLb.grid(row=0, column=2, sticky=tkinter.N + tkinter.S, padx=3)

            self.selectTrain()
        super().body(master)

    def selectTrain(self):
        if self.game == gameDefine.SS:
            if self.copySrcCb.current() in [12, 19, 25]:
                self.v_hurikoText.set(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
            else:
                self.v_hurikoText.set(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"] + textSetting.textList["orgInfoEditor"]["setDeleteLabel"])

            if self.copySrcCb.current() in [27, 29]:
                self.v_oneWheelText.set(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
            else:
                self.v_oneWheelText.set(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"] + textSetting.textList["orgInfoEditor"]["setDeleteLabel"])

    def validate(self):
        if self.game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
            if self.v_infoNotch.get() == 0 and self.v_infoPerf.get() == 0:
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
            checkStatusList = [self.v_infoNotch.get(), self.v_infoPerf.get()]
        else:
            if self.v_infoNotch.get() == 0 and \
                    self.v_infoPerf.get() == 0 and \
                    self.v_infoRain.get() == 0 and \
                    self.v_infoCarb.get() == 0 and \
                    self.v_infoOther.get() == 0 and \
                    self.v_infoHuriko.get() == 0 and \
                    self.v_infoOneWheel.get() == 0:
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
            checkStatusList = [
                self.v_infoNotch.get(),
                self.v_infoPerf.get(),
                self.v_infoRain.get(),
                self.v_infoCarb.get(),
                self.v_infoOther.get(),
                self.v_infoHuriko.get(),
                self.v_infoOneWheel.get(),
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

        if self.game == gameDefine.SS:
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
            errorMsg = textSetting.textList["errorList"]["E4"]
            if not self.decryptFile.setDefaultTrainInfo(srcList, distData, checkStatusList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I47"])
        self.reloadFlag = True


def extractCsvTrainInfo(game, trainIdx, decryptFile):
    filename = decryptFile.trainNameList[trainIdx]
    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("traininfo_csv", "*.csv")])
        errorMsg = textSetting.textList["errorList"]["E63"]
        if file_path:
            if not decryptFile.extractCsvTrainInfo(trainIdx, file_path):
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
    else:
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="txt", filetypes=[("traininfo_text", "*.txt")])
        errorMsg = textSetting.textList["errorList"]["E64"]
        if file_path:
            try:
                data = decryptFile.dataList[decryptFile.trainNameList[trainIdx]]
                w = open(file_path, "wb")
                w.write(data.script)
                w.close()
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I48"])
            except Exception:
                w = codecs.open("error.log", "a", "utf-8", "strict")
                w.write(traceback.format_exc())
                w.close()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def saveCsvTrainInfo(game, trainIdx, decryptFile, reloadFunc):
    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("traindata_csv", "*.csv")])
        if not file_path:
            return
        csvLines = None
        try:
            f = codecs.open(file_path, "r", "utf-8-sig", "strict")
            csvLines = f.readlines()
            f.close()
        except UnicodeDecodeError:
            f = codecs.open(file_path, "r", "shift-jis", "strict")
            csvLines = f.readlines()
            f.close()

        if not decryptFile.checkCsvResult(csvLines):
            mb.showerror(title=textSetting.textList["error"], message=decryptFile.error)
            return
        warnMsg = textSetting.textList["infoList"]["I11"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")

        if result:
            errorMsg = textSetting.textList["errorList"]["E14"]
            if not decryptFile.saveCsvTrainInfo(trainIdx):
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
            reloadFunc()
    else:
        file_path = fd.askopenfilename(filetypes=[("traininfo_text", "*.txt")])
        if not file_path:
            return
        
        f = codecs.open(file_path, "r", "utf-8", "strict")
        lines = f.readlines()
        f.close()
        resultList = decryptFile.decryptLines(lines)
        if resultList is None:
            errorMsg = textSetting.textList["errorList"]["E98"].format(decryptFile.error)
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"], icon="warning")
        if result == "no":
            return

        try:
            data = decryptFile.dataList[decryptFile.trainNameList[trainIdx]]
            with open(file_path, "rb") as f:
                data.script = f.read()
            data.save()
            with open(decryptFile.filePath, "wb") as w:
                w.write(decryptFile.env.file.save())
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
            reloadFunc()
        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])


def editTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc):
    v_edit = widgetList[0]
    cb = widgetList[1]
    menuCb = widgetList[2]
    edit_stage_train_button = widgetList[3]

    set_default_train_info_button = innerButtonList[0]
    extract_csv_train_info_button = innerButtonList[1]
    save_csv_train_info_button = innerButtonList[2]
    edit_button = innerButtonList[3]
    edit_all_button = innerButtonList[4]

    v_edit.set(textSetting.textList["orgInfoEditor"]["trainSave"])
    for btn in btnList:
        btn["state"] = "normal"

    edit_button["command"] = lambda: saveTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc)
    cb["state"] = "disabled"
    menuCb["state"] = "disabled"
    edit_stage_train_button["state"] = "disabled"

    set_default_train_info_button["state"] = "disabled"
    extract_csv_train_info_button["state"] = "disabled"
    save_csv_train_info_button["state"] = "disabled"
    edit_all_button["state"] = "disabled"


def saveTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc):
    v_edit = widgetList[0]
    cb = widgetList[1]
    menuCb = widgetList[2]
    edit_stage_train_button = widgetList[3]

    set_default_train_info_button = innerButtonList[0]
    extract_csv_train_info_button = innerButtonList[1]
    save_csv_train_info_button = innerButtonList[2]
    edit_button = innerButtonList[3]

    v_edit.set(textSetting.textList["orgInfoEditor"]["trainModify"])
    for btn in btnList:
        btn["state"] = "disabled"

    edit_button["command"] = lambda: editTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc)
    cb["state"] = "readonly"
    menuCb["state"] = "readonly"
    edit_stage_train_button["state"] = "normal"

    set_default_train_info_button["state"] = "normal"
    extract_csv_train_info_button["state"] = "normal"
    save_csv_train_info_button["state"] = "normal"

    trainIdx = cb.current()

    errorMsg = textSetting.textList["errorList"]["E4"]
    if not decryptFile.saveTrainInfo(trainIdx, varList):
        decryptFile.printError()
        mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
        return

    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
    reloadFunc()


def editAllTrain(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    result = AllEdit(tabFrame, textSetting.textList["orgInfoEditor"]["allSaveLabel"], decryptFile, rootFrameAppearance)
    if result.reloadFlag:
        reloadFunc()


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
        self.eleCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_ele, width=24, value=self.decryptFile.trainPerfNameList, state="readonly")
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
            result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

            if result:
                perfIndex = self.eleCb.current()
                num = self.v_num.get()

                errorMsg = textSetting.textList["errorList"]["E4"]
                if not self.decryptFile.saveAllEdit(perfIndex, num, self.eleCb2.current()):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                    return False
                return True
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E3"]
            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg, parent=self)

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I54"])
        self.reloadFlag = True
