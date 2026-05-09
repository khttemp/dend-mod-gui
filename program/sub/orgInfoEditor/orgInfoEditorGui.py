import copy
import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

import program.sub.orgInfoEditor.orgInfoEditorProcess as orgInfoEditorProcess
from program.sub.orgInfoEditor.dendDecrypt import LSdecrypt as dendLs
from program.sub.orgInfoEditor.dendDecrypt import BSdecrypt as dendBs
from program.sub.orgInfoEditor.dendDecrypt import CSdecrypt as dendCs
from program.sub.orgInfoEditor.dendDecrypt import RSdecrypt as dendRs
from program.sub.orgInfoEditor.dendDecrypt import SSdecrypt as dendSs

from program.sub.orgInfoEditor.importPy.editStageTrainWidget import EditStageDialog
from program.sub.orgInfoEditor.importPy.tkinterTab import (
    tab1AllWidget, tab2AllWidget, tab3AllWidget
)


class OrgInfoEditorWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict, appearance):
        super().__init__(master)
        self.importDict = importDict
        self.rootFrameAppearance = appearance
        self.decryptFile = None
        self.defaultData = []

        gameList = [
            "Shining Stage",
            "Rising Stage",
            "Climax Stage",
            "Burning Stage",
            "Lightning Stage",
        ]
        self.editStageTrainList = [
            "Rising Stage",
            "Climax Stage",
            "Burning Stage"
        ]
        self.oldGameList = ["RS", "CS", "BS", "LS"]

        headerFrame = ttkCustomWidget.CustomTtkFrame(master)
        headerFrame.pack(fill=tkinter.X, padx=40, pady=(25, 0))

        self.gameCb = ttkCustomWidget.CustomTtkCombobox(headerFrame, width=23, state="readonly", values=gameList)
        self.gameCb.bind("<<ComboboxSelected>>", lambda e: self.selectGame())
        self.gameCb.grid(row=0, column=0, padx=15, pady=(0, 15))
        self.gameCb.current(0)

        self.trainCb = ttkCustomWidget.CustomTtkCombobox(headerFrame, width=40, state="disabled")
        self.trainCb.bind("<<ComboboxSelected>>", lambda e: self.selectTrain())
        self.trainCb.grid(row=0, column=1, padx=20, pady=(0, 15))

        self.menuCb = ttkCustomWidget.CustomTtkCombobox(headerFrame, width=30, state="disabled")
        self.menuCb.bind("<<ComboboxSelected>>", lambda e: self.selectMenu())
        self.menuCb.grid(row=0, column=2, padx=20, pady=(0, 15))

        self.edit_stage_train_button = ttkCustomWidget.CustomTtkButton(headerFrame, text=textSetting.textList["orgInfoEditor"]["editStageDefaultTrain"], width=23, command=self.editStageTrain, state="disabled")
        self.edit_stage_train_button.grid(row=0, column=3, padx=20, pady=(0, 10))

        self.tabFrame = ttkCustomWidget.CustomTtkFrame(master, borderwidth=1, relief="solid")
        self.tabFrame.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 20))

        self.selectGame()

    def deleteWidget(self):
        children = self.tabFrame.winfo_children()
        for child in children:
            child.destroy()

    def selectGame(self):
        self.deleteWidget()
        self.trainCb["state"] = "disabled"
        self.trainCb["values"] = []
        self.trainCb.set("")

        self.menuCb["state"] = "disabled"
        self.menuCb["values"] = []
        self.menuCb.set("")

        if self.gameCb.get() in self.editStageTrainList:
            self.edit_stage_train_button.grid(row=0, column=3)
            self.edit_stage_train_button["state"] = "disabled"
        else:
            self.edit_stage_train_button.grid_remove()

    def selectTrain(self):
        self.selectInfo(self.trainCb.current(), self.menuCb.current())

    def selectMenu(self):
        self.selectInfo(self.trainCb.current(), self.menuCb.current())

    def selectInfo(self, trainIndex, menuIndex):
        self.deleteWidget()

        if menuIndex == 0:
            tab1AllWidget(self.tabFrame, self.decryptFile, trainIndex, self.defaultData, self.rootFrameAppearance, self.reloadWidget)
        elif menuIndex == 1:
            tab2AllWidget(self.tabFrame, self.decryptFile, trainIndex, self.defaultData, self.rootFrameAppearance, self.reloadWidget)
        elif menuIndex == 2:
            tab3AllWidget(self.tabFrame, self.decryptFile, trainIndex, self.rootFrameAppearance, self.reloadWidget)

    def editStageTrain(self):
        EditStageDialog(self.winfo_toplevel(), textSetting.textList["orgInfoEditor"]["editStageLabel"], self.decryptFile, self.rootFrameAppearance)

    def modifiedTrainNameList(self):
        copyTrainNameList = copy.deepcopy(self.decryptFile.trainNameList)
        for index, trainName in enumerate(copyTrainNameList):
            trainOrgInfo = self.decryptFile.trainInfoList[index]
            if trainOrgInfo is None:
                copyTrainNameList[index] = trainName + textSetting.textList["orgInfoEditor"]["dataCorrupted"]
                continue
            editFlag = False

            speedList = trainOrgInfo[0]
            notchCnt = len(speedList) // self.decryptFile.notchContentCnt
            defNotchCnt = len(self.defaultData[index]["notch"])
            if notchCnt != defNotchCnt:
                editFlag = True
            else:
                for i in range(len(speedList)):
                    speed = speedList[i]
                    if i >= 0 and i < notchCnt:
                        defSpeed = self.defaultData[index]["notch"][i]
                    elif i >= notchCnt and i < notchCnt*2:
                        defSpeed = self.defaultData[index]["tlk"][i - notchCnt]
                    elif i >= notchCnt*2 and i < notchCnt*3:
                        defSpeed = self.defaultData[index]["soundNum"][i - notchCnt*2]
                    elif i >= notchCnt*3 and i < notchCnt*4:
                        defSpeed = self.defaultData[index]["add"][i - notchCnt*3]
                    if speed != defSpeed:
                        editFlag = True
                        break

            perfList = trainOrgInfo[1]
            for i in range(len(perfList)):
                perf = perfList[i]
                defPerf = self.defaultData[index]["att"][i]
                if perf != defPerf:
                    editFlag = True
                    break

            if self.decryptFile.game in ["CS", "RS"]:
                hurikoList = trainOrgInfo[2]
                for i in range(len(hurikoList)):
                    huriko = hurikoList[i]
                    defHuriko = self.defaultData[index]["huriko"][i]
                    if huriko != defHuriko:
                        editFlag = True
                        break

            if self.decryptFile.game == "SS":
                rainList = trainOrgInfo[2]
                for i in range(len(rainList)):
                    rain = rainList[i]
                    defRain = self.defaultData[index]["rain"][i]
                    if rain != defRain:
                        editFlag = True
                        break

                carbList = trainOrgInfo[3]
                for i in range(len(carbList)):
                    carb = carbList[i]
                    defCarb = self.defaultData[index]["carb"][i]
                    if carb != defCarb:
                        editFlag = True
                        break

                otherList = trainOrgInfo[4]
                for i in range(len(otherList)):
                    other = otherList[i]
                    defOther = self.defaultData[index]["other"][i]
                    if other != defOther:
                        editFlag = True
                        break

                hurikoList = trainOrgInfo[5]
                if hurikoList is not None:
                    if self.defaultData[index]["huriko"] is not None:
                        for i in range(len(hurikoList)):
                            huriko = hurikoList[i]
                            defHuriko = self.defaultData[index]["huriko"][i]
                            if huriko != defHuriko:
                                editFlag = True
                                break
                    else:
                        editFlag = True
                else:
                    if self.defaultData[index]["huriko"] is not None:
                        editFlag = True

                oneWheelList = trainOrgInfo[6]
                if oneWheelList is not None:
                    if self.defaultData[index]["oneWheel"] is not None:
                        for i in range(len(oneWheelList)):
                            oneWheel = oneWheelList[i]
                            defOneWheel = self.defaultData[index]["oneWheel"][i]
                            if oneWheel != defOneWheel:
                                editFlag = True
                                break
                else:
                    if self.defaultData[index]["oneWheel"] is not None:
                        editFlag = True

            if editFlag:
                copyTrainNameList[index] = trainName + textSetting.textList["orgInfoEditor"]["modified"]

        return copyTrainNameList

    def initSelect(self):
        self.trainCb["values"] = self.modifiedTrainNameList()
        self.trainCb.current(0)
        self.trainCb["state"] = "readonly"

        if self.decryptFile.game in self.oldGameList:
            self.menuCb["values"] = textSetting.textList["orgInfoEditor"]["menuComboValues"]
        else:
            self.menuCb["values"] = textSetting.textList["orgInfoEditor"]["menuComboSSValues"]
        self.menuCb.current(0)
        self.menuCb["state"] = "readonly"
        self.selectInfo(self.trainCb.current(), self.menuCb.current())

        self.edit_stage_train_button["state"] = "normal"

    def openFile(self):
        if self.gameCb.get() == "Lightning Stage":
            file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA.BIN")])
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendLs.LSdecrypt(file_path)
        elif self.gameCb.get() == "Burning Stage":
            file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA2ND.BIN")])
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendBs.BSdecrypt(file_path)
        elif self.gameCb.get() == "Climax Stage":
            file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA3RD.BIN")])
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendCs.CSdecrypt(file_path)
        elif self.gameCb.get() == "Rising Stage":
            file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA4TH.BIN")])
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendRs.RSdecrypt(file_path)
        elif self.gameCb.get() == "Shining Stage":
            file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "train_org_data.den")])
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendSs.SSdecrypt(file_path)
        else:
            return

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E4"])
            return

        result, obj = orgInfoEditorProcess.readDefaultData(self.decryptFile.game)
        if not result:
            mb.showerror(title=textSetting.textList["error"], message=obj["message"])
            return

        self.defaultData = obj["data"]
        self.initSelect()

    def reloadWidget(self):
        self.decryptFile = self.decryptFile.reload()
        idx = self.trainCb.current()
        self.trainCb["values"] = self.modifiedTrainNameList()
        self.trainCb.current(idx)
        self.selectTrain()
