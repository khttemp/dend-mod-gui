import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class StationNameWidget:
    def __init__(self, frame, decryptFile, stationNameList, reloadFunc, selectId):
        self.frame = frame
        self.decryptFile = decryptFile
        self.stationNameList = stationNameList
        self.reloadFunc = reloadFunc
        self.copyStationNameInfo = []
        self.stationNameLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["stationNameLabel"])
        self.stationNameLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        self.headerFrame = ttk.Frame(self.stationNameLf)
        self.headerFrame.pack()

        self.selectLbFrame = ttk.Frame(self.headerFrame)
        self.selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        selectLb = ttk.Label(self.selectLbFrame, text=textSetting.textList["railEditor"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.pack(side=tkinter.LEFT, padx=15, pady=15)

        self.v_select = tkinter.StringVar()
        selectEt = ttk.Entry(self.selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        selectEt.pack(side=tkinter.LEFT, padx=5, pady=15)

        self.btnFrame = ttk.Frame(self.headerFrame)
        self.btnFrame.pack(anchor=tkinter.NE, padx=15)

        editLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonEditLineLabel"], width=25, state="disabled", command=self.editLine)
        editLineBtn.grid(row=0, column=0, padx=10, pady=15)

        insertLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonInsertLineLabel"], width=25, state="disabled", command=self.insertLine)
        insertLineBtn.grid(row=0, column=1, padx=10, pady=15)

        deleteLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonDeleteLineLabel"], width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=15)

        copyLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonCopyLineLabel"], width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=15)

        self.pasteLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonPasteLineLabel"], width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=15)

        btnList = [
            editLineBtn,
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]

        self.treeviewFrame = ScrollbarTreeviewRailEditor(self.stationNameLf, self.v_select, btnList)

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
        result = EditStationNameListWidget(self.frame, textSetting.textList["railEditor"]["modifyStationNameLabel"], self.decryptFile, "modify", num, selectItem)
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
        result = EditStationNameListWidget(self.frame, textSetting.textList["railEditor"]["insertStationNameLabel"], self.decryptFile, "insert", num, selectItem)
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
        result = PasteStationNameDialog(self.frame, textSetting.textList["railEditor"]["pasteStationNameLabel"], self.decryptFile, int(selectItem["treeNum"]), self.copyStationNameInfo)
        if result.reloadFlag:
            self.reloadFunc(selectId)


class EditStationNameListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, num, stationNameInfo):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.stationNameInfo = stationNameInfo
        self.varList = []
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super(EditStationNameListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        stationNameInfoKeyList = list(self.stationNameInfo.keys())
        stationNameInfoKeyList.pop(0)
        for i in range(len(stationNameInfoKeyList)):
            self.stationNameInfoLb = ttk.Label(master, text=textSetting.textList["railEditor"][stationNameInfoKeyList[i]], font=textSetting.textList["font2"])
            self.stationNameInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["CS", "RS"]:
                if i == 0:
                    self.varStationNameInfo = tkinter.StringVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                elif i in [3, 4, 5]:
                    self.varStationNameInfo = tkinter.DoubleVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    self.varStationNameInfo = tkinter.IntVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            elif self.decryptFile.game == "BS":
                if i == 0:
                    self.varStationNameInfo = tkinter.StringVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    self.varStationNameInfo = tkinter.IntVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            elif self.decryptFile.game == "LS":
                if i == 0:
                    self.varStationNameInfo = tkinter.StringVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                elif i in [1, 2]:
                    self.varStationNameInfo = tkinter.IntVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    self.varStationNameInfo = tkinter.DoubleVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=textSetting.textList["font2"])
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])

        if self.mode == "insert":
            self.setInsertWidget(master, len(stationNameInfoKeyList))

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text=textSetting.textList["railEditor"]["posLabel"], font=textSetting.textList["font2"])
        self.insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["railEditor"]["posValue"])
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


class PasteStationNameDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, copyStationNameInfo):
        self.decryptFile = decryptFile
        self.num = num
        self.copyStationNameInfo = copyStationNameInfo
        self.reloadFlag = False
        super(PasteStationNameDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.posLb = ttk.Label(master, text=textSetting.textList["infoList"]["I4"], font=textSetting.textList["font2"])
        self.posLb.pack(padx=10, pady=10)

    def buttonbox(self):
        box = tkinter.Frame(self, padx=5, pady=5)
        self.frontBtn = tkinter.Button(box, text=textSetting.textList["railEditor"]["pasteFront"], font=textSetting.textList["font2"], width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = tkinter.Button(box, text=textSetting.textList["railEditor"]["pasteBack"], font=textSetting.textList["font2"], width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = tkinter.Button(box, text=textSetting.textList["railEditor"]["pasteCancel"], font=textSetting.textList["font2"], width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)
        box.pack()

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
