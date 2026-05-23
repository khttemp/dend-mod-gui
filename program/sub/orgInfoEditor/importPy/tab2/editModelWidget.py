import copy

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class SimpleListWidget(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, frame, text, listInfo, rootFrameAppearance):
        super().__init__(frame)
        self.text = text
        self.simpleList = copy.deepcopy(listInfo)
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False

        simpleListLf = ttkCustomWidget.CustomTtkLabelFrame(self, text=text)
        simpleListLf.pack(anchor=tkinter.NW, padx=10, pady=5, side=tkinter.LEFT)

        btnFrame = ttkCustomWidget.CustomTtkFrame(simpleListLf)
        btnFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        listFrame = ttkCustomWidget.CustomTtkFrame(simpleListLf)
        listFrame.pack()

        self.selectIndexNum = -1
        copySimpleList = self.setListboxInfo(self.simpleList)
        self.v_simpleList = tkinter.StringVar(value=copySimpleList)
        self.simpleListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=25, height=6, listvariable=self.v_simpleList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.simpleListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.simpleListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.simpleListListbox, self.simpleListListbox.curselection()))

    def setListboxInfo(self, simpleList):
        displaySimpleList = []
        if len(simpleList) > 0:
            for i in range(len(simpleList)):
                displaySimpleList.append(simpleList[i])
        else:
            displaySimpleList = [textSetting.textList["orgInfoEditor"]["noList"]]
        return displaySimpleList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["orgInfoEditor"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.simpleList[self.selectIndexNum]
        result = EditSimpleListDialog(self.winfo_toplevel(), self.text + textSetting.textList["orgInfoEditor"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.simpleList[self.selectIndexNum] = result.resultValue
            displaySimpleList = self.setListboxInfo(self.simpleList)
            self.v_simpleList.set(displaySimpleList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            self.simpleListListbox.selection_clear(0, tkinter.END)

    def insert(self):
        result = EditSimpleListDialog(self.winfo_toplevel(), self.text + textSetting.textList["orgInfoEditor"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.simpleList.insert(self.selectIndexNum + result.insertPos, result.resultValue)
            displaySimpleList = self.setListboxInfo(self.simpleList)
            self.v_simpleList.set(displaySimpleList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            self.simpleListListbox.selection_clear(0, tkinter.END)

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.simpleList.pop(self.selectIndexNum)
            displaySimpleList = self.setListboxInfo(self.simpleList)
            self.v_simpleList.set(displaySimpleList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            self.simpleListListbox.selection_clear(0, tkinter.END)


class EditSimpleListDialog(CustomSimpleDialog):
    def __init__(self, master, title, mode, item, rootFrameAppearance):
        self.mode = mode
        self.item = item
        self.insertPos = None
        self.resultValue = ""
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varTemp = tkinter.StringVar()
        if self.mode == "modify":
            self.varTemp.set(self.item)
        txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
        txtEt.grid(columnspan=2, row=1, column=0, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, 2)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["orgInfoEditor"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                res = self.varTemp.get()
                if not res:
                    errorMsg = textSetting.textList["infoList"]["I44"]
                    mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
                    return False
                self.resultValue = res
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class EditModelWidget(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, frame, trainIndex, decryptFile, rootFrameAppearance, reloadWidget):
        super().__init__(frame)
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget

        buttonFrame = ttkCustomWidget.CustomTtkFrame(self)
        buttonFrame.pack(expand=True, fill=tkinter.BOTH)

        editModelButton = ttkCustomWidget.CustomTtkButton(buttonFrame, text=textSetting.textList["orgInfoEditor"]["modelInfoModify"], command=self.editModel)
        editModelButton.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, pady=5)

        buttonFrame.columnconfigure(0, weight=1)

    def editModel(self):
        result = EditModelDialog(self.winfo_toplevel(), textSetting.textList["orgInfoEditor"]["editModelLabel"], self.trainIndex, self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadWidget()


class EditModelDialog(CustomSimpleDialog):
    def __init__(self, master, title, trainIndex, decryptFile, rootFrameAppearance):
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.dirtyFlag = False
        self.reloadFlag = False
        self.rootFrameAppearance = rootFrameAppearance
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        listFrame = ttkCustomWidget.CustomTtkFrame(master)
        listFrame.pack()
        modelInfo = self.decryptFile.trainModelList[self.trainIndex]
        noText = textSetting.textList["orgInfoEditor"]["noList"]

        self.trackModelList = SimpleListWidget(listFrame, textSetting.textList["orgInfoEditor"]["csvDaishaTitle"], modelInfo["trackNames"], self.rootFrameAppearance)
        self.trackModelList.grid(row=0, column=0)
        # LS、BSの場合、台車の数は変更不可
        if self.decryptFile.game in ["LS", "BS"]:
            self.trackModelList.insertBtn.grid_remove()
            self.trackModelList.deleteBtn.grid_remove()

        trainModelNameList = copy.deepcopy(modelInfo["mdlNames"])
        if noText in trainModelNameList:
            noIndex = trainModelNameList.index(noText)
            trainModelNameList.pop(noIndex)
        self.trainModelList = SimpleListWidget(listFrame, textSetting.textList["orgInfoEditor"]["csvMdlTitle"], trainModelNameList, self.rootFrameAppearance)
        self.trainModelList.grid(row=0, column=1)
        # LSの場合、モデルの数は変更不可
        if self.decryptFile.game == "LS":
            self.trainModelList.insertBtn.grid_remove()
            self.trainModelList.deleteBtn.grid_remove()

        pantaModelNameList = copy.deepcopy(modelInfo["pantaNames"])
        if noText in pantaModelNameList:
            noIndex = pantaModelNameList.index(noText)
            pantaModelNameList.pop(noIndex)
        self.pantaModelList = SimpleListWidget(listFrame, textSetting.textList["orgInfoEditor"]["csvPantaTitle"], pantaModelNameList, self.rootFrameAppearance)
        self.pantaModelList.grid(row=1, column=0)

        colModelNameList = copy.deepcopy(modelInfo["colNames"])
        if noText in colModelNameList:
            noIndex = colModelNameList.index(noText)
            colModelNameList.pop(noIndex)
        self.colModelList = SimpleListWidget(listFrame, textSetting.textList["orgInfoEditor"]["csvColTitle"], colModelNameList, self.rootFrameAppearance)
        self.colModelList.grid(row=1, column=1)
        super().body(master)

    def validate(self):
        self.dirtyFlag |= self.trackModelList.dirtyFlag
        self.dirtyFlag |= self.trainModelList.dirtyFlag
        self.dirtyFlag |= self.pantaModelList.dirtyFlag
        self.dirtyFlag |= self.colModelList.dirtyFlag

        if not self.dirtyFlag:
            return True

        warnMsg = textSetting.textList["infoList"]["I63"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            modelInfo = self.decryptFile.trainModelList[self.trainIndex]
            noList = textSetting.textList["orgInfoEditor"]["noList"]

            newTrackList = []
            for i in range(self.trackModelList.simpleListListbox.size()):
                item = self.trackModelList.simpleListListbox.get(i)
                if item == noList:
                    continue
                newTrackList.append(item)
            trackModelCount = len(newTrackList)

            newTrainList = []
            for i in range(self.trainModelList.simpleListListbox.size()):
                item = self.trainModelList.simpleListListbox.get(i)
                if item == noList:
                    continue
                newTrainList.append(item)
            trainModelCount = len(newTrainList)

            newPantaList = []
            for i in range(self.pantaModelList.simpleListListbox.size()):
                item = self.pantaModelList.simpleListListbox.get(i)
                if item == noList:
                    continue
                newPantaList.append(item)
            pantaModelCount = len(newPantaList)

            newColList = []
            for i in range(self.colModelList.simpleListListbox.size()):
                item = self.colModelList.simpleListListbox.get(i)
                if item == noList:
                    continue
                newColList.append(item)
            colModelCount = len(newColList)

            if self.trackModelList.dirtyFlag:
                if self.decryptFile.game in ["LS", "BS"]:
                    if trackModelCount < 1:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(1))
                        return
                elif self.decryptFile.game in ["CS", "RS"]:
                    if trackModelCount < 2:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(2))
                        return
            
            if self.trainModelList.dirtyFlag:
                trainModelText = textSetting.textList["orgInfoEditor"]["csvMdlTitle"]
                trainModelIndexList = modelInfo["mdlList"]
                if self.decryptFile.game in ["BS", "CS"]:
                    if trainModelCount != colModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E136"])
                        return
                if trainModelCount == 0:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E137"].format(trainModelText))
                    return
                for trainModelIndex in trainModelIndexList:
                    if trainModelIndex != -1 and trainModelIndex >= trainModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(trainModelText, trainModelIndex))
                        return
            
            if self.pantaModelList.dirtyFlag:
                pantaModelText = textSetting.textList["orgInfoEditor"]["csvPantaTitle"]
                pantaModelIndexList = modelInfo["pantaList"]
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    if pantaModelCount == 0:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E137"].format(pantaModelText))
                        return
                if pantaModelCount > 0:
                    for pantaModelIndex in pantaModelIndexList:
                        if pantaModelIndex != -1 and pantaModelIndex >= pantaModelCount:
                            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(pantaModelText, pantaModelIndex))
                            return
            
            if self.colModelList.dirtyFlag:
                colModelText = textSetting.textList["orgInfoEditor"]["csvColTitle"]
                colModelIndexList = modelInfo["colList"]
                if self.decryptFile.game in ["BS", "CS"]:
                    if trainModelCount != colModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E136"])
                        return
                if colModelCount == 0:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E137"].format(colModelText))
                    return
                for colModelIndex in colModelIndexList:
                    if colModelIndex != -1 and colModelIndex >= colModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(colModelText, colModelIndex))
                        return

            modelInfo["trackNames"] = newTrackList
            modelInfo["mdlNames"] = newTrainList

            newPantaList.append(textSetting.textList["orgInfoEditor"]["noList"])
            modelInfo["pantaNames"] = newPantaList
            if pantaModelCount == 0:
                if len(modelInfo["pantaList"]) > 0:
                    modelInfo["pantaList"] = []
            else:
                if len(modelInfo["pantaList"]) == 0:
                    modelInfo["pantaList"] = [-1]*len(modelInfo["mdlList"])
            modelInfo["colNames"] = newColList

            if not self.decryptFile.saveModelInfo(self.trainIndex, modelInfo):
                self.decryptFile.printError()
                errorMsg = textSetting.textList["errorList"]["E4"]
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return
            return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I64"])
            self.reloadFlag = True
