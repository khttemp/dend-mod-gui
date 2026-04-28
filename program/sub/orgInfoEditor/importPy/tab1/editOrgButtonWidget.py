import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.orgInfoEditor.importPy.tab1.setDefaultWidget import SetDefaultEdit
from program.sub.orgInfoEditor.importPy.tab1.editAllTrainInfoWidget import AllEdit


class EditOrgButtonWidget(tkinter.Frame):
    def __init__(self, master, decryptFile, defaultData, rootFrameAppearance, reloadWidget):
        super().__init__(master)
        self.root = master
        self.decryptFile = decryptFile
        self.defaultData = defaultData
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget
        self.oldGameList = ["RS", "CS", "BS", "LS"]

        btnFrame = ttkCustomWidget.CustomTtkFrame(master)
        btnFrame.pack(fill=tkinter.X, anchor=tkinter.NW, padx=10, pady=5)

        self.set_default_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"], command=self.setDefault)
        self.set_default_train_info_button.grid(row=0, column=0, padx=5, sticky=tkinter.NSEW)

        if decryptFile.game in self.oldGameList:
            extract_csv_train_info_text = textSetting.textList["orgInfoEditor"]["extractCsv"]
        else:
            extract_csv_train_info_text = textSetting.textList["orgInfoEditor"]["extractText"]
        self.extract_csv_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=extract_csv_train_info_text)
        # command=lambda: extractCsvTrainInfo(game, trainIdx, decryptFile)
        self.extract_csv_train_info_button.grid(row=0, column=1, padx=5, sticky=tkinter.NSEW)

        if decryptFile.game in ["RS", "CS", "BS", "LS"]:
            save_csv_train_info_text = textSetting.textList["orgInfoEditor"]["saveCsv"]
        else:
            save_csv_train_info_text = textSetting.textList["orgInfoEditor"]["saveText"]
        self.save_csv_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=save_csv_train_info_text)
        # command=lambda: saveCsvTrainInfo(game, trainIdx, decryptFile, reloadFunc)
        self.save_csv_train_info_button.grid(row=0, column=2, padx=5, sticky=tkinter.NSEW)

        self.edit_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["orgInfoEditor"]["trainModify"], command=self.editTrain)
        self.edit_button.grid(row=0, column=3, padx=5, sticky=tkinter.NSEW)

        self.save_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["orgInfoEditor"]["trainSave"], command=self.saveTrain)
        self.save_button.grid_remove()

        self.edit_all_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["orgInfoEditor"]["allSave"], command=self.editAllTrain)
        self.edit_all_button.grid(row=0, column=4, padx=5, sticky=tkinter.NSEW)

        btnFrame.grid_columnconfigure(0, weight=1, uniform="button")
        btnFrame.grid_columnconfigure(1, weight=1, uniform="button")
        btnFrame.grid_columnconfigure(2, weight=1, uniform="button")
        btnFrame.grid_columnconfigure(3, weight=1, uniform="button")
        btnFrame.grid_columnconfigure(4, weight=1, uniform="button")

    def setDefault(self):
        orgInfoEditorWindow = self.root.master.winfo_children()[2]
        trainIndex = orgInfoEditorWindow.trainCb.current()
        result = SetDefaultEdit(self.root, textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"], trainIndex, self.decryptFile, self.defaultData, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadWidget()

    def editTrain(self):
        orgInfoEditorWindow = self.root.master.winfo_children()[2]
        orgInfoEditorWindow.gameCb["state"] = "disabled"
        orgInfoEditorWindow.trainCb["state"] = "disabled"
        orgInfoEditorWindow.menuCb["state"] = "disabled"
        orgInfoEditorWindow.edit_stage_train_button["state"] = "disabled"

        self.set_default_train_info_button["state"] = "disabled"
        self.extract_csv_train_info_button["state"] = "disabled"
        self.save_csv_train_info_button["state"] = "disabled"
        self.edit_all_button["state"] = "disabled"

        self.edit_button.grid_remove()
        self.save_button.grid(row=0, column=3, padx=5, sticky=tkinter.NSEW)

        tabFrame = self.root.master.winfo_children()[4]
        notchPerfFrame = tabFrame.winfo_children()[2]

        speedLf = notchPerfFrame.winfo_children()[0]
        scrollbarframe = speedLf.winfo_children()[0]
        canvas = scrollbarframe.winfo_children()[1]
        interior = canvas.winfo_children()[0]

        for notchWidget in interior.winfo_children():
            notchWidget.speedBtn["state"] = "normal"
            notchWidget.tlkBtn["state"] = "normal"
            if self.decryptFile.notchContentCnt > 2:
                notchWidget.soundBtn["state"] = "normal"
                notchWidget.addBtn["state"] = "normal"

        perfLf = notchPerfFrame.winfo_children()[1]
        scrollbarframe = perfLf.winfo_children()[0]
        canvas = scrollbarframe.winfo_children()[1]
        interior = canvas.winfo_children()[0]

        for perfWidget in interior.winfo_children():
            perfWidget.perfBtn["state"] = "normal"

    def saveTrain(self):
        valueList = []
        orgInfoEditorWindow = self.root.master.winfo_children()[2]
        orgInfoEditorWindow.gameCb["state"] = "readonly"
        orgInfoEditorWindow.trainCb["state"] = "readonly"
        orgInfoEditorWindow.menuCb["state"] = "readonly"
        orgInfoEditorWindow.edit_stage_train_button["state"] = "normal"

        self.edit_button.grid(row=0, column=3, padx=5, sticky=tkinter.NSEW)
        self.save_button.grid_remove()

        tabFrame = self.root.master.winfo_children()[4]
        notchPerfFrame = tabFrame.winfo_children()[2]

        speedLf = notchPerfFrame.winfo_children()[0]
        scrollbarframe = speedLf.winfo_children()[0]
        canvas = scrollbarframe.winfo_children()[1]
        interior = canvas.winfo_children()[0]

        for notchWidget in interior.winfo_children():
            valueList.append(notchWidget.speedValue)
            valueList.append(notchWidget.tlkValue)
            if self.decryptFile.notchContentCnt > 2:
                valueList.append(notchWidget.soundValue)
                valueList.append(notchWidget.addValue)

        perfLf = notchPerfFrame.winfo_children()[1]
        scrollbarframe = perfLf.winfo_children()[0]
        canvas = scrollbarframe.winfo_children()[1]
        interior = canvas.winfo_children()[0]

        for i in range(len(self.decryptFile.trainPerfNameList)):
            perfWidget = interior.winfo_children()[i]
            valueList.append(perfWidget.perfValue)

        if self.decryptFile.game in ["CS", "RS"]:
            for i in range(2):
                index = len(self.decryptFile.trainPerfNameList)
                hurikoWidget = interior.winfo_children()[index + i]
                valueList.append(hurikoWidget.hurikoValue)

        trainIndex = orgInfoEditorWindow.trainCb.current()
        if not self.decryptFile.saveTrainInfo(trainIndex, valueList):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return

        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
        self.reloadWidget()

    def editAllTrain(self):
        result = AllEdit(self.root, textSetting.textList["orgInfoEditor"]["allSaveLabel"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadWidget()