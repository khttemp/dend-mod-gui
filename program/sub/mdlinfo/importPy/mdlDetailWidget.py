import copy
import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog

from program.sub.mdlinfo.importPy.tkinterScrollbarTreeviewMdlinfo import ScrollbarTreeviewMdlinfo


class MdlDetailDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.num = num
        self.master = master
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.selectId = None
        self.dirtyFlag = False
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.detailMdlList = decryptFile.allInfoList[self.num]["detailMdlList"]
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

        mdlInfoLf = ttkCustomWidget.CustomTtkLabelFrame(mainFrame, text=textSetting.textList["mdlinfo"]["mdlinfoLf"])
        mdlInfoLf.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.74)

        self.editColorBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["editColorLabel"], width=25, state="disabled", command=self.editColor)
        self.editColorBtn.place(relx=0.33, rely=0.04)

        self.allEditElementBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["allElementModifyLabel"], width=25, state="disabled", command=self.allEditElement)
        self.allEditElementBtn.place(relx=0.78, rely=0.04)

        self.modifyElementBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["elementModifyLabel"], width=25, state="disabled", command=self.modifyElement)
        self.modifyElementBtn.place(relx=0.33, rely=0.13)

        self.insertElementBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["elementInsertLabel"], width=25, state="disabled", command=self.insertElement)
        self.insertElementBtn.place(relx=0.555, rely=0.13)

        self.deleteElementBtn = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["mdlinfo"]["elementDeleteLabel"], width=25, state="disabled", command=self.deleteElement)
        self.deleteElementBtn.place(relx=0.78, rely=0.13)

        btnList = [
            self.editColorBtn,
            self.allEditElementBtn,
            self.modifyElementBtn,
            self.insertElementBtn,
            self.deleteElementBtn
        ]
        self.frame = ScrollbarTreeviewMdlinfo(mdlInfoLf, self.v_select, btnList)

        colIdTuple = [
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

        colTuple = [
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

        self.frame.tree["columns"] = colIdTuple
        self.frame.tree.column("#0", width=0, stretch=False)

        for index, colIdName in enumerate(colIdTuple):
            widthLen = 50
            if colIdName == "treeEle1-3":
                widthLen = 80
            elif colIdName == "treeDiff":
                widthLen = 150
            elif colIdName == "treeEmis":
                widthLen = 150
            self.frame.tree.column(colIdName, anchor=tkinter.CENTER, width=widthLen)
            self.frame.tree.heading(colIdName, text=colTuple[index], anchor=tkinter.CENTER)

        self.frame.tree["displaycolumns"] = colIdTuple
        self.viewData(self.detailMdlList)
        super().body(master)

    def viewData(self, detailMdlList):
        for index, detailMdlInfo in enumerate(detailMdlList):
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
        if len(detailMdlList) == 0:
            self.insertElementBtn["state"] = "normal"

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.detailMdlList):
                self.selectId = len(self.detailMdlList) - 1
            self.frame.tree.selection_set(self.selectId)
            self.frame.tree.see(self.selectId)

    def reloadWidget(self):
        self.dirtyFlag = True
        self.decryptFile = self.decryptFile.reload()
        self.detailMdlList = self.decryptFile.allInfoList[self.num]["detailMdlList"]

        for i in self.frame.tree.get_children():
            self.frame.tree.delete(i)
        self.viewData(self.detailMdlList)
        self.jumpToSelect()

    def editColor(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1

        result = TexImageDialog(self.master, textSetting.textList["mdlinfo"]["texImageLabel"], self.num, detailNum, self.decryptFile, self.detailMdlList, self.rootFrameAppearance)
        if result.dirtyFlag:
            if not self.decryptFile.updateTexImage(self.num, detailNum, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I29"])
            self.selectId = detailNum
            self.reloadWidget()

    def allEditElement(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1

        result = EditDetailDialog(self.master, textSetting.textList["mdlinfo"]["detailModelLabel"], "allEdit", self.num, detailNum, self.detailMdlList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.updateTexList(self.num, result.firstDetailNum, result.newDetailMaterialList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum
            self.reloadWidget()

    def modifyElement(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1

        result = EditDetailDialog(self.master, textSetting.textList["mdlinfo"]["detailModelLabel"], "modify", self.num, detailNum, self.detailMdlList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.updateTex(self.num, detailNum, result.resultValueList, "modify"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum
            self.reloadWidget()

    def insertElement(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        detailNum = int(selectItem["treeNum"]) - 1

        result = EditDetailDialog(self.master, textSetting.textList["mdlinfo"]["detailModelLabel"], "insert", self.num, detailNum, self.detailMdlList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.updateTex(self.num, detailNum + result.insertPos, result.resultValueList, "insert"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum + result.insertPos
            self.reloadWidget()

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
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum
            self.reloadWidget()


class TexImageDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, detailNum, decryptFile, detailMdlList, rootFrameAppearance):
        self.master = master
        self.num = num
        self.detailNum = detailNum
        self.decryptFile = decryptFile
        self.detailMdlList = detailMdlList
        self.txtImgList = copy.deepcopy(detailMdlList[detailNum]["textureImgList"])
        self.rootFrameAppearance = rootFrameAppearance
        self.resultValueList = []
        self.dirtyFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
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
        copyImageList = self.setListboxInfo(self.txtImgList)
        self.v_imageList = tkinter.StringVar(value=copyImageList)
        self.imageListbox = tkinter.Listbox(listFrame, font=textSetting.textList["font2"], listvariable=self.v_imageList, width=30, height=6, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        self.imageListbox.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.imageListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.imageListbox, self.imageListbox.curselection()))
        super().body(master)

    def setListboxInfo(self, imageList):
        displayImageList = []
        if len(imageList) > 0:
            for i in range(len(imageList)):
                displayImageList.append(imageList[i])
        else:
            displayImageList = [textSetting.textList["mdlinfo"]["noList"]]
        return displayImageList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndex = value[0]

        if listbox.get(value[0]) == textSetting.textList["mdlinfo"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.txtImgList[self.selectIndex]
        result = EditTexImageDialog(self.master, textSetting.textList["modify"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.txtImgList[self.selectIndex] = result.resultValue
            displayTexImageList = self.setListboxInfo(self.txtImgList)
            self.v_imageList.set(displayTexImageList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            self.imageListbox.selection_clear(0, tkinter.END)

    def insert(self):
        result = EditTexImageDialog(self.master, textSetting.textList["insert"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.txtImgList.insert(self.selectIndex + result.insertPos, result.resultValue)
            displayTexImageList = self.setListboxInfo(self.txtImgList)
            self.v_imageList.set(displayTexImageList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            self.imageListbox.selection_clear(0, tkinter.END)

    def delete(self):
        warnMsg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)
        if result:
            self.txtImgList.pop(self.selectIndex)
            displayTexImageList = self.setListboxInfo(self.txtImgList)
            self.v_imageList.set(displayTexImageList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            self.imageListbox.selection_clear(0, tkinter.END)

    def validate(self):
        if not self.dirtyFlag:
            return True

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I28"], icon="warning", parent=self)
        if result:
            self.resultValueList = []
            noList = textSetting.textList["mdlinfo"]["noList"]
            for i in range(self.imageListbox.size()):
                item = self.imageListbox.get(i)
                if item == noList:
                    continue
                self.resultValueList.append(item)
            return True


class EditTexImageDialog(CustomSimpleDialog):
    def __init__(self, master, title, mode, item, rootFrameAppearance):
        self.mode = mode
        self.item = item
        self.insertPos = None
        self.resultValue = ""
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varTemp = tkinter.StringVar()
        if self.mode == "modify":
            self.varTemp.set(self.item)
        txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
        txtEt.grid(columnspan=2, row=1, column=0, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, 2)
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
        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                res = self.varTemp.get()
                if not res:
                    mb.showerror(title=textSetting.textList["valueError"], message=textSetting.textList["infoList"]["I44"])
                    return False
                self.resultValue = res
                return True
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False

    def apply(self):
        self.reloadFlag = True


class EditDetailDialog(CustomSimpleDialog):
    def __init__(self, master, title, mode, num, detailNum, detailMdlList, rootFrameAppearance):
        self.mode = mode
        self.num = num
        self.detailNum = detailNum
        self.detailMdlList = detailMdlList
        self.materialList = detailMdlList[detailNum]["materialList"]
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        self.varList = []
        self.varCnt = 0
        self.entryWidth = 20

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        inputFrame = ttkCustomWidget.CustomTtkFrame(master)
        inputFrame.grid(columnspan=2, row=1, column=0, sticky=tkinter.NSEW)

        if self.mode == "allEdit":
            self.setAllEditDetailBody(inputFrame)
        else:
            self.setEditDetailBody(inputFrame)
        super().body(master)

    def setEditDetailBody(self, inputFrame):
        eleLb = ttkCustomWidget.CustomTtkLabel(inputFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["detailModelMeshLabel"])
        eleLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varList.append(tkinter.IntVar(value=self.materialList[0]))
        eleEt = ttkCustomWidget.CustomTtkEntry(inputFrame, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
        eleEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.varCnt += 1

        eleLb = ttkCustomWidget.CustomTtkLabel(inputFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["detailModelMtrlLabel"])
        eleLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        self.varList.append(tkinter.IntVar(value=self.materialList[1]))
        eleEt = ttkCustomWidget.CustomTtkEntry(inputFrame, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
        eleEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)
        self.varCnt += 1

        xLine = ttkCustomWidget.CustomTtkSeparator(inputFrame, orient=tkinter.HORIZONTAL)
        xLine.grid(row=1, column=0, columnspan=4, sticky=tkinter.W + tkinter.E, pady=10)

        headerLabelList = [
            textSetting.textList["mdlinfo"]["treeConst"] + "1",
            "DRAW",
            "TRAN",
            "SPEC",
            "DIFF_R",
            "DIFF_G",
            "DIFF_B",
            "DIFF_A",
            textSetting.textList["mdlinfo"]["treeConst"] + "0",
            "EMIS_R",
            "EMIS_G",
            "EMIS_B",
            textSetting.textList["mdlinfo"]["treeNum2"] + "1",
            textSetting.textList["mdlinfo"]["treeNum2"] + "2",
        ]

        for i, headerLabel in enumerate(headerLabelList):
            if i >= 8:
                eleLb = ttkCustomWidget.CustomTtkLabel(inputFrame, font=textSetting.textList["font2"], text=headerLabel)
                eleLb.grid(row=i - 6, column=2, sticky=tkinter.W + tkinter.E)
                if i in [9, 10, 11]:
                    self.varList.append(tkinter.DoubleVar(value=self.materialList[i + 2]))
                else:
                    self.varList.append(tkinter.IntVar(value=self.materialList[i + 2]))
                eleEt = ttkCustomWidget.CustomTtkEntry(inputFrame, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=i - 6, column=3, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
            else:
                eleLb = ttkCustomWidget.CustomTtkLabel(inputFrame, font=textSetting.textList["font2"], text=headerLabel)
                eleLb.grid(row=i + 2, column=0, sticky=tkinter.W + tkinter.E)
                if i in [4, 5, 6, 7]:
                    self.varList.append(tkinter.DoubleVar(value=self.materialList[i + 2]))
                else:
                    self.varList.append(tkinter.IntVar(value=self.materialList[i + 2]))
                eleEt = ttkCustomWidget.CustomTtkEntry(inputFrame, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=i + 2, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1

        if self.mode == "insert":
            self.setInsertWidget(inputFrame, 10)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["railEditor"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def setAllEditDetailBody(self, master):
        self.checkVarList = []
        self.checkVarCnt = 0

        eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=textSetting.textList["mdlinfo"]["detailModelMeshLabel"])
        eleLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        eleMeshNoLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=self.materialList[0])
        eleMeshNoLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

        headerLabelList = [
            "DRAW",
            "TRAN",
            "SPEC",
            "DIFF_R",
            "DIFF_G",
            "DIFF_B",
            "DIFF_A",
            "EMIS_R",
            "EMIS_G",
            "EMIS_B",
        ]
        valueList = [
            self.materialList[3],
            self.materialList[4],
            self.materialList[5],
            self.materialList[6],
            self.materialList[7],
            self.materialList[8],
            self.materialList[9],
            self.materialList[11],
            self.materialList[12],
            self.materialList[13],
        ]

        for i, headerLabel in enumerate(headerLabelList):
            self.checkVarList.append(tkinter.IntVar(value=0))
            eleCkbtn = ttkCustomWidget.CustomTtkCheckbutton(master, text=headerLabel, variable=self.checkVarList[self.checkVarCnt])
            eleCkbtn.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)

            if i in [0, 1, 2]:
                self.varList.append(tkinter.IntVar(value=valueList[i]))
            else:
                self.varList.append(tkinter.DoubleVar(value=valueList[i]))
            eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
            eleEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.varCnt += 1
            self.checkVarCnt += 1

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueList = []
        if self.mode == "allEdit":
            return self.allEditValidate()
        else:
            return self.commonValidate()

    def commonValidate(self):
        for var in self.varList:
            self.resultValueList.append(var.get())

        newMeshList = [self.varList[0].get(), self.varList[1].get()]
        oldMeshList = [self.materialList[0], self.materialList[1]]
        materialList = [x["materialList"][0:2] for x in self.detailMdlList]
        if self.mode == "modify":
            warnMsg = ""
            if newMeshList != oldMeshList and newMeshList in materialList:
                warnMsg = textSetting.textList["infoList"]["I30"].format(newMeshList[0], newMeshList[1])
                warnMsg += textSetting.textList["infoList"]["I31"]
        elif self.mode == "insert":
            warnMsg = ""
            if newMeshList in materialList:
                warnMsg = textSetting.textList["infoList"]["I30"].format(newMeshList[0], newMeshList[1])
                warnMsg += textSetting.textList["infoList"]["I32"]
        if warnMsg:
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
            if not result:
                return

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        return True

    def allEditValidate(self):
        for var in self.varList:
            self.resultValueList.append(var.get())

        selectMeshNo = self.materialList[0]
        self.firstDetailNum = -1
        findFlag = False
        editLabelList = []
        self.newDetailMaterialList = []

        for detailIdx, detailMdlInfo in enumerate(self.detailMdlList):
            meshNo = detailMdlInfo["materialList"][0]
            varCnt = 0
            checkVarCnt = 0
            if selectMeshNo == meshNo:
                if not findFlag:
                    findFlag = True
                    self.firstDetailNum = detailIdx
                newDetailMdlInfo = copy.deepcopy(detailMdlInfo)
                # "DRAW", "TRAN", "SPEC"
                eleLabelList = ["DRAW", "TRAN", "SPEC"]
                for i in range(3):
                    if self.checkVarList[checkVarCnt].get():
                        if eleLabelList[i] not in editLabelList:
                            editLabelList.append(eleLabelList[i])
                        newDetailMdlInfo["materialList"][3 + i] = self.resultValueList[varCnt]
                    varCnt += 1
                    checkVarCnt += 1
                # DIFF
                colorLabelList = ["DIFF_R", "DIFF_G", "DIFF_B", "DIFF_A"]
                for i in range(4):
                    if self.checkVarList[checkVarCnt].get():
                        if colorLabelList[i] not in editLabelList:
                            editLabelList.append(colorLabelList[i])
                        newDetailMdlInfo["materialList"][6 + i] = self.resultValueList[varCnt]
                    varCnt += 1
                    checkVarCnt += 1
                # EMIS
                colorLabelList = ["EMIS_R", "EMIS_G", "EMIS_B"]
                for i in range(3):
                    if self.checkVarList[checkVarCnt].get():
                        if colorLabelList[i] not in editLabelList:
                            editLabelList.append(colorLabelList[i])
                        newDetailMdlInfo["materialList"][11 + i] = self.resultValueList[varCnt]
                    varCnt += 1
                    checkVarCnt += 1
                self.newDetailMaterialList.append(newDetailMdlInfo["materialList"])
        warnMsg = textSetting.textList["infoList"]["I129"].format(selectMeshNo, "\n".join(editLabelList))
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            return True

    def apply(self):
        self.reloadFlag = True
