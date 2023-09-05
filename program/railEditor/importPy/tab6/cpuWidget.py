import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class CpuWidget:
    def __init__(self, frame, decryptFile, cpuList, reloadFunc, selectId):
        self.frame = frame
        self.decryptFile = decryptFile
        self.cpuList = cpuList
        self.reloadFunc = reloadFunc
        self.copyCpuInfo = []
        self.cpuLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["cpuInfoLabel"])
        self.cpuLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        self.headerFrame = ttk.Frame(self.cpuLf)
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

        self.treeviewFrame = ScrollbarTreeviewRailEditor(self.cpuLf, self.v_select, btnList)

        if len(self.cpuList) == 0:
            insertLineBtn["state"] = "normal"

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            col_tuple = (
                "treeNum",
                "cpuInfoRailNo",
                "cpuInfoConst1",
                "cpuInfoMode",
                "cpuInfoMinLen",
                "cpuInfoMaxLen",
                "cpuInfoMaxSpeed",
                "cpuInfoMinSpeed"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("cpuInfoRailNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoConst1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMode", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMinLen", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMaxLen", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMaxSpeed", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMinSpeed", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["cpuInfoNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoRailNo", text=textSetting.textList["railEditor"]["cpuInfoRailNo"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoConst1", text=textSetting.textList["railEditor"]["cpuInfoConst1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMode", text=textSetting.textList["railEditor"]["cpuInfoMode"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMinLen", text=textSetting.textList["railEditor"]["cpuInfoMinLen"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMaxLen", text=textSetting.textList["railEditor"]["cpuInfoMaxLen"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMaxSpeed", text=textSetting.textList["railEditor"]["cpuInfoMaxSpeed"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMinSpeed", text=textSetting.textList["railEditor"]["cpuInfoMinSpeed"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for cpuInfo in self.cpuList:
                data = (index,)
                data += (cpuInfo[0], cpuInfo[1], cpuInfo[2])
                data += (cpuInfo[3], cpuInfo[4])
                data += (cpuInfo[5], cpuInfo[6])
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1
        else:
            col_tuple = (
                "treeNum",
                "cpuInfoRailNo",
                "cpuInfoList",
                "cpuInfoConst1",
                "cpuInfoMode",
                "cpuInfoMinLen",
                "cpuInfoMaxLen",
                "cpuInfoMaxSpeed",
                "cpuInfoMinSpeed",
                "cpuInfoDefSpeed",
                "cpuInfoList2"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("cpuInfoRailNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoList", anchor=tkinter.CENTER, width=100)
            self.treeviewFrame.tree.column("cpuInfoConst1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMode", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMinLen", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMaxLen", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMaxSpeed", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoMinSpeed", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoDefSpeed", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cpuInfoList2", anchor=tkinter.CENTER, width=100)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["cpuInfoNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoRailNo", text=textSetting.textList["railEditor"]["cpuInfoRailNo"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoList", text=textSetting.textList["railEditor"]["cpuInfoList"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoConst1", text=textSetting.textList["railEditor"]["cpuInfoConst1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMode", text=textSetting.textList["railEditor"]["cpuInfoMode"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMinLen", text=textSetting.textList["railEditor"]["cpuInfoMinLen"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMaxLen", text=textSetting.textList["railEditor"]["cpuInfoMaxLen"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMaxSpeed", text=textSetting.textList["railEditor"]["cpuInfoMaxSpeed"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMinSpeed", text=textSetting.textList["railEditor"]["cpuInfoMinSpeed"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoDefSpeed", text=textSetting.textList["railEditor"]["cpuInfoDefSpeed"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoList2", text=textSetting.textList["railEditor"]["cpuInfoList2"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for cpuInfo in self.cpuList:
                data = (index,)
                data += (cpuInfo[0], )
                data += (",".join(map(str, cpuInfo[1])), )
                data += (cpuInfo[2], cpuInfo[3])
                data += (cpuInfo[4], cpuInfo[5], cpuInfo[6], cpuInfo[7], cpuInfo[8])
                data += (",".join(map(str, cpuInfo[9])), )
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1

        if selectId is not None:
            if selectId >= len(self.cpuList):
                selectId = len(self.cpuList) - 1
            if selectId - 3 < 0:
                self.treeviewFrame.tree.see(0)
            else:
                self.treeviewFrame.tree.see(selectId - 3)
            self.treeviewFrame.tree.selection_set(selectId)

    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = EditCpuListWidget(self.frame, textSetting.textList["railEditor"]["modifyCpuInfoLabel"], self.decryptFile, "modify", num, selectItem)
        if result.reloadFlag:
            if not self.decryptFile.saveCpuInfo(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
            self.reloadFunc(selectId)

    def insertLine(self):
        noCpuInfoFlag = False
        if not self.treeviewFrame.tree.selection():
            noCpuInfoFlag = True
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
        result = EditCpuListWidget(self.frame, textSetting.textList["railEditor"]["insertCpuInfoLabel"], self.decryptFile, "insert", num, selectItem)
        if result.reloadFlag:
            if not noCpuInfoFlag:
                if result.insert == 0:
                    num += 1
            if not self.decryptFile.saveCpuInfo(num, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
            self.reloadFunc(selectId)

    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        warnMsg = textSetting.textList["infoList"]["I9"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.saveCpuInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
            if len(self.cpuList) == 1:
                selectId = None
            self.reloadFunc(selectId)

    def copyLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)

        cpuInfoKeyList = list(selectItem.keys())
        cpuInfoKeyList.pop(0)
        copyList = []
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            for i in range(len(cpuInfoKeyList)):
                key = cpuInfoKeyList[i]
                if i in [3, 4, 5, 6]:
                    copyList.append(float(selectItem[key]))
                else:
                    copyList.append(int(selectItem[key]))
        else:
            for i in range(len(cpuInfoKeyList)):
                key = cpuInfoKeyList[i]
                if i in [0, 2, 3]:
                    copyList.append(int(selectItem[key]))
                elif i in [1, 9]:
                    tempList = [float(x) for x in selectItem[key].split(",")]
                    copyList.append(tempList)
                else:
                    copyList.append(float(selectItem[key]))
        self.copyCpuInfo = copyList
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteCpuDialog(self.frame, textSetting.textList["railEditor"]["pasteCpuInfoLabel"], self.decryptFile, int(selectItem["treeNum"]), self.copyCpuInfo)
        if result.reloadFlag:
            self.reloadFunc(selectId)


class EditCpuListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, num, cpuInfo):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.cpuInfo = cpuInfo
        self.varList = []
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super(EditCpuListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        cpuInfoKeyList = list(self.cpuInfo.keys())
        cpuInfoKeyList.pop(0)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            for i in range(len(cpuInfoKeyList)):
                self.cpuInfoLb = ttk.Label(master, text=textSetting.textList["railEditor"][cpuInfoKeyList[i]], font=textSetting.textList["font2"])
                self.cpuInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i in [3, 4, 5, 6]:
                    self.varCpuInfo = tkinter.DoubleVar()
                    self.varList.append(self.varCpuInfo)
                    self.cpuInfoEt = ttk.Entry(master, textvariable=self.varCpuInfo, font=textSetting.textList["font2"])
                    self.cpuInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varCpuInfo.set(round(float(self.cpuInfo[cpuInfoKeyList[i]]), 3))
                else:
                    self.varCpuInfo = tkinter.IntVar()
                    self.varList.append(self.varCpuInfo)
                    self.cpuInfoEt = ttk.Entry(master, textvariable=self.varCpuInfo, font=textSetting.textList["font2"])
                    self.cpuInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
        else:
            rowNum = 0
            colNum = 0
            for i in range(len(cpuInfoKeyList)):
                if i in [0, 2, 3]:
                    self.cpuInfoLb = ttk.Label(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                    self.cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                    self.varCpuInfo = tkinter.IntVar()
                    self.varList.append(self.varCpuInfo)
                    self.cpuInfoEt = ttk.Entry(master, textvariable=self.varCpuInfo, font=textSetting.textList["font2"])
                    self.cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                    rowNum += 1
                    if self.mode == "modify":
                        self.varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                elif i in [1, 9]:
                    tempList = [float(x) for x in self.cpuInfo[cpuInfoKeyList[i]].split(",")]
                    for j in range(len(tempList)):
                        self.cpuInfoLb = ttk.Label(master, text=textSetting.textList["railEditor"]["cpuInfoLsListLabel"].format(colNum + 1, j), font=textSetting.textList["font2"])
                        self.cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                        self.varCpuInfo = tkinter.DoubleVar()
                        self.varList.append(self.varCpuInfo)
                        self.cpuInfoEt = ttk.Entry(master, textvariable=self.varCpuInfo, font=textSetting.textList["font2"])
                        self.cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                        rowNum += 1
                        if self.mode == "modify":
                            self.varCpuInfo.set(tempList[j])
                    colNum += 1
                    rowNum = 0
                else:
                    self.cpuInfoLb = ttk.Label(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                    self.cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                    self.varCpuInfo = tkinter.DoubleVar()
                    self.varList.append(self.varCpuInfo)
                    self.cpuInfoEt = ttk.Entry(master, textvariable=self.varCpuInfo, font=textSetting.textList["font2"])
                    self.cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                    rowNum += 1
                    if self.mode == "modify":
                        self.varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])

        if self.mode == "insert":
            self.setInsertWidget(master, len(cpuInfoKeyList))

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
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    for i in range(len(self.varList)):
                        try:
                            if i in [3, 4, 5, 6]:
                                res = float(self.varList[i].get())
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E60"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                else:
                    tempList = []
                    tempList2 = []
                    for i in range(len(self.varList)):
                        try:
                            if i in [0, 7, 8]:
                                res = int(self.varList[i].get())
                                self.resultValueList.append(res)
                            elif i in [1, 2, 3, 4, 5, 6]:
                                tempList.append(float(self.varList[i].get()))
                            elif i in [9, 10, 11, 12, 13]:
                                res = float(self.varList[i].get())
                                self.resultValueList.append(res)
                            elif i in [14, 15, 16]:
                                tempList2.append(float(self.varList[i].get()))
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E60"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                    self.resultValueList.insert(1, tempList)
                    self.resultValueList.append(tempList2)
                if self.mode == "insert":
                    self.insert = self.insertCb.current()
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class PasteCpuDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, copyCpuInfo):
        self.decryptFile = decryptFile
        self.num = num
        self.copyCpuInfo = copyCpuInfo
        self.reloadFlag = False
        super(PasteCpuDialog, self).__init__(parent=master, title=title)

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
        if not self.decryptFile.saveCpuInfo(self.num, "insert", self.copyCpuInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        if not self.decryptFile.saveCpuInfo(self.num + 1, "insert", self.copyCpuInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
        self.reloadFlag = True
