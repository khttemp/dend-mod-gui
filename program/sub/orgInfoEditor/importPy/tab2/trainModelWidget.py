import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget


class TrainModelWidget(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, frame, trainIndex, buttonFrame, decryptFile, rootFrameAppearance, reloadWidget):
        super().__init__(frame)
        self.frame = frame
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget

        modelInfo = decryptFile.trainModelList[trainIndex]
        mdlFrame = ttkCustomWidget.CustomTtkFrame(self)
        mdlFrame.pack(padx=4)

        trainLb = ttkCustomWidget.CustomTtkLabel(mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelTrainLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
        trainLb.grid(row=0, column=0)
        modelLb = ttkCustomWidget.CustomTtkLabel(mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelModelLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
        modelLb.grid(row=1, column=0)
        if len(modelInfo["pantaNames"]) > 0:
            pantaLb = ttkCustomWidget.CustomTtkLabel(mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelPantaLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            pantaLb.grid(row=2, column=0)
        if len(modelInfo["colList"]) > 0:
            colLb = ttkCustomWidget.CustomTtkLabel(mdlFrame, text=textSetting.textList["orgInfoEditor"]["modelColLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            colLb.grid(row=3, column=0)

        self.comboList = []

        for i in range(modelInfo["mdlCnt"]):
            mdlNoLb = ttkCustomWidget.CustomTtkLabel(mdlFrame, text=str(i + 1), font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=16, borderwidth=1, relief="solid")
            mdlNoLb.grid(row=0, column=i + 1, sticky=tkinter.W + tkinter.E)

            mdlCb = ttkCustomWidget.CustomTtkCombobox(mdlFrame, font=textSetting.textList["font6"], width=20, value=modelInfo["mdlNames"], state="disabled")
            mdlCb.grid(row=1, column=i + 1)
            if modelInfo["mdlList"][i] == -1:
                mdlCb.current(len(modelInfo["mdlNames"]) - 1)
            else:
                mdlCb.current(modelInfo["mdlList"][i])
            self.comboList.append(mdlCb)

            if len(modelInfo["pantaNames"]) > 0:
                pantaCb = ttkCustomWidget.CustomTtkCombobox(mdlFrame, font=textSetting.textList["font6"], width=20, value=modelInfo["pantaNames"], state="disabled")
                pantaCb.grid(row=2, column=i + 1)
                if modelInfo["pantaList"][i] == -1:
                    pantaCb.current(len(modelInfo["pantaNames"]) - 1)
                else:
                    pantaCb.current(modelInfo["pantaList"][i])
                self.comboList.append(pantaCb)

            if len(modelInfo["colList"]) > 0:
                colCb = ttkCustomWidget.CustomTtkCombobox(mdlFrame, font=textSetting.textList["font6"], width=20, value=modelInfo["colNames"], state="disabled")
                colCb.grid(row=3, column=i + 1)
                if modelInfo["colList"][i] == -1:
                    colCb.current(len(modelInfo["colNames"]) - 1)
                else:
                    colCb.current(modelInfo["colList"][i])
                self.comboList.append(colCb)

        self.editHenseiButton = ttkCustomWidget.CustomTtkButton(buttonFrame, text=textSetting.textList["orgInfoEditor"]["orgModify"], command=self.editHenseiTrain)
        self.editHenseiButton.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, pady=5)
        # LSはパンタ情報がない場合、修正不可
        if self.decryptFile.game == "LS":
            if len(modelInfo["pantaNames"]) == 0:
                self.editHenseiButton["state"] = "disabled"
        self.saveHenseiButton = ttkCustomWidget.CustomTtkButton(buttonFrame, text=textSetting.textList["orgInfoEditor"]["trainSave"], command=self.saveHenseiTrain)

        buttonFrame.columnconfigure(0, weight=1)

    def editHenseiTrain(self):
        root = self.frame.winfo_toplevel()
        orgInfoEditorWindow = root.winfo_children()[2]
        orgInfoEditorWindow.gameCb["state"] = "disabled"
        orgInfoEditorWindow.trainCb["state"] = "disabled"
        orgInfoEditorWindow.menuCb["state"] = "disabled"
        orgInfoEditorWindow.edit_stage_train_button["state"] = "disabled"

        self.editHenseiButton.grid_remove()
        self.saveHenseiButton.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, pady=5)
        
        for idx, combo in enumerate(self.comboList):
            if self.decryptFile.game == "LS":
                if idx % 3 == 1:
                    combo["state"] = "readonly"
            elif self.decryptFile.game in ["BS", "CS"]:
                if idx % 3 != 2:
                    combo["state"] = "readonly"
            else:
                combo["state"] = "readonly"

    def saveHenseiTrain(self):
        root = self.frame.winfo_toplevel()
        orgInfoEditorWindow = root.winfo_children()[2]
        orgInfoEditorWindow.gameCb["state"] = "readonly"
        orgInfoEditorWindow.trainCb["state"] = "readonly"
        orgInfoEditorWindow.menuCb["state"] = "readonly"
        orgInfoEditorWindow.edit_stage_train_button["state"] = "normal"

        comboValueList = []
        for idx, combo in enumerate(self.comboList):
            # LSの場合、パンタのみ変更可能
            if self.decryptFile.game == "LS":
                if idx % 3 != 1:
                    continue
            # BS、CSの場合、モデル・パンタのみ変更可能
            elif self.decryptFile.game in ["BS", "CS"]:
                if idx % 3 == 2:
                    continue
            idx = combo.current()
            if idx == len(combo.cget("values")) - 1:
                idx = 255
            comboValueList.append(idx)

        if not self.decryptFile.saveHensei(self.trainIndex, comboValueList):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return

        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I55"])
        self.reloadWidget()
