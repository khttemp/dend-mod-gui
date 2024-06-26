import copy

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog, CustomAskstring

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


class EditStageInfo(CustomSimpleDialog):
    def __init__(self, master, title, game, decryptFile, rootFrameAppearance):
        self.game = game
        self.decryptFile = decryptFile
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.train_1pLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["stage1PLabel"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
        self.train_1pLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.train_2pLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["stage2PLabel"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
        self.train_2pLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        self.train_3pLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["stage3PLabel"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
        self.train_3pLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)

        self.trainList = []

        trackComboList = textSetting.textList["orgInfoEditor"]["trackComboList"]

        if self.game in [gameDefine.CS, gameDefine.RS]:
            self.trackLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["stageTrackName"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
            self.trackLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)

        stageStartIdx = self.decryptFile.stageEditIdx
        self.trainComboList = copy.deepcopy(self.decryptFile.trainNameList)
        self.trainComboList.append(textSetting.textList["orgInfoEditor"]["noList"])
        for i in range(self.decryptFile.stageCnt):
            info = self.decryptFile.stageList[stageStartIdx + i]
            self.stageLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["stageNumLabel"].format(i + 1), font=textSetting.textList["font2"], anchor=tkinter.CENTER)
            self.stageLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)

            self.train_1pCb = ttkCustomWidget.CustomTtkCombobox(master, font=textSetting.textList["font2"], width=8, value=self.trainComboList)
            self.train_1pCb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.train_1pCb.current(info[1])
            self.trainList.append(self.train_1pCb)
            self.train_2pCb = ttkCustomWidget.CustomTtkCombobox(master, font=textSetting.textList["font2"], width=8, value=self.trainComboList)
            self.train_2pCb.grid(row=i + 1, column=2, sticky=tkinter.W + tkinter.E)
            self.train_2pCb.current(info[2])
            self.trainList.append(self.train_2pCb)
            self.train_3pCb = ttkCustomWidget.CustomTtkCombobox(master, font=textSetting.textList["font2"], width=8, value=self.trainComboList)
            self.train_3pCb.grid(row=i + 1, column=3, sticky=tkinter.W + tkinter.E)
            if info[3] == -1:
                self.train_3pCb.current(len(self.trainComboList) - 1)
            else:
                self.train_3pCb.current(info[3])
            self.trainList.append(self.train_3pCb)

            if self.game in [gameDefine.CS, gameDefine.RS]:
                self.trackCb = ttkCustomWidget.CustomTtkCombobox(master, font=textSetting.textList["font2"], width=8, value=trackComboList)
                self.trackCb.grid(row=i + 1, column=4, sticky=tkinter.W + tkinter.E)
                self.trackCb.current(info[4])
                self.trainList.append(self.trackCb)
        super().body(master)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I42"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            index = self.decryptFile.stageIdx
            # stageAllCnt
            self.decryptFile.byteArr[index]
            index += 1
            stageList = self.decryptFile.stageList

            infoCnt = 4
            if self.game == gameDefine.BS:
                infoCnt = 3

            for i in range(self.decryptFile.stageCnt):
                train_1pCb = self.trainList[infoCnt * i].current()
                if train_1pCb == len(self.trainComboList) - 1:
                    train_1pCb = -1
                stageList[self.decryptFile.stageEditIdx + i][1] = train_1pCb

                train_2pCb = self.trainList[infoCnt * i + 1].current()
                if train_2pCb == len(self.trainComboList) - 1:
                    train_2pCb = -1
                stageList[self.decryptFile.stageEditIdx + i][2] = train_2pCb

                train_3pCb = self.trainList[infoCnt * i + 2].current()
                if train_3pCb == len(self.trainComboList) - 1:
                    train_3pCb = -1
                stageList[self.decryptFile.stageEditIdx + i][3] = train_3pCb

                if self.game in [gameDefine.CS, gameDefine.RS]:
                    trackCb = self.trainList[infoCnt * i + 3].current()
                    stageList[self.decryptFile.stageEditIdx + i][4] = trackCb

            errorMsg = textSetting.textList["errorList"]["E4"]
            if not self.decryptFile.saveStageInfo(stageList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I43"])
