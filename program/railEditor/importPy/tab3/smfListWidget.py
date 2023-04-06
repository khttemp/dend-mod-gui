import copy
import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from program.railEditor.importPy.tkinterScrollbarTreeview import ScrollbarTreeview


class SmfListWidget:
    def __init__(self, frame, decryptFile, smfList, rowNum, reloadFunc, selectId):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = smfList
        self.reloadFunc = reloadFunc
        self.copySmfInfo = []

        self.swfListLf = ttk.LabelFrame(self.frame, text="smf情報")
        self.swfListLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.X)

        self.headerFrame = ttk.Frame(self.swfListLf)
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

        if self.decryptFile.game in ["LS", "BS"]:
            self.listModifyBtn = ttk.Button(self.btnFrame, text="選択した行のリストを修正する", width=25, state="disabled", command=self.listModify)
            self.listModifyBtn.grid(row=1, column=2, padx=10, pady=15)

        btnList = [
            editLineBtn,
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]
        if self.decryptFile.game in ["LS", "BS"]:
            btnList.append(self.listModifyBtn)

        self.treeFrame = ttk.Frame(self.swfListLf)
        self.treeFrame.pack(anchor=tkinter.NW, fill=tkinter.X)

        self.treeviewFrame = ScrollbarTreeview(self.treeFrame, rowNum, self.v_select, btnList)

        if self.decryptFile.game in ["CS", "RS"]:
            col_tuple = ("番号", "smf名", "e1", "e2", "長さ", "e3", "e4", "架線柱No", "架線No")

            self.treeviewFrame.tree['columns'] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("番号", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("smf名", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("e1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("長さ", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e4", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("架線柱No", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("架線No", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smf名", text="smf名", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e1", text="e1", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e2", text="e2", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("長さ", text="長さ", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e3", text="e3", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e4", text="e4", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("架線柱No", text="架線柱No", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("架線No", text="架線No", anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for smfInfo in self.smfList:
                data = (index,)
                data += (smfInfo[0], smfInfo[1], smfInfo[2], smfInfo[3], smfInfo[4], smfInfo[5])
                data += (smfInfo[6], smfInfo[7])
                self.treeviewFrame.tree.insert(parent='', index='end', iid=index, values=data)
                index += 1
        elif self.decryptFile.game == "BS":
            col_tuple = ("番号", "smf名", "長さ", "e1", "e2", "リスト数")

            self.treeviewFrame.tree['columns'] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("番号", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("smf名", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("長さ", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("リスト数", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smf名", text="smf名", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("長さ", text="長さ", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e1", text="e1", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e2", text="e2", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("リスト数", text="リスト数", anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for smfInfo in self.smfList:
                data = (index,)
                data += (smfInfo[0], smfInfo[1], smfInfo[2], smfInfo[3], len(smfInfo[4]))
                self.treeviewFrame.tree.insert(parent='', index='end', iid=index, values=data)
                index += 1
        else:
            col_tuple = ("番号", "smf名", "長さ", "e1", "リスト数")

            self.treeviewFrame.tree['columns'] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("番号", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("smf名", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("長さ", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("e1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("リスト数", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smf名", text="smf名", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("長さ", text="長さ", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("e1", text="e1", anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("リスト数", text="リスト数", anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for smfInfo in self.smfList:
                data = (index,)
                if len(smfInfo[3]) == 0:
                    data += (smfInfo[0], smfInfo[1], smfInfo[2], -1)
                else:
                    data += (smfInfo[0], smfInfo[1], smfInfo[2], len(smfInfo[3]))
                self.treeviewFrame.tree.insert(parent='', index='end', iid=index, values=data)
                index += 1

        if selectId is not None:
            if selectId >= len(self.smfList):
                selectId = len(self.smfList) - 1
            if selectId - 3 < 0:
                self.treeviewFrame.tree.see(0)
            else:
                self.treeviewFrame.tree.see(selectId - 3)
            self.treeviewFrame.tree.selection_set(selectId)

    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        result = EditSmfListWidget(self.frame, "smf修正", self.decryptFile, "modify", num, selectItem)
        if result.reloadFlag:
            if not self.decryptFile.saveSmfInfo(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="smf情報を修正しました")
            self.reloadFunc(selectId)

    def insertLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        result = EditSmfListWidget(self.frame, "smf挿入", self.decryptFile, "insert", num, selectItem)
        if result.reloadFlag:
            if result.insert == 0:
                num += 1
            if not self.decryptFile.saveSmfInfo(num, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="smf情報を修正しました")
            self.reloadFunc(selectId)

    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        warnMsg = "選択した行を削除します。\nそれでもよろしいですか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.saveSmfInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="smf情報を修正しました")
            self.reloadFunc(selectId)

    def copyLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)

        smfInfoKeyList = list(selectItem.keys())
        smfInfoKeyList.pop(0)
        copyList = []

        if self.decryptFile.game in ["CS", "RS"]:
            for i in range(len(smfInfoKeyList)):
                key = smfInfoKeyList[i]
                if i == 0:
                    copyList.append(selectItem[key])
                elif i in [1, 2, 4, 5]:
                    copyList.append(int(selectItem[key], 16))
                else:
                    copyList.append(int(selectItem[key]))
        elif self.decryptFile.game == "BS":
            for i in range(len(smfInfoKeyList)):
                key = smfInfoKeyList[i]
                if i == 0:
                    copyList.append(selectItem[key])
                elif i == 1:
                    copyList.append(int(selectItem[key]))
                elif i in [2, 3]:
                    copyList.append(int(selectItem[key], 16))
                else:
                    tempInfo = self.smfList[int(selectId)][4]
                    copyList.append(tempInfo)
        else:
            for i in range(len(smfInfoKeyList)):
                key = smfInfoKeyList[i]
                if i == 0:
                    copyList.append(selectItem[key])
                elif i == 1:
                    copyList.append(int(selectItem[key]))
                elif i == 2:
                    copyList.append(int(selectItem[key], 16))
                else:
                    tempInfo = self.smfList[int(selectId)][3]
                    copyList.append(tempInfo)
        self.copySmfInfo = copyList
        mb.showinfo(title="成功", message="コピーしました")
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteSmfListDialog(self.frame, "smf貼り付け", self.decryptFile, int(selectItem["番号"]), self.copySmfInfo)
        if result.reloadFlag:
            self.reloadFunc(selectId)

    def listModify(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        originTempList = self.decryptFile.smfList[int(selectId)][-1]
        result = EditListElement(self.frame, "リストの変更", self.decryptFile, originTempList)
        if result.reloadFlag:
            if not self.decryptFile.saveSmfListElement(int(selectId), result.tempList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            mb.showinfo(title="成功", message="リストを修正しました")
            self.reloadFunc(selectId)


class EditSmfListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, num, smfInfo):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.smfInfo = smfInfo
        self.varList = []
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super(EditSmfListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        smfInfoKeyList = list(self.smfInfo.keys())
        smfInfoKeyList.pop(0)
        if self.decryptFile.game in ["CS", "RS"]:
            for i in range(len(smfInfoKeyList)):
                self.smfInfoLb = ttk.Label(master, text=smfInfoKeyList[i], font=("", 14))
                self.smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varSmfInfo = tkinter.StringVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                elif i in [1, 2, 4, 5]:
                    mb = ttk.Menubutton(master, text="switch設定")
                    menu = tkinter.Menu(mb)
                    mb["menu"] = menu

                    Flg0 = tkinter.BooleanVar()
                    Flg1 = tkinter.BooleanVar()
                    Flg2 = tkinter.BooleanVar()
                    Flg3 = tkinter.BooleanVar()
                    Flg4 = tkinter.BooleanVar()
                    Flg5 = tkinter.BooleanVar()
                    Flg6 = tkinter.BooleanVar()
                    Flg7 = tkinter.BooleanVar()
                    flagList = [Flg0, Flg1, Flg2, Flg3, Flg4, Flg5, Flg6, Flg7]
                    self.varList.append(flagList)
                    menu.add_checkbutton(label="フラグ0", variable=Flg7)
                    menu.add_checkbutton(label="フラグ1", variable=Flg6)
                    menu.add_checkbutton(label="フラグ2", variable=Flg5)
                    menu.add_checkbutton(label="フラグ3", variable=Flg4)
                    menu.add_checkbutton(label="フラグ4", variable=Flg3)
                    menu.add_checkbutton(label="フラグ5", variable=Flg2)
                    menu.add_checkbutton(label="フラグ6", variable=Flg1)
                    menu.add_checkbutton(label="フラグ7", variable=Flg0)
                    if self.mode == "modify":
                        val = int(self.smfInfo[smfInfoKeyList[i]], 16)
                        for j in range(8):
                            if val & (2**j) == 0:
                                flagList[j].set(False)
                            else:
                                flagList[j].set(True)

                    mb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                else:
                    self.varSmfInfo = tkinter.IntVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        if i == 3:
                            default = 8
                        else:
                            default = 255
                        self.varSmfInfo.set(default)
        elif self.decryptFile.game == "BS":
            smfInfoKeyList.pop()
            for i in range(len(smfInfoKeyList)):
                self.smfInfoLb = ttk.Label(master, text=smfInfoKeyList[i], font=("", 14))
                self.smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varSmfInfo = tkinter.StringVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                elif i == 1:
                    self.varSmfInfo = tkinter.IntVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        default = 8
                        self.varSmfInfo.set(default)
                elif i in [2, 3]:
                    mb = ttk.Menubutton(master, text="switch設定")
                    menu = tkinter.Menu(mb)
                    mb["menu"] = menu

                    Flg0 = tkinter.BooleanVar()
                    Flg1 = tkinter.BooleanVar()
                    Flg2 = tkinter.BooleanVar()
                    Flg3 = tkinter.BooleanVar()
                    Flg4 = tkinter.BooleanVar()
                    Flg5 = tkinter.BooleanVar()
                    Flg6 = tkinter.BooleanVar()
                    Flg7 = tkinter.BooleanVar()
                    flagList = [Flg0, Flg1, Flg2, Flg3, Flg4, Flg5, Flg6, Flg7]
                    self.varList.append(flagList)
                    menu.add_checkbutton(label="フラグ0", variable=Flg7)
                    menu.add_checkbutton(label="フラグ1", variable=Flg6)
                    menu.add_checkbutton(label="フラグ2", variable=Flg5)
                    menu.add_checkbutton(label="フラグ3", variable=Flg4)
                    menu.add_checkbutton(label="フラグ4", variable=Flg3)
                    menu.add_checkbutton(label="フラグ5", variable=Flg2)
                    menu.add_checkbutton(label="フラグ6", variable=Flg1)
                    menu.add_checkbutton(label="フラグ7", variable=Flg0)
                    if self.mode == "modify":
                        val = int(self.smfInfo[smfInfoKeyList[i]], 16)
                        for j in range(8):
                            if val & (2**j) == 0:
                                flagList[j].set(False)
                            else:
                                flagList[j].set(True)

                    mb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        else:
            smfInfoKeyList.pop()
            for i in range(len(smfInfoKeyList)):
                self.smfInfoLb = ttk.Label(master, text=smfInfoKeyList[i], font=("", 14))
                self.smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varSmfInfo = tkinter.StringVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                elif i == 1:
                    self.varSmfInfo = tkinter.IntVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        default = 8
                        self.varSmfInfo.set(default)
                elif i == 2:
                    mb = ttk.Menubutton(master, text="switch設定")
                    menu = tkinter.Menu(mb)
                    mb["menu"] = menu

                    Flg0 = tkinter.BooleanVar()
                    Flg1 = tkinter.BooleanVar()
                    Flg2 = tkinter.BooleanVar()
                    Flg3 = tkinter.BooleanVar()
                    Flg4 = tkinter.BooleanVar()
                    Flg5 = tkinter.BooleanVar()
                    Flg6 = tkinter.BooleanVar()
                    Flg7 = tkinter.BooleanVar()
                    flagList = [Flg0, Flg1, Flg2, Flg3, Flg4, Flg5, Flg6, Flg7]
                    self.varList.append(flagList)
                    menu.add_checkbutton(label="フラグ0", variable=Flg7)
                    menu.add_checkbutton(label="フラグ1", variable=Flg6)
                    menu.add_checkbutton(label="フラグ2", variable=Flg5)
                    menu.add_checkbutton(label="フラグ3", variable=Flg4)
                    menu.add_checkbutton(label="フラグ4", variable=Flg3)
                    menu.add_checkbutton(label="フラグ5", variable=Flg2)
                    menu.add_checkbutton(label="フラグ6", variable=Flg1)
                    menu.add_checkbutton(label="フラグ7", variable=Flg0)
                    if self.mode == "modify":
                        val = int(self.smfInfo[smfInfoKeyList[i]], 16)
                        for j in range(8):
                            if val & (2**j) == 0:
                                flagList[j].set(False)
                            else:
                                flagList[j].set(True)

                    mb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(smfInfoKeyList))

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
                if self.decryptFile.game in ["CS", "RS"]:
                    try:
                        for i in range(len(self.varList)):
                            if i == 0:
                                res = self.varList[i].get()
                            elif i in [1, 2, 4, 5]:
                                bitList = self.varList[i]
                                res = 0
                                for j in range(len(bitList)):
                                    if bitList[j].get():
                                        res |= (2**j)
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)
                        if self.mode == "insert":
                            self.insert = self.insertCb.current()
                        return True
                    except Exception:
                        errorMsg = "整数で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                elif self.decryptFile.game == "BS":
                    try:
                        for i in range(len(self.varList)):
                            if i == 0:
                                res = self.varList[i].get()
                            elif i in [2, 3]:
                                bitList = self.varList[i]
                                res = 0
                                for j in range(len(bitList)):
                                    if bitList[j].get():
                                        res |= (2**j)
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)

                        if self.mode == "modify":
                            originTempList = self.decryptFile.smfList[self.num][4]
                            self.resultValueList.append(originTempList)
                        else:
                            self.resultValueList.append([])

                        if self.mode == "insert":
                            self.insert = self.insertCb.current()
                        return True
                    except Exception:
                        errorMsg = "整数で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                else:
                    try:
                        for i in range(len(self.varList)):
                            if i == 0:
                                res = self.varList[i].get()
                            elif i == 2:
                                bitList = self.varList[i]
                                res = 0
                                for j in range(len(bitList)):
                                    if bitList[j].get():
                                        res |= (2**j)
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)

                        if self.mode == "modify":
                            originTempList = self.decryptFile.smfList[self.num][3]
                            self.resultValueList.append(originTempList)
                        else:
                            self.resultValueList.append([])

                        if self.mode == "insert":
                            self.insert = self.insertCb.current()
                        return True
                    except Exception:
                        errorMsg = "整数で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True


class PasteSmfListDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, copySmfInfo):
        self.decryptFile = decryptFile
        self.num = num
        self.copySmfInfo = copySmfInfo
        self.reloadFlag = False
        super(PasteSmfListDialog, self).__init__(parent=master, title=title)

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
        if not self.decryptFile.saveSmfInfo(self.num, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="smf情報を修正しました")
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        if not self.decryptFile.saveSmfInfo(self.num + 1, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="smf情報を修正しました")
        self.reloadFlag = True


class EditListElement(sd.Dialog):
    def __init__(self, master, title, decryptFile, tempList):
        self.decryptFile = decryptFile
        self.tempList = copy.deepcopy(tempList)
        self.dirtyFlag = False
        self.reloadFlag = False
        self.resultList = []
        super(EditListElement, self).__init__(parent=master, title=title)

    def body(self, master):
        self.frame = master
        self.resizable(False, False)

        self.btnFrame = ttk.Frame(self.frame)
        self.btnFrame.pack()

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.listFrame = ttk.Frame(self.frame)
        self.listFrame.pack()

        copyTempList = self.setListboxInfo(self.tempList)
        self.v_tempList = tkinter.StringVar(value=copyTempList)
        self.tempListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), width=25, listvariable=self.v_tempList)
        self.tempListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.tempListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.tempListListbox, self.tempListListbox.curselection()))

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == "(なし)":
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def setListboxInfo(self, tempList):
        copyTempList = copy.deepcopy(tempList)
        if len(copyTempList) > 0:
            for i in range(len(copyTempList)):
                tempInfo = copyTempList[i]
                copyTempList[i] = "{0:02d}→{1}".format(i, tempInfo)
        else:
            copyTempList = ["(なし)"]

        return copyTempList

    def modify(self):
        result = EditListElementWidget(self.frame, "リスト変更", self.decryptFile, "modify", self.selectIndexNum, self.tempList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.tempList[self.selectIndexNum] = result.resultValueList
            copyTempList = self.setListboxInfo(self.tempList)
            self.v_tempList.set(copyTempList)

    def insert(self):
        result = EditListElementWidget(self.frame, "リスト挿入", self.decryptFile, "insert", self.selectIndexNum, self.tempList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.tempList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
            copyTempList = self.setListboxInfo(self.tempList)
            self.v_tempList.set(copyTempList)

    def delete(self):
        msg = "{0}番目を削除します。\nそれでもよろしいですか？".format(self.selectIndexNum + 1)
        result = mb.askokcancel(title="警告", message=msg, icon="warning")
        if result:
            self.dirtyFlag = True
            self.tempList.pop(self.selectIndexNum)
            copyTempList = self.setListboxInfo(self.tempList)
            self.v_tempList.set(copyTempList)
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def validate(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title="確認", message="このリストで修正しますか？", parent=self)
            if result:
                self.reloadFlag = True
                return True
        else:
            return True


class EditListElementWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, index, tempList):
        self.decryptFile = decryptFile
        self.mode = mode
        self.index = index
        self.tempList = tempList
        self.varList = []
        self.resultValueList = []
        self.insertPos = -1
        self.dirtyFlag = False
        super(EditListElementWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        if self.decryptFile.game == "BS":
            tempInfoLb = ["e1", "e2", "e3"]
        else:
            tempInfoLb = ["e1", "e2"]
        for i in range(len(tempInfoLb)):
            self.tempLb = ttk.Label(master, text=tempInfoLb[i], font=("", 14))
            self.tempLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.varTemp = tkinter.IntVar()
            if self.mode == "modify":
                tempInfo = self.tempList[self.index]
                self.varTemp.set(tempInfo[i])
            self.varList.append(self.varTemp)
            self.tempEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
            self.tempEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(tempInfoLb))

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
        infoMsg = "この値で修正しますか？"
        if self.mode == "insert":
            infoMsg = "この値で挿入しますか？"
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message=infoMsg, parent=self)
        if result:
            try:
                for i in range(len(self.varList)):
                    try:
                        res = int(self.varList[i].get())
                    except Exception:
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValueList.append(res)
                return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.dirtyFlag = True
