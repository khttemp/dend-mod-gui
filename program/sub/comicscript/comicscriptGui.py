import os
import traceback

import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog
from program.sub.errorLogClass import ErrorLogObj

from program.sub.cmdList import cmdList

from program.sub.comicscript.importPy.tkinterScrollbarTreeviewComicscript import ScrollbarTreeviewComicscript
from program.sub.comicscript.importPy.headerDialogWidget import HeaderDialog
from program.sub.comicscript.dendDecrypt.decrypt import ComicDecrypt
import program.sub.comicscript.comicscriptProcess as comicscriptProcess

errObj = ErrorLogObj()


class ComicscriptWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict, rootFrameAppearance):
        super().__init__(master)
        self.importDict = importDict
        self.rootFrameAppearance = rootFrameAppearance
        self.decryptFile = None
        self.selectId = None
        self.cmdJsonInfo = self.importDict["cmdJsonInfo"]
        self.copyComicData = None

        headerFrame = ttkCustomWidget.CustomTtkFrame(master)
        headerFrame.pack(fill=tkinter.BOTH, padx=40, pady=(20, 0))

        selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        self.v_fileName = tkinter.StringVar()
        fileNameEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
        fileNameEt.grid(columnspan=5, row=0, column=0, pady=(0, 15), sticky=tkinter.EW)

        selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["comicscript"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.grid(columnspan=4, row=1, column=0, pady=(0, 15), sticky=tkinter.EW)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
        selectEt.grid(row=1, column=4, pady=(0, 15), sticky=tkinter.E)

        btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        btnFrame.pack(fill=tkinter.BOTH, padx=(120, 0))

        buttonWidth = 25

        self.editLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["editLineLabel"], width=buttonWidth, state="disabled", command=self.editLine)
        self.editLineBtn.grid(row=0, column=0, padx=10, pady=(0, 20))

        self.insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["insertLineLabel"], width=buttonWidth, state="disabled", command=self.insertLine)
        self.insertLineBtn.grid(row=0, column=1, padx=10, pady=(0, 20))

        self.deleteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["deleteLineLabel"], width=buttonWidth, state="disabled", command=self.deleteLine)
        self.deleteLineBtn.grid(row=0, column=2, padx=10, pady=(0, 20))

        self.copyLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["copyLineLabel"], width=buttonWidth, state="disabled", command=self.copyLine)
        self.copyLineBtn.grid(row=1, column=0, padx=10, pady=(0, 20))

        self.pasteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["pasteLineLabel"], width=buttonWidth, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=(0, 20))

        self.csvExtractBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["csvExtractLabel"], width=buttonWidth, state="disabled", command=self.csvExtract)
        self.csvExtractBtn.grid(row=2, column=0, padx=10, pady=(0, 20))

        self.csvLoadAndSaveBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["csvSaveLabel"], width=buttonWidth, state="disabled", command=self.csvLoadAndSave)
        self.csvLoadAndSaveBtn.grid(row=2, column=1, padx=10, pady=(0, 20))

        self.headerFileEditBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["headerEditLabel"], width=buttonWidth, state="disabled", command=self.headerFileEdit)
        self.headerFileEditBtn.grid(row=2, column=2, padx=10, pady=(0, 20))

        btnFrame.grid_columnconfigure(0, weight=1)
        btnFrame.grid_columnconfigure(1, weight=1)
        btnFrame.grid_columnconfigure(2, weight=1)

        self.btnList = [
            self.editLineBtn,
            self.insertLineBtn,
            self.deleteLineBtn,
            self.copyLineBtn
        ]

        self.scriptLf = ttkCustomWidget.CustomTtkLabelFrame(master, text=textSetting.textList["comicscript"]["scriptLabel"])
        self.scriptLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))

    def deleteWidget(self):
        for btn in self.btnList:
            btn["state"] = "disabled"

        children = self.scriptLf.winfo_children()
        for child in children:
            child.destroy()

    def createWidget(self):
        self.setComicscriptTableHeader()
        self.setComicscriptTableData()

    def setComicscriptTableHeader(self):
        self.frame = ScrollbarTreeviewComicscript(self.scriptLf, self.v_select, self.btnList)

        col_tuple = (
            "treeNum",
            "comicScriptName"
        )
        paramList = []
        for i in range(self.decryptFile.max_param):
            paramList.append(textSetting.textList["comicscript"]["paramNumLabel"].format(i+1))
        col_tuple = col_tuple + tuple(paramList)

        self.frame.tree["columns"] = col_tuple
        self.frame.tree.column("#0", width=0, stretch=False)

        self.frame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, minwidth=50)
        self.frame.tree.column("comicScriptName", anchor=tkinter.CENTER, width=150, minwidth=150)
        self.frame.tree.heading("treeNum", text=textSetting.textList["comicscript"]["treeNum"], anchor=tkinter.CENTER)
        self.frame.tree.heading("comicScriptName", text=textSetting.textList["comicscript"]["treeName"], anchor=tkinter.CENTER)

        for i in range(self.decryptFile.max_param):
            col_name = textSetting.textList["comicscript"]["paramNumLabel"].format(i+1)
            self.frame.tree.column(col_name, anchor=tkinter.CENTER, width=100, minwidth=100)
            self.frame.tree.heading(col_name, text=col_name, anchor=tkinter.CENTER)

    def setComicscriptTableData(self):
        game = comicscriptProcess.getGameOption(self.importDict["configPath"])
        for index, comicData in enumerate(self.decryptFile.comicDataList):
            data = (index + 1, comicData[0])
            paramCnt = comicData[1]
            paramList = []
            for i in range(paramCnt):
                paramList.append(comicData[2 + i])
            data = data + tuple(paramList)

            if self.cmdJsonInfo is not None:
                cmdInfo = self.cmdJsonInfo[comicData[0]]
                if "comicscript" not in cmdInfo:
                    availableList = []
                else:
                    availableList = cmdInfo["comicscript"]

            if game not in availableList:
                tags = "notAvailable"
            else:
                tags = "available"
            self.frame.tree.insert(parent="", index="end", iid=index, values=data, tags=tags)
        self.frame.tree.tag_configure("notAvailable", background="#666666", foreground="red")

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.decryptFile.comicDataList):
                self.selectId = len(self.decryptFile.comicDataList) - 1
            self.frame.tree.selection_set(self.selectId)
            self.frame.tree.see(self.selectId)

    def reloadFile(self):
        try:
            self.decryptFile = self.decryptFile.reload()
            self.deleteWidget()
            self.createWidget()
            self.jumpToSelect()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E6"])

    def editLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        comicData = self.decryptFile.comicDataList[num]
        result = EditComicscriptDialog(self.editLineBtn.winfo_toplevel(), textSetting.textList["comicscript"]["cmdModify"], num, comicData, cmdList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveFile(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num
            self.reloadFile()

    def insertLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = EditComicscriptDialog(self.insertLineBtn.winfo_toplevel(), textSetting.textList["comicscript"]["cmdInsert"], num, None, cmdList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveFile(num + result.insertPos, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num + result.insertPos
            self.reloadFile()

    def deleteLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result:
            if not self.decryptFile.saveFile(num, "delete"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num
            self.reloadFile()

    def copyLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        self.copyComicData = self.decryptFile.comicDataList[num]
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = int(self.frame.tree.selection()[0])
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["treeNum"]) - 1

        result = PasteDialog(self.pasteLineBtn.winfo_toplevel(), textSetting.textList["comicscript"]["cmdPaste"], self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveFile(num + result.insertPos, "insert", self.copyComicData):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
            self.selectId = num + result.insertPos
            self.reloadFile()

    def csvExtract(self):
        filename = os.path.splitext(os.path.basename(self.decryptFile.filePath))[0] + ".csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("comicscript_csv", "*.csv")])
        if not file_path:
            return

        try:
            comicscriptProcess.writeCsv(file_path, self.decryptFile.comicDataList)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def csvLoadAndSave(self):
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("comicscript_csv", "*.csv")])
        if not file_path:
            return

        processResult, obj = comicscriptProcess.loadCsvData(file_path, cmdList)
        if not processResult:
            mb.showerror(title=textSetting.textList["error"], message=obj["message"])
            return
        msg = textSetting.textList["infoList"]["I15"].format(obj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            if not self.decryptFile.saveComicList(obj["data"]):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I16"])
            self.reloadFile()

    def headerFileEdit(self):
        result = HeaderDialog(self.headerFileEditBtn.winfo_toplevel(), textSetting.textList["comicscript"]["headerInfo"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFile()

    def openFile(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["comicscript"]["fileType"], "*.BIN")])

        if not file_path:
            return
        del self.decryptFile
        self.decryptFile = ComicDecrypt(file_path, cmdList)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E6"])
            return

        filename = os.path.basename(file_path)
        self.v_fileName.set(filename)

        self.deleteWidget()
        self.createWidget()
        self.headerFileEditBtn["state"] = "normal"
        self.csvExtractBtn["state"] = "normal"
        self.csvLoadAndSaveBtn["state"] = "normal"
        self.pasteLineBtn["state"] = "disabled"


class EditComicscriptDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, comicData, cmdList, rootFrameAppearance):
        self.num = num
        self.comicData = comicData
        self.cmdList = cmdList
        self.sortedCmdList = sorted(cmdList, key=str.lower)
        self.reloadFlag = False
        self.insertPos = 0
        self.resultValueList = []
        if comicData is not None:
            self.mode = "modify"
        else:
            self.mode = "insert"
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        cmdLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["treeName"], width=12, font=textSetting.textList["font2"])
        cmdLb.grid(row=1, column=0, sticky=tkinter.N+tkinter.S)
        self.v_cmd = tkinter.StringVar()
        cmdCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_cmd, width=25, font=textSetting.textList["font2"], state="readonly", value=self.sortedCmdList)
        cmdCb.grid(row=1, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        cmdCb.current(0)
        if self.mode == "modify":
            idx = self.sortedCmdList.index(self.comicData[0])
            cmdCb.current(idx)

        paramCntLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["paramLabel"], width=12, font=textSetting.textList["font2"])
        paramCntLb.grid(row=2, column=0, sticky=tkinter.N+tkinter.S)
        self.v_paramCnt = tkinter.IntVar()
        paramCntList = [cnt for cnt in range(0, 16)]
        self.paramCntCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_paramCnt, width=25, font=textSetting.textList["font2"], state="readonly", value=paramCntList)
        self.paramCntCb.grid(row=2, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        self.paramCntCb.current(0)

        if self.mode == "insert":
            positionLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["posLabel"], width=12, font=textSetting.textList["font2"])
            positionLb.grid(row=3, column=0, sticky=tkinter.N+tkinter.S)
            self.v_position = tkinter.StringVar()
            positionList = textSetting.textList["comicscript"]["posValue"]
            self.positionCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_position, width=25, font=textSetting.textList["font2"], state="readonly", value=positionList)
            self.positionCb.grid(row=3, column=1, sticky=tkinter.N+tkinter.S, pady=10)
            self.positionCb.current(0)

        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(columnspan=2, row=4, column=0, sticky=tkinter.E + tkinter.W, pady=10)

        self.v_paramList = []
        self.paramFrame = ttkCustomWidget.CustomTtkFrame(master)
        self.paramFrame.grid(columnspan=2, row=5, column=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        self.paramCntCb.bind("<<ComboboxSelected>>", lambda e: self.selectParam())
        if self.mode == "modify":
            self.paramCntCb.current(self.comicData[1])
            self.selectParam()
        super().body(master)

    def selectParam(self):
        self.v_paramList = []
        children = self.paramFrame.winfo_children()
        for child in children:
            child.destroy()

        paramCnt = self.paramCntCb.current()
        if paramCnt == 0:
            paramLb = ttkCustomWidget.CustomTtkLabel(self.paramFrame)
            paramLb.grid(row=0, column=0)

        for i in range(paramCnt):
            paramLb = ttkCustomWidget.CustomTtkLabel(self.paramFrame, text=textSetting.textList["comicscript"]["paramNumLabel"].format(i + 1), width=12, font=textSetting.textList["font2"])
            paramLb.grid(row=i, column=0, sticky=tkinter.N+tkinter.S)
            v_param = tkinter.DoubleVar()
            self.v_paramList.append(v_param)
            paramEt = ttkCustomWidget.CustomTtkEntry(self.paramFrame, textvariable=v_param, width=27, font=textSetting.textList["font2"])
            paramEt.grid(row=i, column=1, sticky=tkinter.N+tkinter.S)
            if self.mode == "modify" and i < self.comicData[1]:
                self.v_paramList[i].set(self.comicData[2 + i])

    def validate(self):
        self.resultValueList = []
        self.resultValueList.append(self.v_cmd.get())
        self.resultValueList.append(self.v_paramCnt.get())

        for i, var in enumerate(self.v_paramList):
            paramMsg = textSetting.textList["comicscript"]["paramNumLabel"].format(i + 1)
            try:
                var.get()
            except Exception:
                errorMsg = "{0} [{1}]".format(textSetting.textList["errorList"]["E5"], paramMsg)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            self.resultValueList.append(var.get())

        msg = textSetting.textList["infoList"]["I21"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=msg)
        if result:
            if self.mode == "insert":
                self.insertPos = 1
                if self.positionCb.current() == 1:
                    self.insertPos = 0
            return True

    def apply(self):
        self.reloadFlag = True


class PasteDialog(CustomSimpleDialog):
    def __init__(self, master, title, rootFrameAppearance):
        self.insertPos = 0
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
        self.frontBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["comicscript"]["pasteFront"], style="custom.paste.TButton", width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["comicscript"]["pasteBack"], style="custom.paste.TButton", width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["comicscript"]["pasteCancel"], style="custom.paste.TButton", width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)

    def frontInsert(self):
        self.ok()
        self.reloadFlag = True
        self.insertPos = 0

    def backInsert(self):
        self.ok()
        self.reloadFlag = True
        self.insertPos = 1
