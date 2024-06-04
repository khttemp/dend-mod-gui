import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class StationNameWidget:
    def __init__(self, root, frame, decryptFile, stationNameList, rootFrameAppearance, reloadFunc, selectId):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.stationNameList = stationNameList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.copyStationNameInfo = []
        stationNameLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["stationNameLabel"])
        stationNameLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        headerFrame = ttkCustomWidget.CustomTtkFrame(stationNameLf)
        headerFrame.pack()

        selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["railEditor"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.pack(side=tkinter.LEFT, padx=15, pady=15)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        selectEt.pack(side=tkinter.LEFT, padx=5, pady=15)

        btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        btnFrame.pack(anchor=tkinter.NE, padx=15)

        editLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonEditLineLabel"], width=25, state="disabled", command=self.editLine)
        editLineBtn.grid(row=0, column=0, padx=10, pady=15)

        insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonInsertLineLabel"], width=25, state="disabled", command=self.insertLine)
        insertLineBtn.grid(row=0, column=1, padx=10, pady=15)

        deleteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonDeleteLineLabel"], width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=15)

        copyLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonCopyLineLabel"], width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=15)

        self.pasteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonPasteLineLabel"], width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=15)

        btnList = [
            editLineBtn,
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]

        self.treeviewFrame = ScrollbarTreeviewRailEditor(stationNameLf, self.v_select, btnList)

        if len(self.stationNameList) == 0:
            insertLineBtn["state"] = "normal"

        if self.decryptFile.game in ["CS", "RS"]:
            col_tuple = (
                "treeNum",
                "stationNameName",
                "stationNameFlag",
                "stationNameRailNo",
                "stationNameF1",
                "stationNameF2",
                "stationNameF3",
                "stationNameE1",
                "stationNameE2",
                "stationNameE3",
                "stationNameE4"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("stationNameName", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("stationNameFlag", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameRailNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameE1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameE2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameE3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameE4", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["stationNameNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameName", text=textSetting.textList["railEditor"]["stationNameName"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameFlag", text=textSetting.textList["railEditor"]["stationNameFlag"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameRailNo", text=textSetting.textList["railEditor"]["stationNameRailNo"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF1", text=textSetting.textList["railEditor"]["stationNameF1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF2", text=textSetting.textList["railEditor"]["stationNameF2"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF3", text=textSetting.textList["railEditor"]["stationNameF3"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameE1", text=textSetting.textList["railEditor"]["stationNameE1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameE2", text=textSetting.textList["railEditor"]["stationNameE2"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameE3", text=textSetting.textList["railEditor"]["stationNameE3"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameE4", text=textSetting.textList["railEditor"]["stationNameE4"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for stNameInfo in self.stationNameList:
                data = (index,)
                data += (stNameInfo[0], stNameInfo[1], stNameInfo[2])
                data += (round(float(stNameInfo[3]), 3), round(float(stNameInfo[4]), 3), round(float(stNameInfo[5]), 3))
                data += (stNameInfo[6], stNameInfo[7], stNameInfo[8], stNameInfo[9])
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1
        elif self.decryptFile.game == "BS":
            col_tuple = (
                "treeNum",
                "stationNameName",
                "stationNameFlag",
                "stationNameRailNo"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("stationNameName", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("stationNameFlag", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameRailNo", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["stationNameNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameName", text=textSetting.textList["railEditor"]["stationNameName"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameFlag", text=textSetting.textList["railEditor"]["stationNameFlag"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameRailNo", text=textSetting.textList["railEditor"]["stationNameRailNo"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for stNameInfo in self.stationNameList:
                data = (index,)
                data += (stNameInfo[0], stNameInfo[1], stNameInfo[2])
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1
        elif self.decryptFile.game == "LS":
            col_tuple = (
                "treeNum",
                "stationNameName",
                "stationNameFlag",
                "stationNameRailNo",
                "stationNameF1",
                "stationNameF2",
                "stationNameF3",
                "stationNameF4",
                "stationNameF5",
                "stationNameF6"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("stationNameName", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("stationNameFlag", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameRailNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF4", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF5", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("stationNameF6", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["stationNameNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameName", text=textSetting.textList["railEditor"]["stationNameName"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameFlag", text=textSetting.textList["railEditor"]["stationNameFlag"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameRailNo", text=textSetting.textList["railEditor"]["stationNameRailNo"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF1", text=textSetting.textList["railEditor"]["stationNameF1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF2", text=textSetting.textList["railEditor"]["stationNameF2"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF3", text=textSetting.textList["railEditor"]["stationNameF3"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF4", text=textSetting.textList["railEditor"]["stationNameF4"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF5", text=textSetting.textList["railEditor"]["stationNameF5"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("stationNameF6", text=textSetting.textList["railEditor"]["stationNameF6"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for stNameInfo in self.stationNameList:
                data = (index,)
                data += (stNameInfo[0], stNameInfo[1], stNameInfo[2])
                data += (stNameInfo[3], stNameInfo[4], stNameInfo[5], stNameInfo[6], stNameInfo[7], stNameInfo[8])
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1

        if selectId is not None:
            if selectId >= len(self.stationNameList):
                selectId = len(self.stationNameList) - 1
            if selectId - 3 < 0:
                self.treeviewFrame.tree.see(0)
            else:
                self.treeviewFrame.tree.see(selectId - 3)
            self.treeviewFrame.tree.selection_set(selectId)

    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = EditStationNameListWidget(self.root, textSetting.textList["railEditor"]["modifyStationNameLabel"], self.decryptFile, "modify", num, selectItem, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveStationNameInfo(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
            self.reloadFunc(selectId)

    def insertLine(self):
        noStationNameInfoFlag = False
        if not self.treeviewFrame.tree.selection():
            noStationNameInfoFlag = True
            selectId = None
            num = 0
            keyList = self.treeviewFrame.tree["columns"]
            selectItem = {}
            for key in keyList:
                selectItem[key] = None
        else:
            selectId = self.treeviewFrame.tree.selection()[0]
            selectItem = self.treeviewFrame.tree.set(selectId)
            num = int(selectItem["treeNum"])
        result = EditStationNameListWidget(self.root, textSetting.textList["railEditor"]["insertStationNameLabel"], self.decryptFile, "insert", num, selectItem, self.rootFrameAppearance)
        if result.reloadFlag:
            if noStationNameInfoFlag:
                if result.insert == 0:
                    num += 1
            if not self.decryptFile.saveStationNameInfo(num, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
            self.reloadFunc(selectId)

    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        warnMsg = textSetting.textList["infoList"]["I9"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.saveStationNameInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
            if len(self.stationNameList) == 1:
                selectId = None
            self.reloadFunc(selectId)

    def copyLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)

        stationNameInfoKeyList = list(selectItem.keys())
        stationNameInfoKeyList.pop(0)
        copyList = []
        for i in range(len(stationNameInfoKeyList)):
            key = stationNameInfoKeyList[i]
            copyList.append(selectItem[key])
        self.copyStationNameInfo = copyList
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteStationNameDialog(self.root, textSetting.textList["railEditor"]["pasteStationNameLabel"], self.decryptFile, int(selectItem["treeNum"]), self.copyStationNameInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc(selectId)


class EditStationNameListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, num, stationNameInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.stationNameInfo = stationNameInfo
        self.varList = []
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        stationNameInfoKeyList = list(self.stationNameInfo.keys())
        stationNameInfoKeyList.pop(0)
        for i in range(len(stationNameInfoKeyList)):
            stationNameInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"][stationNameInfoKeyList[i]], font=textSetting.textList["font2"])
            stationNameInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["CS", "RS"]:
                if i == 0:
                    varStationNameInfo = tkinter.StringVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                elif i in [3, 4, 5]:
                    varStationNameInfo = tkinter.DoubleVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    varStationNameInfo = tkinter.IntVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            elif self.decryptFile.game == "BS":
                if i == 0:
                    varStationNameInfo = tkinter.StringVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    varStationNameInfo = tkinter.IntVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            elif self.decryptFile.game == "LS":
                if i == 0:
                    varStationNameInfo = tkinter.StringVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                elif i in [1, 2]:
                    varStationNameInfo = tkinter.IntVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    varStationNameInfo = tkinter.DoubleVar()
                    self.varList.append(varStationNameInfo)
                    stationNameInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])

        if self.mode == "insert":
            self.setInsertWidget(master, len(stationNameInfoKeyList))
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["railEditor"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                for i in range(len(self.varList)):
                    if self.decryptFile.game in ["CS", "RS"]:
                        try:
                            if i == 0:
                                res = self.varList[i].get()
                            elif i in [3, 4, 5]:
                                res = float(self.varList[i].get())
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E60"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                    elif self.decryptFile.game == "BS":
                        try:
                            if i == 0:
                                res = self.varList[i].get()
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E60"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                    elif self.decryptFile.game == "LS":
                        try:
                            if i == 0:
                                res = self.varList[i].get()
                            elif i in [1, 2]:
                                res = int(self.varList[i].get())
                            else:
                                res = float(self.varList[i].get())
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E60"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False

                if self.mode == "insert":
                    self.insert = self.insertCb.current()
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class PasteStationNameDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, num, copyStationNameInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.num = num
        self.copyStationNameInfo = copyStationNameInfo
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
        self.frontBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["railEditor"]["pasteFront"], style="custom.paste.TButton", width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["railEditor"]["pasteBack"], style="custom.paste.TButton", width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["railEditor"]["pasteCancel"], style="custom.paste.TButton", width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)

    def frontInsert(self):
        self.ok()
        if not self.decryptFile.saveStationNameInfo(self.num, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        if not self.decryptFile.saveStationNameInfo(self.num + 1, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
        self.reloadFlag = True
