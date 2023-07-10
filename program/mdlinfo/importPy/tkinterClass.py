import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


class TreeViewDialog(sd.Dialog):
    def __init__(self, master, title, num, decryptFile):
        self.num = num
        self.master = master
        self.decryptFile = decryptFile
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.detailMdlList = decryptFile.allInfoList[self.num]["detailMdlList"]
        super(TreeViewDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        mainFrame = ttk.Frame(master, width=800, height=360)
        mainFrame.pack()

        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        fileNameEt = ttk.Entry(mainFrame, textvariable=self.v_smfName, font=("", 14), width=20, state="readonly", justify="center")
        fileNameEt.place(relx=0.04, rely=0.03)

        self.mdlInfoLf = tkinter.LabelFrame(mainFrame, text="モデル詳細情報")
        self.mdlInfoLf.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.74)

        self.frame = ttk.Frame(self.mdlInfoLf)
        self.frame.pack(expand=True, fill=tkinter.BOTH)

        self.tree = ttk.Treeview(self.frame, selectmode="browse")

        self.scrollbar_x = ttk.Scrollbar(self.frame, orient=tkinter.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=lambda first, last: self.scrollbar_x.set(first, last))
        self.scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.scrollbar_y = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=lambda first, last: self.scrollbar_y.set(first, last))
        self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.tree.pack(expand=True, fill=tkinter.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.treeSelect)

        self.colTuple = [
            "番号", "カラー数",
            "mesh",
            "const1",
            "ele1-3",
            "f1-4",
            "const0",
            "f5-7",
            "num1", "num2"
        ]

        self.tree['columns'] = self.colTuple
        self.tree.column('#0', width=0, stretch=False)

        for colName in self.colTuple:
            widthLen = 50
            if colName == "ele1-3":
                widthLen = 80
            elif colName == "f1-4":
                widthLen = 150
            elif colName == "f5-7":
                widthLen = 150
            self.tree.column(colName, anchor=tkinter.CENTER, width=widthLen)
            self.tree.heading(colName, text=colName, anchor=tkinter.CENTER)

        self.tree["displaycolumns"] = self.colTuple

        self.viewData(self.detailMdlList)

        self.editColorBtn = ttk.Button(mainFrame, text="カラー情報を修正する", width=25, state="disabled", command=self.editColor)
        self.editColorBtn.place(relx=0.42, rely=0.03)

        self.editElementBtn = ttk.Button(mainFrame, text="詳細要素を修正する", width=25, state="disabled", command=self.editElement)
        self.editElementBtn.place(relx=0.1, rely=0.13)

        self.insertElementBtn = ttk.Button(mainFrame, text="詳細要素を挿入する", width=25, state="disabled", command=self.insertElement)
        self.insertElementBtn.place(relx=0.42, rely=0.13)

        self.deleteElementBtn = ttk.Button(mainFrame, text="詳細要素を削除する", width=25, state="disabled", command=self.deleteElement)
        self.deleteElementBtn.place(relx=0.74, rely=0.13)

    def viewData(self, detailMdlList):
        index = 0
        for detailMdlInfo in detailMdlList:
            for i in range(len(self.colTuple)):
                data = (index + 1, detailMdlInfo["colorCnt"])
                data += (",".join(str(n) for n in detailMdlInfo["textureList"][0:2]),)
                data += (detailMdlInfo["textureList"][2],)
                data += (",".join(str(n) for n in detailMdlInfo["textureList"][3:6]),)
                data += (",".join(str(n) for n in detailMdlInfo["textureList"][6:10]),)
                data += (detailMdlInfo["textureList"][10],)
                data += (",".join(str(n) for n in detailMdlInfo["textureList"][11:14]),)
                data += (detailMdlInfo["textureList"][14],)
                data += (detailMdlInfo["textureList"][15],)
            self.tree.insert(parent='', index='end', iid=index, values=data)
            index += 1

    def treeSelect(self, event):
        selectId = self.tree.selection()[0]
        selectItem = self.tree.set(selectId)

        if selectItem["mesh"] == "0,0":
            self.editColorBtn['state'] = 'disabled'
        else:
            self.editColorBtn['state'] = 'normal'
        self.editElementBtn['state'] = 'normal'
        self.insertElementBtn['state'] = 'normal'
        self.deleteElementBtn['state'] = 'normal'

    def reload(self):
        self.decryptFile = self.decryptFile.reload()
        self.detailMdlList = self.decryptFile.allInfoList[self.num]["detailMdlList"]

        for i in self.tree.get_children():
            self.tree.delete(i)
        self.viewData(self.detailMdlList)

    def editColor(self):
        selectId = int(self.tree.selection()[0])
        selectItem = self.tree.set(selectId)
        detailNum = int(selectItem["番号"]) - 1
        result = TexImageDialog(self.master, "イメージ改造", self.num, detailNum, self.decryptFile, self.detailMdlList)
        if result.dirtyFlag:
            self.reload()
            self.tree.selection_set(selectId)

    def editElement(self):
        selectId = int(self.tree.selection()[0])
        selectItem = self.tree.set(selectId)
        detailNum = int(selectItem["番号"]) - 1
        result = DetailDialog(self.master, "モデル要素改造", "edit", self.num, detailNum, self.decryptFile, self.colTuple, self.detailMdlList)
        if result.cancelFlag:
            self.reload()
            self.tree.selection_set(selectId)

    def insertElement(self):
        selectId = int(self.tree.selection()[0])
        selectItem = self.tree.set(selectId)
        detailNum = int(selectItem["番号"]) - 1
        result = DetailDialog(self.master, "モデル要素改造", "insert", self.num, detailNum, self.decryptFile, self.colTuple, self.detailMdlList)
        if result.cancelFlag:
            self.reload()
            self.tree.selection_set(selectId)

    def deleteElement(self):
        selectId = int(self.tree.selection()[0])
        selectItem = self.tree.set(selectId)
        detailNum = int(selectItem["番号"]) - 1
        warnMsg = "{0}番目を削除します。\nそれでもよろしいですか？".format(detailNum + 1)
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

        if result:
            if not self.decryptFile.updateTex(self.num, detailNum, [], "delete"):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            mb.showinfo(title="成功", message="モデル要素情報を修正しました")
            selectId -= 1
            if selectId < 0:
                selectId = 0
            self.reload()
            self.tree.selection_set(selectId)


class TexImageDialog(sd.Dialog):
    def __init__(self, master, title, num, detailNum, decryptFile, detailMdlList):
        self.num = num
        self.detailNum = detailNum
        self.decryptFile = decryptFile
        self.txtImgList = detailMdlList[self.detailNum]["textureImgList"]
        self.dirtyFlag = False
        self.selectIndex = None
        self.selectValue = None
        super(TexImageDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.btnFrame = tkinter.Frame(master, pady=5)
        self.btnFrame.pack()
        self.listFrame = tkinter.Frame(master)
        self.listFrame.pack()

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.imageLb = tkinter.Label(self.listFrame, font=("", 14), text="イメージリスト")
        self.imageLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_imageList = tkinter.StringVar(value=self.txtImgList)
        self.imageListbox = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_imageList, width=30)
        self.imageListbox.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.imageListbox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, self.imageListbox.curselection()))

    def buttonActive(self, event, value):
        if len(value) > 0:
            self.selectIndex = value[0]
            self.selectValue = self.imageListbox.get(value[0])
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        else:
            self.selectValue = None
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        self.insertBtn["state"] = "normal"

    def modify(self):
        result = sd.askstring(title="変更", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            self.dirtyFlag = True
            self.imageListbox.delete(self.selectIndex)
            self.imageListbox.insert(self.selectIndex, result)

    def insert(self):
        result = sd.askstring(title="挿入", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            self.dirtyFlag = True
            self.imageListbox.insert(tkinter.END, result)

    def delete(self):
        warnMsg = "{0}番目を削除します。\nそれでもよろしいですか？".format(self.selectIndex + 1)
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

        if result:
            self.dirtyFlag = True
            self.imageListbox.delete(self.selectIndex)
            self.imageListbox.select_set(tkinter.END)

    def validate(self):
        if not self.dirtyFlag:
            return True

        warnMsg = "イメージ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)

        if result:
            imgList = []
            for i in range(self.imageListbox.size()):
                imgList.append(self.imageListbox.get(i))
            if not self.decryptFile.updateTexImage(self.num, self.detailNum, imgList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title="成功", message="イメージ情報を修正しました")


class DetailDialog(sd.Dialog):
    def __init__(self, master, title, mode, num, detailNum, decryptFile, colTuple, detailMdlList):
        self.mode = mode
        self.num = num
        self.detailNum = detailNum
        self.decryptFile = decryptFile
        self.colTuple = colTuple[2:]
        self.textureList = detailMdlList[self.detailNum]["textureList"]
        self.cancelFlag = False
        self.detailMdlList = detailMdlList
        super(DetailDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        index = 0
        self.varList = []
        self.fontSize = 12
        self.entryWidth = 20
        for colName in self.colTuple:
            if colName == "mesh":
                self.eleLb = ttk.Label(master, font=("", self.fontSize), text="Mesh No")
                self.eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.v_ele = tkinter.IntVar()
                self.v_ele.set(self.textureList[index])
                self.eleEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_ele, width=self.entryWidth)
                self.eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varList.append(self.v_ele)
                index += 1

                self.eleLb = ttk.Label(master, font=("", self.fontSize), text="Mtrl No")
                self.eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.v_ele = tkinter.IntVar()
                self.v_ele.set(self.textureList[index])
                self.eleEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_ele, width=self.entryWidth)
                self.eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varList.append(self.v_ele)
                index += 1
            elif colName == "ele1-3":
                for i in range(3):
                    self.eleLb = ttk.Label(master, font=("", self.fontSize), text="ele{0}".format(i + 1))
                    self.eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.v_ele = tkinter.IntVar()
                    self.v_ele.set(self.textureList[index])
                    self.eleEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_ele, width=self.entryWidth)
                    self.eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varList.append(self.v_ele)
                    index += 1
            elif colName == "f1-4":
                for i in range(4):
                    self.eleLb = ttk.Label(master, font=("", self.fontSize), text="f{0}".format(i + 1))
                    self.eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.v_ele = tkinter.DoubleVar()
                    self.v_ele.set(self.textureList[index])
                    self.eleEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_ele, width=self.entryWidth)
                    self.eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varList.append(self.v_ele)
                    index += 1
            elif colName == "f5-7":
                for i in range(3):
                    self.eleLb = ttk.Label(master, font=("", self.fontSize), text="f{0}".format(i + 5))
                    self.eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.v_ele = tkinter.DoubleVar()
                    self.v_ele.set(self.textureList[index])
                    self.eleEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_ele, width=self.entryWidth)
                    self.eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varList.append(self.v_ele)
                    index += 1
            else:
                self.eleLb = ttk.Label(master, font=("", self.fontSize), text=colName)
                self.eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.v_ele = tkinter.IntVar()
                self.v_ele.set(self.textureList[index])
                self.eleEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_ele, width=self.entryWidth)
                self.eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varList.append(self.v_ele)
                index += 1

    def validate(self):
        textureList = [x["textureList"][0:2] for x in self.detailMdlList]
        newMeshList = [self.varList[0].get(), self.varList[1].get()]
        oldMeshList = [self.textureList[0], self.textureList[1]]
        if self.mode == "edit":
            warnMsg = ""
            if newMeshList != oldMeshList and newMeshList in textureList:
                warnMsg = "【注意！】重複する要素({0}-{1})があります\n".format(newMeshList[0], newMeshList[1])
            warnMsg += "モデル要素情報を修正しますか？"
        elif self.mode == "insert":
            warnMsg = ""
            if newMeshList in textureList:
                warnMsg = "【注意！】重複する要素({0}-{1})があります\n".format(newMeshList[0], newMeshList[1])
            warnMsg += "モデル要素情報を挿入しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)

        if result:
            varList = []
            for var in self.varList:
                varList.append(var.get())

            if not self.decryptFile.updateTex(self.num, self.detailNum, varList, self.mode):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            return True

    def apply(self):
        self.cancelFlag = True
        mb.showinfo(title="成功", message="モデル要素情報を修正しました")


class ImageDialog(sd.Dialog):
    def __init__(self, master, title, num, decryptFile):
        self.num = num
        self.decryptFile = decryptFile
        self.imgList = decryptFile.allInfoList[self.num]["imgList"]
        self.dirtyFlag = False
        self.selectIndex = None
        self.selectValue = None
        super(ImageDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.btnFrame = tkinter.Frame(master, pady=5)
        self.btnFrame.pack()
        self.listFrame = tkinter.Frame(master)
        self.listFrame.pack()

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.imageLb = tkinter.Label(self.listFrame, font=("", 14), text="イメージリスト")
        self.imageLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_imageList = tkinter.StringVar(value=self.imgList)
        self.imageListbox = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_imageList, width=30)
        self.imageListbox.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.imageListbox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, self.imageListbox.curselection()))

    def buttonActive(self, event, value):
        if len(value) > 0:
            self.selectIndex = value[0]
            self.selectValue = self.imageListbox.get(value[0])
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        else:
            self.selectValue = None
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        self.insertBtn["state"] = "normal"

    def modify(self):
        result = sd.askstring(title="変更", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            self.dirtyFlag = True
            self.imageListbox.delete(self.selectIndex)
            self.imageListbox.insert(self.selectIndex, result)

    def insert(self):
        result = sd.askstring(title="挿入", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            self.dirtyFlag = True
            self.imageListbox.insert(tkinter.END, result)

    def delete(self):
        warnMsg = "{0}番目を削除します。\nそれでもよろしいですか？".format(self.selectIndex + 1)
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

        if result:
            self.dirtyFlag = True
            self.imageListbox.delete(self.selectIndex)
            self.imageListbox.select_set(tkinter.END)

    def validate(self):
        if not self.dirtyFlag:
            return True

        warnMsg = "イメージ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)

        if result:
            imgList = []
            for i in range(self.imageListbox.size()):
                imgList.append(self.imageListbox.get(i))
            if not self.decryptFile.updateImage(self.num, imgList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title="成功", message="イメージ情報を修正しました")


class SmfDetailDialog(sd.Dialog):
    def __init__(self, master, title, num, decryptFile):
        self.num = num
        self.master = master
        self.selectIndex = None
        self.selectItem = None
        self.maxSize = 0
        self.decryptFile = decryptFile
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.smfDetailList = decryptFile.allInfoList[self.num]["smfDetailList"]
        super(SmfDetailDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        mainFrame = ttk.Frame(master, width=720, height=360)
        mainFrame.pack()

        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        fileNameEt = ttk.Entry(mainFrame, textvariable=self.v_smfName, font=("", 14), width=20, state="readonly", justify="center")
        fileNameEt.place(relx=0.02, rely=0.03)

        self.mdlInfoLf = tkinter.LabelFrame(mainFrame, text="smf要素情報")
        self.mdlInfoLf.place(relx=0.02, rely=0.14, relwidth=0.96, relheight=0.80)

        self.frame = ttk.Frame(self.mdlInfoLf)
        self.frame.pack(expand=True, fill=tkinter.BOTH)

        self.tree = ttk.Treeview(self.frame, selectmode="browse")

        self.scrollbar_x = ttk.Scrollbar(self.frame, orient=tkinter.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=lambda first, last: self.scrollbar_x.set(first, last))
        self.scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.scrollbar_y = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=lambda first, last: self.scrollbar_y.set(first, last))
        self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.tree.pack(expand=True, fill=tkinter.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.treeSelect)

        self.colTuple = [
            "番号", "名称",
            "param1", "param2", "param3",
            "param4", "param5", "param6"
        ]

        self.tree['columns'] = self.colTuple
        self.tree.column('#0', width=0, stretch=False)

        for colName in self.colTuple:
            widthLen = 50
            if colName == "名称":
                widthLen = 80
            self.tree.column(colName, anchor=tkinter.CENTER, width=widthLen)
            self.tree.heading(colName, text=colName, anchor=tkinter.CENTER)

        self.tree["displaycolumns"] = self.colTuple

        self.viewData(self.smfDetailList)

        self.modifyBtn = ttk.Button(mainFrame, text="smf要素を\n修正する", width=16, state="disabled", command=self.modify)
        self.modifyBtn.place(relx=0.34, rely=0.03)

        self.insertBtn = ttk.Button(mainFrame, text="smf要素を\n挿入する", width=16, state="normal", command=self.insert)
        self.insertBtn.place(relx=0.57, rely=0.03)

        self.deleteBtn = ttk.Button(mainFrame, text="smf要素を\n削除する", width=16, state="disabled", command=self.delete)
        self.deleteBtn.place(relx=0.8, rely=0.03)

    def treeSelect(self, event):
        selectId = self.tree.selection()[0]
        self.selectItem = self.tree.set(selectId)
        self.selectIndex = int(self.selectItem["番号"]) - 1

        self.modifyBtn['state'] = 'normal'
        self.deleteBtn['state'] = 'normal'

    def viewData(self, smfDetailList):
        index = 0
        self.maxSize = 0
        for smfDetailInfo in smfDetailList:
            data = (index + 1,)
            for smfDetail in smfDetailInfo["smfDetail"]:
                data += (smfDetail,)
            self.tree.insert(parent='', index='end', iid=index, values=data)
            index += 1
            self.maxSize += 1

    def reload(self):
        self.decryptFile = self.decryptFile.reload()
        self.smfDetailList = self.decryptFile.allInfoList[self.num]["smfDetailList"]

        for i in self.tree.get_children():
            self.tree.delete(i)
        self.viewData(self.smfDetailList)

    def modify(self):
        valueList = []
        for colName in self.colTuple:
            valueList.append(self.selectItem[colName])
        result = SmfDetailEditDialog(self.master, "smf要素改造", self.num, self.selectIndex, self.maxSize, self.decryptFile, self.colTuple, valueList)
        if result.dirtyFlag:
            self.reload()
            if self.selectIndex is not None and self.selectIndex >= 0:
                self.tree.selection_set(self.selectIndex)

    def insert(self):
        result = SmfDetailEditDialog(self.master, "smf要素改造", self.num, self.selectIndex, self.maxSize, self.decryptFile, self.colTuple, None)
        if result.dirtyFlag:
            self.reload()
            if self.selectIndex is not None and self.selectIndex >= 0:
                self.tree.selection_set(self.selectIndex)

    def delete(self):
        warnMsg = "{0}番目を削除します。\nそれでもよろしいですか？".format(self.selectIndex + 1)
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

        if result:
            if not self.decryptFile.updateSmfDetail(self.num, self.selectIndex, 0, None):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            mb.showinfo(title="成功", message="smf要素情報を修正しました")
            self.reload()
            if self.selectIndex is not None:
                if self.selectIndex >= len(self.smfDetailList):
                    self.selectIndex = len(self.smfDetailList) - 1

                if self.selectIndex >= 0:
                    self.tree.selection_set(self.selectIndex)


class SmfDetailEditDialog(sd.Dialog):
    def __init__(self, master, title, smfNum, num, maxSize, decryptFile, colTuple, valueList):
        self.smfNum = smfNum
        self.smfDetailNum = num
        self.maxSize = maxSize
        self.decryptFile = decryptFile
        self.colTuple = colTuple[1:]
        self.dirtyFlag = False
        self.valueList = None

        if valueList is not None:
            self.valueList = valueList[1:]
        super(SmfDetailEditDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.varList = []
        self.fontSize = 12
        self.entryWidth = 20

        index = 0
        if self.valueList is None:
            self.position = ttk.Label(master, font=("", self.fontSize), text="挿入する位置")
            self.position.grid(row=index, column=0, sticky=tkinter.N + tkinter.S)
            if self.smfDetailNum is not None:
                positionList = ["{0}番の後".format(self.smfDetailNum + 1), "{0}番の前".format(self.smfDetailNum + 1)]
            else:
                positionList = ["最終番の後"]
            self.v_position = tkinter.StringVar()
            self.positionCb = ttk.Combobox(master, textvariable=self.v_position, width=self.entryWidth, state="readonly", value=positionList)
            self.positionCb.grid(row=index, column=1, sticky=tkinter.N + tkinter.S, pady=10)
            self.v_position.set(positionList[0])
            index += 1

            self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
            self.xLine.grid(columnspan=2, row=index, column=0, sticky=tkinter.W + tkinter.E, pady=10)
            index += 1

        valueIndex = 0
        for colName in self.colTuple:
            self.v_ele = None
            self.eleLb = ttk.Label(master, font=("", self.fontSize), text=colName)
            self.eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
            if colName == "名称":
                self.v_ele = tkinter.StringVar()
            else:
                self.v_ele = tkinter.DoubleVar()
            self.eleEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_ele, width=self.entryWidth)
            self.eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
            self.varList.append(self.v_ele)

            if self.valueList is not None:
                self.v_ele.set(self.valueList[valueIndex])
                valueIndex += 1
            index += 1

    def validate(self):
        warnMsg = "smf要素情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)

        if result:
            pos = 0
            num = 0
            if self.valueList is None:
                posList = self.v_position.get().split("番の")
                if posList[0] == "最終":
                    num = self.maxSize - 1
                else:
                    num = int(posList[0]) - 1

                if posList[1] == "後":
                    pos += 1
                elif posList[1] == "前":
                    pos -= 1
            else:
                num = self.smfDetailNum

            valueList = []
            for var in self.varList:
                valueList.append(var.get())

            if not self.decryptFile.updateSmfDetail(self.smfNum, num, pos, valueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            return True

    def apply(self):
        self.dirtyFlag = True
        mb.showinfo(title="成功", message="smf要素情報を修正しました")


class BinFileOrFlagEditDialog(sd.Dialog):
    def __init__(self, master, title, num, decryptFile):
        self.smfNum = num
        self.decryptFile = decryptFile
        self.smfName = decryptFile.allInfoList[self.smfNum]["smfName"]
        self.binFile = decryptFile.allInfoList[self.smfNum]["binInfo"][0]
        self.flag = decryptFile.allInfoList[self.smfNum]["binInfo"][1]
        self.dirtyFlag = False
        super(BinFileOrFlagEditDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.fontSize = 12
        self.entryWidth = 20
        self.smfNameLb = ttk.Label(master, text="smf名")
        self.smfNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        self.smfNameEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_smfName, width=self.entryWidth)
        self.smfNameEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        self.binFileLb = ttk.Label(master, text="binファイル")
        self.binFileLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_binFile = tkinter.StringVar()
        self.v_binFile.set(self.binFile)
        self.binFileEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_binFile, width=self.entryWidth)
        self.binFileEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)

        self.flagLb = ttk.Label(master, text="フラグ")
        self.flagLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
        self.v_flag = tkinter.IntVar()
        self.v_flag.set(self.flag)
        self.flagEt = ttk.Entry(master, font=("", self.fontSize), textvariable=self.v_flag, width=self.entryWidth)
        self.flagEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        warnMsg = "binファイル、フラグ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)

        if result:
            varList = []
            if not self.v_smfName.get():
                mb.showerror(title="エラー", message="smf名が空文字です")
                return False
            varList.append(self.v_smfName.get())
            varList.append(self.v_binFile.get())
            varList.append(self.v_flag.get())

            if not self.decryptFile.updateBinFileOrFlag(self.smfNum, varList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            return True

    def apply(self):
        self.dirtyFlag = True
        mb.showinfo(title="成功", message="binファイル、フラグ情報を修正しました")


class CopyMdlDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile):
        self.decryptFile = decryptFile
        self.smfName = []
        self.cbSmfName = []

        index = 1
        for allInfo in decryptFile.allInfoList:
            self.smfName.append(allInfo["smfName"])
            self.cbSmfName.append("({0}){1}".format(index, allInfo["smfName"]))
            index += 1
        self.dirtyFlag = False
        self.copyByteArr = None
        super(CopyMdlDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        msg = "コピーする要素を選んでください。\nコピーした要素は最終番に追加されます"
        self.lb = ttk.Label(master, text=msg, font=("", 12))
        self.lb.pack()

        self.v_cb = tkinter.StringVar()
        self.cb = ttk.Combobox(master, textvariable=self.v_cb, font=("", 12), width=30, state="readonly", value=self.cbSmfName)
        self.v_cb.set(self.cbSmfName[0])
        self.cb.pack()

    def validate(self):
        idx = self.cb.current()
        warnMsg = "{0}をコピーしますか？".format(self.smfName[idx])
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)

        if result:
            self.copyByteArr = bytearray()
            index = self.decryptFile.allInfoList[idx]["smfIndex"]
            if idx + 1 >= len(self.decryptFile.allInfoList):
                self.copyByteArr = self.decryptFile.byteArr[index:]
            else:
                lastIndex = self.decryptFile.allInfoList[idx + 1]["smfIndex"]
                self.copyByteArr = self.decryptFile.byteArr[index:lastIndex]

            return True

    def apply(self):
        self.dirtyFlag = True


class PasteDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, copyInfoByteArr):
        self.decryptFile = decryptFile
        self.num = num
        self.copyInfoByteArr = copyInfoByteArr
        self.reloadFlag = False
        super(PasteDialog, self).__init__(parent=master, title=title)

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
        if not self.decryptFile.copySaveFile(self.num - 1, self.copyInfoByteArr):
            self.decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        self.ok()
        mb.showinfo(title="成功", message="貼り付けしました")
        self.reloadFlag = True

    def backInsert(self):
        if not self.decryptFile.copySaveFile(self.num, self.copyInfoByteArr):
            self.decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        self.ok()
        mb.showinfo(title="成功", message="貼り付けしました")
        self.reloadFlag = True
