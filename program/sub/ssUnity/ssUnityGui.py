import os
import traceback

import program.sub.textSetting as textSetting
import program.sub.errorLogClass as errorLogClass
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.ssUnity.importPy.tkinterScrollbarTreeviewSSUnity import ScrollbarTreeviewSSUnity
import program.sub.ssUnity.ssUnityProcess as ssUnityProcess

from program.sub.ssUnity.SSDecrypt.denDecrypt import DenDecrypt
from program.sub.ssUnity.SSDecrypt.resourcesDecrypt import ResourcesDecrypt

import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb

errObj = errorLogClass.ErrorLogObj()


class SSUnityWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict):
        super().__init__(master)
        self.importDict = importDict
        self.decryptFile = None

        headerFrame = ttkCustomWidget.CustomTtkFrame(master)
        headerFrame.pack(fill=tkinter.BOTH, padx=40, pady=(20, 0))

        self.v_radioGroup = tkinter.IntVar()
        self.v_radioGroup.set(0)

        self.v_fileName = tkinter.StringVar()
        fileNameEt = ttkCustomWidget.CustomTtkEntry(headerFrame, textvariable=self.v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
        fileNameEt.grid(columnspan=10, row=0, column=0, pady=(0, 15), sticky=tkinter.EW)

        selectLb = ttkCustomWidget.CustomTtkLabel(headerFrame, text=textSetting.textList["ssUnity"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.grid(columnspan=9, row=1, column=0, pady=(0, 15), sticky=tkinter.EW)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(headerFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
        selectEt.grid(row=1, column=9, pady=(0, 15), sticky=tkinter.E)

        self.monoCombo = ttkCustomWidget.CustomTtkCombobox(headerFrame, font=textSetting.textList["font2"], state="disabled")
        self.monoCombo.grid(row=0, column=10, padx=25, pady=(0, 15), sticky=tkinter.E)
        self.monoCombo.bind("<<ComboboxSelected>>", self.changeResourceMonoEvent)
        self.monoCombo.grid_remove()

        denRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text=textSetting.textList["ssUnity"]["editDenFile"], command=self.radioButtonTrigger, variable=self.v_radioGroup, value=0)
        denRb.grid(row=0, column=11, padx=25, pady=(0, 15))
        resourcesRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text=textSetting.textList["ssUnity"]["editResourcesAssets"], command=self.radioButtonTrigger, variable=self.v_radioGroup, value=1)
        resourcesRb.grid(row=0, column=12, padx=25, pady=(0, 15))

        self.extractButton = ttkCustomWidget.CustomTtkButton(headerFrame, text=textSetting.textList["ssUnity"]["extractFileLabel"], width=25, state="disabled", command=self.extractFunc)
        self.extractButton.grid(row=1, column=10, padx=25, sticky=tkinter.E, pady=(0, 15))
        self.loadAndSaveButton = ttkCustomWidget.CustomTtkButton(headerFrame, text=textSetting.textList["ssUnity"]["saveFileLabel"], width=25, state="disabled", command=self.loadAndSaveFunc)
        self.loadAndSaveButton.grid(row=1, column=11, padx=25, pady=(0, 15))

        self.assetsSaveButton = ttkCustomWidget.CustomTtkButton(headerFrame, text=textSetting.textList["ssUnity"]["saveResourcesAssets"], width=25, state="disabled", command=self.assetsSaveFunc)
        self.assetsSaveButton.grid(row=1, column=12, padx=25, pady=(0, 15))
        self.assetsSaveButton.grid_remove()

        self.v_btnList = [
            self.extractButton,
            self.loadAndSaveButton,
            self.assetsSaveButton
        ]

        searchLb = ttkCustomWidget.CustomTtkLabel(headerFrame, text=textSetting.textList["ssUnity"]["searchText"], font=textSetting.textList["font2"])
        searchLb.grid(row=2, column=0, sticky=tkinter.EW)

        self.v_search = tkinter.StringVar()
        self.searchEt = ttkCustomWidget.CustomTtkEntry(headerFrame, textvariable=self.v_search, font=textSetting.textList["font7"], state="readonly", justify="center")
        self.searchEt.grid(columnspan=9, row=2, column=1, sticky=tkinter.EW)
        self.searchEt.bind("<KeyRelease>", self.tableFilterEvent)

        self.contentsLf = ttkCustomWidget.CustomTtkLabelFrame(master, text=textSetting.textList["ssUnity"]["scriptLabel"])
        self.contentsLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))

        headerFrame.grid_columnconfigure(10, weight=1)
        headerFrame.grid_columnconfigure(11, weight=1)
        headerFrame.grid_columnconfigure(12, weight=1)

        self.frame = None

    def radioButtonTrigger(self):
        self.v_fileName.set("")
        self.v_select.set("")
        self.v_search.set("")
        self.searchEt["state"] = "readonly"
        self.monoCombo.set("")
        self.monoCombo["state"] = "disabled"
        self.deleteAllWidgetInLabelFrame()

        selectedRadioId = self.v_radioGroup.get()
        if selectedRadioId == 0:
            self.extractButton["text"] = textSetting.textList["ssUnity"]["extractFile"]
            self.extractButton["command"] = self.extractFunc

            self.loadAndSaveButton["text"] = textSetting.textList["ssUnity"]["saveFile"]
            self.loadAndSaveButton["command"] = self.loadAndSaveFunc

            self.assetsSaveButton.grid_remove()
            self.monoCombo.grid_remove()
        elif selectedRadioId == 1:
            self.extractButton["text"] = textSetting.textList["ssUnity"]["extractCsv"]
            self.extractButton["command"] = self.csvExtractFunc

            self.loadAndSaveButton["text"] = textSetting.textList["ssUnity"]["saveCsv"]
            self.loadAndSaveButton["command"] = self.csvLoadAndSaveFunc

            self.assetsSaveButton.grid(row=1, column=12, padx=25, pady=(0, 15))
            self.monoCombo.grid(row=0, column=10, padx=25, pady=(0, 15))

    def deleteAllWidgetInLabelFrame(self):
        for children in self.contentsLf.winfo_children():
            children.destroy()
        
        for btn in self.v_btnList:
            btn["state"] = "disabled"

    def createWidget(self, reloadFlag = False):
        if not reloadFlag:
            self.v_search.set("")
            self.searchEt["state"] = "normal"

        self.frame = ScrollbarTreeviewSSUnity(self.contentsLf, self.v_select, self.v_btnList)
        col_tuple = (
            "treeNum",
            "treePathId",
            "treeName",
            "treeName2",
            "treeKind",
            "treeSize"
        )
        self.frame.tree["columns"] = col_tuple
        self.frame.tree.column("#0", width=0, stretch=False)

        self.frame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, minwidth=50)
        self.frame.tree.column("treePathId", anchor=tkinter.CENTER)
        self.frame.tree.column("treeName", anchor=tkinter.CENTER)
        self.frame.tree.column("treeName2", anchor=tkinter.CENTER)
        self.frame.tree.column("treeKind", anchor=tkinter.CENTER)
        self.frame.tree.column("treeSize", anchor=tkinter.CENTER)
        self.frame.tree.heading("treeNum", text=textSetting.textList["ssUnity"]["headerNum"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treePathId", text=textSetting.textList["ssUnity"]["headerPathId"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeName", text=textSetting.textList["ssUnity"]["headerName"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeName2", text=textSetting.textList["ssUnity"]["headerName"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeKind", text=textSetting.textList["ssUnity"]["headerKind"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeSize", text=textSetting.textList["ssUnity"]["headerSize"], anchor=tkinter.CENTER)

    def createDenTable(self):
        for index, dataList in enumerate(self.decryptFile.allList):
            data = (index + 1, )
            data += ("", dataList[0], "", dataList[1], dataList[2])
            self.frame.tree.insert(parent="", index="end", iid=index, values=data)
        self.frame.tree["displaycolumns"] = (
            "treeNum",
            "treeName",
            "treeKind",
            "treeSize"
        )

    def createMonoTable(self):
        if self.monoCombo.current() == 0:
            for index, trainName in enumerate(self.decryptFile.trainNameList):
                data = (index + 1, )
                trainData = self.decryptFile.trainOrgInfoList[trainName]
                data += (trainData["num"], trainName, "", trainData["data"]["className"], trainData["data"]["size"])
                self.frame.tree.insert(parent="", index="end", iid=index, values=data)
            self.frame.tree.tag_configure("dirty", foreground="red")
            self.frame.tree["displaycolumns"] = (
                "treeNum",
                "treeName",
                "treeKind",
                "treeSize"
            )
        elif self.monoCombo.current() == 1:
            index = 0
            trainIdx = 0
            tagList = ["", "gray"]
            for trainModelName in self.decryptFile.trainModelNameList:
                changeMeshTexInfoList = self.decryptFile.changeMeshTexList[trainModelName]
                tags = tagList[trainIdx % 2]
                for changeMeshTexInfo in changeMeshTexInfoList:
                    data = (index + 1, )
                    meshTexInfo = changeMeshTexInfo["data"]["meshData"]
                    gameObjectName = changeMeshTexInfo["data"]["monoData"].m_GameObject.read().name
                    meshName = meshTexInfo[3]
                    data += (changeMeshTexInfo["num"], )
                    data += (trainModelName, "{0}({1})".format(gameObjectName, meshName), changeMeshTexInfo["data"]["className"], changeMeshTexInfo["data"]["size"])
                    self.frame.tree.insert(parent="", index="end", iid=index, values=data, tags=tags)
                    index += 1
                if len(changeMeshTexInfoList) > 0:
                    trainIdx += 1
            self.frame.tree.tag_configure("gray", background="#CCCCCC")
            self.frame.tree.tag_configure("dirty", foreground="red")
            self.frame.tree["displaycolumns"] = (
                "treeNum",
                "treePathId",
                "treeName",
                "treeName2",
                "treeKind",
                "treeSize"
            )

    def changeResourceMonoEvent(self, event):
        self.changeResourceMono()

    def changeResourceMono(self):
        self.v_select.set("")
        self.deleteAllWidgetInLabelFrame()
        self.createWidget()
        self.createMonoTable()

    def tableFilterEvent(self, event):
        self.tableFilterFunc()

    def tableFilterFunc(self):
        self.v_select.set("")
        if len(self.frame.tree.selection()) > 0:
            self.frame.tree.selection_remove(self.frame.tree.selection())

        self.filterData()
    
    def filterData(self):
        selectedRadioId = self.v_radioGroup.get()
        if selectedRadioId == 0:
            for i in range(len(self.decryptFile.allList)):
                self.frame.tree.reattach(i, "", tkinter.END)
        elif selectedRadioId == 1:
            if self.monoCombo.current() == 0:
                for i in range(len(self.decryptFile.trainNameList)):
                    self.frame.tree.reattach(i, "", tkinter.END)
            elif self.monoCombo.current() == 1:
                index = 0
                for trainModelName in self.decryptFile.trainModelNameList:
                    changeMeshTexInfoList = self.decryptFile.changeMeshTexList[trainModelName]
                    for changeMeshTexInfo in changeMeshTexInfoList:
                        index += 1
                for i in range(index):
                    self.frame.tree.reattach(i, "", tkinter.END)

        search = self.v_search.get()
        for i in self.frame.tree.get_children():
            item = self.frame.tree.item(i)
            name = item["values"][2]
            if search.upper() not in name.upper():
                if self.v_radioGroup.get() == 1 and self.monoCombo.current() == 1:
                    name2 = item["values"][3]
                    if search.upper() in name2.upper():
                        continue
                self.frame.tree.detach(i)

    def openFile(self):
        selectedRadioId = self.v_radioGroup.get()
        if selectedRadioId not in [0, 1]:
            return

        if selectedRadioId == 0:
            file_path = fd.askopenfilename(filetypes=[("DEND_SS", "*.den")])
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = DenDecrypt(file_path)
        else:
            file_path = fd.askopenfilename(filetypes=[("resources.assets", "resources.assets")])
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = ResourcesDecrypt(file_path)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        filename = os.path.basename(file_path)
        self.v_fileName.set(filename)
        self.deleteAllWidgetInLabelFrame()
        self.createWidget()

        if selectedRadioId == 0:
            self.createDenTable()
        else:
            self.monoCombo["values"] = ""
            self.monoCombo["values"] = self.decryptFile.keyNameList
            self.monoCombo["state"] = "normal"
            self.monoCombo.current(0)
            self.createMonoTable()

    def reloadFile(self):
        if not self.decryptFile.filePath:
            return

        try:
            if not self.decryptFile.open():
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return

            selectId = None
            if self.v_select.get() != "":
                selectId = int(self.v_select.get())

            self.deleteAllWidgetInLabelFrame()
            self.createWidget(True)
            selectedRadioId = self.v_radioGroup.get()
            if selectedRadioId == 0:
                self.createDenTable()
            else:
                self.createMonoTable()

            if self.v_search.get() != "":
                self.filterData()

            if selectId is not None:
                for idx, itemId in enumerate(self.frame.tree.get_children()):
                    item = self.frame.tree.item(itemId)
                    num = item["values"][0]
                    if selectId == num:
                        self.frame.tree.see(idx)
                        self.frame.tree.selection_set(itemId)
                        break
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def extractFunc(self):
        selectId = self.frame.tree.selection()[0]
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        dataName = self.decryptFile.allList[num][0]
        excelFlag = False
        if dataName == "stagedata":
            excelFlag = True

        fileType = selectItem["treeKind"]
        if fileType == "TextAsset":
            ext = "*.txt"
        elif fileType == "TextAsset(bytes)":
            ext = "*.png"
        elif fileType == "AudioClip":
            ext = "*.wav"

        fileTypes = [(textSetting.textList["ssUnity"]["loadSaveFileLabel"], "*" + ext), ]
        defExt = ext
        if excelFlag:
            fileTypes.insert(0, (textSetting.textList["ssUnity"]["loadSaveFileExcelLabel"], "*.xlsx"))
            defExt = ".xlsx"

        file_path = fd.asksaveasfilename(initialfile=dataName, filetypes=fileTypes, defaultextension=defExt)
        if file_path:
            try:
                data = self.decryptFile.allList[num][-1]
                if excelFlag and os.path.splitext(file_path)[1].lower() == ".xlsx":
                    rootPath = self.importDict["rootPath"]
                    configPath = self.importDict["configPath"]
                    result, message = ssUnityProcess.extractDenFileByExcel(file_path, data, rootPath, configPath)
                    if not result:
                        mb.showerror(title=textSetting.textList["error"], message=message)
                        return
                    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I113"])
                    if message:
                        mb.showwarning(title=textSetting.textList["error"], message=message)
                else:
                    if not ssUnityProcess.extractDenFile(file_path, fileType, data):
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                        return
                    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I110"])
            except Exception:
                errObj.write(traceback.format_exc())
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E89"])

    def loadAndSaveFunc(self):
        selectId = self.frame.tree.selection()[0]
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        dataName = self.decryptFile.allList[num][0]
        excelFlag = False
        if dataName == "stagedata":
            excelFlag = True

        fileType = selectItem["treeKind"]
        if fileType == "TextAsset":
            ext = "*.txt"
        elif fileType == "TextAsset(bytes)":
            ext = "*.png"
        elif fileType == "AudioClip":
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E90"])
            return

        fileTypes = [(textSetting.textList["ssUnity"]["loadSaveFileLabel"], "*" + ext), ]
        defExt = ext
        if excelFlag:
            fileTypes.insert(0, (textSetting.textList["ssUnity"]["loadSaveFileExcelLabel"], "*.xlsx"))
            defExt = ".xlsx"

        file_path = fd.askopenfilename(filetypes=fileTypes, defaultextension=defExt)
        if file_path:
            try:
                data = self.decryptFile.allList[num][-1]
                if os.path.splitext(file_path)[1].lower() != ".xlsx":
                    script = ssUnityProcess.getScriptData(file_path)
                else:
                    rootPath = self.importDict["rootPath"]
                    configPath = self.importDict["configPath"]
                    result, obj = ssUnityProcess.loadExcelData(file_path, data, rootPath, configPath)
                    if not result:
                        mb.showerror(title=textSetting.textList["error"], message=obj["message"])
                        return
                    if obj["message"]:
                        result = mb.askquestion(title=textSetting.textList["confirm"], message=obj["message"], icon="warning")
                        if result == "no":
                            return
                    script = ssUnityProcess.getScriptDataByExcel(obj["data"])
                result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"], icon="warning")
                if result == "no":
                    return
                ssUnityProcess.saveDenFile(data, self.decryptFile, script)
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
                self.reloadFile()
            except Exception:
                errObj.write(traceback.format_exc())
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"]) 

    def csvExtractFunc(self):
        selectId = self.frame.tree.selection()[0]
        selectItem = self.frame.tree.set(selectId)

        monoComboId = self.monoCombo.current()
        if monoComboId == 0:
            trainName = selectItem["treeName"]
            data = self.decryptFile.trainOrgInfoList[trainName]["data"]["monoData"]

            file_path = fd.asksaveasfilename(initialfile=trainName, defaultextension="csv", filetypes=[("trainOrgInfo", "*.csv")])
            if file_path:
                try:
                    trainOrgInfo = self.decryptFile.getTrainOrgInfo(data.raw_data)
                    if trainOrgInfo is None:
                        self.decryptFile.printError()
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                        return
                    ssUnityProcess.writeCsv(file_path, trainOrgInfo)
                    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
                except Exception:
                    errObj.write(traceback.format_exc())
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])
        elif monoComboId == 1:
            pathId = int(selectItem["treePathId"])
            trainModelName = selectItem["treeName"]

            filename = "{0}_{1}".format(trainModelName, pathId)
            file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("changeMeshTex", "*.csv")])
            if file_path:
                try:
                    meshTexInfoList = self.decryptFile.changeMeshTexList[trainModelName]
                    meshTexInfo = [item for item in meshTexInfoList if item["num"] == pathId][0]
                    ssUnityProcess.writeMeshCsv(file_path, meshTexInfo)
                    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
                except Exception:
                    errObj.write(traceback.format_exc())
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def csvLoadAndSaveFunc(self):
        selectId = self.frame.tree.selection()[0]
        selectItem = self.frame.tree.set(selectId)

        monoComboId = self.monoCombo.current()
        if monoComboId == 0:
            trainName = selectItem["treeName"]
            file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("trainOrgInfo", "*.csv")])
            if not file_path:
                return
            csvLines = None
            try:
                f = open(file_path, "r", encoding="utf-8-sig")
                csvLines = f.readlines()
                f.close()

                if not self.decryptFile.checkCsv(csvLines):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=self.decryptFile.error)
                    return
                if not self.decryptFile.saveCsv(trainName):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I111"])
                self.frame.tree.set(selectId, column="treeSize", value=str(self.decryptFile.trainOrgInfoList[trainName]["data"]["size"]))
            except Exception:
                errObj.write(traceback.format_exc())
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
        elif monoComboId == 1:
            trainModelName = selectItem["treeName"]
            pathId = int(selectItem["treePathId"])
            file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("changeMeshTex", "*.csv")])
            if not file_path:
                return
            try:
                f = open(file_path, "r", encoding="utf-8-sig")
                csvLines = f.readlines()
                f.close()
                if not self.decryptFile.saveChangeMeshTex(csvLines, trainModelName, pathId):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I111"])
                changeMeshTexFilterInfo = [item for item in self.decryptFile.changeMeshTexList[trainModelName] if item["num"] == pathId][0]
                self.frame.tree.set(selectId, column="treeSize", value=str(changeMeshTexFilterInfo["data"]["size"]))
            except Exception:
                errObj.write(traceback.format_exc())
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

        self.frame.tree.item(selectId, tags=("dirty",))

    def assetsSaveFunc(self):
        self.assetsSaveButton["state"] = "disabled"
        self.assetsSaveButton.update()
        try:
            if not self.decryptFile.saveAssets():
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I112"])
            self.reloadFile()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
