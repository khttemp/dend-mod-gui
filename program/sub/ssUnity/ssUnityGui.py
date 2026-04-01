import os
import traceback

import program.sub.textSetting as textSetting
import program.sub.errorLogClass as errorLogClass
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget
import program.sub.ssUnity.ssUnityProcess as ssUnityProcess

from program.sub.ssUnity.SSDecrypt.denDecrypt import DenDecrypt
from program.sub.ssUnity.SSDecrypt.resourcesDecrypt import ResourcesDecrypt

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QGroupBox,
    QVBoxLayout, QHBoxLayout,
    QRadioButton, QComboBox, QPushButton, QButtonGroup,
    QFileDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

errObj = errorLogClass.ErrorLogObj()
mb = customMessageBoxWidget.CustomMessageBox()


class SSUnityWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font7 = QFont(textSetting.textList["font7"][0], textSetting.textList["font7"][1])
        labelHeight = 28
        buttonWidth = 200
        buttonHeight = 28

        mainLayout = QVBoxLayout(self)
        mainLayout.addSpacing(10)
        # header
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout, 2)

        # headerLeft
        headerLeftLayout = QVBoxLayout()
        headerLeftLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(20)
        headerLayout.addLayout(headerLeftLayout, 3)
        # headerLeft - fileName
        self.fileNameLabel = QLabel("", font=font2)
        self.fileNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileNameLabel.setFixedHeight(labelHeight)
        headerLeftLayout.addWidget(self.fileNameLabel)

        # headerLeft - select
        headerSelectLayout = QHBoxLayout()
        headerSelectLayout.setContentsMargins(0, 15, 0, 15)
        headerLeftLayout.addLayout(headerSelectLayout)
        # headerLeft - select - Label1
        selectLabel = QLabel(textSetting.textList["ssUnity"]["selectNum"], font=font2)
        selectLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(selectLabel, 8)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel, 3)

        # headerLeft - search
        headerSearchLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerSearchLayout)
        # headerLeft - search - Label
        searchLabel = QLabel(textSetting.textList["ssUnity"]["searchText"], font=font2)
        headerSearchLayout.addWidget(searchLabel, 1)
        # headerLeft - search - LineEdit
        self.searchLineEdit = QLineEdit("", font=font7)
        self.searchLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.searchLineEdit.setReadOnly(True)
        self.searchLineEdit.textChanged.connect(self.tableFilterFunc)
        headerSearchLayout.addWidget(self.searchLineEdit, 9)

        # headerRight
        headerRightLayout = QVBoxLayout()
        headerRightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(20)
        headerLayout.addLayout(headerRightLayout, 9)

        # headerRight - radioLayout
        headerRadioLayout = QHBoxLayout()
        headerRadioLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRadioLayout)
        # headerRight - radioLayout - combo
        self.monoCombo = QComboBox(font=font2)
        self.monoCombo.setEnabled(False)
        self.monoCombo.currentIndexChanged.connect(self.changeResourceMono)
        headerRadioLayout.addWidget(self.monoCombo, 1)
        headerRadioLayout.addSpacing(50)
        # headerRight - radioLayout - radio1
        denRadioButton = QRadioButton(textSetting.textList["ssUnity"]["editDenFile"])
        denRadioButton.toggled.connect(self.radioButtonTrigger)
        headerRadioLayout.addWidget(denRadioButton, 1)
        # headerRight - radioLayout - radio2
        resourcesRadioButton = QRadioButton(textSetting.textList["ssUnity"]["editResourcesAssets"])
        resourcesRadioButton.toggled.connect(self.radioButtonTrigger)
        headerRadioLayout.addWidget(resourcesRadioButton, 1)
        headerRightLayout.addSpacing(10)
        # RadioGroup
        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(denRadioButton, 1)
        self.radioGroup.addButton(resourcesRadioButton, 2)

        # headerRight - buttonLayout
        headerRightButtonLayout = QHBoxLayout()
        headerRightButtonLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout)
        # headerRight - buttonLayout - button1
        self.extractButton = QPushButton(textSetting.textList["ssUnity"]["extractFileLabel"])
        self.extractButton.setFixedSize(buttonWidth, buttonHeight)
        self.extractButton.setEnabled(False)
        self.extractButton.clicked.connect(self.extractFunc)
        headerRightButtonLayout.addWidget(self.extractButton)
        headerRightButtonLayout.addStretch(1)
        # headerRight - buttonLayout - button2
        self.loadAndSaveButton = QPushButton(textSetting.textList["ssUnity"]["saveFileLabel"])
        self.loadAndSaveButton.setFixedSize(buttonWidth, buttonHeight)
        self.loadAndSaveButton.setEnabled(False)
        self.loadAndSaveButton.clicked.connect(self.loadAndSaveFunc)
        headerRightButtonLayout.addWidget(self.loadAndSaveButton)
        headerRightButtonLayout.addStretch(1)
        # headerRight - buttonLayout - button3
        self.assertsSaveButton = QPushButton(textSetting.textList["ssUnity"]["saveResourcesAssets"])
        self.assertsSaveButton.setFixedSize(buttonWidth, buttonHeight)
        self.assertsSaveButton.setEnabled(False)
        headerRightButtonLayout.addWidget(self.assertsSaveButton, 1)

        # content
        contentFrame = QGroupBox(textSetting.textList["ssUnity"]["scriptLabel"])
        mainLayout.addWidget(contentFrame, 11)
        contentLayout = QVBoxLayout()
        contentFrame.setLayout(contentLayout)
        self.contentTable = QTableWidget()
        self.contentTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contentTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contentTable.setCornerButtonEnabled(False)
        self.contentTable.itemSelectionChanged.connect(self.onSelectionChanged)
        contentLayout.addWidget(self.contentTable)

        # hide setting
        monoComboSize = self.monoCombo.sizePolicy()
        monoComboSize.setRetainSizeWhenHidden(True)
        self.monoCombo.setSizePolicy(monoComboSize)
        assertsSaveButtonSize = self.assertsSaveButton.sizePolicy()
        assertsSaveButtonSize.setRetainSizeWhenHidden(True)
        self.assertsSaveButton.setSizePolicy(assertsSaveButtonSize)

        # radioButton default setting
        denRadioButton.setChecked(True)

    def radioButtonTrigger(self, isChecked):
        if not isChecked:
            return

        self.fileNameLabel.setText("")
        self.searchLineEdit.setText("")
        self.searchLineEdit.setReadOnly(True)
        self.monoCombo.clear()
        self.monoCombo.setEnabled(False)
        self.clearTable()

        selectedRadioId = self.radioGroup.checkedId()
        if selectedRadioId == 1:
            self.extractButton.setText(textSetting.textList["ssUnity"]["extractFile"])
            self.extractButton.clicked.disconnect()
            self.extractButton.clicked.connect(self.extractFunc)

            self.loadAndSaveButton.setText(textSetting.textList["ssUnity"]["saveFile"])
            self.loadAndSaveButton.clicked.disconnect()
            self.loadAndSaveButton.clicked.connect(self.loadAndSaveFunc)

            self.assertsSaveButton.hide()

            self.monoCombo.hide()
        elif selectedRadioId == 2:
            self.extractButton.setText(textSetting.textList["ssUnity"]["extractCsv"])
            self.extractButton.clicked.disconnect()
            self.extractButton.clicked.connect(self.csvExtractFunc)

            self.loadAndSaveButton.setText(textSetting.textList["ssUnity"]["saveCsv"])
            self.loadAndSaveButton.clicked.disconnect()
            self.loadAndSaveButton.clicked.connect(self.csvLoadAndSaveFunc)

            self.assertsSaveButton.show()

            self.monoCombo.show()

    def clearTable(self):
        self.contentTable.clearSelection()
        self.contentTable.clear()
        self.contentTable.setRowCount(0)
        self.contentTable.setColumnCount(0)

    def createDenTable(self):
        headerLabelList = [
            textSetting.textList["ssUnity"]["headerName"],
            textSetting.textList["ssUnity"]["headerKind"],
            textSetting.textList["ssUnity"]["headerSize"]
        ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)
        for dataList in self.decryptFile.allList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for colIdx in range(3):
                item = QTableWidgetItem(str(dataList[colIdx]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, colIdx, item)

    def createMonoTable(self, index):
        if index == 0:
            headerLabelList = [
                textSetting.textList["ssUnity"]["headerName"],
                textSetting.textList["ssUnity"]["headerKind"],
                textSetting.textList["ssUnity"]["headerSize"]
            ]
            self.contentTable.setColumnCount(len(headerLabelList))
            self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.contentTable.setHorizontalHeaderLabels(headerLabelList)

            for trainName in self.decryptFile.trainNameList:
                rowCount = self.contentTable.rowCount()
                self.contentTable.insertRow(rowCount)
                trainData = self.decryptFile.trainOrgInfoList[trainName]
                dataList = [
                    trainName,
                    trainData["data"]["className"],
                    trainData["data"]["size"]
                ]
                for colIdx in range(3):
                    item = QTableWidgetItem(str(dataList[colIdx]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.contentTable.setItem(rowCount, colIdx, item)
        elif index == 1:
            headerLabelList = [
                textSetting.textList["ssUnity"]["headerPathId"],
                textSetting.textList["ssUnity"]["headerName"],
                textSetting.textList["ssUnity"]["headerName"],
                textSetting.textList["ssUnity"]["headerKind"],
                textSetting.textList["ssUnity"]["headerSize"]
            ]
            self.contentTable.setColumnCount(len(headerLabelList))
            self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.contentTable.setHorizontalHeaderLabels(headerLabelList)

            for trainModelName in self.decryptFile.trainModelNameList:
                changeMeshTexInfoList = self.decryptFile.changeMeshTexList[trainModelName]
                for changeMeshTexInfo in changeMeshTexInfoList:
                    rowCount = self.contentTable.rowCount()
                    self.contentTable.insertRow(rowCount)

                    meshTexInfo = changeMeshTexInfo["data"]["meshData"]
                    gameObjectName = changeMeshTexInfo["data"]["monoData"].m_GameObject.read().name
                    meshName = meshTexInfo[3]
                    dataList = [
                        changeMeshTexInfo["num"],
                        trainModelName,
                        "{0}({1})".format(gameObjectName, meshName),
                        changeMeshTexInfo["data"]["className"],
                        changeMeshTexInfo["data"]["size"]
                    ]
                    for colIdx in range(5):
                        item = QTableWidgetItem(str(dataList[colIdx]))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.contentTable.setItem(rowCount, colIdx, item)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.extractButton.setEnabled(False)
            self.loadAndSaveButton.setEnabled(False)
            self.assertsSaveButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.extractButton.setEnabled(True)
        self.loadAndSaveButton.setEnabled(True)
        self.assertsSaveButton.setEnabled(True)

    def changeResourceMono(self, index):
        self.searchLineEdit.setText("")
        self.clearTable()
        self.createMonoTable(index)

    def tableFilterFunc(self):
        for row in range(self.contentTable.rowCount()):
            self.contentTable.setRowHidden(row, False)
        filterText = self.searchLineEdit.text().lower()
        if not filterText:
            return

        self.contentTable.clearSelection()
        for row in range(self.contentTable.rowCount()):
            item = self.contentTable.item(row, 0)
            if not item:
                continue
            name = item.text().lower()
            if filterText not in name:
                selectedRadioId = self.radioGroup.checkedId()
                if selectedRadioId == 2 and self.monoCombo.currentIndex() == 1:
                    item2 = self.contentTable.item(row, 2)
                    if item2 and filterText in item2.text().lower():
                        continue
                self.contentTable.setRowHidden(row, True)

    def openFile(self):
        selectedRadioId = self.radioGroup.checkedId()
        if selectedRadioId not in [1, 2]:
            return

        if selectedRadioId == 1:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                "DEND_SS (*.den)"
            )
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = DenDecrypt(file_path)
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                "resources.assets (resources.assets)"
            )
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = ResourcesDecrypt(file_path)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        filename = os.path.basename(file_path)
        self.lastDir = os.path.dirname(file_path)
        self.fileNameLabel.setText(filename)
        self.searchLineEdit.setReadOnly(False)

        if selectedRadioId == 1:
            self.clearTable()
            self.createDenTable()
        else:
            self.monoCombo.clear()
            self.monoCombo.setEnabled(True)
            self.monoCombo.addItems(self.decryptFile.keyNameList)

    def reloadFile(self):
        if not self.decryptFile.filePath:
            return

        try:
            if not self.decryptFile.open():
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            self.searchLineEdit.setText("")
            selectedRadioId = self.radioGroup.checkedId()
            if selectedRadioId == 1:
                self.clearTable()
                self.createDenTable()
            else:
                self.monoCombo.clear()
                self.monoCombo.setEnabled(True)
                self.monoCombo.addItems(self.decryptFile.keyNameList)
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def extractFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        row = selectedItems[0].row()
        dataName = self.decryptFile.allList[row][0]
        excelFlag = False
        if dataName == "stagedata":
            excelFlag = True

        fileType = self.contentTable.item(row, 1).text()
        if fileType == "TextAsset":
            ext = "*.txt"
        elif fileType == "TextAsset(bytes)":
            ext = "*.png"
        elif fileType == "AudioClip":
            ext = "*.wav"

        fileTypes = "{0} ({1})".format(textSetting.textList["ssUnity"]["loadSaveFileLabel"], ext)
        if excelFlag:
            fileTypes = "{0} (*.xlsx);;{1}".format(textSetting.textList["ssUnity"]["loadSaveFileExcelLabel"], fileTypes)

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            os.path.join(self.lastDir, dataName),
            fileTypes
        )
        if file_path:
            try:
                data = self.decryptFile.allList[row][-1]
                if excelFlag:
                    configPath = self.importDict["configPath"]
                    result, errorMessage, warningMessage = ssUnityProcess.extractDenFileByExcel(file_path, data, configPath)
                    if errorMessage:
                        mb.showerror(title=textSetting.textList["error"], message=errorMessage)
                        return
                    if warningMessage:
                        mb.showwarning(title=textSetting.textList["error"], message=warningMessage)
                    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I113"])
                else:
                    if not ssUnityProcess.extractDenFile(file_path, fileType, data):
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                        return
                    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I110"])
            except Exception:
                errObj.write(traceback.format_exc())
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E89"])

    def loadAndSaveFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        row = selectedItems[0].row()
        dataName = self.decryptFile.allList[row][0]
        excelFlag = False
        if dataName == "stagedata":
            excelFlag = True

        fileType = self.contentTable.item(row, 1).text()
        if fileType == "TextAsset":
            ext = "*.txt"
        elif fileType == "TextAsset(bytes)":
            ext = "*.png"
        elif fileType == "AudioClip":
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E90"])
            return

        fileTypes = "{0} ({1})".format(textSetting.textList["ssUnity"]["loadSaveFileLabel"], ext)
        if excelFlag:
            fileTypes = "{0} (*.xlsx);;{1}".format(textSetting.textList["ssUnity"]["loadSaveFileExcelLabel"], fileTypes)

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            os.path.join(self.lastDir, dataName),
            fileTypes
        )
        if file_path:
            try:
                data = self.decryptFile.allList[row][-1]
                if os.path.splitext(file_path)[1].lower() != ".xlsx":
                    ssUnityProcess.saveDenFile(file_path, data, self.decryptFile)
                else:
                    configPath = self.importDict["configPath"]
                    result, newLinesObj, errMsgObj = ssUnityProcess.loadExcelData(file_path, data, configPath)
                    if not result:
                        mb.showerror(title=textSetting.textList["error"], message=errMsgObj["message"])
                        return
                    if "warning" in errMsgObj:
                        result = mb.askyesnoWarning(title=textSetting.textList["confirm"], message=errMsgObj["warning"])
                        if result == mb.NO:
                            return
                    result = mb.askyesnoWarning(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"])
                    if result == mb.NO:
                        return
                    ssUnityProcess.saveDenFileByExcel(data, self.decryptFile, newLinesObj)
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
                self.reloadFile()
            except Exception:
                errObj.write(traceback.format_exc())
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"]) 

    def csvExtractFunc(self):
        pass

    def csvLoadAndSaveFunc(self):
        pass

    def assetsSaveFunc(self):
        pass
