import os
import tkinter
import traceback

from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog
from program.sub.errorLogClass import ErrorLogObj

from program.sub.mdlinfo.dendDecrypt.decrypt import MdlDecrypt
from program.sub.mdlinfo.importPy.tkinterScrollbarTreeviewMdlinfo import ScrollbarTreeviewMdlinfo
from program.sub.mdlinfo.importPy.mdlDetailWidget import MdlDetailDialog
from program.sub.mdlinfo.importPy.smfDetailWidget import SmfDetailDialog

from program.sub.smf.dendDecrypt.decrypt import SmfDecrypt

errObj = ErrorLogObj


class MdlinfoWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict, rootFrameAppearance):
        super().__init__(master)
        self.importDict = importDict
        self.rootFrameAppearance = rootFrameAppearance
        self.decryptFile = None
        self.selectId = None
        self.copyInfoByteArr = None

        headerFrame = ttkCustomWidget.CustomTtkFrame(master)
        headerFrame.pack(fill=tkinter.BOTH, padx=40, pady=(20, 0))

        selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        self.v_fileName = tkinter.StringVar()
        fileNameEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
        fileNameEt.grid(columnspan=5, row=0, column=0, pady=(0, 15), sticky=tkinter.EW)

        selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["mdlinfo"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.grid(columnspan=4, row=1, column=0, pady=(0, 15), sticky=tkinter.EW)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
        selectEt.grid(row=1, column=4, pady=(0, 15), sticky=tkinter.E)

        searchLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["mdlinfo"]["searchModel"], font=textSetting.textList["font2"])
        searchLb.grid(columnspan=2, row=2, column=0, pady=(0, 15), sticky=tkinter.E)

        self.v_search = tkinter.StringVar()
        self.searchEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_search, font=textSetting.textList["font2"], state="readonly", justify="center")
        self.searchEt.grid(columnspan=6, row=2, column=3, pady=(0, 15), sticky=tkinter.EW)
        self.searchEt.bind("<KeyRelease>", self.filterModelList)

        btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        btnFrame.pack(fill=tkinter.BOTH, padx=(40, 0))

        self.mdlDetailBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlDetailLabel"], width=25, state="disabled", command=self.mdlDetailFunc)
        self.mdlDetailBtn.grid(row=0, column=0, padx=10, pady=(0, 20))

        self.mdlTypeBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlTypeLabel"], width=25, state="disabled", command=self.mdlTypeFunc)
        self.mdlTypeBtn.grid(row=0, column=1, padx=10, pady=(0, 20))

        self.mdlSmfElementBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlSmfEleLabel"], width=25, state="disabled", command=self.mdlSmfElementFunc)
        self.mdlSmfElementBtn.grid(row=0, column=2, padx=10, pady=(0, 20))

        self.binFileOrFlagBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["binFileFlagLabel"], width=25, state="disabled", command=self.binFileOrFlagFunc)
        self.binFileOrFlagBtn.grid(row=1, column=0, padx=10, pady=(0, 20))

        self.copyAnotherMdlinfoBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["copyAnotherMdlinfoLabel"], width=25, state="disabled", command=self.copyAnotherMdlinfoFunc)
        self.copyAnotherMdlinfoBtn.grid(row=1, column=1, padx=10, pady=(0, 20))

        self.mdlinfoDeleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlinfoDeleteLabel"], width=25, state="disabled", command=self.mdlinfoDeleteFunc)
        self.mdlinfoDeleteBtn.grid(row=1, column=2, padx=10, pady=(0, 20))

        self.mdlinfoCopyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlinfoCopyLabel"], width=25, state="disabled", command=self.mdlinfoCopyFunc)
        self.mdlinfoCopyBtn.grid(row=2, column=0, padx=10, pady=(0, 20))

        self.mdlinfoPasteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlinfoPasteLabel"], width=25, state="disabled", command=self.mdlinfoPasteFunc)
        self.mdlinfoPasteBtn.grid(row=2, column=1, padx=10, pady=(0, 20))

        self.addSmfModelBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["addSmfModelLabel"], width=25, state="disabled", command=self.addSmfModelFunc)
        self.addSmfModelBtn.grid(row=2, column=2, padx=10, pady=(0, 20))

        self.btnList = [
            self.mdlDetailBtn,
            self.mdlTypeBtn,
            self.mdlSmfElementBtn,
            self.binFileOrFlagBtn,
            self.mdlinfoDeleteBtn,
            self.mdlinfoCopyBtn
        ]

        btnFrame.grid_columnconfigure(0, weight=1)
        btnFrame.grid_columnconfigure(1, weight=1)
        btnFrame.grid_columnconfigure(2, weight=1)

        self.mdlInfoLf = ttkCustomWidget.CustomTtkLabelFrame(master, text=textSetting.textList["mdlinfo"]["scriptLabel"])
        self.mdlInfoLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))
    
    def deleteAllWidgetInLabelFrame(self):
        for btn in self.btnList:
            btn["state"] = "disabled"

        for children in self.mdlInfoLf.winfo_children():
            children.destroy()

    def createWidget(self):
        self.frame = ScrollbarTreeviewMdlinfo(self.mdlInfoLf, self.v_select, self.btnList)

        col_tuple = (
            "treeNum",
            "treeSmf",
            "treeSmfType",
            "treeSmfEleNum",
            "binFileLabel",
            "binFileFlag"
        )
        self.frame.tree["columns"] = col_tuple

        self.frame.tree.column("#0", width=0, stretch=False)
        self.frame.tree.column("treeNum", anchor=tkinter.CENTER, width=60, stretch=False)
        self.frame.tree.column("treeSmf", anchor=tkinter.CENTER)
        self.frame.tree.column("treeSmfType", anchor=tkinter.CENTER, width=60, stretch=False)
        self.frame.tree.column("treeSmfEleNum", anchor=tkinter.CENTER, width=80, stretch=False)
        self.frame.tree.column("binFileLabel", anchor=tkinter.CENTER)
        self.frame.tree.column("binFileFlag", anchor=tkinter.CENTER, width=60, stretch=False)

        self.frame.tree.heading("treeNum", text=textSetting.textList["mdlinfo"]["treeNum"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeSmf", text=textSetting.textList["mdlinfo"]["treeSmf"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeSmfType", text=textSetting.textList["mdlinfo"]["treeSmfType"], anchor=tkinter.CENTER)
        self.frame.tree.heading("treeSmfEleNum", text=textSetting.textList["mdlinfo"]["treeSmfEleNum"], anchor=tkinter.CENTER)
        self.frame.tree.heading("binFileLabel", text=textSetting.textList["mdlinfo"]["binFileLabel"], anchor=tkinter.CENTER)
        self.frame.tree.heading("binFileFlag", text=textSetting.textList["mdlinfo"]["binFileFlag"], anchor=tkinter.CENTER)

        self.frame.tree["displaycolumns"] = col_tuple
        self.viewData()

    def viewData(self):
        for index, mdlInfo in enumerate(self.decryptFile.allInfoList):
            binName = "-"
            if mdlInfo["binInfo"][0]:
                binName = mdlInfo["binInfo"][0]
            data = (index + 1, mdlInfo["smfName"])
            data += (mdlInfo["smfType"],)
            data += (len(mdlInfo["smfDetailList"]),)
            data += (binName, mdlInfo["binInfo"][1])
            self.frame.tree.insert(parent="", index="end", iid=index, values=data)
        self.filterData()

    def filterModelList(self, event):
        self.v_select.set("")
        if len(self.frame.tree.selection()) > 0:
            self.frame.tree.selection_remove(self.frame.tree.selection())
        self.filterData()

    def filterData(self):
        for i in range(len(self.decryptFile.allInfoList)):
            self.frame.tree.reattach(i, "", tkinter.END)

        search = self.v_search.get()
        for i in self.frame.tree.get_children():
            item = self.frame.tree.item(i)
            modelName = item["values"][1]
            if search.upper() not in modelName.upper():
                self.frame.tree.detach(i)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.decryptFile.allInfoList):
                self.selectId = len(self.decryptFile.allInfoList) - 1
            self.frame.tree.selection_set(self.selectId)
            self.frame.tree.see(self.selectId)

    def reloadFile(self):
        try:
            for btn in self.btnList:
                btn["state"] = "disabled"
            for i in range(len(self.decryptFile.allInfoList)):
                if self.frame.tree.exists(i):
                    self.frame.tree.delete(i)
            self.decryptFile = self.decryptFile.reload()

            self.viewData()
            self.jumpToSelect()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def openFile(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["mdlinfo"]["fileType"], "MDLINFO*.BIN")])

        if not file_path:
            return
        del self.decryptFile
        self.decryptFile = MdlDecrypt(file_path)
        
        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E18"])
            return

        self.v_select.set("")
        filename = os.path.basename(file_path)
        self.v_fileName.set(filename)
        self.searchEt["state"] = "normal"

        self.deleteAllWidgetInLabelFrame()
        self.createWidget()
        self.copyAnotherMdlinfoBtn["state"] = "normal"
        self.addSmfModelBtn["state"] = "normal"
        self.copyInfoByteArr = None
        self.mdlinfoPasteBtn["state"] = "disabled"

    def mdlDetailFunc(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = MdlDetailDialog(self.mdlDetailBtn.winfo_toplevel(), textSetting.textList["mdlinfo"]["detailModelInfo"], num, self.decryptFile, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.selectId = num
            self.reloadFile()

    def mdlTypeFunc(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = SmfTypeDialog(self.mdlTypeBtn.winfo_toplevel(), textSetting.textList["mdlinfo"]["detailModelTypeInfo"], num, self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.updateType(num, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I120"])
            self.selectId = num
            self.reloadFile()

    def mdlSmfElementFunc(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = SmfDetailDialog(self.mdlSmfElementBtn.winfo_toplevel(), textSetting.textList["mdlinfo"]["smfInfo"], num, self.decryptFile, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.selectId = num
            self.reloadFile()

    def binFileOrFlagFunc(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = BinFileOrFlagEditDialog(self.binFileOrFlagBtn.winfo_toplevel(), textSetting.textList["mdlinfo"]["binFileOrFlagLabel"], num, self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.updateBinFileOrFlag(num, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I36"])
            self.selectId = num
            self.reloadFile()

    def copyAnotherMdlinfoFunc(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["mdlinfo"]["fileType"], "MDLINFO*.BIN")])
        if not file_path:
            return

        tempDecryptFile = MdlDecrypt(file_path)
        if not tempDecryptFile.open():
            tempDecryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E18"])
            return

        result = CopyMdlDialog(self.copyAnotherMdlinfoBtn.winfo_toplevel(), textSetting.textList["mdlinfo"]["copyAnotherMdlinfo"], tempDecryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            del tempDecryptFile
            tempDecryptFile = None

            if not self.decryptFile.copy(result.copyByteArr):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
            self.selectId = len(self.decryptFile.allInfoList)
            self.reloadFile()

    def mdlinfoDeleteFunc(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        warnMsg = textSetting.textList["infoList"]["I25"].format(num + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.delete(num):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = num
            self.reloadFile()

    def mdlinfoCopyFunc(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        index = self.decryptFile.allInfoList[num]["smfIndex"]
        if num + 1 < len(self.decryptFile.allInfoList):
            nextIndex = self.decryptFile.allInfoList[num + 1]["smfIndex"]
            self.copyInfoByteArr = self.decryptFile.byteArr[index:nextIndex]
        else:
            self.copyInfoByteArr = self.decryptFile.byteArr[index:]

        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.mdlinfoPasteBtn["state"] = "normal"

    def mdlinfoPasteFunc(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = PasteDialog(self.mdlinfoPasteBtn.winfo_toplevel(), textSetting.textList["mdlinfo"]["copyModelLabel"], self.decryptFile, num, self.copyInfoByteArr, self.rootFrameAppearance)
        if result.reloadFlag:
            self.selectId = num + result.insertPos
            self.reloadFile()

    def addSmfModelFunc(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["smf"]["fileType"], "*.SMF")])
        if not file_path:
            return

        smfDecryptFile = SmfDecrypt(file_path)
        if not smfDecryptFile.open():
            smfDecryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])
            return

        meshInfoList = smfDecryptFile.meshList
        filename = os.path.basename(file_path)
        if not self.decryptFile.readSMFSave(filename, meshInfoList):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
        self.selectId = len(self.decryptFile.allInfoList)
        self.reloadFile()


class SmfTypeDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.master = master
        self.num = num
        self.decryptFile = decryptFile
        self.smfType = decryptFile.allInfoList[self.num]["smfType"]
        self.reloadFlag = False
        self.resultValue = None
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        self.entryWidth = 20
        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        smfTypeLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["smfTypeLabel"], font=textSetting.textList["font2"])
        smfTypeLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_smfType = tkinter.IntVar()
        self.v_smfType.set(self.smfType)
        smfTypeEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_smfType, width=self.entryWidth)
        smfTypeEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I119"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            self.resultValue = int(self.v_smfType.get())
            return True

    def apply(self):
        self.reloadFlag = True


class BinFileOrFlagEditDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.smfNum = num
        self.decryptFile = decryptFile
        self.smfName = decryptFile.allInfoList[self.smfNum]["smfName"]
        self.binFile = decryptFile.allInfoList[self.smfNum]["binInfo"][0]
        self.flag = decryptFile.allInfoList[self.smfNum]["binInfo"][1]
        self.reloadFlag = False
        self.resultValueList = []
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        self.entryWidth = 20

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        smfNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["smfNameLabel"], font=textSetting.textList["font2"])
        smfNameLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_smfName = tkinter.StringVar()
        self.v_smfName.set(self.smfName)
        smfNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_smfName, width=self.entryWidth)
        smfNameEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)

        binFileLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["binFileLabel"], font=textSetting.textList["font2"])
        binFileLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
        self.v_binFile = tkinter.StringVar()
        self.v_binFile.set(self.binFile)
        binFileEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_binFile, width=self.entryWidth)
        binFileEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)

        flagLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlinfo"]["binFileFlag"], font=textSetting.textList["font2"])
        flagLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E)
        self.v_flag = tkinter.IntVar()
        self.v_flag.set(self.flag)
        flagEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_flag, width=self.entryWidth)
        flagEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I35"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)

        if result:
            self.resultValueList = []
            if not self.v_smfName.get():
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E17"])
                return False
            self.resultValueList.append(self.v_smfName.get())
            self.resultValueList.append(self.v_binFile.get())
            self.resultValueList.append(self.v_flag.get())
            return True

    def apply(self):
        self.reloadFlag = True


class CopyMdlDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.smfName = []
        self.cbSmfName = []

        for index, allInfo in enumerate(decryptFile.allInfoList):
            self.smfName.append(allInfo["smfName"])
            self.cbSmfName.append("({0}){1}".format(index + 1, allInfo["smfName"]))
        self.reloadFlag = False
        self.copyByteArr = None
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
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
            index = self.decryptFile.allInfoList[idx]["smfIndex"]

            if idx + 1 < len(self.decryptFile.allInfoList):
                lastIndex = self.decryptFile.allInfoList[idx + 1]["smfIndex"]
                self.copyByteArr = self.decryptFile.byteArr[index:lastIndex]
            else:
                self.copyByteArr = self.decryptFile.byteArr[index:]
            return True

    def apply(self):
        self.reloadFlag = True


class PasteDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, num, copyInfoByteArr, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.num = num
        self.copyInfoByteArr = copyInfoByteArr
        self.reloadFlag = False
        self.insertPos = 0
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
        if not self.decryptFile.copySaveFile(self.num, self.copyInfoByteArr):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return
        self.ok()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
        self.reloadFlag = True
        self.insertPos = 0

    def backInsert(self):
        if not self.decryptFile.copySaveFile(self.num + 1, self.copyInfoByteArr):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return
        self.ok()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
        self.reloadFlag = True
        self.insertPos = 1
