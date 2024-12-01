import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog, CustomAskstring

from program.mdlinfo.importPy.tkinterScrollbarTreeviewMdlinfo import ScrollbarTreeviewMdlinfo


class TreeViewDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.num = num
        self.master = master
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.detailMdlList = decryptFile.allInfoList[self.num]["detailMdlList"]
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        mainFrame = ttkCustomWidget.CustomTtkFrame(master, width=800, height=360)
        mainFrame.pack()

        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        fileNameEt = ttkCustomWidget.CustomTtkEntry(mainFrame, textvariable=self.v_smfName, font=textSetting.textList["font2"], width=20, state="readonly", justify="center")
        fileNameEt.place(relx=0.04, rely=0.03)

        mdlInfoLf = ttkCustomWidget.CustomTtkLabelFrame(mainFrame, text=textSetting.textList["mdlinfo"]["mdlinfoLf"])
        mdlInfoLf.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.74)

        self.editColorBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["editColorLabel"], width=25, state="disabled", command=self.editColor)
        self.editColorBtn.place(relx=0.42, rely=0.03)

        self.editElementBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["elementModifyLabel"], width=25, state="disabled", command=self.editElement)
        self.editElementBtn.place(relx=0.1, rely=0.13)

        self.insertElementBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["elementInsertLabel"], width=25, state="disabled", command=self.insertElement)
        self.insertElementBtn.place(relx=0.42, rely=0.13)

        self.deleteElementBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["elementDeleteLabel"], width=25, state="disabled", command=self.deleteElement)
        self.deleteElementBtn.place(relx=0.74, rely=0.13)

        self.frame = ScrollbarTreeviewMdlinfo(mdlInfoLf, None, [])

        self.colIdTuple = [
            "treeNum",
            "treeColorNum",
            "treeMesh",
            "treeConst1",
            "treeEle1-3",
            "treeDiff",
            "treeConst0",
            "treeEmis",
            "treeNum2_1",
            "treeNum2_2",
        ]

        self.colTuple = [
            textSetting.textList["mdlinfo"]["treeNum"],
            textSetting.textList["mdlinfo"]["treeColorNum"],
            textSetting.textList["mdlinfo"]["treeMesh"],
            textSetting.textList["mdlinfo"]["treeConst"] + "1",
            textSetting.textList["mdlinfo"]["treeEle1-3"],
            textSetting.textList["mdlinfo"]["treeDiff"],
            textSetting.textList["mdlinfo"]["treeConst"] + "0",
            textSetting.textList["mdlinfo"]["treeEmis"],
            textSetting.textList["mdlinfo"]["treeNum2"] + "1",
            textSetting.textList["mdlinfo"]["treeNum2"] + "2",
        ]

        self.frame.tree["columns"] = self.colIdTuple
        self.frame.tree.column("#0", width=0, stretch=False)

        for index, colIdName in enumerate(self.colIdTuple):
            widthLen = 50
            if colIdName == "treeEle1-3":
                widthLen = 80
            elif colIdName == "treeDiff":
                widthLen = 150
            elif colIdName == "treeEmis":
                widthLen = 150
            self.frame.tree.column(colIdName, anchor=tkinter.CENTER, width=widthLen)
            self.frame.tree.heading(colIdName, text=self.colTuple[index], anchor=tkinter.CENTER)

        self.frame.tree["displaycolumns"] = self.colIdTuple
        self.viewData(self.detailMdlList)
        self.frame.tree.bind("<<TreeviewSelect>>", self.treeSelect)
        super().body(master)

    def viewData(self, detailMdlList):
        index = 0
        for detailMdlInfo in detailMdlList:
            for i in range(len(self.colIdTuple)):
                data = (index + 1, detailMdlInfo["colorCnt"])
                data += (",".join(str(n) for n in detailMdlInfo["materialList"][0:2]),)
                data += (detailMdlInfo["materialList"][2],)
                data += (",".join(str(n) for n in detailMdlInfo["materialList"][3:6]),)
                data += (",".join(str(n) for n in detailMdlInfo["materialList"][6:10]),)
                data += (detailMdlInfo["materialList"][10],)
                data += (",".join(str(n) for n in detailMdlInfo["materialList"][11:14]),)
                data += (detailMdlInfo["materialList"][14],)
                data += (detailMdlInfo["materialList"][15],)
            self.frame.tree.insert(parent="", index="end", iid=index, values=data)
            index += 1

    def treeSelect(self, event):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        self.editColorBtn["state"] = "normal"
        self.editElementBtn["state"] = "normal"
        self.insertElementBtn["state"] = "normal"
        self.deleteElementBtn["state"] = "normal"

    def reload(self):
        self.decryptFile = self.decryptFile.reload()
        self.detailMdlList = self.decryptFile.allInfoList[self.num]["detailMdlList"]

        for i in self.frame.tree.get_children():
            self.frame.tree.delete(i)
        self.viewData(self.detailMdlList)

    def editColor(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1
        result = TexImageDialog(self.master, textSetting.textList["mdlinfo"]["texImageLabel"], self.num, detailNum, self.decryptFile, self.detailMdlList, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.reload()
            self.frame.tree.selection_set(selectId)

    def editElement(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1
        result = DetailDialog(self.master, textSetting.textList["mdlinfo"]["detailModelLabel"], "edit", self.num, detailNum, self.decryptFile, self.colIdTuple, self.colTuple, self.detailMdlList, self.rootFrameAppearance)
        if result.cancelFlag:
            self.reload()
            self.frame.tree.selection_set(selectId)

    def insertElement(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1
        result = DetailDialog(self.master, textSetting.textList["mdlinfo"]["detailModelLabel"], "insert", self.num, detailNum, self.decryptFile, self.colIdTuple, self.colTuple, self.detailMdlList, self.rootFrameAppearance)
        if result.cancelFlag:
            self.reload()
            self.frame.tree.selection_set(selectId)

    def deleteElement(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1
        warnMsg = textSetting.textList["infoList"]["I25"].format(detailNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

        if result:
            if not self.decryptFile.updateTex(self.num, detailNum, [], "delete"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            selectId -= 1
            if selectId < 0:
                selectId = 0
            self.reload()
            self.frame.tree.selection_set(selectId)


class TexImageDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, detailNum, decryptFile, detailMdlList, rootFrameAppearance):
        self.master = master
        self.num = num
        self.detailNum = detailNum
        self.decryptFile = decryptFile
        self.txtImgList = detailMdlList[self.detailNum]["textureImgList"]
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False
        self.selectIndex = None
        self.selectValue = None
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        btnFrame = ttkCustomWidget.CustomTtkFrame(master)
        btnFrame.pack(pady=5)
        listFrame = ttkCustomWidget.CustomTtkFrame(master)
        listFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        imageLb = ttkCustomWidget.CustomTtkLabel(listFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["imageListLabel"])
        imageLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_imageList = tkinter.StringVar(value=self.txtImgList)
        self.imageListbox = tkinter.Listbox(listFrame, font=textSetting.textList["font2"], listvariable=self.v_imageList, width=30, height=6, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        self.imageListbox.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.imageListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, self.imageListbox.curselection()))
        super().body(master)

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
        resultObj = CustomAskstring(self.master, title=textSetting.textList["modify"], prompt=textSetting.textList["infoList"]["I27"], initialvalue=self.selectValue, bgColor=self.rootFrameAppearance.bgColor)
        result = resultObj.result

        if result:
            self.dirtyFlag = True
            self.imageListbox.delete(self.selectIndex)
            self.imageListbox.insert(self.selectIndex, result)

            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        resultObj = CustomAskstring(self.master, title=textSetting.textList["insert"], prompt=textSetting.textList["infoList"]["I27"], initialvalue=self.selectValue, bgColor=self.rootFrameAppearance.bgColor)
        result = resultObj.result

        if result:
            self.dirtyFlag = True
            self.imageListbox.insert(tkinter.END, result)

            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        warnMsg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

        if result:
            self.dirtyFlag = True
            self.imageListbox.delete(self.selectIndex)

            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def validate(self):
        if not self.dirtyFlag:
            return True

        warnMsg = textSetting.textList["infoList"]["I28"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            imgList = []
            for i in range(self.imageListbox.size()):
                imgList.append(self.imageListbox.get(i))
            if not self.decryptFile.updateTexImage(self.num, self.detailNum, imgList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I29"])


class DetailDialog(CustomSimpleDialog):
    def __init__(self, master, title, mode, num, detailNum, decryptFile, colIdTuple, colTuple, detailMdlList, rootFrameAppearance):
        self.mode = mode
        self.num = num
        self.detailNum = detailNum
        self.decryptFile = decryptFile
        self.colIdTuple = colIdTuple[2:]
        self.colTuple = colTuple[2:]
        self.materialList = detailMdlList[self.detailNum]["materialList"]
        self.cancelFlag = False
        self.detailMdlList = detailMdlList
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        index = 0
        self.varList = []
        self.varCnt = 0
        self.entryWidth = 20
        for idx, colIdName in enumerate(self.colIdTuple):
            if colIdName == "treeMesh":
                eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["detailModelMeshLabel"])
                eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.IntVar(value=self.materialList[index]))
                eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
                index += 1

                eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["detailModelMtrlLabel"])
                eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.IntVar(value=self.materialList[index]))
                eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
                index += 1
            elif colIdName == "treeEle1-3":
                for i in range(3):
                    eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["detailModelEleNum"].format(i + 1))
                    eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.varList.append(tkinter.IntVar(value=self.materialList[index]))
                    eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                    eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varCnt += 1
                    index += 1
            elif colIdName == "treeDiff":
                colorLabelList = ["DIFF_R", "DIFF_G", "DIFF_B", "DIFF_A"]
                for i in range(4):
                    eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=colorLabelList[i])
                    eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.varList.append(tkinter.DoubleVar(value=self.materialList[index]))
                    eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                    eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varCnt += 1
                    index += 1
            elif colIdName == "treeEmis":
                colorLabelList = ["EMIS_R", "EMIS_G", "EMIS_B"]
                for i in range(3):
                    eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=colorLabelList[i])
                    eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.varList.append(tkinter.DoubleVar(value=self.materialList[index]))
                    eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                    eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varCnt += 1
                    index += 1
            else:
                eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=self.colTuple[idx])
                eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.IntVar(value=self.materialList[index]))
                eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
                index += 1
        super().body(master)

    def validate(self):
        materialList = [x["materialList"][0:2] for x in self.detailMdlList]
        newMeshList = [self.varList[0].get(), self.varList[1].get()]
        oldMeshList = [self.materialList[0], self.materialList[1]]
        if self.mode == "edit":
            warnMsg = ""
            if newMeshList != oldMeshList and newMeshList in materialList:
                warnMsg = textSetting.textList["infoList"]["I30"].format(newMeshList[0], newMeshList[1])
            warnMsg += textSetting.textList["infoList"]["I31"]
        elif self.mode == "insert":
            warnMsg = ""
            if newMeshList in materialList:
                warnMsg = textSetting.textList["infoList"]["I30"].format(newMeshList[0], newMeshList[1])
            warnMsg += textSetting.textList["infoList"]["I32"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            varList = []
            for var in self.varList:
                varList.append(var.get())

            if not self.decryptFile.updateTex(self.num, self.detailNum, varList, self.mode):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        self.cancelFlag = True
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])


class SmfTypeDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.master = master
        self.num = num
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.smfType = decryptFile.allInfoList[self.num]["smfType"]
        self.dirtyFlag = False
        self.selectIndex = None
        self.selectValue = None
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.entryWidth = 20
        smfTypeLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["smfTypeLabel"], font=textSetting.textList["font2"])
        smfTypeLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_smfType = tkinter.IntVar()
        self.v_smfType.set(self.smfType)
        smfTypeEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_smfType, width=self.entryWidth)
        smfTypeEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I119"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            if not self.decryptFile.updateType(self.num, self.v_smfType.get()):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        self.dirtyFlag = True
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I120"])


class SmfDetailDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.num = num
        self.master = master
        self.selectIndex = None
        self.selectItem = None
        self.maxSize = 0
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.smfDetailList = decryptFile.allInfoList[self.num]["smfDetailList"]
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        mainFrame = ttkCustomWidget.CustomTtkFrame(master, width=720, height=360)
        mainFrame.pack()

        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        fileNameEt = ttkCustomWidget.CustomTtkEntry(mainFrame, textvariable=self.v_smfName, font=textSetting.textList["font2"], width=20, state="readonly", justify="center")
        fileNameEt.place(relx=0.02, rely=0.03)

        mdlInfoLf = ttkCustomWidget.CustomTtkLabelFrame(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfo"])
        mdlInfoLf.place(relx=0.02, rely=0.14, relwidth=0.96, relheight=0.80)

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfoModify"], width=16, state="disabled", command=self.modify)
        self.modifyBtn.place(relx=0.34, rely=0.03)

        self.insertBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfoInsert"], width=16, state="normal", command=self.insert)
        self.insertBtn.place(relx=0.57, rely=0.03)

        self.deleteBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["smfInfoDelete"], width=16, state="disabled", command=self.delete)
        self.deleteBtn.place(relx=0.8, rely=0.03)

        self.frame = ScrollbarTreeviewMdlinfo(mdlInfoLf, None, [])

        self.colIdTuple = [
            "treeNum",
            "smfName",
            "smfParam1",
            "smfParam2",
            "smfParam3",
            "smfParam4",
            "smfParam5",
            "smfParam6",
        ]

        self.colTuple = [
            textSetting.textList["mdlinfo"]["treeNum"],
            textSetting.textList["mdlinfo"]["smfName"],
            textSetting.textList["mdlinfo"]["smfParam"] + "1",
            textSetting.textList["mdlinfo"]["smfParam"] + "2",
            textSetting.textList["mdlinfo"]["smfParam"] + "3",
            textSetting.textList["mdlinfo"]["smfParam"] + "4",
            textSetting.textList["mdlinfo"]["smfParam"] + "5",
            textSetting.textList["mdlinfo"]["smfParam"] + "6",
        ]

        self.frame.tree["columns"] = self.colIdTuple
        self.frame.tree.column("#0", width=0, stretch=False)

        for index, colIdName in enumerate(self.colIdTuple):
            widthLen = 50
            if colIdName == "smfName":
                widthLen = 80
            self.frame.tree.column(colIdName, anchor=tkinter.CENTER, width=widthLen)
            self.frame.tree.heading(colIdName, text=self.colTuple[index], anchor=tkinter.CENTER)

        self.frame.tree["displaycolumns"] = self.colIdTuple
        self.viewData(self.smfDetailList)
        self.frame.tree.bind("<<TreeviewSelect>>", self.treeSelect)
        super().body(master)

    def treeSelect(self, event):
        if len(self.frame.tree.selection()) > 0:
            selectId = self.frame.tree.selection()[0]
            self.selectItem = self.frame.tree.set(selectId)
            self.selectIndex = int(self.selectItem["treeNum"]) - 1

            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"

    def viewData(self, smfDetailList):
        index = 0
        self.maxSize = 0
        for smfDetailInfo in smfDetailList:
            data = (index + 1,)
            for smfDetail in smfDetailInfo["smfDetail"]:
                data += (smfDetail,)
            self.frame.tree.insert(parent="", index="end", iid=index, values=data)
            index += 1
            self.maxSize += 1

    def reload(self):
        self.decryptFile = self.decryptFile.reload()
        self.smfDetailList = self.decryptFile.allInfoList[self.num]["smfDetailList"]

        for i in self.frame.tree.get_children():
            self.frame.tree.delete(i)
        self.viewData(self.smfDetailList)

    def modify(self):
        valueList = []
        for colIdName in self.colIdTuple:
            valueList.append(self.selectItem[colIdName])
        result = SmfDetailEditDialog(self.master, textSetting.textList["mdlinfo"]["smfElementModify"], self.num, self.selectIndex, self.maxSize, self.decryptFile, self.colIdTuple, self.colTuple, valueList, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.reload()
            if self.selectIndex is not None and self.selectIndex >= 0:
                self.frame.tree.selection_set(self.selectIndex)

    def insert(self):
        result = SmfDetailEditDialog(self.master, textSetting.textList["mdlinfo"]["smfElementInsert"], self.num, self.selectIndex, self.maxSize, self.decryptFile, self.colIdTuple, self.colTuple, None, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.reload()
            if self.selectIndex is not None and self.selectIndex >= 0:
                self.frame.tree.selection_set(self.selectIndex)

    def delete(self):
        warnMsg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

        if result:
            if not self.decryptFile.updateSmfDetail(self.num, self.selectIndex, 0, None):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])
            self.reload()
            if len(self.smfDetailList) > 0:
                if self.selectIndex is not None:
                    if self.selectIndex >= len(self.smfDetailList):
                        self.selectIndex = len(self.smfDetailList) - 1

                    if self.selectIndex >= 0:
                        self.frame.tree.selection_set(self.selectIndex)
            else:
                self.modifyBtn["state"] = "disabled"
                self.deleteBtn["state"] = "disabled"


class SmfDetailEditDialog(CustomSimpleDialog):
    def __init__(self, master, title, smfNum, num, maxSize, decryptFile, colIdTuple, colTuple, valueList, rootFrameAppearance):
        self.smfNum = smfNum
        self.smfDetailNum = num
        self.maxSize = maxSize
        self.decryptFile = decryptFile
        self.colIdTuple = colIdTuple[1:]
        self.colTuple = colTuple[1:]
        self.dirtyFlag = False
        self.valueList = None

        if valueList is not None:
            self.valueList = valueList[1:]
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        self.varList = []
        self.fontSize = 12
        self.entryWidth = 20

        index = 0
        if self.valueList is None:
            position = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["posLabel"])
            position.grid(row=index, column=0, sticky=tkinter.N + tkinter.S)
            if self.smfDetailNum is not None:
                positionList = [textSetting.textList["mdlinfo"]["pos1"].format(self.smfDetailNum + 1), textSetting.textList["mdlinfo"]["pos2"].format(self.smfDetailNum + 1)]
            else:
                positionList = [textSetting.textList["mdlinfo"]["pos3"]]
            self.v_position = tkinter.StringVar()
            positionCb = ttkCustomWidget.CustomTtkCombobox(master, font=textSetting.textList["font2"], textvariable=self.v_position, width=self.entryWidth, state="readonly", value=positionList)
            positionCb.grid(row=index, column=1, sticky=tkinter.N + tkinter.S, pady=10)
            self.v_position.set(positionList[0])
            index += 1

            xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
            xLine.grid(columnspan=2, row=index, column=0, sticky=tkinter.W + tkinter.E, pady=10)
            index += 1

        valueIndex = 0
        for idx, colIdName in enumerate(self.colIdTuple):
            v_ele = None
            eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=self.colTuple[idx])
            eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
            if colIdName == "smfName":
                v_ele = tkinter.StringVar()
            else:
                v_ele = tkinter.DoubleVar()
            self.varList.append(v_ele)
            eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[idx], width=self.entryWidth)
            eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)

            if self.valueList is not None:
                v_ele.set(self.valueList[valueIndex])
                valueIndex += 1
            index += 1
        super().body(master)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I34"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            pos = 0
            num = 0
            if self.valueList is None:
                posList = self.v_position.get().split(textSetting.textList["mdlinfo"]["posSplit"])
                if posList[0] == textSetting.textList["mdlinfo"]["posLast"]:
                    num = self.maxSize - 1
                else:
                    num = int(posList[0]) - 1

                if posList[1] == textSetting.textList["mdlinfo"]["pos4"]:
                    pos += 1
                elif posList[1] == textSetting.textList["mdlinfo"]["pos5"]:
                    pos -= 1
            else:
                num = self.smfDetailNum

            valueList = []
            for var in self.varList:
                valueList.append(var.get())

            if not self.decryptFile.updateSmfDetail(self.smfNum, num, pos, valueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        self.dirtyFlag = True
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])


class BinFileOrFlagEditDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.smfNum = num
        self.decryptFile = decryptFile
        self.smfName = decryptFile.allInfoList[self.smfNum]["smfName"]
        self.binFile = decryptFile.allInfoList[self.smfNum]["binInfo"][0]
        self.flag = decryptFile.allInfoList[self.smfNum]["binInfo"][1]
        self.dirtyFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.entryWidth = 20
        smfNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["smfNameLabel"], font=textSetting.textList["font2"])
        smfNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        smfNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_smfName, width=self.entryWidth)
        smfNameEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        binFileLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["binFileLabel"], font=textSetting.textList["font2"])
        binFileLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_binFile = tkinter.StringVar()
        self.v_binFile.set(self.binFile)
        binFileEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_binFile, width=self.entryWidth)
        binFileEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)

        flagLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["binFileFlag"], font=textSetting.textList["font2"])
        flagLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
        self.v_flag = tkinter.IntVar()
        self.v_flag.set(self.flag)
        flagEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_flag, width=self.entryWidth)
        flagEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I35"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            varList = []
            if not self.v_smfName.get():
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E17"])
                return False
            varList.append(self.v_smfName.get())
            varList.append(self.v_binFile.get())
            varList.append(self.v_flag.get())

            if not self.decryptFile.updateBinFileOrFlag(self.smfNum, varList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        self.dirtyFlag = True
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I36"])


class CopyMdlDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
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
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        msg = textSetting.textList["infoList"]["I37"]
        lb = ttkCustomWidget.CustomTtkLabel(master, text=msg, font=textSetting.textList["font2"])
        lb.pack()

        self.v_cb = tkinter.StringVar()
        self.v_cb.set(self.cbSmfName[0])
        self.cb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_cb, font=textSetting.textList["font2"], width=30, state="readonly", value=self.cbSmfName)
        self.cb.pack()
        super().body(master)

    def validate(self):
        idx = self.cb.current()
        warnMsg = textSetting.textList["infoList"]["I38"].format(self.smfName[idx])
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

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


class PasteDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, num, copyInfoByteArr, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.num = num
        self.copyInfoByteArr = copyInfoByteArr
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
        self.frontBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlinfo"]["pasteFront"], style="custom.paste.TButton", width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlinfo"]["pasteBack"], style="custom.paste.TButton", width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlinfo"]["pasteCancel"], style="custom.paste.TButton", width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)

    def frontInsert(self):
        if not self.decryptFile.copySaveFile(self.num - 1, self.copyInfoByteArr):
            self.decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        self.ok()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
        self.reloadFlag = True

    def backInsert(self):
        if not self.decryptFile.copySaveFile(self.num, self.copyInfoByteArr):
            self.decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        self.ok()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
        self.reloadFlag = True
