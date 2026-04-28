import copy

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog, CustomAskstring

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


class TrainModelWidget():
    def __init__(self, root, trainIdx, game, frame, widgetList, innerButtonList, decryptFile, rootFrameAppearance, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        edit_hensei_button = innerButtonList[3]
        edit_hensei_button["command"] = lambda: self.editHenseiTrain(widgetList, innerButtonList, reloadFunc)

        if self.game not in [gameDefine.LS, gameDefine.BS]:
            edit_model_button = innerButtonList[4]
            edit_model_button["command"] = lambda: self.editModel()
        else:
            edit_model_button = innerButtonList[4]
            edit_model_button.destroy()

        modelInfo = self.decryptFile.trainModelList[self.trainIdx]

        self.mdlFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        self.mdlFrame.pack(padx=4)

        self.trainLb = ttkCustomWidget.CustomTtkLabel(self.mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelTrainLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
        self.trainLb.grid(row=0, column=0)
        self.modelLb = ttkCustomWidget.CustomTtkLabel(self.mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelModelLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
        self.modelLb.grid(row=1, column=0)
        if len(modelInfo["pantaNames"]) > 0:
            self.pantaLb = ttkCustomWidget.CustomTtkLabel(self.mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelPantaLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            self.pantaLb.grid(row=2, column=0)
        if len(modelInfo["colList"]) > 0:
            self.colLb = ttkCustomWidget.CustomTtkLabel(self.mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelColLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            self.colLb.grid(row=3, column=0)

        self.mdlNoLbList = []
        self.comboList = []

        for i in range(modelInfo["mdlCnt"]):
            self.mdlNoLb = ttkCustomWidget.CustomTtkLabel(self.mdlFrame, text=str(i + 1), font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=16, borderwidth=1, relief="solid")
            self.mdlNoLb.grid(row=0, column=i + 1, sticky=tkinter.W + tkinter.E)
            self.mdlNoLbList.append(self.mdlNoLb)

            self.mdlCb = ttkCustomWidget.CustomTtkCombobox(self.mdlFrame, font=textSetting.textList["font6"], width=20, value=modelInfo["mdlNames"], state="disabled")
            self.mdlCb.grid(row=1, column=i + 1)
            if modelInfo["mdlList"][i] == -1:
                self.mdlCb.current(len(modelInfo["mdlNames"]) - 1)
            else:
                self.mdlCb.current(modelInfo["mdlList"][i])
            self.comboList.append(self.mdlCb)

            if len(modelInfo["pantaNames"]) > 0:
                self.pantaCb = ttkCustomWidget.CustomTtkCombobox(self.mdlFrame, font=textSetting.textList["font6"], width=20, value=modelInfo["pantaNames"], state="disabled")
                self.pantaCb.grid(row=2, column=i + 1)
                if modelInfo["pantaList"][i] == -1:
                    self.pantaCb.current(len(modelInfo["pantaNames"]) - 1)
                else:
                    self.pantaCb.current(modelInfo["pantaList"][i])
                self.comboList.append(self.pantaCb)

            if len(modelInfo["colList"]) > 0:
                self.colCb = ttkCustomWidget.CustomTtkCombobox(self.mdlFrame, font=textSetting.textList["font6"], width=20, value=modelInfo["colNames"], state="disabled")
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

        v_edit.set(textSetting.textList["orgInfoEditor"]["trainSave"])
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

        if self.game not in [gameDefine.LS, gameDefine.BS]:
            edit_model_button = innerButtonList[4]
            edit_model_button["state"] = "disabled"

        for combo in self.comboList:
            combo["state"] = "readonly"

        if self.game == gameDefine.LS:
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
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return

        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I55"])
        self.reloadFunc()

    def editModel(self):
        result = EditModelInfo(self.root, textSetting.textList["orgInfoEditor"]["editModelLabel"], self.game, self.trainIdx, self.decryptFile, self, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc()


class EditModelInfo(CustomSimpleDialog):
    def __init__(self, master, title, game, trainIdx, decryptFile, trainWidget, rootFrameAppearance):
        self.game = game
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.trainWidget = trainWidget
        self.henseiCnt = 0
        self.reloadFlag = False
        self.rootFrameAppearance = rootFrameAppearance
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, frame):
        modelInfo = self.decryptFile.trainModelList[self.trainIdx]
        self.henseiCnt = modelInfo["mdlCnt"]

        self.btnFrame = ttkCustomWidget.CustomTtkFrame(frame)
        self.btnFrame.pack(pady=5)
        self.listFrame = ttkCustomWidget.CustomTtkFrame(frame)
        self.listFrame.pack()

        self.editableNum = len(self.trainWidget.comboList) // modelInfo["mdlCnt"]

        self.selectListNum = 0
        self.selectIndex = 0
        self.selectValue = ""
        self.modelInfo = None

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(self.btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(self.btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(self.btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.trackModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvDaishaTitle"])
        self.trackModelLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_trackModel = tkinter.StringVar(value=modelInfo["trackNames"])
        self.trackModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_trackModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        self.trackModelList.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.trackModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 0, self.trackModelList.curselection()))

        self.padLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, width=3)
        self.padLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        self.trainModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvMdlTitle"])
        self.trainModelLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        trainModelList = copy.deepcopy(modelInfo["mdlNames"])
        trainModelList.pop()
        self.v_trainModel = tkinter.StringVar(value=trainModelList)
        self.trainModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_trainModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        self.trainModelList.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)
        self.trainModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 1, self.trainModelList.curselection()))

        self.padLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, width=3)
        self.padLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)

        self.pantaModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvPantaTitle"])
        self.pantaModelLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)
        pantaModelList = copy.deepcopy(modelInfo["pantaNames"])
        pantaModelList.pop()
        self.v_pantaModel = tkinter.StringVar(value=pantaModelList)
        self.pantaModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_pantaModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        self.pantaModelList.grid(row=1, column=4, sticky=tkinter.W + tkinter.E)
        self.pantaModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 2, self.pantaModelList.curselection()))

        if self.editableNum == 3:
            self.padLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, width=3)
            self.padLb.grid(row=0, column=5, sticky=tkinter.W + tkinter.E)

            self.colModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvColTitle"])
            self.colModelLb.grid(row=0, column=6, sticky=tkinter.W + tkinter.E)
            colModelList = copy.deepcopy(modelInfo["colNames"])
            colModelList.pop()
            self.v_colModel = tkinter.StringVar(value=colModelList)
            self.colModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_colModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
            self.colModelList.grid(row=1, column=6, sticky=tkinter.W + tkinter.E)
            self.colModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 3, self.colModelList.curselection()))
        super().body(frame)

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
        resultObj = CustomAskstring(self, title=textSetting.textList["modify"], prompt=textSetting.textList["infoList"]["I27"], initialvalue=self.selectValue, bgColor=self.rootFrameAppearance.bgColor)
        result = resultObj.result

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
        resultObj = CustomAskstring(self, title=textSetting.textList["insert"], prompt=textSetting.textList["infoList"]["I27"], initialvalue=self.selectValue, bgColor=self.rootFrameAppearance.bgColor)
        result = resultObj.result

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
            selectName = textSetting.textList["orgInfoEditor"]["csvDaishaTitle"]
            if self.game in [gameDefine.LS, gameDefine.BS]:
                if self.trackModelList.size() <= 1:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(1))
                    return
            elif self.game in [gameDefine.CS, gameDefine.RS]:
                if self.trackModelList.size() <= 2:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(2))
                    return
        elif self.selectListNum == 1:
            selectName = textSetting.textList["orgInfoEditor"]["csvMdlTitle"]
            for i in range(self.henseiCnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum * i].current():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(i + 1))
                    return
        elif self.selectListNum == 2:
            selectName = textSetting.textList["orgInfoEditor"]["csvPantaTitle"]
            for i in range(self.henseiCnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum * i + 1].current():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(i + 1))
                    return
        elif self.selectListNum == 3:
            selectName = textSetting.textList["orgInfoEditor"]["csvColTitle"]
            for i in range(self.henseiCnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum * i + 2].current():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(i + 1))
                    return

        warnMsg = textSetting.textList["infoList"]["I62"].format(selectName, self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

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
        warnMsg = textSetting.textList["infoList"]["I63"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            modelInfo = self.decryptFile.trainModelList[self.trainIdx]

            newTrackList = []
            for i in range(self.trackModelList.size()):
                newTrackList.append(self.trackModelList.get(i))
            modelInfo["trackNames"] = newTrackList

            newTrainList = []
            for i in range(self.trainModelList.size()):
                newTrainList.append(self.trainModelList.get(i))
            newTrainList.append(textSetting.textList["orgInfoEditor"]["noList"])
            modelInfo["mdlNames"] = newTrainList

            newPantaList = []
            for i in range(self.pantaModelList.size()):
                newPantaList.append(self.pantaModelList.get(i))
            newPantaList.append(textSetting.textList["orgInfoEditor"]["noList"])
            modelInfo["pantaNames"] = newPantaList

            if self.editableNum == 3:
                newColList = []
                for i in range(self.colModelList.size()):
                    newColList.append(self.colModelList.get(i))
                newColList.append(textSetting.textList["orgInfoEditor"]["noList"])
                modelInfo["colNames"] = newColList
            else:
                newColList = []
                colName = modelInfo["colNames"][0]
                for i in range(self.trainModelList.size()):
                    newColList.append(colName)
                newColList.append(textSetting.textList["orgInfoEditor"]["noList"])
                modelInfo["colNames"] = newColList

            if not self.decryptFile.saveModelInfo(self.trainIdx, modelInfo):
                self.decryptFile.printError()
                errorMsg = textSetting.textList["errorList"]["E4"]
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I64"])
        self.reloadFlag = True
