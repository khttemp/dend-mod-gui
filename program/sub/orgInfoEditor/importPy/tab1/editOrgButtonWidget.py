import tkinter
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.orgInfoEditor.importPy.tab1.setDefaultWidget import SetDefaultEdit
from program.sub.orgInfoEditor.importPy.tab1.editAllTrainInfoWidget import AllEdit
import program.sub.orgInfoEditor.importPy.tab1.trainInfoProcess as trainInfoProcess


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
        self.extract_csv_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=extract_csv_train_info_text, command=self.extractCsvTrainInfo)
        self.extract_csv_train_info_button.grid(row=0, column=1, padx=5, sticky=tkinter.NSEW)

        if decryptFile.game in ["RS", "CS", "BS", "LS"]:
            save_csv_train_info_text = textSetting.textList["orgInfoEditor"]["saveCsv"]
        else:
            save_csv_train_info_text = textSetting.textList["orgInfoEditor"]["saveText"]
        self.save_csv_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=save_csv_train_info_text, command=self.saveCsvTrainInfo)
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

    def extractCsvTrainInfo(self):
        orgInfoEditorWindow = self.root.master.winfo_children()[2]
        trainIndex = orgInfoEditorWindow.trainCb.current()

        filename = self.decryptFile.trainNameList[trainIndex]
        if self.decryptFile.game in self.oldGameList:
            file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("traininfo_csv", "*.csv")])
            if file_path:
                if not self.decryptFile.extractCsvTrainInfo(trainIndex, file_path):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E63"])
                    return False
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        else:
            file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="txt", filetypes=[("traininfo_text", "*.txt")])
            if file_path:
                data = self.decryptFile.dataList[self.decryptFile.trainNameList[trainIndex]]
                if not trainInfoProcess.extractTrainInfoByDenFile(file_path, data):
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E64"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I48"])

    def saveCsvTrainInfo(self):
        orgInfoEditorWindow = self.root.master.winfo_children()[2]
        trainIndex = orgInfoEditorWindow.trainCb.current()

        if self.decryptFile.game in self.oldGameList:
            file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("traindata_csv", "*.csv")])
            if not file_path:
                return

            if not self.decryptFile.checkCsvResult(file_path):
                mb.showerror(title=textSetting.textList["error"], message=self.decryptFile.error)
                return
            result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I11"], icon="warning")
            if result:
                if not self.decryptFile.saveCsvTrainInfo(trainIndex):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return False
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
                self.reloadWidget()
        else:
            file_path = fd.askopenfilename(filetypes=[("traininfo_text", "*.txt")])
            if not file_path:
                return

            lines = trainInfoProcess.loadTrainInfoTextFile(file_path)
            resultList = self.decryptFile.decryptLines(lines)
            if resultList is None:
                errorMsg = textSetting.textList["errorList"]["E98"].format(self.decryptFile.error)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"], icon="warning")
            if result == "no":
                return

            data = self.decryptFile.dataList[self.decryptFile.trainNameList[trainIndex]]
            if not trainInfoProcess.saveTrainInfoDenFile(file_path, data, self.decryptFile):
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
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