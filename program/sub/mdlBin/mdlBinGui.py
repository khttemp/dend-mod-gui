import os
import copy
import traceback

import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog
from program.sub.errorLogClass import ErrorLogObj

from program.sub.cmdList import cmdList
from program.sub.mdlBin.dendDecrypt.decrypt import MdlBinDecrypt
from program.sub.mdlBin.importPy.tkinterScrollbarTreeviewMdlBin import ScrollbarTreeviewMdlBin
from program.sub.mdlBin.importPy.headerDialogWidget import HeaderDialog 
import program.sub.mdlBin.mdlBinProcess as mdlBinProcess

errObj = ErrorLogObj()


class MdlBinWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict, rootFrameAppearance):
        super().__init__(master)
        self.importDict = importDict
        self.rootFrameAppearance = rootFrameAppearance
        self.decryptFile = None
        self.selectId = None
        self.copyScriptData = None

        headerFrame = ttkCustomWidget.CustomTtkFrame(master)
        headerFrame.pack(fill=tkinter.BOTH, padx=40, pady=(20, 0))

        selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        self.v_fileName = tkinter.StringVar()
        fileNameEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_fileName, font=textSetting.textList["font2"], width=22, state="readonly", justify="center")
        fileNameEt.grid(columnspan=4, row=0, column=0, pady=(0, 15), sticky=tkinter.EW)

        self.v_ver = tkinter.StringVar()
        fileVerEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_ver, font=textSetting.textList["font2"], width=2, state="readonly", justify="center")
        fileVerEt.grid(row=0, column=5, pady=(0, 15))

        selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["mdlBin"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.grid(columnspan=3, row=1, column=0, pady=(0, 15))

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
        selectEt.grid(columnspan=2, row=1, column=3, pady=(0, 15))

        self.csvExtractBtn = ttkCustomWidget.CustomTtkButton(selectLbFrame, text=textSetting.textList["mdlBin"]["csvExtractLabel"], width=20, state="disabled", command=self.csvExtract)
        self.csvExtractBtn.grid(columnspan=3, row=2, column=0, padx=(0, 15), pady=(0, 15), sticky=tkinter.EW)

        self.csvLoadAndSaveBtn = ttkCustomWidget.CustomTtkButton(selectLbFrame, text=textSetting.textList["mdlBin"]["csvSaveLabel"], width=20, state="disabled", command=self.csvLoadAndSave)
        self.csvLoadAndSaveBtn.grid(columnspan=3, row=2, column=3, padx=(0, 15), pady=(0, 15), sticky=tkinter.EW)

        btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        btnFrame.pack(fill=tkinter.BOTH, padx=(40, 0))

        self.editLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["editLineLabel"], width=25, state="disabled", command=self.editLine)
        self.editLineBtn.grid(row=0, column=0, padx=10, pady=(0, 20))

        self.insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["insertLineLabel"], width=25, state="disabled", command=self.insertLine)
        self.insertLineBtn.grid(row=0, column=1, padx=10, pady=(0, 20))

        self.deleteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["deleteLineLabel"], width=25, state="disabled", command=self.deleteLine)
        self.deleteLineBtn.grid(row=0, column=2, padx=10, pady=(0, 20))

        self.copyLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["copyLineLabel"], width=25, state="disabled", command=self.copyLine)
        self.copyLineBtn.grid(row=1, column=0, padx=10, pady=(0, 20))

        self.pasteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["pasteLineLabel"], width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=(0, 20))

        self.headerEditBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["headerEditLabel"], width=25, state="disabled", command=self.headerEdit)
        self.headerEditBtn.grid(row=1, column=2, padx=10, pady=(0, 20))

        self.listHeaderModifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["listHeaderModifyBtnLabel"], width=25, state="disabled", command=self.listHeaderModify)
        self.listHeaderModifyBtn.grid(row=2, column=0, padx=10, pady=(0, 20))

        self.listNumModifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["listNumModifyBtnLabel"], width=25, state="disabled", command=self.listNumModify)
        self.listNumModifyBtn.grid(row=2, column=1, padx=10, pady=(0, 20))

        self.numModifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlBin"]["numModifyBtnLabel"], width=25, state="disabled", command=self.numModify)
        self.numModifyBtn.grid(row=2, column=2, padx=10, pady=(0, 20))

        btnFrame.grid_columnconfigure(0, weight=1)
        btnFrame.grid_columnconfigure(1, weight=1)
        btnFrame.grid_columnconfigure(2, weight=1)

        self.btnList = [
            self.editLineBtn,
            self.insertLineBtn,
            self.deleteLineBtn,
            self.copyLineBtn,
            self.listHeaderModifyBtn,
            self.listNumModifyBtn,
            self.numModifyBtn
        ]

        self.scriptLf = ttkCustomWidget.CustomTtkLabelFrame(master, text=textSetting.textList["mdlBin"]["scriptLabel"])
        self.scriptLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))

    def deleteWidget(self):
        for btn in self.btnList:
            btn["state"] = "disabled"

        children = self.scriptLf.winfo_children()
        for child in children:
            child.destroy()

    def createWidget(self):
        self.setMdlBinTableHeader()
        self.setMdlBinTableData()

    def setMdlBinTableHeader(self):
        self.frame = ScrollbarTreeviewMdlBin(self.scriptLf, self.v_select, self.btnList)

        col_tuple = (
            "treeNum",
            "treeDelay",
            "treeName",
            "treeSection"
        )
        paramList = []
        for i in range(self.decryptFile.max_param):
            paramList.append(textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1))
        col_tuple = col_tuple + tuple(paramList)

        self.frame.tree["columns"] = col_tuple

        self.frame.tree.column("#0", width=0, stretch=False)
        self.frame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, minwidth=50)
        self.frame.tree.column("treeDelay", anchor=tkinter.CENTER, width=50, minwidth=50)
        self.frame.tree.column("treeName", anchor=tkinter.CENTER, width=150, minwidth=150)
        self.frame.tree.column("treeSection", stretch=False)
        for i in range(self.decryptFile.max_param):
            col_name = textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)
            self.frame.tree.column(col_name, anchor=tkinter.CENTER, width=100, minwidth=100)

        displayTuple = (
            "treeNum",
            "treeDelay",
            "treeName"
        )

        displayList = []
        self.frame.tree.heading("treeNum", text=textSetting.textList["mdlBin"]["treeNum"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeDelay", text=textSetting.textList["mdlBin"]["treeDelay"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeName", text=textSetting.textList["mdlBin"]["treeName"], anchor=tkinter.CENTER)
        for i in range(self.decryptFile.max_param):
            col_name = textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)
            displayList.append(col_name)
            self.frame.tree.heading(col_name, text=col_name, anchor=tkinter.CENTER)

        displayTuple = displayTuple + tuple(displayList)
        self.frame.tree["displaycolumns"] = displayTuple

    def setMdlBinTableData(self):
        index = 0
        num = 0
        for scriptDataInfoList in self.decryptFile.scriptDataAllInfoList:
            listNum = 0
            for scriptDataInfo in scriptDataInfoList:
                sectionNum = 0
                headerInfo = (index + 1, "-", "---#{0}, {1}#---".format(num, listNum))
                headerInfo += ("{0},{1},{2}".format(num, listNum, sectionNum), )
                headerInfo += (",".join(str(n) for n in scriptDataInfo[0]), )
                self.frame.tree.insert(parent="", index="end", iid=index, values=headerInfo)
                index += 1

                sectionNum += 1
                for scriptData in scriptDataInfo[1:]:
                    data = (index + 1, scriptData[0], cmdList[scriptData[1]])
                    data += ("{0},{1},{2}".format(num, listNum, sectionNum), )
                    paramCnt = scriptData[2]
                    paramList = []
                    for i in range(paramCnt):
                        paramList.append(scriptData[4 + i])
                    data = data + tuple(paramList)
                    self.frame.tree.insert(parent="", index="end", iid=index, values=data)
                    index += 1
                    sectionNum += 1
                listNum += 1
            num += 1

    def jumpToSelect(self):
        maxRow = len(self.frame.tree.get_children())
        if self.selectId is not None:
            if self.selectId >= maxRow:
                self.selectId = maxRow - 1
            self.frame.tree.selection_set(self.selectId)
            self.frame.tree.see(self.selectId)

    def reloadFile(self):
        try:
            for btn in self.btnList:
                btn["state"] = "disabled"
            for item in self.frame.tree.get_children():
                self.frame.tree.delete(item)
            self.decryptFile = self.decryptFile.reload()

            self.deleteWidget()
            self.createWidget()
            self.jumpToSelect()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def openFile(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["mdlBin"]["fileType"], "*.BIN")])
        if not file_path:
            return

        del self.decryptFile
        self.decryptFile = MdlBinDecrypt(file_path, cmdList)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E6"])
            return
        
        filename = os.path.basename(file_path)
        self.v_fileName.set(filename)
        self.v_ver.set(self.decryptFile.ver)

        self.deleteWidget()
        self.createWidget()
        self.headerEditBtn["state"] = "normal"
        self.csvExtractBtn["state"] = "normal"
        self.csvLoadAndSaveBtn["state"] = "normal"
        self.pasteLineBtn["state"] = "disabled"

    def getScriptData(self, itemId):
        arr = itemId.split(",")
        num = int(arr[0])
        scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[num]
        listNum = int(arr[1])
        scriptDataInfo = scriptDataInfoList[listNum]
        cmdDiff = int(arr[2])
        return scriptDataInfo[1:][cmdDiff - 1]

    def getHeaderData(self, itemId):
        arr = itemId.split(",")
        num = int(arr[0])
        scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[num]
        listNum = int(arr[1])
        scriptDataInfo = scriptDataInfoList[listNum]
        return scriptDataInfo[0]

    def editLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        itemId = selectItem["treeSection"]
        scriptData = self.getScriptData(itemId)
        result = EditMdlBinDialog(self.editLineBtn.winfo_toplevel(), textSetting.textList["mdlBin"]["cmdModify"], self.decryptFile.ver, itemId, scriptData, cmdList, self.rootFrameAppearance)
        if result.reloadFlag:
            itemIdArr = [int(x) for x in itemId.split(",")]
            if not self.decryptFile.saveFile(itemIdArr, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num
            self.reloadFile()

    def insertLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        itemId = selectItem["treeSection"]
        result = EditMdlBinDialog(self.insertLineBtn.winfo_toplevel(), textSetting.textList["mdlBin"]["cmdInsert"], self.decryptFile.ver, itemId, None, cmdList, self.rootFrameAppearance)
        if result.reloadFlag:
            itemIdArr = [int(x) for x in itemId.split(",")]
            scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[itemIdArr[0]]
            scriptDataInfo = scriptDataInfoList[itemIdArr[1]]
            if len(scriptDataInfo[1:]) >= 255:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E142"].format(itemIdArr[0], itemIdArr[1]))
                return

            itemIdArr[2] += result.insertPos
            if not self.decryptFile.saveFile(itemIdArr, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num + result.insertPos
            self.reloadFile()

    def deleteLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        itemId = selectItem["treeSection"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result:
            itemIdArr = [int(x) for x in itemId.split(",")]
            if not self.decryptFile.saveFile(itemIdArr, "delete"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num
            self.reloadFile()

    def copyLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)

        itemId = selectItem["treeSection"]
        self.copyScriptData = copy.deepcopy(self.getScriptData(itemId))
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        itemId = selectItem["treeSection"]
        result = PasteDialog(self.pasteLineBtn.winfo_toplevel(), textSetting.textList["mdlBin"]["cmdPaste"], self.rootFrameAppearance)
        if result.reloadFlag:
            itemIdArr = [int(x) for x in itemId.split(",")]
            scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[itemIdArr[0]]
            scriptDataInfo = scriptDataInfoList[itemIdArr[1]]
            if len(scriptDataInfo[1:]) >= 255:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E142"].format(itemIdArr[0], itemIdArr[1]))
                return

            itemIdArr[2] += result.insertPos
            if not self.decryptFile.saveFile(itemIdArr, "insert", self.copyScriptData):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
            self.selectId = num + result.insertPos
            self.reloadFile()

    def headerEdit(self):
        result = HeaderDialog(self.headerEditBtn.winfo_toplevel(), textSetting.textList["mdlBin"]["headerInfo"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFile()

    def listHeaderModify(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        itemId = selectItem["treeSection"]
        itemIdArr = [int(x) for x in itemId.split(",")]
        headerInfo = self.getHeaderData(itemId)
        result = ListHeaderModifyDialog(self.listHeaderModifyBtn.winfo_toplevel(), textSetting.textList["mdlBin"]["listHeaderModifyLabel"], headerInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveListHeader(itemIdArr, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I23"])
            self.selectId = num
            self.reloadFile()

    def listNumModify(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        itemId = selectItem["treeSection"]
        itemIdArr = [int(x) for x in itemId.split(",")]
        listNumCount = len(self.decryptFile.scriptDataAllInfoList[itemIdArr[0]])
        result = ListNumModifyDialog(self.listNumModifyBtn.winfo_toplevel(), textSetting.textList["mdlBin"]["listNumModifyLabel"], itemIdArr, listNumCount, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveListNum(itemIdArr, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I22"])
            self.selectId = num
            self.reloadFile()

    def numModify(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        numCount = len(self.decryptFile.scriptDataAllInfoList)
        result = NumModifyDialog(self.numModifyBtn.winfo_toplevel(), textSetting.textList["mdlBin"]["numModifyLabel"], numCount, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveNumFile(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I141"])
            self.selectId = num
            self.reloadFile()

    def csvExtract(self):
        filename = os.path.splitext(os.path.basename(self.decryptFile.filePath))[0]
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("mdlbin_csv", "*.csv")])
        if not file_path:
            return

        try:
            mdlBinProcess.writeCsv(file_path, self.decryptFile.scriptDataAllInfoList, cmdList)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def csvLoadAndSave(self):
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("mdlbin_csv", "*.csv")])
        if not file_path:
            return

        processResult, obj = mdlBinProcess.loadCsvData(file_path, cmdList)
        if not processResult:
            mb.showerror(title=textSetting.textList["error"], message=obj["message"])
            return
        msg = textSetting.textList["infoList"]["I15"].format(obj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            if not self.decryptFile.saveCsv(obj["data"]):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I16"])
            self.reloadFile()


class EditMdlBinDialog(CustomSimpleDialog):
    def __init__(self, master, title, ver, itemId, scriptData, cmdList, rootFrameAppearance):
        self.ver = ver
        self.itemId = itemId
        self.scriptData = scriptData
        self.cmdList = cmdList
        self.sortedCmdList = sorted(cmdList, key=str.lower)
        self.reloadFlag = False
        self.insertPos = 0
        self.resultValueList = []
        if scriptData is not None:
            self.mode = "modify"
        else:
            self.mode = "insert"
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        delayLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["treeDelay"], width=12, font=textSetting.textList["font2"])
        delayLb.grid(row=1, column=0, sticky=tkinter.N+tkinter.S)
        self.v_delay = tkinter.IntVar()
        if self.mode == "modify":
            self.v_delay.set(self.scriptData[0])
        else:
            self.v_delay.set(0)
        delayEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_delay, width=27, font=textSetting.textList["font2"])
        delayEt.grid(row=1, column=1, sticky=tkinter.N+tkinter.S, pady=10)

        cmdLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["treeName"], width=12, font=textSetting.textList["font2"])
        cmdLb.grid(row=2, column=0, sticky=tkinter.N+tkinter.S)
        self.v_cmd = tkinter.StringVar()
        cmdCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_cmd, width=25, font=textSetting.textList["font2"], state="readonly", value=self.sortedCmdList)
        cmdCb.grid(row=2, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        cmdCb.current(0)
        if self.mode == "modify":
            idx = self.sortedCmdList.index(self.cmdList[self.scriptData[1]])
            cmdCb.current(idx)

        paramCntLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["paramLabel"], width=12, font=textSetting.textList["font2"])
        paramCntLb.grid(row=3, column=0, sticky=tkinter.N+tkinter.S)
        self.v_paramCnt = tkinter.IntVar()
        paramCntList = [cnt for cnt in range(0, 16)]
        self.paramCntCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_paramCnt, width=25, font=textSetting.textList["font2"], state="readonly", value=paramCntList)
        self.paramCntCb.grid(row=3, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        self.paramCntCb.current(0)

        if self.mode == "insert":
            positionLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], width=12, font=textSetting.textList["font2"])
            positionLb.grid(row=4, column=0, sticky=tkinter.N+tkinter.S)
            self.v_position = tkinter.StringVar()
            positionList = textSetting.textList["mdlBin"]["posValue"]
            self.positionCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_position, width=25, font=textSetting.textList["font2"], state="readonly", value=positionList)
            self.positionCb.grid(row=4, column=1, sticky=tkinter.N+tkinter.S, pady=10)
            self.positionCb.current(0)

        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(columnspan=2, row=5, column=0, sticky=tkinter.E + tkinter.W, pady=10)

        self.v_paramList = []
        self.paramFrame = ttkCustomWidget.CustomTtkFrame(master)
        self.paramFrame.grid(columnspan=2, row=6, column=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        self.paramCntCb.bind("<<ComboboxSelected>>", lambda e: self.selectParam())
        if self.mode == "modify":
            self.paramCntCb.current(self.scriptData[2])
            self.selectParam()
        super().body(master)

    def selectParam(self):
        self.v_paramList = []
        children = self.paramFrame.winfo_children()
        for child in children:
            child.destroy()

        paramCnt = self.paramCntCb.current()
        if paramCnt == 0:
            paramLb = ttkCustomWidget.CustomTtkLabel(self.paramFrame)
            paramLb.grid(row=0, column=0)

        for i in range(paramCnt):
            paramLb = ttkCustomWidget.CustomTtkLabel(self.paramFrame, text=textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1), width=12, font=textSetting.textList["font2"])
            paramLb.grid(row=i, column=0, sticky=tkinter.N+tkinter.S)
            v_param = tkinter.StringVar()
            self.v_paramList.append(v_param)
            paramEt = ttkCustomWidget.CustomTtkEntry(self.paramFrame, textvariable=v_param, width=27, font=textSetting.textList["font2"])
            paramEt.grid(row=i, column=1, sticky=tkinter.N+tkinter.S)
            if self.mode == "modify" and i < self.scriptData[2]:
                self.v_paramList[i].set(self.scriptData[4 + i])

    def validate(self):
        self.resultValueList = []
        try:
            self.v_delay.get()
        except Exception:
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return

        self.resultValueList.append(self.v_delay.get())
        self.resultValueList.append(self.cmdList.index(self.v_cmd.get()))
        self.resultValueList.append(self.v_paramCnt.get())
        self.resultValueList.append(0xFF)

        floatFlag = True
        strCount = 0
        strParamList = []
        for i, var in enumerate(self.v_paramList):
            paramMsg = textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)
            if not var.get():
                errorMsg = textSetting.textList["errorList"]["E139"].format(paramMsg)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            if floatFlag:
                try:
                    float(var.get())
                except ValueError:
                    floatFlag = False
                    if self.ver == 1:
                        errorMsg = "{0} [{1}]".format(textSetting.textList["errorList"]["E5"], paramMsg)
                        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                        return

            if floatFlag:
                self.resultValueList.append(float(var.get()))
            else:
                self.resultValueList.append(var.get())
                strCount += 1
                strParamList.append(paramMsg)

        if self.ver >= 2:
            if strCount > 0:
                self.resultValueList[3] = strCount

        if self.ver == 2:
            if self.v_cmd.get() not in ["MDL_GETINDEX", "SET_LENSFLEAR_MT"]:
                if strCount > 0:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E140"])
                    return
            else:
                errorMsg = textSetting.textList["errorList"]["E141"].format(self.v_cmd.get())
                if strCount != 1:
                    mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                    return
                else:
                    param2 = textSetting.textList["mdlBin"]["paramNumLabel"].format(2)
                    if strParamList[0] != param2:
                        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                        return

        msg = "\n".join(strParamList)
        if msg:
            msg += "\n"
            msg += textSetting.textList["infoList"]["I17"]
        msg += textSetting.textList["infoList"]["I21"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=msg)
        if result:
            if self.mode == "insert":
                self.insertPos = 1
                if self.positionCb.current() == 1:
                    self.insertPos = 0
            return True

    def apply(self):
        self.reloadFlag = True


class PasteDialog(CustomSimpleDialog):
    def __init__(self, master, title, rootFrameAppearance):
        self.insertPos = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        posLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I4"], font=textSetting.textList["font2"])
        posLb.pack(padx=10, pady=10)
        super().body(master)

    def buttonbox(self):
        super().buttonbox()
        for idx, child in enumerate(self.buttonList):
            child.destroy()
        self.box.config(padx=5, pady=5)
        self.frontBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlBin"]["pasteFront"], style="custom.paste.TButton", width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlBin"]["pasteBack"], style="custom.paste.TButton", width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlBin"]["pasteCancel"], style="custom.paste.TButton", width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)

    def frontInsert(self):
        self.ok()
        self.reloadFlag = True
        self.insertPos = 0

    def backInsert(self):
        self.ok()
        self.reloadFlag = True
        self.insertPos = 1


class ListHeaderModifyDialog(CustomSimpleDialog):
    def __init__(self, master, title, headerInfo, rootFrameAppearance):
        self.headerInfo = headerInfo
        self.v_paramList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(3):
            paramLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1), font=textSetting.textList["font2"])
            paramLb.grid(row=i + 1, column=0, sticky=tkinter.N + tkinter.S)
            self.v_paramList.append(tkinter.IntVar(value=self.headerInfo[i]))
            paramEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_paramList[i], width=20, font=textSetting.textList["font2"])
            paramEt.grid(row=i + 1, column=1, sticky=tkinter.N + tkinter.S)
        super().body(master)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if not result:
            return

        for i in range(3):
            try:
                param = self.v_paramList[i].get()
                self.resultValueList.append(param)
            except Exception:
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
        return True

    def apply(self):
        self.reloadFlag = True


class ListNumModifyDialog(CustomSimpleDialog):
    def __init__(self, master, title, itemIdArr, listNum, rootFrameAppearance):
        self.itemIdArr = itemIdArr
        self.listNum = listNum
        self.resultValue = -1
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        listLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I18"].format(self.itemIdArr[0]), font=textSetting.textList["font2"])
        listLb.grid(row=0, column=0)

        self.v_listNum = tkinter.IntVar()
        self.v_listNum.set(self.listNum)
        sp = ttkCustomWidget.CustomTtkSpinbox(master, textvariable=self.v_listNum, font=textSetting.textList["font2"], from_=1, to=255, width=5)
        sp.grid(row=0, column=1, padx=10)

        list2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I19"], font=textSetting.textList["font2"])
        list2Lb.grid(row=0, column=2)
        super().body(master)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if not result:
            return

        try:
            self.resultValue = int(self.v_listNum.get())
            if self.resultValue < 1 or self.resultValue > 255:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
                return
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
            return

        if self.resultValue < self.listNum:
            warnMsg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
            if not result:
                return
        return True

    def apply(self):
        self.reloadFlag = True


class NumModifyDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, rootFrameAppearance):
        self.num = num
        self.resultValue = -1
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        numLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I24"], font=textSetting.textList["font2"])
        numLb.grid(row=0, column=0)

        self.v_num = tkinter.IntVar()
        self.v_num.set(self.num)
        sp = ttkCustomWidget.CustomTtkSpinbox(master, textvariable=self.v_num, font=textSetting.textList["font2"], from_=1, to=255, width=5)
        sp.grid(row=0, column=1, padx=10)

        self.num2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I19"], font=textSetting.textList["font2"])
        self.num2Lb.grid(row=0, column=2)
        super().body(master)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if not result:
            return

        try:
            self.resultValue = int(self.v_num.get())
            if self.resultValue < 1 or self.resultValue > 255:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
                return
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
            return

        if self.resultValue < self.num:
            warnMsg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
            if not result:
                return
        return True

    def apply(self):
        self.reloadFlag = True
