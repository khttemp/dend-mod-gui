import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class Else3ListWidget:
    def __init__(self, root, frame, decryptFile, else3List, rootFrameAppearance, reloadFunc, selectId):
        self.text = textSetting.textList["railEditor"]["else3Label"]
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.else3List = else3List
        self.copyElse3Info = []
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        if self.decryptFile.game == "LS":
            self.text = textSetting.textList["railEditor"]["camLabel"]
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

        insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonInsertLineLabel"], width=25, state="disabled", command=self.insertLine)
        insertLineBtn.grid(row=0, column=1, padx=10, pady=15)

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
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn,
            listModifyBtn
        ]

        self.treeviewFrame = ScrollbarTreeviewRailEditor(elseLf, self.v_select, btnList)

        if len(self.else3List) == 0:
            insertLineBtn["state"] = "normal"

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

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for else3Info in self.else3List:
                data = (index,)
                data += (else3Info[0], len(else3Info[1]))
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1

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

            index = 0
            for else3Info in self.else3List:
                data = (index,)
                data += (else3Info[0], else3Info[1], else3Info[2], len(else3Info[3]))
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1

        if selectId is not None:
            if selectId >= len(self.else3List):
                selectId = len(self.else3List) - 1
            if selectId - 3 < 0:
                self.treeviewFrame.tree.see(0)
            else:
                self.treeviewFrame.tree.see(selectId - 3)
            self.treeviewFrame.tree.selection_set(selectId)

    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = EditElse3ListCntWidget(self.root, textSetting.textList["railEditor"]["editElse3Label"].format(self.text), "modify", self.decryptFile, selectItem, self.rootFrameAppearance)
        if result.reloadFlag:
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                self.else3List[num][0] = result.resultValueList[0]
            elif self.decryptFile.game == "LS":
                for j in range(3):
                    self.else3List[num][j] = result.resultValueList[j]

            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(selectId)

    def insertLine(self):
        noElse3InfoFlag = False
        if not self.treeviewFrame.tree.selection():
            noElse3InfoFlag = True
            selectId = None
            num = 0
            keyList = self.treeviewFrame.tree["columns"]
            selectItem = {}
            for key in keyList:
                selectItem[key] = None
        else:
            selectId = self.treeviewFrame.tree.selection()[0]
            selectItem = self.treeviewFrame.tree.set(selectId)
            num = int(selectItem["treeNum"])
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = EditElse3ListCntWidget(self.root, textSetting.textList["railEditor"]["insertElse3Label"].format(self.text), "insert", self.decryptFile, selectItem, self.rootFrameAppearance)
        if result.reloadFlag:
            if not noElse3InfoFlag:
                if result.insert == 0:
                    num += 1
            insertInfo = []
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                insertInfo.append(result.resultValueList[0])
                insertInfo.append([[0, 0, 0, 0, 0]])
            elif self.decryptFile.game == "LS":
                for j in range(3):
                    insertInfo.append(result.resultValueList[j])
                insertInfo.append([])

            self.else3List.insert(num, insertInfo)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(selectId)

    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        warnMsg = textSetting.textList["infoList"]["I9"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result:
            self.else3List.pop(num)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            if len(self.else3List) == 1:
                selectId = None
            self.reloadFunc(selectId)

    def copyLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])

        smfInfoKeyList = list(selectItem.keys())
        smfInfoKeyList.pop(0)
        copyList = []

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            key = smfInfoKeyList[0]
            copyList.append(int(selectItem[key]))
            copyList.append(self.else3List[num][-1])
        else:
            for i in range(len(smfInfoKeyList)):
                key = smfInfoKeyList[i]
                if i < len(smfInfoKeyList)-1:
                    copyList.append(float(selectItem[key]))
                else:
                    copyList.append(self.else3List[num][-1])

        self.copyElse3Info = copyList
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])

        result = PasteElse3ListDialog(self.root, textSetting.textList["railEditor"]["pasteElse3InfoLabel"].format(self.text), self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if result.insert == 0:
                num += 1
            self.else3List.insert(num, self.copyElse3Info)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(selectId)

    def listModify(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])

        result = Else3ElementListWidget(self.root, textSetting.textList["railEditor"]["editElse3ElementLabel"].format(self.text), self.text, num, self.decryptFile, self.else3List, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc(selectId)

    def else3ExtractCsv(self):
        filename = self.decryptFile.filename + "_else3.csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("else3_csv", "*.csv")])
        errorMsg = textSetting.textList["errorList"]["E7"]
        if file_path:
            try:
                w = open(file_path, "w")
                w.write("railNo,num,type,railPos,binIndex,anime1,anime2\n")
                for else3Info in self.decryptFile.else3List:
                    w.write("{0},{1},".format(else3Info[0], len(else3Info[1])))
                    for j in range(len(else3Info[1])):
                        if j != 0:
                            w.write(",,")
                        w.write(",".join([str(x) for x in else3Info[1][j]]))
                        w.write("\n")
                w.close()
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
            except PermissionError:
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)

    def else3LoadAndSaveCsv(self):
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("else3_csv", "*.csv")])
        if not file_path:
            return
        f = open(file_path)
        csvLines = f.readlines()
        f.close()

        else3List = []
        else3Info = []
        tempList = []
        csvLines.pop(0)
        firstReadFlag = True
        num = 0
        readNum = 0
        try:
            for i in range(len(csvLines)):
                csvLine = csvLines[i].strip()
                arr = csvLine.split(",")
                if len(arr) < 7:
                    errorMsg = textSetting.textList["errorList"]["E15"].format(i + 2)
                    mb.showerror(title=textSetting.textList["readError"], message=errorMsg)
                    return

                if firstReadFlag:
                    else3Info = []
                    if arr[0] == "" or arr[1] == "":
                        errorMsg = textSetting.textList["errorList"]["E15"].format(i + 2)
                        mb.showerror(title=textSetting.textList["readError"], message=errorMsg)
                        return
                    num = int(arr[1])
                    else3Info.append(int(arr[0]))
                    tempList = []
                    firstReadFlag = False
                else:
                    if arr[0] != "" or arr[1] != "":
                        errorMsg = textSetting.textList["errorList"]["E15"].format(i + 2)
                        mb.showerror(title=textSetting.textList["readError"], message=errorMsg)
                        return
                tempList.append([int(x) for x in arr[2:]])
                readNum += 1
                if readNum == num:
                    readNum = 0
                    num = 0
                    firstReadFlag = True
                    else3Info.append(tempList)
                    else3List.append(else3Info)

            if readNum != num:
                errorMsg = textSetting.textList["errorList"]["E92"].format(i + 2)
                mb.showerror(title=textSetting.textList["readError"], message=errorMsg)
                return

            msg = textSetting.textList["infoList"]["I15"].format(len(csvLines) + 1)
            result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")

            if result:
                if not self.decryptFile.saveElse3List(else3List):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format("else3"))
                self.reloadFunc()
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E14"]
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return


class EditElse3ListCntWidget(CustomSimpleDialog):
    def __init__(self, master, title, mode, decryptFile, selectItem, rootFrameAppearance):
        self.mode = mode
        self.decryptFile = decryptFile
        self.selectItem = selectItem
        self.varList = []
        self.resultValueList = []
        self.insert = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        else3InfoKeyList = list(self.selectItem.keys())
        else3InfoKeyList.pop(0)
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            else3InfoLbList = textSetting.textList["railEditor"]["editElse3LabelList"]
            for i in range(len(else3InfoKeyList)):
                else3Lb = ttkCustomWidget.CustomTtkLabel(master, text=else3InfoLbList[i], font=textSetting.textList["font2"])
                else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                key = else3InfoKeyList[i]
                varElse3 = tkinter.IntVar()
                if self.mode == "modify":
                    varElse3.set(self.selectItem[key])
                self.varList.append(varElse3)
                else3Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                if i == 1:
                    else3Et["state"] = "disabled"
                    varElse3.set(1)
        elif self.decryptFile.game == "LS":
            else3InfoLbList = textSetting.textList["railEditor"]["editElse3LsLabelList"]
            for i in range(len(else3InfoKeyList)):
                else3Lb = ttkCustomWidget.CustomTtkLabel(master, text=else3InfoLbList[i], font=textSetting.textList["font2"])
                else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                key = else3InfoKeyList[i]
                if i == 3:
                    varElse3 = tkinter.IntVar()
                else:
                    varElse3 = tkinter.DoubleVar()
                if self.mode == "modify":
                    varElse3.set(self.selectItem[key])
                self.varList.append(varElse3)
                else3Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                if i == 3:
                    else3Et["state"] = "disabled"

        if self.mode == "insert":
            self.setInsertWidget(master, len(else3InfoKeyList))
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
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    for i in range(len(self.varList)):
                        try:
                            res = int(self.varList[i].get())
                            if i == 0:
                                if res < 0:
                                    errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                                    return False
                                self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False

                    if self.mode == "insert":
                        self.insert = self.insertCb.current()
                    return True
                elif self.decryptFile.game == "LS":
                    for i in range(len(self.varList)):
                        try:
                            if i != 3:
                                res = float(self.varList[i].get())
                                self.resultValueList.append(res)
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False

                    if self.mode == "insert":
                        self.insert = self.insertCb.current()
                    return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class Else3ElementListWidget(CustomSimpleDialog):
    def __init__(self, master, title, text, else3Num, decryptFile, else3List, rootFrameAppearance):
        self.master = master
        self.text = text
        self.else3Num = else3Num
        self.decryptFile = decryptFile
        self.else3List = else3List
        self.else3ListInfo = else3List[else3Num][-1]
        self.copyElse3List = []
        self.btnList = []
        self.varList = []
        self.resultValueList = []
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
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

        insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonInsertLineLabel"], width=25, state="disabled", command=self.insertLine)
        insertLineBtn.grid(row=0, column=1, padx=10, pady=10)

        deleteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonDeleteLineLabel"], width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=10)

        copyLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonCopyLineLabel"], width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=10)

        self.pasteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["commonPasteLineLabel"], width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=10)

        self.treeFrame = ttkCustomWidget.CustomTtkFrame(mainFrame)
        self.treeFrame.pack(expand=True, fill=tkinter.BOTH)

        self.btnList = [
            editLineBtn,
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]

        self.setViewData()
        super().body(master)

    def setViewData(self):
        self.treeviewFrame = ScrollbarTreeviewRailEditor(self.treeFrame, self.v_select, self.btnList)
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

            index = 0
            for else3Info in self.else3ListInfo:
                data = (index,)
                data += (else3Info[0], else3Info[1], else3Info[2], else3Info[3], else3Info[4])
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1
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

            index = 0
            for else3Info in self.else3ListInfo:
                data = (index,)
                data += (else3Info[0], else3Info[1], else3Info[2], else3Info[3], else3Info[4])
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data)
                index += 1

        if len(self.else3ListInfo) == 0:
            self.btnList[1]["state"] = "normal"

    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = EditElse3ListWidget(self.master, textSetting.textList["railEditor"]["editElse3ElementModifyLabel"].format(self.text), "modify", self.decryptFile, selectItem, self.rootFrameAppearance)
        if result.reloadFlag:
            self.else3List[self.else3Num][-1][num] = result.resultValueList

            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(int(selectId))

    def insertLine(self):
        noElse3ListInfoFlag = False
        if not self.treeviewFrame.tree.selection():
            noElse3ListInfoFlag = True
            selectId = None
            num = 0
            keyList = self.treeviewFrame.tree["columns"]
            selectItem = {}
            for key in keyList:
                selectItem[key] = None
        else:
            selectId = self.treeviewFrame.tree.selection()[0]
            selectItem = self.treeviewFrame.tree.set(selectId)
            num = int(selectItem["treeNum"])
        result = EditElse3ListWidget(self.master, textSetting.textList["railEditor"]["editElse3ElementInsertLabel"].format(self.text), "insert", self.decryptFile, selectItem, self.rootFrameAppearance)
        if result.reloadFlag:
            if not noElse3ListInfoFlag:
                if result.insert == 0:
                    num += 1
            self.else3List[self.else3Num][-1].insert(num, result.resultValueList)

            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            if selectId is not None:
                self.reloadFunc(int(selectId))
            else:
                self.reloadFunc(None)

    def deleteLine(self):
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            if len(self.else3ListInfo) == 1:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E93"].format(1))
                return

        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        warnMsg = textSetting.textList["infoList"]["I9"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result:
            self.else3List[self.else3Num][-1].pop(num)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            if len(self.else3ListInfo) > 1:
                self.reloadFunc(int(selectId))
            else:
                self.reloadFunc(None)

    def copyLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])

        copyList = self.else3List[self.else3Num][-1][num]

        self.copyElse3List = copyList
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])

        result = PasteElse3ListDialog(self.master, textSetting.textList["railEditor"]["pasteElse3InfoLabel"].format(self.text), self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if result.insert == 0:
                num += 1
            self.else3List[self.else3Num][-1].insert(num, self.copyElse3List)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.text))
            self.reloadFunc(int(selectId))

    def reloadFunc(self, selectId):
        self.decryptFile = self.decryptFile.reload()
        self.else3List = self.decryptFile.else3List
        self.else3ListInfo = self.else3List[self.else3Num][-1]
        self.reloadFlag = True
        for child in self.treeFrame.winfo_children():
            child.destroy()

        self.setViewData()

        if selectId is not None:
            if selectId >= len(self.else3ListInfo):
                selectId = len(self.else3ListInfo) - 1
            if selectId - 3 < 0:
                self.treeviewFrame.tree.see(0)
            else:
                self.treeviewFrame.tree.see(selectId - 3)
            self.treeviewFrame.tree.selection_set(selectId)
        else:
            self.v_select.set("")
            for btn in self.btnList:
                btn["state"] = "disabled"
            self.btnList[1]["state"] = "normal"


class EditElse3ListWidget(CustomSimpleDialog):
    def __init__(self, master, title, mode, decryptFile, selectItem, rootFrameAppearance):
        self.mode = mode
        self.decryptFile = decryptFile
        self.selectItem = selectItem
        self.varList = []
        self.resultValueList = []
        self.insert = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        else3ElementListInfoKeyList = list(self.selectItem.keys())
        else3ElementListInfoKeyList.pop(0)
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            else3InfoLbList = textSetting.textList["railEditor"]["editElse3ElementLabelList"]
            for i in range(len(else3InfoLbList)):
                key = else3ElementListInfoKeyList[i]
                else3Lb = ttkCustomWidget.CustomTtkLabel(master, text=else3InfoLbList[i], font=textSetting.textList["font2"])
                else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                varElse3 = tkinter.IntVar()
                self.varList.append(varElse3)
                if self.mode == "modify":
                    varElse3.set(self.selectItem[key])
                else3Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        elif self.decryptFile.game == "LS":
            else3LsInfoLbList = textSetting.textList["railEditor"]["editElse3LsElementLabelList"]
            for i in range(len(else3LsInfoLbList)):
                key = else3ElementListInfoKeyList[i]
                else3Lb = ttkCustomWidget.CustomTtkLabel(master, text=else3LsInfoLbList[i], font=textSetting.textList["font2"])
                else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 4:
                    varElse3 = tkinter.IntVar()
                else:
                    varElse3 = tkinter.DoubleVar()
                self.varList.append(varElse3)
                if self.mode == "modify":
                    varElse3.set(self.selectItem[key])
                else3Et = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(else3ElementListInfoKeyList))
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
                if self.mode == "insert":
                    self.insert = self.insertCb.current()

                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    for i in range(len(self.varList)):
                        try:
                            res = int(self.varList[i].get())
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    return True
                elif self.decryptFile.game == "LS":
                    for i in range(len(self.varList)):
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
                    return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class PasteElse3ListDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.insert = 0
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
        self.insert = 1
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        self.insert = 0
        self.reloadFlag = True
