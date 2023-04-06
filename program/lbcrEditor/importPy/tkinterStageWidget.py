import copy

import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

LS = 0
BS = 1
CS = 2
RS = 3


class EditStageInfo(sd.Dialog):
    def __init__(self, master, title, game, decryptFile):
        self.game = game
        self.decryptFile = decryptFile
        super(EditStageInfo, self).__init__(parent=master, title=title)

    def body(self, master):
        self.train_1pLb = tkinter.Label(master, text="1P", font=("", 14))
        self.train_1pLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.train_2pLb = tkinter.Label(master, text="2P", font=("", 14))
        self.train_2pLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        self.train_3pLb = tkinter.Label(master, text="3P", font=("", 14))
        self.train_3pLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)

        self.trainList = []

        trackComboList = ["標準軌", "狭軌"]

        if self.game > BS:
            self.trackLb = tkinter.Label(master, text="台車", font=("", 14))
            self.trackLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)

        stageStartIdx = self.decryptFile.stageEditIdx
        self.trainComboList = copy.deepcopy(self.decryptFile.trainNameList)
        self.trainComboList.append("なし")
        for i in range(self.decryptFile.stageCnt):
            info = self.decryptFile.stageList[stageStartIdx + i]
            self.stageLb = tkinter.Label(master, text="{0}ステージ".format(i + 1), font=("", 14))
            self.stageLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)

            self.train_1pCb = ttk.Combobox(master, font=("", 14), width=8, value=self.trainComboList)
            self.train_1pCb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.train_1pCb.current(info[1])
            self.trainList.append(self.train_1pCb)
            self.train_2pCb = ttk.Combobox(master, font=("", 14), width=8, value=self.trainComboList)
            self.train_2pCb.grid(row=i + 1, column=2, sticky=tkinter.W + tkinter.E)
            self.train_2pCb.current(info[2])
            self.trainList.append(self.train_2pCb)
            self.train_3pCb = ttk.Combobox(master, font=("", 14), width=8, value=self.trainComboList)
            self.train_3pCb.grid(row=i + 1, column=3, sticky=tkinter.W + tkinter.E)
            if info[3] == -1:
                self.train_3pCb.current(len(self.trainComboList) - 1)
            else:
                self.train_3pCb.current(info[3])
            self.trainList.append(self.train_3pCb)

            if self.game > BS:
                self.trackCb = ttk.Combobox(master, font=("", 14), width=8, value=trackComboList)
                self.trackCb.grid(row=i + 1, column=4, sticky=tkinter.W + tkinter.E)
                self.trackCb.current(info[4])
                self.trainList.append(self.trackCb)

    def validate(self):
        warnMsg = "ステージ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            index = self.decryptFile.stageIdx
            # stageAllCnt
            self.decryptFile.byteArr[index]
            index += 1
            stageList = self.decryptFile.stageList

            infoCnt = 4
            if self.game == BS:
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

                if self.game > BS:
                    trackCb = self.trainList[infoCnt * i + 3].current()
                    stageList[self.decryptFile.stageEditIdx + i][4] = trackCb

            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            if not self.decryptFile.saveStageInfo(stageList):
                self.decryptFile.printError()
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="ステージ設定を修正しました")
