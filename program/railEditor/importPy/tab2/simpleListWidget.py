import copy

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


class SimpleListWidget:
    def __init__(self, frame, text, decryptFile, listInfo, index, listCntVer, reloadFunc):
        self.frame = frame
        self.text = text
        self.decryptFile = decryptFile
        self.index = index
        self.listCntVer = listCntVer
        self.reloadFunc = reloadFunc
        self.simpleList = copy.deepcopy(listInfo)
        self.selectIndexNum = -1

        self.simpleListLf = ttk.LabelFrame(self.frame, text=text)
        self.simpleListLf.pack(anchor=tkinter.NW, padx=10, side=tkinter.LEFT)

        self.btnFrame = ttk.Frame(self.simpleListLf)
        self.btnFrame.pack()

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.listFrame = ttk.Frame(self.simpleListLf)
        self.listFrame.pack()

        copySimpleList = self.setListboxInfo(self.simpleList)
        self.v_simpleList = tkinter.StringVar(value=copySimpleList)
        self.simpleListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), width=25, listvariable=self.v_simpleList)
        self.simpleListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.simpleListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.simpleListListbox, self.simpleListListbox.curselection()))

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

    def setListboxInfo(self, listboxInfo):
        self.simpleList = listboxInfo
        copySimpleList = copy.deepcopy(self.simpleList)
        if len(copySimpleList) > 0:
            for i in range(len(copySimpleList)):
                simpleName = copySimpleList[i]
                copySimpleList[i] = "{0:02d}→{1}".format(i, simpleName)
        else:
            copySimpleList = ["(なし)"]

        return copySimpleList

    def modify(self):
        result = EditSimpleListWidget(self.frame, self.text + "の変更", self.decryptFile, "modify", self.selectIndexNum, self.simpleList)
        if result.reloadFlag:
            if not self.decryptFile.saveSimpleList(self.index, self.listCntVer, result.simpleList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            mb.showinfo(title="成功", message=self.text + "を修正しました")
            self.reloadFunc()

    def insert(self):
        result = EditSimpleListWidget(self.frame, self.text + "の挿入", self.decryptFile, "insert", self.selectIndexNum, self.simpleList)
        if result.reloadFlag:
            if not self.decryptFile.saveSimpleList(self.index, self.listCntVer, result.simpleList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            mb.showinfo(title="成功", message=self.text + "を修正しました")
            self.reloadFunc()

    def delete(self):
        msg = "{0}番目を削除します。\nそれでもよろしいですか？".format(self.selectIndexNum + 1)
        result = mb.askokcancel(title="警告", message=msg, icon="warning")
        if result:
            self.simpleList.pop(self.selectIndexNum)
            if not self.decryptFile.saveSimpleList(self.index, self.listCntVer, self.simpleList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            mb.showinfo(title="成功", message=self.text + "を修正しました")
            self.reloadFunc()


class EditSimpleListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, index, simpleList):
        self.decryptFile = decryptFile
        self.mode = mode
        self.index = index
        self.simpleList = simpleList
        self.reloadFlag = False
        super(EditSimpleListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.tempNameLb = ttk.Label(master, text="値", font=("", 12), width=12)
        self.tempNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varTemp = tkinter.StringVar()
        if self.mode == "modify":
            self.varTemp.set(self.simpleList[self.index])
        self.txtEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
        self.txtEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, 1)

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
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                res = self.varTemp.get()
                if not res:
                    errorMsg = "値を入力してください。"
                    mb.showerror(title="値エラー", message=errorMsg)
                    return False
                if self.mode == "modify":
                    self.simpleList[self.index] = res
                else:
                    insertIdx = self.insertCb.current()
                    if insertIdx == 0:
                        self.simpleList.insert(self.index + 1, res)
                    else:
                        self.simpleList.insert(self.index, res)
                return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
