import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog

from program.mdlinfo.importPy.tkinterScrollbarTreeviewMdlinfo import ScrollbarTreeviewMdlinfo


class SmfDetailDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.master = master
        self.num = num
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.selectId = None
        self.dirtyFlag = False
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.smfDetailList = decryptFile.allInfoList[self.num]["smfDetailList"]
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        mainFrame = ttkCustomWidget.CustomTtkFrame(master, width=840, height=360)
        mainFrame.pack()

        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        fileNameEt = ttkCustomWidget.CustomTtkEntry(mainFrame, textvariable=self.v_smfName, font=textSetting.textList["font2"], width=20, state="readonly", justify="center")
        fileNameEt.place(relx=0.04, rely=0.03)

        selectLb = ttkCustomWidget.CustomTtkLabel(mainFrame, text=textSetting.textList["mdlinfo"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.place(relx=0.03, rely=0.13)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(mainFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
        selectEt.place(relx=0.21, rely=0.13)

        mdlInfoLf = ttkCustomWidget.CustomTtkLabelFrame(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfo"])
        mdlInfoLf.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.74)

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfoModify"], width=25, state="disabled", command=self.modify)
        self.modifyBtn.place(relx=0.33, rely=0.03)

        self.insertBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfoInsert"], width=25, state="disabled", command=self.insert)
        self.insertBtn.place(relx=0.555, rely=0.03)

        self.deleteBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfoDelete"], width=25, state="disabled", command=self.delete)
        self.deleteBtn.place(relx=0.78, rely=0.03)

        btnList = [
            self.modifyBtn,
            self.insertBtn,
            self.deleteBtn
        ]

        self.frame = ScrollbarTreeviewMdlinfo(mdlInfoLf, self.v_select, btnList)

        colIdTuple = [
            "treeNum",
            "smfName",
            "smfParam1",
            "smfParam2",
            "smfParam3",
            "smfParam4",
            "smfParam5",
            "smfParam6",
        ]

        colTuple = [
            textSetting.textList["mdlinfo"]["treeNum"],
            textSetting.textList["mdlinfo"]["smfName"],
            textSetting.textList["mdlinfo"]["smfParam"] + "1",
            textSetting.textList["mdlinfo"]["smfParam"] + "2",
            textSetting.textList["mdlinfo"]["smfParam"] + "3",
            textSetting.textList["mdlinfo"]["smfParam"] + "4",
            textSetting.textList["mdlinfo"]["smfParam"] + "5",
            textSetting.textList["mdlinfo"]["smfParam"] + "6",
        ]

        self.frame.tree["columns"] = colIdTuple
        self.frame.tree.column("#0", width=0, stretch=False)

        for index, colIdName in enumerate(colIdTuple):
            widthLen = 50
            if colIdName == "smfName":
                widthLen = 80
            self.frame.tree.column(colIdName, anchor=tkinter.CENTER, width=widthLen)
            self.frame.tree.heading(colIdName, text=colTuple[index], anchor=tkinter.CENTER)

        self.frame.tree["displaycolumns"] = colIdTuple
        self.viewData(self.smfDetailList)
        super().body(master)

    def viewData(self, smfDetailList):
        for index, smfDetailInfo in enumerate(smfDetailList):
            data = (index + 1,)
            for smfDetail in smfDetailInfo["smfDetail"]:
                data += (smfDetail,)
            self.frame.tree.insert(parent="", index="end", iid=index, values=data)
        if len(smfDetailList) == 0:
            self.insertBtn["state"] = "normal"

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.smfDetailList):
                self.selectId = len(self.smfDetailList) - 1
            self.frame.tree.selection_set(self.selectId)
            self.frame.tree.see(self.selectId)

    def reloadWidget(self):
        self.dirtyFlag = True
        self.decryptFile = self.decryptFile.reload()
        self.smfDetailList = self.decryptFile.allInfoList[self.num]["smfDetailList"]

        for i in self.frame.tree.get_children():
            self.frame.tree.delete(i)
        self.viewData(self.smfDetailList)
        self.jumpToSelect()

    def modify(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1

        result = EditSmfDetailDialog(self.master, textSetting.textList["mdlinfo"]["smfElementModify"], "modify", detailNum, self.smfDetailList[detailNum], self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.updateSmfDetail(self.num, detailNum, result.resultValueList, "modify"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])
            self.selectId = detailNum
            self.dirtyFlag = True
            self.reloadWidget()

    def insert(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1

        result = EditSmfDetailDialog(self.master, textSetting.textList["mdlinfo"]["smfElementInsert"], "insert", detailNum, self.smfDetailList[detailNum], self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.updateSmfDetail(self.num, detailNum + result.insertPos, result.resultValueList, "insert"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])
            self.selectId = detailNum + result.insertPos
            self.dirtyFlag = True
            self.reloadWidget()

    def delete(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1

        warnMsg = textSetting.textList["infoList"]["I25"].format(detailNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)
        if result:
            if not self.decryptFile.updateSmfDetail(self.num, detailNum, None, "delete"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])
            self.selectId = detailNum
            self.dirtyFlag = True
            self.reloadWidget()


class EditSmfDetailDialog(CustomSimpleDialog):
    def __init__(self, master, title, mode, detailNum, smfDetailInfo, rootFrameAppearance):
        self.mode = mode
        self.detailNum = detailNum
        self.smfDetailInfo = smfDetailInfo["smfDetail"]
        self.reloadFlag = False
        self.insertPos = None
        self.resultValueList = []
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        headerLabelList = [
            textSetting.textList["mdlinfo"]["smfName"],
            textSetting.textList["mdlinfo"]["smfParam"] + "1",
            textSetting.textList["mdlinfo"]["smfParam"] + "2",
            textSetting.textList["mdlinfo"]["smfParam"] + "3",
            textSetting.textList["mdlinfo"]["smfParam"] + "4",
            textSetting.textList["mdlinfo"]["smfParam"] + "5",
            textSetting.textList["mdlinfo"]["smfParam"] + "6",
        ]
        self.varList = []
        self.varCnt = 0
        self.entryWidth = 20

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        inputFrame = ttkCustomWidget.CustomTtkFrame(master)
        inputFrame.grid(columnspan=2, row=1, column=0, sticky=tkinter.NSEW)

        for i, headerLabel in enumerate(headerLabelList):
            eleLb = ttkCustomWidget.CustomTtkLabel(inputFrame, font=textSetting.textList["font2"], text=headerLabel)
            eleLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i == 0:
                self.varList.append(tkinter.StringVar())
            else:
                self.varList.append(tkinter.IntVar())
            eleEt = ttkCustomWidget.CustomTtkEntry(inputFrame, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
            eleEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

            if self.mode == "modify":
                self.varList[self.varCnt].set(self.smfDetailInfo[i])
            self.varCnt += 1
        
        if self.mode == "insert":
            self.setInsertWidget(inputFrame, 7)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["orgInfoEditor"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I34"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            self.resultValueList = []
            if not self.varList[0].get():
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E138"])
                return False

            for var in self.varList:
                self.resultValueList.append(var.get())

            if self.mode == "insert":
                self.insertPos = 1
                if self.insertCb.current() == 1:
                    self.insertPos = 0
            return True

    def apply(self):
        self.reloadFlag = True
