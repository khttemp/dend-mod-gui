import copy

import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog
import program.sub.railEditor.importPy.tab9.else3CsvProcess as else3CsvProcess

from program.sub.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class Else3ListWidget:
    def __init__(self, frame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
        self.text = textSetting.textList["railEditor"]["else3Label"]
        self.frame = frame
        self.decryptFile = decryptFile
        self.else3List = decryptFile.else3List
        self.copyElse3Info = []
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.selectId = selectId

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.title = textSetting.textList["railEditor"]["else3Label"]
        else:
            self.title = textSetting.textList["railEditor"]["camLabel"]

        elseLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=self.text)
        elseLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        headerFrame = ttkCustomWidget.CustomTtkFrame(elseLf)
        headerFrame.pack()

        selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        numLabelCsvBtnFrame = ttkCustomWidget.CustomTtkFrame(selectLbFrame)
        numLabelCsvBtnFrame.pack()
        numLabelFrame = ttkCustomWidget.CustomTtkFrame(numLabelCsvBtnFrame)
        numLabelFrame.pack()

        selectLb = ttkCustomWidget.CustomTtkLabel(numLabelFrame, text=textSetting.textList["railEditor"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.pack(side=tkinter.LEFT, padx=15, pady=15)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(numLabelFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        selectEt.pack(side=tkinter.LEFT, padx=5, pady=15)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            csvBtnFrame = ttkCustomWidget.CustomTtkFrame(numLabelCsvBtnFrame)
            csvBtnFrame.pack(side=tkinter.LEFT, padx=5, pady=10)

            else3ExtractCsvBtn = ttkCustomWidget.CustomTtkButton(csvBtnFrame, text=textSetting.textList["railEditor"]["else3ExtractCsvLabel"], width=20, command=lambda: self.else3ExtractCsv())
            else3ExtractCsvBtn.grid(row=0, column=0, padx=15)
            else3LoadAndSaveCsvBtn = ttkCustomWidget.CustomTtkButton(csvBtnFrame, text=textSetting.textList["railEditor"]["else3LoadAndSaveCsvLabel"], width=20, command=lambda: self.else3LoadAndSaveCsv())
            else3LoadAndSaveCsvBtn.grid(row=0, column=1, padx=15)

        btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        btnFrame.pack(anchor=tkinter.NE, padx=15)

        editLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonEditLineLabel"], width=25, state="disabled", command=self.editLine)
        editLineBtn.grid(row=0, column=0, padx=10, pady=15)

        self.insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonInsertLineLabel"], width=25, state="disabled", command=self.insertLine)
        self.insertLineBtn.grid(row=0, column=1, padx=10, pady=15)

        deleteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonDeleteLineLabel"], width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=15)

        copyLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonCopyLineLabel"], width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=15)

        self.pasteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonPasteLineLabel"], width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=15)

        listModifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["editElse3InfoListLabel"], width=25, state="disabled", command=self.listModify)
        listModifyBtn.grid(row=1, column=2, padx=10, pady=15)

        btnList = [
            editLineBtn,
            self.insertLineBtn,
            deleteLineBtn,
            copyLineBtn,
            listModifyBtn
        ]

        self.treeviewFrame = ScrollbarTreeviewRailEditor(elseLf, self.v_select, btnList)

        self.createElse3Table()
        self.jumpToSelect()

    def createElse3Table(self):
        self.setElse3TableHeader()
        self.setElse3TableData()
        if len(self.else3List) == 0:
            self.insertLineBtn["state"] = "normal"

    def setElse3TableHeader(self):
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            col_tuple = (
                "treeNum",
                "railNo",
                "else3ListNum",
            )
            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("railNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("else3ListNum", anchor=tkinter.CENTER, width=50)

            else3InfoLbList = textSetting.textList["railEditor"]["editElse3LabelList"]
            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["else3Num"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("railNo", text=else3InfoLbList[0], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("else3ListNum", text=else3InfoLbList[1], anchor=tkinter.CENTER)
        else:
            col_tuple = (
                "treeNum",
                "cameraF1",
                "cameraF2",
                "cameraF3",
                "cameraListNum",
            )
            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("cameraF1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cameraF2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cameraF3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("cameraListNum", anchor=tkinter.CENTER, width=50)

            else3InfoLbList = textSetting.textList["railEditor"]["editElse3LsLabelList"]
            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["else3Num"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cameraF1", text=else3InfoLbList[0], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cameraF2", text=else3InfoLbList[1], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cameraF3", text=else3InfoLbList[2], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("cameraListNum", text=else3InfoLbList[3], anchor=tkinter.CENTER)
        self.treeviewFrame.tree["displaycolumns"] = col_tuple

    def setElse3TableData(self):
        for index, else3Info in enumerate(self.else3List):
            data = (index,)
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                data += (else3Info[0], len(else3Info[1]))
            elif self.decryptFile.game in ["LSTrial", "LS"]:
                data += (else3Info[0], else3Info[1], else3Info[2], len(else3Info[3]))
            self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.else3List):
                self.selectId = len(self.else3List) - 1
            self.treeviewFrame.tree.see(self.selectId)
            self.treeviewFrame.tree.selection_set(self.selectId)

    def editLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        headerNameList = [self.treeviewFrame.tree.heading(col)["text"] for col in self.treeviewFrame.tree.cget("columns")]
        headerNameList.pop(0)
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        item = self.else3List[num]
        result = EditElse3ListWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["editElse3Label"].format(self.text), self.decryptFile, "modify", headerNameList, item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.else3List[num] = result.resultValueList
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(selectId)

    def insertLine(self):
        headerNameList = [self.treeviewFrame.tree.heading(col)["text"] for col in self.treeviewFrame.tree.cget("columns")]
        headerNameList.pop(0)

        if not self.treeviewFrame.tree.selection():
            selectId = None
            num = 0
        else:
            selectId = self.treeviewFrame.tree.selection()[0]
            selectItem = self.treeviewFrame.tree.set(selectId)
            num = int(selectItem["treeNum"]) + 1
        result = EditElse3ListWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["insertElse3Label"].format(self.text), self.decryptFile, "insert", headerNameList, None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.else3List.insert(num + result.insertPos, result.resultValueList)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(selectId)

    def deleteLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result:
            self.else3List.pop(num)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            if len(self.else3List) == 0:
                selectId = None
            self.reloadFunc(selectId)

    def copyLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        self.copyElse3Info = copy.deepcopy(self.else3List[num])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = PasteElse3ListDialog(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["pasteElse3InfoLabel"].format(self.text), self.decryptFile, num, self.copyElse3Info, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc(selectId)

    def listModify(self):
        if not self.treeviewFrame.tree.selection():
            return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        item = self.else3List[num]
        result = Else3ElementWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["editElse3ElementLabel"].format(self.text), self.decryptFile, num, item, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.reloadFunc(selectId)

    def else3ExtractCsv(self):
        filename = self.decryptFile.filename + "_else3.csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("else3_csv", "*.csv")])
        if file_path:
            try:
                else3CsvProcess.extractCsv(file_path, self.else3List)
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
            except PermissionError:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def else3LoadAndSaveCsv(self):
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("else3_csv", "*.csv")])
        if not file_path:
            return

        else3Obj, message = else3CsvProcess.loadCsv(file_path)
        if message:
            mb.showerror(title=textSetting.textList["error"], message=message)
            return

        msg = textSetting.textList["infoList"]["I15"].format(else3Obj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            else3List = else3Obj["data"]
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format("else3"))
            self.reloadFunc()


class EditElse3ListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, headerNameList, else3Info, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.headerNameList = headerNameList
        self.else3Info = else3Info
        self.railNoList = []
        self.insertPos = None
        self.resultValueList = []
        self.reloadFlag = False
        self.varList = []
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            else3InfoLabelList = copy.deepcopy(textSetting.textList["railEditor"]["editElse3LabelList"])
            self.railNoList = [x[0] for x in self.decryptFile.else3List]
        else:
            else3InfoLabelList = copy.deepcopy(textSetting.textList["railEditor"]["editElse3LsLabelList"])
        else3InfoLabelList.pop()

        for i, else3InfoLabel in enumerate(else3InfoLabelList):
            else3Lb = ttkCustomWidget.CustomTtkLabel(master, text=else3InfoLabel, font=textSetting.textList["font2"])
            else3Lb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                varElse3 = tkinter.IntVar()
                if self.mode == "modify":
                    varElse3.set(self.else3Info[i])
                self.varList.append(varElse3)
            else:
                varElse3 = tkinter.DoubleVar()
                if self.mode == "modify":
                    varElse3.set(self.else3Info[i])
                self.varList.append(varElse3)
            else3Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            else3Et.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(else3InfoLabelList) + 1)
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
                for i in range(len(self.varList)):
                    if self.decryptFile.game in ["BS", "CS", "RS"]:
                        try:
                            res = int(self.varList[i].get())
                            if i == 0:
                                isValidFlag = True
                                railNo = int(self.varList[i].get())
                                if self.mode == "modify":
                                    originRailNo = self.else3Info[0]
                                    if originRailNo != railNo and railNo in self.railNoList:
                                        isValidFlag = False
                                elif self.mode == "insert":
                                    if railNo in self.railNoList:
                                        isValidFlag = False

                                if not isValidFlag:
                                    if self.decryptFile.game in ["BS", "CS"]:
                                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E131"].format(railNo))
                                        return
                                    else:
                                        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["errorList"]["E132"].format(railNo), icon="warning")
                                        if not result:
                                            return

                                if res < 0:
                                    errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                                    return False
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                    else:
                        try:
                            res = float(self.varList[i].get())
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False

                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    if self.mode == "modify":
                        originTempList = self.else3Info[1]
                        self.resultValueList.append(originTempList)
                    else:
                        self.resultValueList.append([[0, 0, 0, 0, 0]])
                else:
                    if self.mode == "modify":
                        originTempList = self.else3Info[3]
                        self.resultValueList.append(originTempList)
                    else:
                        self.resultValueList.append([])

                if self.mode == "insert":
                    self.insertPos = 0
                    if self.insertCb.current() == 1:
                        self.insertPos = -1
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class PasteElse3ListDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, num, copyElse3Info, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.num = num
        self.copyElse3Info = copyElse3Info
        self.railNoList = [x[0] for x in self.decryptFile.else3List]
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
        successMsg = textSetting.textList["infoList"]["I79"]
        newRailNo = self.copyElse3Info[0]
        if self.decryptFile.game in ["BS", "CS"]:
            while newRailNo in self.railNoList:
                newRailNo -= 1
            if newRailNo < 0:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E133"])
                return
            self.copyElse3Info[0] = newRailNo
            successMsg += ("\n" + textSetting.textList["infoList"]["I140"].format(newRailNo))

        self.ok()
        self.reloadFlag = True
        self.decryptFile.else3List.insert(self.num, self.copyElse3Info)
        if not self.decryptFile.saveElse3List(self.decryptFile.else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=successMsg)

    def backInsert(self):
        successMsg = textSetting.textList["infoList"]["I79"]
        newRailNo = self.copyElse3Info[0]
        if self.decryptFile.game in ["BS", "CS"]:
            while newRailNo in self.railNoList:
                newRailNo += 1
            self.copyElse3Info[0] = newRailNo
            successMsg += ("\n" + textSetting.textList["infoList"]["I140"].format(newRailNo))

        self.ok()
        self.reloadFlag = True
        self.decryptFile.else3List.insert(self.num + 1, self.copyElse3Info)
        if not self.decryptFile.saveElse3List(self.decryptFile.else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=successMsg)


class Else3ElementWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, else3Num, item, rootFrameAppearance):
        self.master = master
        self.decryptFile = decryptFile
        self.else3Num = else3Num
        self.else3ElementList = item[-1]
        self.copyElse3ElementInfo = []
        self.resultValueList = []
        self.dirtyFlag = False
        self.varList = []
        self.rootFrameAppearance = rootFrameAppearance
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.text = textSetting.textList["railEditor"]["else3Label"]
        else:
            self.text = textSetting.textList["railEditor"]["camLabel"]

        mainFrame = ttkCustomWidget.CustomTtkFrame(master, width=720, height=360)
        mainFrame.pack()

        selectLbBtnFrame = ttkCustomWidget.CustomTtkFrame(mainFrame)
        selectLbBtnFrame.pack()

        selectLbFrame = ttkCustomWidget.CustomTtkFrame(selectLbBtnFrame)
        selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["railEditor"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.pack(side=tkinter.LEFT, padx=15, pady=15)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        selectEt.pack(side=tkinter.LEFT, padx=5, pady=15)

        btnFrame = ttkCustomWidget.CustomTtkFrame(selectLbBtnFrame)
        btnFrame.pack(padx=15)

        editLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonEditLineLabel"], width=25, state="disabled", command=self.editLine)
        editLineBtn.grid(row=0, column=0, padx=10, pady=10)

        self.insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonInsertLineLabel"], width=25, state="disabled", command=self.insertLine)
        self.insertLineBtn.grid(row=0, column=1, padx=10, pady=10)

        deleteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonDeleteLineLabel"], width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=10)

        copyLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonCopyLineLabel"], width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=10)

        self.pasteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonPasteLineLabel"], width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=10)

        self.treeFrame = ttkCustomWidget.CustomTtkFrame(mainFrame)
        self.treeFrame.pack(expand=True, fill=tkinter.BOTH)

        btnList = [
            editLineBtn,
            self.insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]

        self.treeviewFrame = ScrollbarTreeviewRailEditor(self.treeFrame, self.v_select, btnList)

        self.createElse3ElementTable()
        super().body(master)

    def createElse3ElementTable(self):
        self.setElse3ElementTableHeader()
        self.setElse3ElementTableData()
        if len(self.else3ElementList) == 0:
            self.insertLineBtn["state"] = "normal"

    def setElse3ElementTableHeader(self):
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            col_tuple = (
                "treeNum",
                "else3Type",
                "else3RailPos",
                "else3BinIndex",
                "else3Anime1",
                "else3Anime2"
            )
            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("else3Type", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("else3RailPos", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("else3BinIndex", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("else3Anime1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("else3Anime2", anchor=tkinter.CENTER, width=50)

            else3InfoLbList = textSetting.textList["railEditor"]["editElse3ElementLabelList"]
            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["else3Num"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("else3Type", text=else3InfoLbList[0], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("else3RailPos", text=else3InfoLbList[1], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("else3BinIndex", text=else3InfoLbList[2], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("else3Anime1", text=else3InfoLbList[3], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("else3Anime2", text=else3InfoLbList[4], anchor=tkinter.CENTER)
        else:
            col_tuple = (
                "treeNum",
                "listF1",
                "listF2",
                "listF3",
                "listTime",
                "listType"
            )
            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("listF1", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("listF2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("listF3", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("listTime", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("listType", anchor=tkinter.CENTER, width=50)

            else3LsInfoLbList = textSetting.textList["railEditor"]["editElse3LsElementLabelList"]
            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["else3Num"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("listF1", text=else3LsInfoLbList[0], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("listF2", text=else3LsInfoLbList[1], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("listF3", text=else3LsInfoLbList[2], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("listTime", text=else3LsInfoLbList[3], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("listType", text=else3LsInfoLbList[4], anchor=tkinter.CENTER)
        self.treeviewFrame.tree["displaycolumns"] = col_tuple

    def setElse3ElementTableData(self):
        for index, else3ElementInfo in enumerate(self.else3ElementList):
            data = (index,)
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                data += (else3ElementInfo[0], else3ElementInfo[1], else3ElementInfo[2], else3ElementInfo[3], else3ElementInfo[4])
            else:
                data += (else3ElementInfo[0], else3ElementInfo[1], else3ElementInfo[2], else3ElementInfo[3], else3ElementInfo[4])
            self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)

    def jumpToSelect(self, selectId):
        if selectId is not None:
            if selectId >= len(self.else3ElementList):
                selectId = len(self.else3ElementList) - 1
            self.treeviewFrame.tree.see(selectId)
            self.treeviewFrame.tree.selection_set(selectId)

    def clearTable(self):
        for item in self.treeviewFrame.tree.get_children():
            self.treeviewFrame.tree.delete(item)

    def reloadFunc(self, selectId=None):
        self.decryptFile = self.decryptFile.reload()
        self.else3ElementList = self.decryptFile.else3List[self.else3Num][-1]
        self.clearTable()
        self.setElse3ElementTableData()
        self.jumpToSelect(selectId)

    def editLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        headerNameList = [self.treeviewFrame.tree.heading(col)["text"] for col in self.treeviewFrame.tree.cget("columns")]
        headerNameList.pop(0)
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        item = self.else3ElementList[num]
        result = EditElse3ElementWidget(self.winfo_toplevel(), textSetting.textList["railEditor"]["editElse3ElementModifyLabel"].format(self.text), self.decryptFile, "modify", headerNameList, item, self.rootFrameAppearance)
        if result.reloadFlag:
            else3List = self.decryptFile.else3List
            else3List[self.else3Num][-1][num] = result.resultValueList
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(num)
            self.dirtyFlag = True

    def insertLine(self):
        headerNameList = [self.treeviewFrame.tree.heading(col)["text"] for col in self.treeviewFrame.tree.cget("columns")]
        headerNameList.pop(0)
        if not self.treeviewFrame.tree.selection():
            selectId = None
            num = 0
        else:
            selectId = self.treeviewFrame.tree.selection()[0]
            selectItem = self.treeviewFrame.tree.set(selectId)
            num = int(selectItem["treeNum"]) + 1
        result = EditElse3ElementWidget(self.winfo_toplevel(), textSetting.textList["railEditor"]["editElse3ElementInsertLabel"].format(self.text), self.decryptFile, "insert", headerNameList, None, self.rootFrameAppearance)
        if result.reloadFlag:
            else3List = self.decryptFile.else3List
            else3List[self.else3Num][-1].insert(num + result.insertPos, result.resultValueList)
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(num)
            self.dirtyFlag = True

    def deleteLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            if len(self.else3ElementList) == 1:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E93"].format(1))
                return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result:
            else3List = self.decryptFile.else3List
            else3List[self.else3Num][-1].pop(num)
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc()
            self.dirtyFlag = True

    def copyLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        self.copyElse3ElementInfo = copy.deepcopy(self.decryptFile.else3List[self.else3Num][-1][num])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        if not self.treeviewFrame.tree.selection():
            return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = PasteElse3ElementDialog(self.winfo_toplevel(), textSetting.textList["railEditor"]["pasteElse3InfoLabel"].format(self.text), self.decryptFile, self.else3Num, num, self.copyElse3ElementInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc(num)
            self.dirtyFlag = True


class EditElse3ElementWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, headerNameList, item, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.headerNameList = headerNameList
        self.else3Element = item
        self.insertPos = None
        self.resultValueList = []
        self.varList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i, else3ElementInfoLabel in enumerate(self.headerNameList):
            else3Lb = ttkCustomWidget.CustomTtkLabel(master, text=else3ElementInfoLabel, font=textSetting.textList["font2"])
            else3Lb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                varElse3 = tkinter.IntVar()
                self.varList.append(varElse3)
                if self.mode == "modify":
                    varElse3.set(self.else3Element[i])
            else:
                if i == 4:
                    varElse3 = tkinter.IntVar()
                else:
                    varElse3 = tkinter.DoubleVar()
                self.varList.append(varElse3)
                if self.mode == "modify":
                    varElse3.set(self.else3Element[i])
            else3Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            else3Et.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(self.headerNameList) + 1)
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
                for i in range(len(self.varList)):
                    if self.decryptFile.game in ["BS", "CS", "RS"]:
                        try:
                            res = int(self.varList[i].get())
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    else:
                        try:
                            if i == 4:
                                res = int(self.varList[i].get())
                            else:
                                res = float(self.varList[i].get())
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                        self.resultValueList.append(res)

                if self.mode == "insert":
                    self.insertPos = 0
                    if self.insertCb.current() == 1:
                        self.insertPos = -1
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class PasteElse3ElementDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, selectNum, num, copyElse3ElementInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.selectNum = selectNum
        self.num = num
        self.copyElse3ElementInfo = copyElse3ElementInfo
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
        else3List = self.decryptFile.else3List
        else3List[self.selectNum][-1].insert(self.num, self.copyElse3ElementInfo)
        if not self.decryptFile.saveElse3List(else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        else3List = self.decryptFile.else3List
        else3List[self.selectNum][-1].insert(self.num + 1, self.copyElse3ElementInfo)
        if not self.decryptFile.saveElse3List(else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
        self.reloadFlag = True
