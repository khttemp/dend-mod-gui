import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class StationNameWidget:
    def __init__(self, frame, decryptFile, stationNameList, reloadFunc, selectId):
        self.frame = frame
        self.decryptFile = decryptFile
        self.stationNameList = stationNameList
        self.reloadFunc = reloadFunc
        self.copyStationNameInfo = []
        self.stationNameLf = ttk.LabelFrame(self.frame, text="駅名位置情報")
        self.stationNameLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        self.headerFrame = ttk.Frame(self.stationNameLf)
        self.headerFrame.pack()

        self.selectLbFrame = ttk.Frame(self.headerFrame)
        self.selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        selectLb = ttk.Label(self.selectLbFrame, text="選択した行番号：", font=("", 14))
        selectLb.pack(side=tkinter.LEFT, padx=15, pady=15)

        self.v_select = tkinter.StringVar()
        selectEt = ttk.Entry(self.selectLbFrame, textvariable=self.v_select, font=("", 14), width=5, state="readonly", justify="center")
        selectEt.pack(side=tkinter.LEFT, padx=5, pady=15)

        self.btnFrame = ttk.Frame(self.headerFrame)
        self.btnFrame.pack(anchor=tkinter.NE, padx=15)

        editLineBtn = ttk.Button(self.btnFrame, text="選択した行を修正する", width=25, state="disabled", command=self.editLine)
        editLineBtn.grid(row=0, column=0, padx=10, pady=15)

        insertLineBtn = ttk.Button(self.btnFrame, text="選択した行に挿入する", width=25, state="disabled", command=self.insertLine)
        insertLineBtn.grid(row=0, column=1, padx=10, pady=15)

        deleteLineBtn = ttk.Button(self.btnFrame, text="選択した行を削除する", width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=15)

        copyLineBtn = ttk.Button(self.btnFrame, text="選択した行をコピーする", width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=15)

        self.pasteLineBtn = ttk.Button(self.btnFrame, text="選択した行に貼り付けする", width=25, state="disabled", command=self.pasteLine)
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
            col_tuple = ("番号", "駅名", "駅フラグ", "レールNo", "f1", "f2", "f3", "e1", "e2", "e3", "e4")

            self.treeviewFrame.tree['columns'] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("番号", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("駅名", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("駅フラグ", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("レールNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e4", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("駅名", text="駅名", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("駅フラグ", text="駅フラグ", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("レールNo", text="レールNo", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f1", text="f1", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f2", text="f2", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f3", text="f3", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e1", text="e1", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e2", text="e2", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e3", text="e3", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e4", text="e4", anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for stNameInfo in self.stationNameList:
                data = (index,)
                data += (stNameInfo[0], stNameInfo[1], stNameInfo[2])
                data += (round(float(stNameInfo[3]), 3), round(float(stNameInfo[4]), 3), round(float(stNameInfo[5]), 3))
                data += (stNameInfo[6], stNameInfo[7], stNameInfo[8], stNameInfo[9])
                self.treeviewFrame.tree.insert(parent='', index='end', iid=index, values=data)
                index += 1
        elif self.decryptFile.game == "BS":
            col_tuple = ("番号", "駅名", "駅フラグ", "レールNo")

            self.treeviewFrame.tree['columns'] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("番号", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("駅名", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("駅フラグ", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("レールNo", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("駅名", text="駅名", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("駅フラグ", text="駅フラグ", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("レールNo", text="レールNo", anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for stNameInfo in self.stationNameList:
                data = (index,)
                data += (stNameInfo[0], stNameInfo[1], stNameInfo[2])
                self.treeviewFrame.tree.insert(parent='', index='end', iid=index, values=data)
                index += 1
        elif self.decryptFile.game == "LS":
            col_tuple = ("番号", "駅名", "駅フラグ", "レールNo", "f1", "f2", "f3", "f4", "f5", "f6")

            self.treeviewFrame.tree['columns'] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("番号", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("駅名", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("駅フラグ", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("レールNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f4", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f5", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("f6", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("駅名", text="駅名", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("駅フラグ", text="駅フラグ", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("レールNo", text="レールNo", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f1", text="f1", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f2", text="f2", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f3", text="f3", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f4", text="f4", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f5", text="f5", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("f6", text="f6", anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for stNameInfo in self.stationNameList:
                data = (index,)
                data += (stNameInfo[0], stNameInfo[1], stNameInfo[2])
                data += (stNameInfo[3], stNameInfo[4], stNameInfo[5], stNameInfo[6], stNameInfo[7], stNameInfo[8])
                self.treeviewFrame.tree.insert(parent='', index='end', iid=index, values=data)
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
        num = int(selectItem["番号"])
        result = EditStationNameListWidget(self.frame, "駅名位置修正", self.decryptFile, "modify", num, selectItem)
        if result.reloadFlag:
            if not self.decryptFile.saveStationNameInfo(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名位置情報を修正しました")
            self.reloadFunc(selectId)

    def insertLine(self):
        noStationNameInfoFlag = False
        if not self.treeviewFrame.tree.selection():
            noStationNameInfoFlag = True
            selectId = None
            num = 0
            keyList = self.treeviewFrame.tree['columns']
            selectItem = {}
            for key in keyList:
                selectItem[key] = None
        else:
            selectId = self.treeviewFrame.tree.selection()[0]
            selectItem = self.treeviewFrame.tree.set(selectId)
            num = int(selectItem["番号"])
        result = EditStationNameListWidget(self.frame, "駅名位置挿入", self.decryptFile, "insert", num, selectItem)
        if result.reloadFlag:
            if noStationNameInfoFlag:
                if result.insert == 0:
                    num += 1
            if not self.decryptFile.saveStationNameInfo(num, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名位置情報を修正しました")
            self.reloadFunc(selectId)

    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        warnMsg = "選択した行を削除します。\nそれでもよろしいですか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.saveStationNameInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名位置情報を修正しました")
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
        mb.showinfo(title="成功", message="コピーしました")
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteStationNameDialog(self.frame, "駅名位置貼り付け", self.decryptFile, int(selectItem["番号"]), self.copyStationNameInfo)
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
            self.stationNameInfoLb = ttk.Label(master, text=stationNameInfoKeyList[i], font=("", 14))
            self.stationNameInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["CS", "RS"]:
                if i == 0:
                    self.varStationNameInfo = tkinter.StringVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                elif i in [3, 4, 5]:
                    self.varStationNameInfo = tkinter.DoubleVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    self.varStationNameInfo = tkinter.IntVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            elif self.decryptFile.game == "BS":
                if i == 0:
                    self.varStationNameInfo = tkinter.StringVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    self.varStationNameInfo = tkinter.IntVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            elif self.decryptFile.game == "LS":
                if i == 0:
                    self.varStationNameInfo = tkinter.StringVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                elif i in [1, 2]:
                    self.varStationNameInfo = tkinter.IntVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
                else:
                    self.varStationNameInfo = tkinter.DoubleVar()
                    self.varList.append(self.varStationNameInfo)
                    self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                    self.stationNameInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])

        if self.mode == "insert":
            self.setInsertWidget(master, len(stationNameInfoKeyList))

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text="挿入する位置", font=("", 12))
        self.insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=("", 12), textvariable=self.v_insert, values=["後", "前"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
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
                            errorMsg = "整数で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                    elif self.decryptFile.game == "BS":
                        try:
                            if i == 0:
                                res = self.varList[i].get()
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = "整数で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
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
                            errorMsg = "整数で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)

                if self.mode == "insert":
                    self.insert = self.insertCb.current()
                return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

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
        self.posLb = ttk.Label(master, text="挿入する位置を選んでください", font=("", 14))
        self.posLb.pack(padx=10, pady=10)

    def buttonbox(self):
        box = tkinter.Frame(self, padx=5, pady=5)
        self.frontBtn = tkinter.Button(box, text="前", font=("", 12), width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = tkinter.Button(box, text="後", font=("", 12), width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = tkinter.Button(box, text="Cancel", font=("", 12), width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)
        box.pack()

    def frontInsert(self):
        self.ok()
        if not self.decryptFile.saveStationNameInfo(self.num, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="駅名位置情報を修正しました")
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        if not self.decryptFile.saveStationNameInfo(self.num + 1, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="駅名位置情報を修正しました")
        self.reloadFlag = True
