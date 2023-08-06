import codecs
import tkinter
import traceback
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
from tkinter import filedialog as fd

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


def setDefault(tabFrame, decryptFile, game, trainIdx, defaultData, reloadFunc):
    result = SetDefaultEdit(tabFrame, "車両の性能をデフォルトに戻す", decryptFile, game, trainIdx, defaultData)
    if result.reloadFlag:
        reloadFunc()


class SetDefaultEdit(sd.Dialog):
    def __init__(self, master, title, decryptFile, game, trainIdx, defaultData):
        self.decryptFile = decryptFile
        self.game = game
        self.trainIdx = trainIdx
        self.defaultData = defaultData
        self.reloadFlag = False
        super(SetDefaultEdit, self).__init__(parent=master, title=title)

    def body(self, master):
        self.copySrcCb = ttk.Combobox(master, width=12, font=("", 14), value=self.decryptFile.trainNameList, state="readonly")
        self.copySrcCb.bind("<<ComboboxSelected>>", lambda e: self.selectTrain())
        self.copySrcCb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S, padx=3)
        self.copySrcCb.current(self.trainIdx)

        self.v_infoNotch = tkinter.IntVar()
        self.v_infoNotch.set(0)
        self.infoNotchCb = tkinter.Checkbutton(master, text="ノッチ", font=("", 14), variable=self.v_infoNotch)
        self.infoNotchCb.grid(row=0, column=1, sticky=tkinter.W, padx=3)

        self.v_infoPerf = tkinter.IntVar()
        self.v_infoPerf.set(0)
        self.infoPerfCb = tkinter.Checkbutton(master, text="性能", font=("", 14), variable=self.v_infoPerf)
        self.infoPerfCb.grid(row=1, column=1, sticky=tkinter.W, padx=3)

        if self.game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
            self.infoDefLb = tkinter.Label(master, text="をデフォルトに戻す", font=("", 14))
            self.infoDefLb.grid(row=1, column=2, sticky=tkinter.N + tkinter.S, padx=3)
        else:
            self.v_infoRain = tkinter.IntVar()
            self.v_infoRain.set(0)
            self.infoRainCb = tkinter.Checkbutton(master, text="雨", font=("", 14), variable=self.v_infoRain)
            self.infoRainCb.grid(row=2, column=1, sticky=tkinter.W, padx=3)

            self.v_infoCarb = tkinter.IntVar()
            self.v_infoCarb.set(0)
            self.infoCarbCb = tkinter.Checkbutton(master, text="カーブ", font=("", 14), variable=self.v_infoCarb)
            self.infoCarbCb.grid(row=3, column=1, sticky=tkinter.W, padx=3)

            self.v_infoOther = tkinter.IntVar()
            self.v_infoOther.set(0)
            self.infoOtherCb = tkinter.Checkbutton(master, text="Other", font=("", 14), variable=self.v_infoOther)
            self.infoOtherCb.grid(row=4, column=1, sticky=tkinter.W, padx=3)

            self.v_infoHuriko = tkinter.IntVar()
            self.v_infoHuriko.set(0)
            self.v_hurikoText = tkinter.StringVar()
            self.v_hurikoText.set("振り子")
            self.infoHurikoCb = tkinter.Checkbutton(master, textvariable=self.v_hurikoText, font=("", 14), variable=self.v_infoHuriko)
            self.infoHurikoCb.grid(row=5, column=1, sticky=tkinter.W, padx=3)

            self.v_infoOneWheel = tkinter.IntVar()
            self.v_infoOneWheel.set(0)
            self.v_oneWheelText = tkinter.StringVar()
            self.v_oneWheelText.set("片輪走行")
            self.infoOneWheelCb = tkinter.Checkbutton(master, textvariable=self.v_oneWheelText, font=("", 14), variable=self.v_infoOneWheel)
            self.infoOneWheelCb.grid(row=6, column=1, sticky=tkinter.W, padx=3)

            self.infoDefLb = tkinter.Label(master, text="をデフォルトに戻す", font=("", 14))
            self.infoDefLb.grid(row=0, column=2, sticky=tkinter.N + tkinter.S, padx=3)

            self.selectTrain()

    def selectTrain(self):
        if self.game == gameDefine.SS:
            if self.copySrcCb.current() in [12, 19, 25]:
                self.v_hurikoText.set("振り子")
            else:
                self.v_hurikoText.set("振り子(削除)")

            if self.copySrcCb.current() in [27, 29]:
                self.v_oneWheelText.set("片輪走行")
            else:
                self.v_oneWheelText.set("片輪走行(削除)")

    def validate(self):
        if self.game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
            if self.v_infoNotch.get() == 0 and self.v_infoPerf.get() == 0:
                mb.showerror(title="エラー", message="コピー項目を選択してください")
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
                mb.showerror(title="エラー", message="コピー項目を選択してください")
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
                warnMsg += "※{0}のノッチ情報を{1}ノッチまで戻します。\n".format(self.decryptFile.trainNameList[srcIdx], distNotchNum)
            elif srcNotchNum < distNotchNum:
                warnMsg += "※{0}のノッチ情報を{1}ノッチまで戻します。\n".format(self.decryptFile.trainNameList[srcIdx], srcNotchNum)

        if self.v_infoNotch.get() == 1:
            warnMsg += "「ノッチ」"
        if self.v_infoPerf.get() == 1:
            warnMsg += "「性能」"

        if self.game == gameDefine.SS:
            if self.v_infoRain.get() == 1:
                warnMsg += "「雨」"
            if self.v_infoCarb.get() == 1:
                warnMsg += "「カーブ」"
            if self.v_infoOther.get() == 1:
                warnMsg += "「Other」"
            if self.v_infoHuriko.get() == 1:
                warnMsg += "「振り子」"
            if self.v_infoOneWheel.get() == 1:
                warnMsg += "「片輪走行」"
        warnMsg += "を\n全部元に戻しますか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

        if result:
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            if not self.decryptFile.setDefaultTrainInfo(srcList, distData, checkStatusList):
                self.decryptFile.printError()
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="データを元に戻しました")
        self.reloadFlag = True


def extractCsvTrainInfo(game, trainIdx, decryptFile):
    filename = decryptFile.trainNameList[trainIdx]
    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension='csv', filetypes=[('traininfo_csv', '*.csv')])
        errorMsg = "CSVで取り出す機能が失敗しました。\n権限問題の可能性があります。"
        if file_path:
            if not decryptFile.extractCsvTrainInfo(trainIdx, file_path):
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return False
            mb.showinfo(title="成功", message="CSVで取り出しました")
    else:
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension='txt', filetypes=[('ファイル', '*.txt')])
        errorMsg = "テキストで取り出す機能が失敗しました。\n権限問題の可能性があります。"
        if file_path:
            try:
                data = decryptFile.dataList[decryptFile.trainNameList[trainIdx]]
                w = open(file_path, "wb")
                w.write(data.script)
                w.close()
                mb.showinfo(title="成功", message="テキストで取り出しました")
            except Exception:
                w = open("error.log", "a")
                w.write(traceback.format_exc())
                w.close()
                mb.showerror(title="エラー", message=errorMsg)


def saveCsvTrainInfo(game, trainIdx, decryptFile, reloadFunc):
    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        file_path = fd.askopenfilename(defaultextension='csv', filetypes=[("traindata_csv", "*.csv")])
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
            mb.showerror(title="エラー", message=decryptFile.error)
            return
        warnMsg = "選択したCSVで上書きします。\nそれでもよろしいですか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")

        if result:
            errorMsg = "予想外のエラーです"
            if not decryptFile.saveCsvTrainInfo(trainIdx):
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return False
            mb.showinfo(title="成功", message="車両情報を改造しました")
            reloadFunc()
    else:
        file_path = fd.askopenfilename(filetypes=[("ファイル", "*.txt")])
        if not file_path:
            return
        result = mb.askquestion(title="確認", message="denファイルを上書きします\nそれでもよろしいでしょうか？\n(権限問題で上書き失敗することもあります)", icon="warning")
        if result == "no":
            return

        try:
            data = decryptFile.dataList[decryptFile.trainNameList[trainIdx]]
            with open(file_path, "rb") as f:
                data.script = f.read()
            data.save()
            with open(decryptFile.filePath, "wb") as w:
                w.write(decryptFile.env.file.save())
            mb.showinfo(title="成功", message="denファイルを上書きしました")
            reloadFunc()
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message="予想外のエラーです")


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

    v_edit.set("保存する")
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

    v_edit.set("この車両を修正する")
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

    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
    if not decryptFile.saveTrainInfo(trainIdx, varList):
        decryptFile.printError()
        mb.showerror(title="保存エラー", message=errorMsg)
        return

    mb.showinfo(title="成功", message="車両を改造しました")
    reloadFunc()


def editAllTrain(tabFrame, decryptFile, reloadFunc):
    result = AllEdit(tabFrame, "全車両の性能を一括修正", decryptFile)
    if result.reloadFlag:
        reloadFunc()


class AllEdit(sd.Dialog):
    def __init__(self, master, title, decryptFile):
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.reloadFlag = False
        super(AllEdit, self).__init__(parent=master, title=title)

    def body(self, master):
        self.eleLb = tkinter.Label(master, text="要素", width=5, font=("", 14))
        self.eleLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S, padx=3)
        self.v_ele = tkinter.StringVar()
        self.eleCb = ttk.Combobox(master, textvariable=self.v_ele, width=24, value=self.decryptFile.trainPerfNameList, state="readonly")
        self.eleCb.grid(row=0, column=1, sticky=tkinter.N + tkinter.S, padx=3)
        self.v_ele.set(self.decryptFile.trainPerfNameList[0])

        self.allLb = tkinter.Label(master, text="を全部", width=5, font=("", 14))
        self.allLb.grid(row=0, column=2, sticky=tkinter.N + tkinter.S, padx=3)

        self.v_num = tkinter.DoubleVar()
        self.v_num.set(1.0)
        self.numEt = tkinter.Entry(master, textvariable=self.v_num, width=6, font=("", 14), justify="right")
        self.numEt.grid(row=0, column=3, sticky=tkinter.N + tkinter.S, padx=3)

        calcList = ["倍にする", "にする"]
        self.v_ele2 = tkinter.StringVar()
        self.eleCb2 = ttk.Combobox(master, textvariable=self.v_ele2, font=("", 14), width=8, value=calcList, state="readonly")
        self.v_ele2.set(calcList[0])

        self.eleCb2.grid(row=0, column=4, sticky=tkinter.N + tkinter.S, padx=3)

    def validate(self):
        try:
            result = float(self.v_num.get())
            if self.eleCb2.current() == 0:
                warnMsg = "全車両同じ倍率で変更され、すぐ保存されます。\nそれでもよろしいですか？"
            else:
                warnMsg = "全車両同じ数値で変更され、すぐ保存されます。\nそれでもよろしいですか？"
            result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

            if result:
                perfIndex = self.eleCb.current()
                num = self.v_num.get()

                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                if not self.decryptFile.saveAllEdit(perfIndex, num, self.eleCb2.current()):
                    self.decryptFile.printError()
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False
                return True
        except Exception:
            errorMsg = "数字で入力してください。"
            mb.showerror(title="数字エラー", message=errorMsg, parent=self)

    def apply(self):
        mb.showinfo(title="成功", message="全車両を改造しました")
        self.reloadFlag = True
