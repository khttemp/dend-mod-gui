import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class CpuWidget:
    def __init__(self, root, frame, decryptFile, cpuList, rootFrameAppearance, reloadFunc, selectId):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.cpuList = cpuList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.copyCpuInfo = []
        cpuLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["cpuInfoLabel"])
        cpuLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        headerFrame = ttkCustomWidget.CustomTtkFrame(cpuLf)
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

        self.treeviewFrame = ScrollbarTreeviewRailEditor(cpuLf, self.v_select, btnList)

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

            if self.decryptFile.game == "CS":
                col_tuple += ("cpuInfoDefSpeed", )

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
            if self.decryptFile.game == "CS":
                self.treeviewFrame.tree.column("cpuInfoDefSpeed", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["cpuInfoNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoRailNo", text=textSetting.textList["railEditor"]["cpuInfoRailNo"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoConst1", text=textSetting.textList["railEditor"]["cpuInfoConst1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMode", text=textSetting.textList["railEditor"]["cpuInfoMode"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMinLen", text=textSetting.textList["railEditor"]["cpuInfoMinLen"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMaxLen", text=textSetting.textList["railEditor"]["cpuInfoMaxLen"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMaxSpeed", text=textSetting.textList["railEditor"]["cpuInfoMaxSpeed"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cpuInfoMinSpeed", text=textSetting.textList["railEditor"]["cpuInfoMinSpeed"], anchor=tkinter.CENTER)
            if self.decryptFile.game == "CS":
                self.treeviewFrame.tree.heading("cpuInfoDefSpeed", text=textSetting.textList["railEditor"]["cpuInfoDefSpeed"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for cpuInfo in self.cpuList:
                data = (index,)
                data += (cpuInfo[0], cpuInfo[1], cpuInfo[2])
                data += (cpuInfo[3], cpuInfo[4])
                data += (cpuInfo[5], cpuInfo[6])
                if self.decryptFile.game == "CS":
                    data += (cpuInfo[7], )
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1
        elif self.decryptFile.game == "LS":
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
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.readFlag:
                col_tuple = (
                    "treeNum",
                    "cpuInfoRailNo",
                    "cpuInfoList",
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
                    data += (cpuInfo[2], )
                    data += (cpuInfo[3], cpuInfo[4], cpuInfo[5], cpuInfo[6], cpuInfo[7], )
                    data += (",".join(map(str, cpuInfo[8])), )
                    self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                    index += 1
            else:
                col_tuple = (
                    "treeNum",
                    "cpuInfoList",
                    "cpuInfoMode",
                    "cpuInfoMinLen"
                )

                self.treeviewFrame.tree["columns"] = col_tuple
                self.treeviewFrame.tree.column("#0", width=0, stretch=False)
                self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
                self.treeviewFrame.tree.column("cpuInfoList", anchor=tkinter.CENTER, width=100)
                self.treeviewFrame.tree.column("cpuInfoMode", anchor=tkinter.CENTER, width=50)
                self.treeviewFrame.tree.column("cpuInfoMinLen", anchor=tkinter.CENTER, width=50)

                self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["cpuInfoNum"], anchor=tkinter.CENTER)
                self.treeviewFrame.tree.heading("cpuInfoList", text=textSetting.textList["railEditor"]["cpuInfoList"], anchor=tkinter.CENTER)
                self.treeviewFrame.tree.heading("cpuInfoMode", text=textSetting.textList["railEditor"]["cpuInfoMode"], anchor=tkinter.CENTER)
                self.treeviewFrame.tree.heading("cpuInfoMinLen", text=textSetting.textList["railEditor"]["cpuInfoMinLen"], anchor=tkinter.CENTER)

                self.treeviewFrame.tree["displaycolumns"] = col_tuple

                index = 0
                for cpuInfo in self.cpuList:
                    data = (index,)
                    data += (",".join(map(str, cpuInfo[0])), )
                    data += (cpuInfo[1], cpuInfo[2], )
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
        result = EditCpuListWidget(self.root, textSetting.textList["railEditor"]["modifyCpuInfoLabel"], self.decryptFile, "modify", num, selectItem, self.rootFrameAppearance)
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
        result = EditCpuListWidget(self.root, textSetting.textList["railEditor"]["insertCpuInfoLabel"], self.decryptFile, "insert", num, selectItem, self.rootFrameAppearance)
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
        elif self.decryptFile.game == "LS":
            for i in range(len(cpuInfoKeyList)):
                key = cpuInfoKeyList[i]
                if i in [0, 2, 3]:
                    copyList.append(int(selectItem[key]))
                elif i in [1, 9]:
                    tempList = [float(x) for x in selectItem[key].split(",")]
                    copyList.append(tempList)
                else:
                    copyList.append(float(selectItem[key]))
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.readFlag:
                for i in range(len(cpuInfoKeyList)):
                    key = cpuInfoKeyList[i]
                    if i in [0, 2]:
                        copyList.append(int(selectItem[key]))
                    elif i in [1, 8]:
                        tempList = [float(x) for x in selectItem[key].split(",")]
                        copyList.append(tempList)
                    else:
                        copyList.append(float(selectItem[key]))
            else:
                for i in range(len(cpuInfoKeyList)):
                    key = cpuInfoKeyList[i]
                    if i == 1:
                        copyList.append(int(selectItem[key]))
                    elif i == 0:
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
        result = PasteCpuDialog(self.root, textSetting.textList["railEditor"]["pasteCpuInfoLabel"], self.decryptFile, int(selectItem["treeNum"]), self.copyCpuInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc(selectId)


class EditCpuListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, num, cpuInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.cpuInfo = cpuInfo
        self.varList = []
        self.varCnt = 0
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        cpuInfoKeyList = list(self.cpuInfo.keys())
        cpuInfoKeyList.pop(0)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            for i in range(len(cpuInfoKeyList)):
                cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"][cpuInfoKeyList[i]], font=textSetting.textList["font2"])
                cpuInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i >= 3:
                    varCpuInfo = tkinter.DoubleVar()
                    self.varList.append(varCpuInfo)
                    cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                    cpuInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varCpuInfo.set(round(float(self.cpuInfo[cpuInfoKeyList[i]]), 3))
                    self.varCnt += 1
                else:
                    varCpuInfo = tkinter.IntVar()
                    self.varList.append(varCpuInfo)
                    cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                    cpuInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                    self.varCnt += 1
        elif self.decryptFile.game == "LS":
            rowNum = 0
            colNum = 0
            for i in range(len(cpuInfoKeyList)):
                if i in [0, 2, 3]:
                    cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                    cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                    varCpuInfo = tkinter.IntVar()
                    self.varList.append(varCpuInfo)
                    cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                    cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                    rowNum += 1
                    if self.mode == "modify":
                        varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                    self.varCnt += 1
                elif i in [1, 9]:
                    if i == 0:
                        tempListLen = 6
                    else:
                        tempListLen = 3
                    if self.mode == "modify":
                        tempList = [float(x) for x in self.cpuInfo[cpuInfoKeyList[i]].split(",")]
                    for j in range(tempListLen):
                        cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["cpuInfoLsListLabel"].format(colNum + 1, j), font=textSetting.textList["font2"])
                        cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                        varCpuInfo = tkinter.DoubleVar()
                        self.varList.append(varCpuInfo)
                        cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                        cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                        rowNum += 1
                        if self.mode == "modify":
                            varCpuInfo.set(tempList[j])
                        self.varCnt += 1
                    colNum += 1
                    rowNum = 0
                else:
                    cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                    cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                    varCpuInfo = tkinter.DoubleVar()
                    self.varList.append(varCpuInfo)
                    cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                    cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                    rowNum += 1
                    if self.mode == "modify":
                        varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                    self.varCnt += 1
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.readFlag:
                rowNum = 0
                colNum = 0
                for i in range(len(cpuInfoKeyList)):
                    if i in [0, 2]:
                        cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                        cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                        varCpuInfo = tkinter.IntVar()
                        self.varList.append(varCpuInfo)
                        cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                        cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                        rowNum += 1
                        if self.mode == "modify":
                            varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                        self.varCnt += 1
                    elif i in [1, 8]:
                        if i == 1:
                            tempListLen = 6
                        else:
                            tempListLen = 3
                        if self.mode == "modify":
                            tempList = [float(x) for x in self.cpuInfo[cpuInfoKeyList[i]].split(",")]
                        for j in range(tempListLen):
                            cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["cpuInfoLsListLabel"].format(colNum + 1, j), font=textSetting.textList["font2"])
                            cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                            varCpuInfo = tkinter.DoubleVar()
                            self.varList.append(varCpuInfo)
                            cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                            cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                            rowNum += 1
                            if self.mode == "modify":
                                varCpuInfo.set(tempList[j])
                            self.varCnt += 1
                        colNum += 1
                        rowNum = 0
                    else:
                        cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                        cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                        varCpuInfo = tkinter.DoubleVar()
                        self.varList.append(varCpuInfo)
                        cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                        cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                        rowNum += 1
                        if self.mode == "modify":
                            varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                        self.varCnt += 1
            else:
                rowNum = 0
                colNum = 0
                for i in range(len(cpuInfoKeyList)):
                    if i == 1:
                        cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                        cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                        varCpuInfo = tkinter.IntVar()
                        self.varList.append(varCpuInfo)
                        cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                        cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                        rowNum += 1
                        if self.mode == "modify":
                            varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                        self.varCnt += 1
                    elif i == 0:
                        tempListLen = 6
                        if self.mode == "modify":
                            tempList = [float(x) for x in self.cpuInfo[cpuInfoKeyList[i]].split(",")]
                        for j in range(tempListLen):
                            cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["cpuInfoLsListLabel"].format(colNum + 1, j), font=textSetting.textList["font2"])
                            cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                            varCpuInfo = tkinter.DoubleVar()
                            self.varList.append(varCpuInfo)
                            cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                            cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                            rowNum += 1
                            if self.mode == "modify":
                                varCpuInfo.set(tempList[j])
                            self.varCnt += 1
                        colNum += 1
                        rowNum = 0
                    else:
                        cpuInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=cpuInfoKeyList[i], font=textSetting.textList["font2"])
                        cpuInfoLb.grid(row=rowNum, column=2 * colNum, sticky=tkinter.W + tkinter.E)
                        varCpuInfo = tkinter.DoubleVar()
                        self.varList.append(varCpuInfo)
                        cpuInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                        cpuInfoEt.grid(row=rowNum, column=2 * colNum + 1, sticky=tkinter.W + tkinter.E)
                        rowNum += 1
                        if self.mode == "modify":
                            varCpuInfo.set(self.cpuInfo[cpuInfoKeyList[i]])
                        self.varCnt += 1

        if self.mode == "insert":
            if self.decryptFile.game == "LSTrial" and not self.decryptFile.readFlag:
                self.setInsertWidget(master, 6)
            else:
                self.setInsertWidget(master, len(cpuInfoKeyList))
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
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    for i in range(len(self.varList)):
                        try:
                            if i >= 3:
                                res = float(self.varList[i].get())
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E60"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                elif self.decryptFile.game == "LS":
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
                elif self.decryptFile.game == "LSTrial":
                    if self.decryptFile.readFlag:
                        tempList = []
                        tempList2 = []
                        for i in range(len(self.varList)):
                            try:
                                if i in [0, 7]:
                                    res = int(self.varList[i].get())
                                    self.resultValueList.append(res)
                                elif i in [1, 2, 3, 4, 5, 6]:
                                    tempList.append(float(self.varList[i].get()))
                                elif i in [8, 9, 10, 11, 12]:
                                    res = float(self.varList[i].get())
                                    self.resultValueList.append(res)
                                elif i in [13, 14, 15]:
                                    tempList2.append(float(self.varList[i].get()))
                            except Exception:
                                errorMsg = textSetting.textList["errorList"]["E60"]
                                mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                                return False
                        self.resultValueList.insert(1, tempList)
                        self.resultValueList.append(tempList2)
                    else:
                        tempList = []
                        for i in range(len(self.varList)):
                            try:
                                if i in [0, 1, 2, 3, 4, 5]:
                                    tempList.append(float(self.varList[i].get()))
                                elif i == 6:
                                    res = int(self.varList[i].get())
                                    self.resultValueList.append(res)
                                else:
                                    res = float(self.varList[i].get())
                                    self.resultValueList.append(res)
                            except Exception:
                                errorMsg = textSetting.textList["errorList"]["E60"]
                                mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                                return False
                        self.resultValueList.insert(0, tempList)
                if self.mode == "insert":
                    self.insert = self.insertCb.current()
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class PasteCpuDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, num, copyCpuInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.num = num
        self.copyCpuInfo = copyCpuInfo
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
