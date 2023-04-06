import copy

import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

LS = 0
BS = 1
CS = 2
RS = 3


class TrainModelWidget():
    def __init__(self, root, trainIdx, game, frame, widgetList, innerButtonList, decryptFile, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.reloadFunc = reloadFunc

        edit_hensei_button = innerButtonList[3]
        edit_hensei_button["command"] = lambda: self.editHenseiTrain(widgetList, innerButtonList, reloadFunc)

        if self.game not in [LS, BS]:
            edit_model_button = innerButtonList[4]
            edit_model_button["command"] = lambda: self.editModel()
        else:
            edit_model_button = innerButtonList[4]
            edit_model_button.destroy()

        modelInfo = self.decryptFile.trainModelList[self.trainIdx]

        self.btnFrame = ttk.Frame(self.frame)
        self.btnFrame.pack(anchor=tkinter.NW, padx=20)

        self.mdlFrame = ttk.Frame(self.frame)
        self.mdlFrame.pack(side=tkinter.LEFT, padx=20)

        self.trainLb = tkinter.Label(self.mdlFrame, text="車両", font=("", 20), width=6, borderwidth=1, relief="solid")
        self.trainLb.grid(row=0, column=0)
        self.modelLb = tkinter.Label(self.mdlFrame, text="モデル", font=("", 20), width=6, borderwidth=1, relief="solid")
        self.modelLb.grid(row=1, column=0)
        if len(modelInfo["pantaNames"]) > 0:
            self.pantaLb = tkinter.Label(self.mdlFrame, text="パンタ", font=("", 20), width=6, borderwidth=1, relief="solid")
            self.pantaLb.grid(row=2, column=0)
        if len(modelInfo["colList"]) > 0:
            self.colLb = tkinter.Label(self.mdlFrame, text="COL", font=("", 20), width=6, borderwidth=1, relief="solid")
            self.colLb.grid(row=3, column=0)

        self.mdlNoLbList = []
        self.comboList = []

        for i in range(modelInfo["mdlCnt"]):
            self.mdlNoLb = tkinter.Label(self.mdlFrame, text=str(i + 1), font=("", 20), width=16, borderwidth=1, relief="solid")
            self.mdlNoLb.grid(row=0, column=i + 1)
            self.mdlNoLbList.append(self.mdlNoLb)

            self.mdlCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["mdlNames"], state="disabled")
            self.mdlCb.grid(row=1, column=i + 1)
            if modelInfo["mdlList"][i] == -1:
                self.mdlCb.current(len(modelInfo["mdlNames"]) - 1)
            else:
                self.mdlCb.current(modelInfo["mdlList"][i])
            self.comboList.append(self.mdlCb)

            if len(modelInfo["pantaNames"]) > 0:
                self.pantaCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["pantaNames"], state="disabled")
                self.pantaCb.grid(row=2, column=i + 1)
                if modelInfo["pantaList"][i] == -1:
                    self.pantaCb.current(len(modelInfo["pantaNames"]) - 1)
                else:
                    self.pantaCb.current(modelInfo["pantaList"][i])
                self.comboList.append(self.pantaCb)

            if len(modelInfo["colList"]) > 0:
                self.colCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["colNames"], state="disabled")
                self.colCb.grid(row=3, column=i + 1)
                if modelInfo["colList"][i] == -1:
                    self.colCb.current(len(modelInfo["colNames"]) - 1)
                else:
                    self.colCb.current(modelInfo["colList"][i])
                self.comboList.append(self.colCb)

    def editHenseiTrain(self, widgetList, innerButtonList, reloadFunc):
        v_edit = widgetList[0]
        cb = widgetList[1]
        menuCb = widgetList[2]
        edit_stage_train_button = widgetList[3]

        v_edit.set("保存する")
        cb["state"] = "disabled"
        menuCb["state"] = "disabled"
        edit_stage_train_button["state"] = "disabled"

        notchBtn = innerButtonList[0]
        henseiBtn = innerButtonList[1]
        colorBtn = innerButtonList[2]
        edit_hensei_button = innerButtonList[3]

        notchBtn["state"] = "disabled"
        henseiBtn["state"] = "disabled"
        colorBtn["state"] = "disabled"
        edit_hensei_button["command"] = lambda: self.saveHenseiTrain(widgetList, reloadFunc)

        if self.game not in [LS, BS]:
            edit_model_button = innerButtonList[4]
            edit_model_button["state"] = "disabled"

        for combo in self.comboList:
            combo["state"] = "readonly"

        if self.game == LS:
            modelInfo = self.decryptFile.trainModelList[self.trainIdx]
            for i in range(len(self.comboList)):
                if len(modelInfo["pantaNames"]) == 0:
                    self.comboList[i]["state"] = "disabled"
                else:
                    if i % 2 == 0:
                        self.comboList[i]["state"] = "disabled"

    def saveHenseiTrain(self, widgetList, reloadFunc):
        cb = widgetList[1]
        menuCb = widgetList[2]
        edit_stage_train_button = widgetList[3]

        cb["state"] = "readonly"
        menuCb["state"] = "readonly"
        edit_stage_train_button["state"] = "normal"

        if not self.decryptFile.saveHensei(self.trainIdx, self):
            self.decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return

        mb.showinfo(title="成功", message="編成数を修正しました")
        self.reloadFunc()

    def editModel(self):
        result = EditModelInfo(self.root, "モデル情報修正", self.game, self.trainIdx, self.decryptFile, self)
        if result.reloadFlag:
            self.reloadFunc()


class EditModelInfo(sd.Dialog):
    def __init__(self, master, title, game, trainIdx, decryptFile, trainWidget):
        self.game = game
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.trainWidget = trainWidget
        self.henseiCnt = 0
        self.reloadFlag = False
        super(EditModelInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        modelInfo = self.decryptFile.trainModelList[self.trainIdx]
        self.henseiCnt = modelInfo["mdlCnt"]

        self.btnFrame = tkinter.Frame(frame, pady=5)
        self.btnFrame.pack()
        self.listFrame = tkinter.Frame(frame)
        self.listFrame.pack()

        self.editableNum = len(self.trainWidget.comboList) // modelInfo["mdlCnt"]

        self.selectListNum = 0
        self.selectIndex = 0
        self.selectValue = ""
        self.modelInfo = None

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.trackModelLb = tkinter.Label(self.listFrame, font=("", 14), text="台車モデル")
        self.trackModelLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_trackModel = tkinter.StringVar(value=modelInfo["trackNames"])
        self.trackModelList = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_trackModel)
        self.trackModelList.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.trackModelList.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 0, self.trackModelList.curselection()))

        self.padLb = tkinter.Label(self.listFrame, width=3)
        self.padLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        self.trainModelLb = tkinter.Label(self.listFrame, font=("", 14), text="車両モデル")
        self.trainModelLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        trainModelList = copy.deepcopy(modelInfo["mdlNames"])
        trainModelList.pop()
        self.v_trainModel = tkinter.StringVar(value=trainModelList)
        self.trainModelList = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_trainModel)
        self.trainModelList.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)
        self.trainModelList.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 1, self.trainModelList.curselection()))

        self.padLb = tkinter.Label(self.listFrame, width=3)
        self.padLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)

        self.pantaModelLb = tkinter.Label(self.listFrame, font=("", 14), text="パンタモデル")
        self.pantaModelLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)
        pantaModelList = copy.deepcopy(modelInfo["pantaNames"])
        pantaModelList.pop()
        self.v_pantaModel = tkinter.StringVar(value=pantaModelList)
        self.pantaModelList = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_pantaModel)
        self.pantaModelList.grid(row=1, column=4, sticky=tkinter.W + tkinter.E)
        self.pantaModelList.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 2, self.pantaModelList.curselection()))

        if self.editableNum == 3:
            self.padLb = tkinter.Label(self.listFrame, width=3)
            self.padLb.grid(row=0, column=5, sticky=tkinter.W + tkinter.E)

            self.colModelLb = tkinter.Label(self.listFrame, font=("", 14), text="COLモデル")
            self.colModelLb.grid(row=0, column=6, sticky=tkinter.W + tkinter.E)
            colModelList = copy.deepcopy(modelInfo["colNames"])
            colModelList.pop()
            self.v_colModel = tkinter.StringVar(value=colModelList)
            self.colModelList = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_colModel)
            self.colModelList.grid(row=1, column=6, sticky=tkinter.W + tkinter.E)
            self.colModelList.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 3, self.colModelList.curselection()))

    def buttonActive(self, event, num, value):
        if len(value) == 0:
            return
        self.selectListNum = num
        self.selectIndex = value[0]
        if num == 0:
            self.selectValue = self.trackModelList.get(value[0])
        elif num == 1:
            self.selectValue = self.trainModelList.get(value[0])
        elif num == 2:
            self.selectValue = self.pantaModelList.get(value[0])
        elif num == 3:
            self.selectValue = self.colModelList.get(value[0])

        self.modifyBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"
        self.deleteBtn["state"] = "normal"

    def modify(self):
        result = sd.askstring(title="変更", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            if self.selectListNum == 0:
                self.trackModelList.delete(self.selectIndex)
                self.trackModelList.insert(self.selectIndex, result)
            elif self.selectListNum == 1:
                self.trainModelList.delete(self.selectIndex)
                self.trainModelList.insert(self.selectIndex, result)
            elif self.selectListNum == 2:
                self.pantaModelList.delete(self.selectIndex)
                self.pantaModelList.insert(self.selectIndex, result)
            elif self.selectListNum == 3:
                self.colModelList.delete(self.selectIndex)
                self.colModelList.insert(self.selectIndex, result)

            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = sd.askstring(title="挿入", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            if self.selectListNum == 0:
                self.trackModelList.insert(tkinter.END, result)
            elif self.selectListNum == 1:
                self.trainModelList.insert(tkinter.END, result)
            elif self.selectListNum == 2:
                self.pantaModelList.insert(tkinter.END, result)
            elif self.selectListNum == 3:
                self.colModelList.insert(tkinter.END, result)

            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        selectName = ""

        if self.selectListNum == 0:
            selectName = "台車モデル"
            if self.game <= BS:
                if self.trackModelList.size() <= 1:
                    mb.showerror(title="エラー", message="台車モデルは1個以上である必要あります")
                    return
            else:
                if self.trackModelList.size() <= 2:
                    mb.showerror(title="エラー", message="台車モデルは2個以上である必要あります")
                    return
        elif self.selectListNum == 1:
            selectName = "車両モデル"
            for i in range(self.henseiCnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum * i].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i + 1))
                    return
        elif self.selectListNum == 2:
            selectName = "パンタモデル"
            for i in range(self.henseiCnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum * i + 1].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i + 1))
                    return
        elif self.selectListNum == 3:
            selectName = "COLモデル"
            for i in range(self.henseiCnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum * i + 2].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i + 1))
                    return

        warnMsg = "{0}の{1}番目を削除します。\nそれでもよろしいですか？".format(selectName, self.selectIndex + 1)
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

        if result:
            if self.selectListNum == 0:
                self.trackModelList.delete(self.selectIndex)
            elif self.selectListNum == 1:
                self.trainModelList.delete(self.selectIndex)
            elif self.selectListNum == 2:
                self.pantaModelList.delete(self.selectIndex)
            elif self.selectListNum == 3:
                self.colModelList.delete(self.selectIndex)

            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def validate(self):
        warnMsg = "モデル情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            modelInfo = self.decryptFile.trainModelList[self.trainIdx]

            newTrackList = []
            for i in range(self.trackModelList.size()):
                newTrackList.append(self.trackModelList.get(i))
            modelInfo["trackNames"] = newTrackList

            newTrainList = []
            for i in range(self.trainModelList.size()):
                newTrainList.append(self.trainModelList.get(i))
            newTrainList.append("なし")
            modelInfo["mdlNames"] = newTrainList

            newPantaList = []
            for i in range(self.pantaModelList.size()):
                newPantaList.append(self.pantaModelList.get(i))
            newPantaList.append("なし")
            modelInfo["pantaNames"] = newPantaList

            if self.editableNum == 3:
                newColList = []
                for i in range(self.colModelList.size()):
                    newColList.append(self.colModelList.get(i))
                newColList.append("なし")
                modelInfo["colNames"] = newColList
            else:
                newColList = []
                colName = modelInfo["colNames"][0]
                for i in range(self.trainModelList.size()):
                    newColList.append(colName)
                newColList.append("なし")
                modelInfo["colNames"] = newColList

            if not self.decryptFile.saveModelInfo(self.trainIdx, modelInfo):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return

            return True

    def apply(self):
        mb.showinfo(title="成功", message="モデルリストを修正しました")
        self.reloadFlag = True
