import copy
import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class SmfListWidget:
    def __init__(self, frame, decryptFile, smfList, reloadFunc, selectId):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = smfList
        self.reloadFunc = reloadFunc
        self.copySmfInfo = []

        self.swfListLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["smfInfoLabel"])
        self.swfListLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        self.headerFrame = ttk.Frame(self.swfListLf)
        self.headerFrame.pack()

        self.selectLbFrame = ttk.Frame(self.headerFrame)
        self.selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        selectLb = ttk.Label(self.selectLbFrame, text=textSetting.textList["railEditor"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.pack(side=tkinter.LEFT, padx=15, pady=15)

        self.v_select = tkinter.StringVar()
        selectEt = ttk.Entry(self.selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        selectEt.pack(side=tkinter.LEFT, padx=5, pady=15)

        self.btnFrame = ttk.Frame(self.headerFrame)
        self.btnFrame.pack(anchor=tkinter.NE, padx=15)

        editLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonEditLineLabel"], width=25, state="disabled", command=self.editLine)
        editLineBtn.grid(row=0, column=0, padx=10, pady=15)

        insertLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonInsertLineLabel"], width=25, state="disabled", command=self.insertLine)
        insertLineBtn.grid(row=0, column=1, padx=10, pady=15)

        deleteLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonDeleteLineLabel"], width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=15)

        copyLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonCopyLineLabel"], width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=15)

        self.pasteLineBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["commonPasteLineLabel"], width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=15)

        if self.decryptFile.game in ["LS", "BS"]:
            self.listModifyBtn = ttk.Button(self.btnFrame, text=textSetting.textList["railEditor"]["editSmfElementListLabel"], width=25, state="disabled", command=self.listModify)
            self.listModifyBtn.grid(row=1, column=2, padx=10, pady=15)

        btnList = [
            editLineBtn,
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]
        if self.decryptFile.game in ["LS", "BS"]:
            btnList.append(self.listModifyBtn)

        useModelListObj = self.getUseModelList()

        self.treeviewFrame = ScrollbarTreeviewRailEditor(self.swfListLf, self.v_select, btnList)

        if len(self.smfList) == 0:
            insertLineBtn["state"] = "normal"

        style = ttk.Style()
        style.map("Treeview", foreground=self.fixed_map(style, "foreground"), background=self.fixed_map(style, "background"))

        if self.decryptFile.game in ["CS", "RS"]:
            col_tuple = (
                "treeNum",
                "smfInfoName",
                "smfInfoFlag1",
                "smfInfoFlag2",
                "smfInfoLength",
                "smfInfoMesh1",
                "smfInfoMesh2",
                "smfInfoKasenchuNo",
                "smfInfoKasenNo"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("smfInfoName", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("smfInfoFlag1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoFlag2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoLength", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoMesh1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoMesh2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoKasenchuNo", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoKasenNo", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["smfInfoNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoName", text=textSetting.textList["railEditor"]["smfInfoName"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoFlag1", text=textSetting.textList["railEditor"]["smfInfoFlag1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoFlag2", text=textSetting.textList["railEditor"]["smfInfoFlag2"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoLength", text=textSetting.textList["railEditor"]["smfInfoLength"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoMesh1", text=textSetting.textList["railEditor"]["smfInfoMesh1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoMesh2", text=textSetting.textList["railEditor"]["smfInfoMesh2"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoKasenchuNo", text=textSetting.textList["railEditor"]["smfInfoKasenchuNo"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoKasenNo", text=textSetting.textList["railEditor"]["smfInfoKasenNo"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for smfInfo in self.smfList:
                data = (index,)
                tags = "used"
                if smfInfo[0] not in useModelListObj["rail"] and smfInfo[0] not in useModelListObj["amb"]:
                    tags = "notUse"
                elif smfInfo[0] in useModelListObj["rail"] and smfInfo[0] in useModelListObj["amb"]:
                    tags = "allUse"
                elif smfInfo[0] in useModelListObj["rail"]:
                    tags = "rail"
                else:
                    tags = "amb"
                data += (smfInfo[0], self.toHex(smfInfo[1]), self.toHex(smfInfo[2]), smfInfo[3], smfInfo[4], smfInfo[5])
                data += (smfInfo[6], smfInfo[7])
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data, tags=tags)
                index += 1
        elif self.decryptFile.game == "BS":
            col_tuple = (
                "treeNum",
                "smfInfoName",
                "smfInfoLength",
                "smfInfoMesh1",
                "smfInfoMesh2",
                "smfInfoElementList"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("smfInfoName", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("smfInfoLength", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoMesh1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoMesh2", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoElementList", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["smfInfoNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoName", text=textSetting.textList["railEditor"]["smfInfoName"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoLength", text=textSetting.textList["railEditor"]["smfInfoLength"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoMesh1", text=textSetting.textList["railEditor"]["smfInfoMesh1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoMesh2", text=textSetting.textList["railEditor"]["smfInfoMesh2"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoElementList", text=textSetting.textList["railEditor"]["smfInfoElementList"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for smfInfo in self.smfList:
                data = (index,)
                tags = "used"
                if smfInfo[0] not in useModelListObj["rail"] and smfInfo[0] not in useModelListObj["amb"]:
                    tags = "notUse"
                elif smfInfo[0] in useModelListObj["rail"] and smfInfo[0] in useModelListObj["amb"]:
                    tags = "allUse"
                elif smfInfo[0] in useModelListObj["rail"]:
                    tags = "rail"
                else:
                    tags = "amb"
                data += (smfInfo[0], smfInfo[1], smfInfo[2], smfInfo[3], len(smfInfo[4]))
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data, tags=tags)
                index += 1
        else:
            col_tuple = (
                "treeNum",
                "smfInfoName",
                "smfInfoLength",
                "smfInfoE1",
                "smfInfoElementList"
            )

            self.treeviewFrame.tree["columns"] = col_tuple
            self.treeviewFrame.tree.column("#0", width=0, stretch=False)
            self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
            self.treeviewFrame.tree.column("smfInfoName", anchor=tkinter.CENTER, width=130)
            self.treeviewFrame.tree.column("smfInfoLength", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoE1", anchor=tkinter.CENTER, width=50)
            self.treeviewFrame.tree.column("smfInfoElementList", anchor=tkinter.CENTER, width=50)

            self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["smfInfoNum"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoName", text=textSetting.textList["railEditor"]["smfInfoName"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoLength", text=textSetting.textList["railEditor"]["smfInfoLength"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoE1", text=textSetting.textList["railEditor"]["smfInfoE1"], anchor=tkinter.CENTER)
            self.treeviewFrame.tree.heading("smfInfoElementList", text=textSetting.textList["railEditor"]["smfInfoElementList"], anchor=tkinter.CENTER)

            self.treeviewFrame.tree["displaycolumns"] = col_tuple

            index = 0
            for smfInfo in self.smfList:
                data = (index,)
                tags = "used"
                if smfInfo[0] not in useModelListObj["rail"] and smfInfo[0] not in useModelListObj["amb"]:
                    tags = "notUse"
                elif smfInfo[0] in useModelListObj["rail"] and smfInfo[0] in useModelListObj["amb"]:
                    tags = "allUse"
                elif smfInfo[0] in useModelListObj["rail"]:
                    tags = "rail"
                else:
                    tags = "amb"

                if len(smfInfo[3]) == 0:
                    data += (smfInfo[0], smfInfo[1], smfInfo[2], -1)
                else:
                    data += (smfInfo[0], smfInfo[1], smfInfo[2], len(smfInfo[3]))
                self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data, tags=tags)
                index += 1

        self.treeviewFrame.tree.tag_configure("notUse", background="#CCCCCC")
        self.treeviewFrame.tree.tag_configure("rail", background="#FFC8C8")
        self.treeviewFrame.tree.tag_configure("amb", background="#C8FFFF")

        if selectId is not None:
            if selectId >= len(self.smfList):
                selectId = len(self.smfList) - 1
            if selectId - 3 < 0:
                self.treeviewFrame.tree.see(0)
            else:
                self.treeviewFrame.tree.see(selectId - 3)
            self.treeviewFrame.tree.selection_set(selectId)

    def toHex(self, num):
        return "0x{0:02x}".format(num)

    def fixed_map(self, style, option):
        return [elm for elm in style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]

    def getUseModelList(self):
        mdlInfoObj = {}
        railMdlSet = set()
        ambMdlSet = set()

        mdlNo = None
        kasenchuNo = None
        kasenNo = None
        for rail in self.decryptFile.railList:
            if len(rail) < 15:
                continue

            if self.decryptFile.game == "LS":
                offset = 0
                if self.decryptFile.ver == "DEND_MAP_VER0101":
                    offset = 2
                mdlNo = rail[7 + offset]
            else:
                mdlNo = rail[6]

            if len(self.decryptFile.smfList) > mdlNo:
                mdlName = self.decryptFile.smfList[mdlNo][0]
                railMdlSet.add(mdlName)

            if self.decryptFile.game == "LS":
                offset = 0
                if self.decryptFile.ver == "DEND_MAP_VER0101":
                    offset = 2
                if rail[8 + offset] == -1:
                    kasenchuNo = rail[12 + offset]
                    kasenNo = rail[13 + offset]
                    fixAmbNo = rail[14 + offset]
                else:
                    kasenchuNo = rail[9 + offset]
                    kasenNo = rail[10 + offset]
                    fixAmbNo = rail[11 + offset]

                if kasenchuNo != -1:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
                if kasenNo != -1:
                    if len(self.decryptFile.smfList) > kasenNo:
                        kasenName = self.decryptFile.smfList[kasenNo][0]
                        railMdlSet.add(kasenName)
                if fixAmbNo != -1:
                    if len(self.decryptFile.smfList) > fixAmbNo:
                        fixAmbName = self.decryptFile.smfList[fixAmbNo][0]
                        ambMdlSet.add(fixAmbName)
            elif self.decryptFile.game == "BS":
                kasenNo = rail[7]
                kasenchuNo = rail[8]
                if kasenchuNo != -1:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
                if kasenNo != -1:
                    if len(self.decryptFile.smfList) > kasenNo:
                        kasenName = self.decryptFile.smfList[kasenNo][0]
                        railMdlSet.add(kasenName)
            else:
                kasenNo = rail[7]
                if kasenNo != -1 and len(self.decryptFile.smfList) > kasenNo:
                    kasenName = self.decryptFile.smfList[kasenNo][0]
                    railMdlSet.add(kasenName)

                kasenchuNo = rail[8]
                if kasenchuNo == -2:
                    pass
                elif kasenchuNo == -1:
                    if len(self.decryptFile.smfList) > mdlNo:
                        kasenchuNo = self.decryptFile.smfList[mdlNo][-2]
                        if kasenchuNo != 255:
                            if len(self.decryptFile.smfList) > kasenchuNo:
                                kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                                railMdlSet.add(kasenchuName)

                        kasenNo = self.decryptFile.smfList[mdlNo][-1]
                        if kasenNo != 255:
                            if len(self.decryptFile.smfList) > kasenNo:
                                kasenName = self.decryptFile.smfList[kasenNo][0]
                                railMdlSet.add(kasenName)
                else:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
        mdlInfoObj["rail"] = railMdlSet

        for amb in self.decryptFile.ambList:
            if self.decryptFile.game == "LS":
                if len(amb) > 3:
                    ambMdlNo = amb[3]
                    if ambMdlNo != 0:
                        if len(self.decryptFile.smfList) > ambMdlNo:
                            ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                            ambMdlSet.add(ambMdlName)
            elif self.decryptFile.game == "BS":
                if len(amb) > 3:
                    ambMdlNo = amb[3]
                    if ambMdlNo >= 0 and len(self.decryptFile.smfList) > ambMdlNo:
                        ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                        ambMdlSet.add(ambMdlName)
            else:
                if len(amb) > 23:
                    ambMdlNo = amb[12]
                    if len(self.decryptFile.smfList) > ambMdlNo:
                        ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                        ambMdlSet.add(ambMdlName)

                    childcnt = amb[12 + 11]
                    for i in range(childcnt):
                        ambMdlNo = amb[24 + i*11]
                        if len(self.decryptFile.smfList) > ambMdlNo:
                            ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                            ambMdlSet.add(ambMdlName)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            for else3Info in self.decryptFile.else3List:
                for j in range(len(else3Info[1])):
                    tempList = else3Info[1][j]
                    if tempList[3] == -1:
                        ambMdlName = self.decryptFile.smfList[tempList[4]][0]
                        ambMdlSet.add(ambMdlName)
        mdlInfoObj["amb"] = ambMdlSet

        return mdlInfoObj

    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        result = EditSmfListWidget(self.frame, textSetting.textList["railEditor"]["modifySmfInfo"], self.decryptFile, "modify", num, selectItem)
        if result.reloadFlag:
            if not self.decryptFile.saveSmfInfo(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
            self.reloadFunc(selectId)

    def insertLine(self):
        noSmfInfoFlag = False
        if not self.treeviewFrame.tree.selection():
            noSmfInfoFlag = True
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
        result = EditSmfListWidget(self.frame, textSetting.textList["railEditor"]["insertSmfInfo"], self.decryptFile, "insert", num, selectItem)
        if result.reloadFlag:
            if not noSmfInfoFlag:
                if result.insert == 0:
                    num += 1
            if not self.decryptFile.saveSmfInfo(num, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
            self.reloadFunc(selectId)

    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["treeNum"])
        warnMsg = textSetting.textList["infoList"]["I9"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.saveSmfInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
            if len(self.smfList) == 1:
                selectId = None
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
                elif i in [1, 2]:
                    copyList.append(int(selectItem[key], 16))
                else:
                    copyList.append(int(selectItem[key]))
        elif self.decryptFile.game == "BS":
            for i in range(len(smfInfoKeyList)):
                key = smfInfoKeyList[i]
                if i == 0:
                    copyList.append(selectItem[key])
                elif i in [1, 2, 3]:
                    copyList.append(int(selectItem[key]))
                else:
                    tempInfo = self.smfList[int(selectId)][4]
                    copyList.append(tempInfo)
        else:
            for i in range(len(smfInfoKeyList)):
                key = smfInfoKeyList[i]
                if i == 0:
                    copyList.append(selectItem[key])
                elif i in [1, 2]:
                    copyList.append(int(selectItem[key]))
                else:
                    tempInfo = self.smfList[int(selectId)][3]
                    copyList.append(tempInfo)
        self.copySmfInfo = copyList
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteSmfListDialog(self.frame, textSetting.textList["railEditor"]["pasteSmfInfo"], self.decryptFile, int(selectItem["treeNum"]), self.copySmfInfo)
        if result.reloadFlag:
            self.reloadFunc(selectId)

    def listModify(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        originTempList = self.decryptFile.smfList[int(selectId)][-1]
        result = EditListElement(self.frame, textSetting.textList["railEditor"]["editSmfElementList"], self.decryptFile, originTempList)
        if result.reloadFlag:
            if not self.decryptFile.saveSmfListElement(int(selectId), result.tempList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I80"])
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
            modelFlagList = textSetting.textList["railEditor"]["modelFlagList"]
            for i in range(len(smfInfoKeyList)):
                self.smfInfoLb = ttk.Label(master, text=textSetting.textList["railEditor"][smfInfoKeyList[i]], font=textSetting.textList["font2"])
                self.smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varSmfInfo = tkinter.StringVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=textSetting.textList["font2"])
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                elif i in [1, 2]:
                    mb = ttk.Menubutton(master, text=textSetting.textList["railEditor"]["setSmfSwitch"])
                    menu = tkinter.Menu(mb, tearoff=0)
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
                    menu.add_checkbutton(label=modelFlagList[i - 1][7], variable=Flg7)
                    menu.add_checkbutton(label=modelFlagList[i - 1][6], variable=Flg6)
                    menu.add_checkbutton(label=modelFlagList[i - 1][5], variable=Flg5)
                    menu.add_checkbutton(label=modelFlagList[i - 1][4], variable=Flg4)
                    menu.add_checkbutton(label=modelFlagList[i - 1][3], variable=Flg3)
                    menu.add_checkbutton(label=modelFlagList[i - 1][2], variable=Flg2)
                    menu.add_checkbutton(label=modelFlagList[i - 1][1], variable=Flg1)
                    menu.add_checkbutton(label=modelFlagList[i - 1][0], variable=Flg0)
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
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=textSetting.textList["font2"])
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
                self.smfInfoLb = ttk.Label(master, text=smfInfoKeyList[i], font=textSetting.textList["font2"])
                self.smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varSmfInfo = tkinter.StringVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=textSetting.textList["font2"])
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                else:
                    self.varSmfInfo = tkinter.IntVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=textSetting.textList["font2"])
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        if i == 1:
                            default = 8
                        else:
                            default = 255
                        self.varSmfInfo.set(default)
        else:
            smfInfoKeyList.pop()
            for i in range(len(smfInfoKeyList)):
                self.smfInfoLb = ttk.Label(master, text=smfInfoKeyList[i], font=textSetting.textList["font2"])
                self.smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varSmfInfo = tkinter.StringVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=textSetting.textList["font2"])
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                else:
                    self.varSmfInfo = tkinter.IntVar()
                    self.varList.append(self.varSmfInfo)
                    self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=textSetting.textList["font2"])
                    self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        if i == 1:
                            default = 8
                        else:
                            default = 255
                        self.varSmfInfo.set(default)

        if self.mode == "insert":
            self.setInsertWidget(master, len(smfInfoKeyList))

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text=textSetting.textList["railEditor"]["posLabel"], font=textSetting.textList["font2"])
        self.insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["railEditor"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                if self.decryptFile.game in ["CS", "RS"]:
                    try:
                        for i in range(len(self.varList)):
                            if i == 0:
                                res = self.varList[i].get()
                            elif i in [1, 2]:
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
                        errorMsg = textSetting.textList["errorList"]["E60"]
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
                elif self.decryptFile.game == "BS":
                    try:
                        for i in range(len(self.varList)):
                            if i == 0:
                                res = self.varList[i].get()
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
                        errorMsg = textSetting.textList["errorList"]["E60"]
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
                else:
                    try:
                        for i in range(len(self.varList)):
                            if i == 0:
                                res = self.varList[i].get()
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
                        errorMsg = textSetting.textList["errorList"]["E60"]
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

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
        self.posLb = ttk.Label(master, text=textSetting.textList["infoList"]["I4"], font=textSetting.textList["font2"])
        self.posLb.pack(padx=10, pady=10)

    def buttonbox(self):
        box = tkinter.Frame(self, padx=5, pady=5)
        self.frontBtn = tkinter.Button(box, text=textSetting.textList["railEditor"]["pasteFront"], font=textSetting.textList["font2"], width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = tkinter.Button(box, text=textSetting.textList["railEditor"]["pasteBack"], font=textSetting.textList["font2"], width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = tkinter.Button(box, text=textSetting.textList["railEditor"]["pasteCancel"], font=textSetting.textList["font2"], width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)
        box.pack()

    def frontInsert(self):
        self.ok()
        if not self.decryptFile.saveSmfInfo(self.num, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        if not self.decryptFile.saveSmfInfo(self.num + 1, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
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

        self.modifyBtn = tkinter.Button(self.btnFrame, font=textSetting.textList["font2"], text=textSetting.textList["modify"], state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=textSetting.textList["font2"], text=textSetting.textList["insert"], state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=textSetting.textList["font2"], text=textSetting.textList["delete"], state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.listFrame = ttk.Frame(self.frame)
        self.listFrame.pack()

        copyTempList = self.setListboxInfo(self.tempList)
        self.v_tempList = tkinter.StringVar(value=copyTempList)
        self.tempListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=textSetting.textList["font2"], width=25, listvariable=self.v_tempList)
        self.tempListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.tempListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.tempListListbox, self.tempListListbox.curselection()))

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["railEditor"]["noList"]:
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
            copyTempList = [textSetting.textList["railEditor"]["noList"]]

        return copyTempList

    def modify(self):
        result = EditListElementWidget(self.frame, textSetting.textList["railEditor"]["modifySmfElementListLabel"], self.decryptFile, "modify", self.selectIndexNum, self.tempList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.tempList[self.selectIndexNum] = result.resultValueList
            copyTempList = self.setListboxInfo(self.tempList)
            self.v_tempList.set(copyTempList)

    def insert(self):
        result = EditListElementWidget(self.frame, textSetting.textList["railEditor"]["insertSmfElementListLabel"], self.decryptFile, "insert", self.selectIndexNum, self.tempList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.tempList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
            copyTempList = self.setListboxInfo(self.tempList)
            self.v_tempList.set(copyTempList)

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
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
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I70"], parent=self)
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
            tempInfoLb = textSetting.textList["railEditor"]["smfElementListLabel1"]
        else:
            tempInfoLb = textSetting.textList["railEditor"]["smfElementListLabel2"]
        for i in range(len(tempInfoLb)):
            self.tempLb = ttk.Label(master, text=tempInfoLb[i], font=textSetting.textList["font2"])
            self.tempLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.varTemp = tkinter.IntVar()
            if self.mode == "modify":
                tempInfo = self.tempList[self.index]
                self.varTemp.set(tempInfo[i])
            self.varList.append(self.varTemp)
            self.tempEt = ttk.Entry(master, textvariable=self.varTemp, font=textSetting.textList["font2"])
            self.tempEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(tempInfoLb))

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text=textSetting.textList["railEditor"]["posLabel"], font=textSetting.textList["font2"])
        self.insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["railEditor"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        infoMsg = textSetting.textList["infoList"]["I21"]
        if self.mode == "insert":
            infoMsg = textSetting.textList["infoList"]["I71"]
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=infoMsg, parent=self)
        if result:
            try:
                for i in range(len(self.varList)):
                    try:
                        res = int(self.varList[i].get())
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
        self.dirtyFlag = True
