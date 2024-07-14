import copy
import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from program.railEditor.importPy.tkinterScrollbarTreeviewRailEditor import ScrollbarTreeviewRailEditor


class SmfListWidget:
    def __init__(self, root, frame, decryptFile, smfList, rootFrameAppearance, reloadFunc, selectId):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = smfList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.copySmfInfo = []

        swfListLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["smfInfoLabel"])
        swfListLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.BOTH, expand=True)

        headerFrame = ttkCustomWidget.CustomTtkFrame(swfListLf)
        headerFrame.pack()

        selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, pady=10)

        selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["railEditor"]["selectNum"], font=textSetting.textList["font2"])
        selectLb.grid(columnspan=2, row=0, column=0)

        self.v_select = tkinter.StringVar()
        selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_select, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        selectEt.grid(row=0, column=2, pady=5)

        self.v_railLb = tkinter.StringVar(value="")
        usedRailLb = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_railLb, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        usedRailLb.grid(row=1, column=1, pady=(15, 0))

        self.v_ambLb = tkinter.StringVar(value="")
        usedAmbLb = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=self.v_ambLb, font=textSetting.textList["font2"], width=5, state="readonly", justify="center")
        usedAmbLb.grid(row=1, column=2, pady=(15, 0))

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

        if self.decryptFile.game in ["LSTrial", "LS", "BS"]:
            listModifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["railEditor"]["editSmfElementListLabel"], width=25, state="disabled", command=self.listModify)
            listModifyBtn.grid(row=1, column=2, padx=10, pady=15)

        btnList = [
            editLineBtn,
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]
        if self.decryptFile.game in ["LSTrial", "LS", "BS"]:
            btnList.append(listModifyBtn)

        useModelListObj = self.getUseModelList()

        self.treeviewFrame = ScrollbarTreeviewRailEditor(swfListLf, self.v_select, btnList, self.customSelectFunc)

        if len(self.smfList) == 0:
            insertLineBtn["state"] = "normal"

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
        elif self.decryptFile.game in ["LSTrial", "LS"]:
            if self.decryptFile.game == "LS" or (self.decryptFile.game == "LSTrial" and self.decryptFile.readFlag):
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
            else:
                col_tuple = (
                    "treeNum",
                    "smfInfoName",
                    "smfInfoLength",
                    "smfInfoElementList"
                )
                self.treeviewFrame.tree["columns"] = col_tuple
                self.treeviewFrame.tree.column("#0", width=0, stretch=False)
                self.treeviewFrame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, stretch=False)
                self.treeviewFrame.tree.column("smfInfoName", anchor=tkinter.CENTER, width=130)
                self.treeviewFrame.tree.column("smfInfoLength", anchor=tkinter.CENTER, width=50)
                self.treeviewFrame.tree.column("smfInfoElementList", anchor=tkinter.CENTER, width=50)

                self.treeviewFrame.tree.heading("treeNum", text=textSetting.textList["railEditor"]["smfInfoNum"], anchor=tkinter.CENTER)
                self.treeviewFrame.tree.heading("smfInfoName", text=textSetting.textList["railEditor"]["smfInfoName"], anchor=tkinter.CENTER)
                self.treeviewFrame.tree.heading("smfInfoLength", text=textSetting.textList["railEditor"]["smfInfoLength"], anchor=tkinter.CENTER)
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

                    if len(smfInfo[2]) == 0:
                        data += (smfInfo[0], smfInfo[1], -1)
                    else:
                        data += (smfInfo[0], smfInfo[1], len(smfInfo[2]))
                    self.treeviewFrame.tree.insert(parent="", index="end", iid=index, values=data, tags=tags)
                    index += 1

        self.treeviewFrame.tree.tag_configure("notUse", background="#CCCCCC", foreground="black")
        self.treeviewFrame.tree.tag_configure("rail", background="#FFC8C8", foreground="black")
        self.treeviewFrame.tree.tag_configure("amb", background="#C8FFFF", foreground="black")

        if selectId is not None:
            if selectId >= len(self.smfList):
                selectId = len(self.smfList) - 1
            if selectId - 3 < 0:
                self.treeviewFrame.tree.see(0)
            else:
                self.treeviewFrame.tree.see(selectId - 3)
            self.treeviewFrame.tree.selection_set(selectId)

    def customSelectFunc(self):
        if len(self.treeviewFrame.tree.selection()) > 0:
            selectId = self.treeviewFrame.tree.selection()[0]
            selectItem = self.treeviewFrame.tree.item(selectId)
            tagName = selectItem["tags"][0]
            if tagName == "notUse":
                self.v_railLb.set("")
                self.v_ambLb.set("")
            elif tagName == "allUse":
                self.v_railLb.set(textSetting.textList["railEditor"]["usedRail"])
                self.v_ambLb.set(textSetting.textList["railEditor"]["usedAmb"])
            elif tagName == "rail":
                self.v_railLb.set(textSetting.textList["railEditor"]["usedRail"])
                self.v_ambLb.set("")
            elif tagName == "amb":
                self.v_railLb.set("")
                self.v_ambLb.set(textSetting.textList["railEditor"]["usedAmb"])

    def toHex(self, num):
        return "0x{0:02x}".format(num)

    def getUseModelList(self):
        mdlInfoObj = {}
        railMdlSet = set()
        ambMdlSet = set()

        # rail
        for rail in self.decryptFile.railList:
            if self.decryptFile.game != "LSTrial" and len(rail) < 15:
                continue

            if self.decryptFile.game == "LSTrial":
                if self.decryptFile.oldFlag:
                    mdlNo = rail[9]
                    if len(self.decryptFile.smfList) > mdlNo:
                        mdlName = self.decryptFile.smfList[mdlNo][0]
                        railMdlSet.add(mdlName)

                    kasenNo = rail[10]
                    if kasenNo != -1:
                        if len(self.decryptFile.smfList) > kasenNo:
                            kasenName = self.decryptFile.smfList[kasenNo][0]
                            railMdlSet.add(kasenName)
                else:
                    mdlNo = rail[7]
                    if len(self.decryptFile.smfList) > mdlNo:
                        mdlName = self.decryptFile.smfList[mdlNo][0]
                        railMdlSet.add(mdlName)

                    offset = 0
                    if self.decryptFile.readFlag or self.decryptFile.filenameNum == 7:
                        if rail[8] == -1:
                            offset = 3
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
            elif self.decryptFile.game == "LS":
                offset = 0
                if self.decryptFile.ver == "DEND_MAP_VER0101":
                    offset = 2
                mdlNo = rail[7 + offset]
                if len(self.decryptFile.smfList) > mdlNo:
                    mdlName = self.decryptFile.smfList[mdlNo][0]
                    railMdlSet.add(mdlName)

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
                mdlNo = rail[6]
                if len(self.decryptFile.smfList) > mdlNo:
                    mdlName = self.decryptFile.smfList[mdlNo][0]
                    railMdlSet.add(mdlName)

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
                mdlNo = rail[6]
                if len(self.decryptFile.smfList) > mdlNo:
                    mdlName = self.decryptFile.smfList[mdlNo][0]
                    railMdlSet.add(mdlName)

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
        if self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag:
            for amb in self.decryptFile.ambList:
                kasenchuNo = amb[10]
                if kasenchuNo != -1:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
        mdlInfoObj["rail"] = railMdlSet

        # amb
        for amb in self.decryptFile.ambList:
            if self.decryptFile.game == "LSTrial":
                if self.decryptFile.oldFlag:
                    leftAmbMdlNo = amb[8]
                    rightAmbMdlNo = amb[9]
                    fixAmbMdlNo = amb[11]
                    if leftAmbMdlNo != -1:
                        if len(self.decryptFile.smfList) > leftAmbMdlNo:
                            kasenName = self.decryptFile.smfList[leftAmbMdlNo][0]
                            ambMdlSet.add(kasenName)
                    if rightAmbMdlNo != -1:
                        if len(self.decryptFile.smfList) > rightAmbMdlNo:
                            kasenName = self.decryptFile.smfList[rightAmbMdlNo][0]
                            ambMdlSet.add(kasenName)
                    if fixAmbMdlNo != -1:
                        if len(self.decryptFile.smfList) > fixAmbMdlNo:
                            kasenName = self.decryptFile.smfList[fixAmbMdlNo][0]
                            ambMdlSet.add(kasenName)
                else:
                    if len(amb) > 3:
                        ambMdlNo = amb[3]
                        if ambMdlNo != 0:
                            if len(self.decryptFile.smfList) > ambMdlNo:
                                ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                                ambMdlSet.add(ambMdlName)
            elif self.decryptFile.game == "LS":
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
        result = EditSmfListWidget(self.root, textSetting.textList["railEditor"]["modifySmfInfo"], self.decryptFile, "modify", num, selectItem, self.rootFrameAppearance)
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
        result = EditSmfListWidget(self.root, textSetting.textList["railEditor"]["insertSmfInfo"], self.decryptFile, "insert", num, selectItem, self.rootFrameAppearance)
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
        elif self.decryptFile.game in ["LSTrial", "LS"]:
            for i in range(len(smfInfoKeyList)):
                key = smfInfoKeyList[i]
                if self.decryptFile.game == "LS" or (self.decryptFile.game == "LSTrial" and self.decryptFile.readFlag):
                    if i == 0:
                        copyList.append(selectItem[key])
                    elif i in [1, 2]:
                        copyList.append(int(selectItem[key]))
                    else:
                        tempInfo = self.smfList[int(selectId)][3]
                        copyList.append(tempInfo)
                else:
                    if i == 0:
                        copyList.append(selectItem[key])
                    elif i == 1:
                        copyList.append(int(selectItem[key]))
                    else:
                        tempInfo = self.smfList[int(selectId)][2]
                        copyList.append(tempInfo)
        self.copySmfInfo = copyList
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteSmfListDialog(self.root, textSetting.textList["railEditor"]["pasteSmfInfo"], self.decryptFile, int(selectItem["treeNum"]), self.copySmfInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.reloadFunc(selectId)

    def listModify(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        originTempList = self.decryptFile.smfList[int(selectId)][-1]
        result = EditListElement(self.root, textSetting.textList["railEditor"]["editSmfElementList"], self.decryptFile, originTempList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveSmfListElement(int(selectId), result.tempList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I80"])
            self.reloadFunc(selectId)


class EditSmfListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, num, smfInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.smfInfo = smfInfo
        self.rootFrameAppearance = rootFrameAppearance
        self.varList = []
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        smfInfoKeyList = list(self.smfInfo.keys())
        smfInfoKeyList.pop(0)
        if self.decryptFile.game in ["CS", "RS"]:
            modelFlagList = textSetting.textList["railEditor"]["modelFlagList"]
            for i in range(len(smfInfoKeyList)):
                smfInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"][smfInfoKeyList[i]], font=textSetting.textList["font2"])
                smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varList.append(tkinter.StringVar())
                    smfInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varList[i].set(self.smfInfo[smfInfoKeyList[i]])
                elif i in [1, 2]:
                    mb = ttkCustomWidget.CustomTtkMenubutton(master, text=textSetting.textList["railEditor"]["setSmfSwitch"])
                    menu = tkinter.Menu(mb, tearoff=0, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
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
                    self.varList.append(tkinter.IntVar())
                    smfInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varList[i].set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        if i == 3:
                            default = 8
                        else:
                            default = 255
                        self.varList[i].set(default)
        elif self.decryptFile.game == "BS":
            smfInfoKeyList.pop()
            for i in range(len(smfInfoKeyList)):
                smfInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=smfInfoKeyList[i], font=textSetting.textList["font2"])
                smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varList.append(tkinter.StringVar())
                    smfInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varList[i].set(self.smfInfo[smfInfoKeyList[i]])
                else:
                    self.varList.append(tkinter.IntVar())
                    smfInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varList[i].set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        if i == 1:
                            default = 8
                        else:
                            default = 255
                        self.varList[i].set(default)
        else:
            smfInfoKeyList.pop()
            for i in range(len(smfInfoKeyList)):
                smfInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=smfInfoKeyList[i], font=textSetting.textList["font2"])
                smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 0:
                    self.varList.append(tkinter.StringVar())
                    smfInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                    if self.mode == "modify":
                        self.varList[i].set(self.smfInfo[smfInfoKeyList[i]])
                else:
                    self.varList.append(tkinter.IntVar())
                    smfInfoEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
                    smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                    if self.mode == "modify":
                        self.varList[i].set(self.smfInfo[smfInfoKeyList[i]])
                    elif self.mode == "insert":
                        if i == 1:
                            default = 8
                        else:
                            default = 255
                        self.varList[i].set(default)

        if self.mode == "insert":
            self.setInsertWidget(master, len(smfInfoKeyList))
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
                elif self.decryptFile.game in ["LSTrial", "LS"]:
                    try:
                        for i in range(len(self.varList)):
                            if i == 0:
                                res = self.varList[i].get()
                            else:
                                res = int(self.varList[i].get())
                            self.resultValueList.append(res)

                        if self.mode == "modify":
                            if self.decryptFile.game == "LS" or (self.decryptFile.game == "LSTrial" and self.decryptFile.readFlag):
                                originTempList = self.decryptFile.smfList[self.num][3]
                            else:
                                originTempList = self.decryptFile.smfList[self.num][2]
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


class PasteSmfListDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, num, copySmfInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.num = num
        self.copySmfInfo = copySmfInfo
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
        self.frontBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["railEditor"]["pasteFront"], style="custom.paste.TButton", command=self.frontInsert)
        self.frontBtn.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.backBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["railEditor"]["pasteBack"], style="custom.paste.TButton", command=self.backInsert)
        self.backBtn.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.cancelBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["railEditor"]["pasteCancel"], style="custom.paste.TButton", command=self.cancel)
        self.cancelBtn.pack(side=tkinter.LEFT, padx=5, pady=5)

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


class EditListElement(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, tempList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.tempList = copy.deepcopy(tempList)
        self.dirtyFlag = False
        self.reloadFlag = False
        self.resultList = []
        self.rootFrameAppearance = rootFrameAppearance
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.frame = master
        self.resizable(False, False)

        btnFrame = ttkCustomWidget.CustomTtkFrame(master)
        btnFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        listFrame = ttkCustomWidget.CustomTtkFrame(master)
        listFrame.pack()

        copyTempList = self.setListboxInfo(self.tempList)
        self.v_tempList = tkinter.StringVar(value=copyTempList)
        tempListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=25, height=6, listvariable=self.v_tempList, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        tempListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        tempListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(tempListListbox, tempListListbox.curselection()))
        super().body(master)

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
        result = EditListElementWidget(self.frame, textSetting.textList["railEditor"]["modifySmfElementListLabel"], self.decryptFile, "modify", self.selectIndexNum, self.tempList, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.tempList[self.selectIndexNum] = result.resultValueList
            copyTempList = self.setListboxInfo(self.tempList)
            self.v_tempList.set(copyTempList)

    def insert(self):
        result = EditListElementWidget(self.frame, textSetting.textList["railEditor"]["insertSmfElementListLabel"], self.decryptFile, "insert", self.selectIndexNum, self.tempList, self.rootFrameAppearance)
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


class EditListElementWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, index, tempList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.index = index
        self.tempList = tempList
        self.varList = []
        self.resultValueList = []
        self.insertPos = -1
        self.dirtyFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        if self.decryptFile.game == "BS":
            tempInfoLb = textSetting.textList["railEditor"]["smfElementListLabel1"]
        else:
            tempInfoLb = textSetting.textList["railEditor"]["smfElementListLabel2"]
        for i in range(len(tempInfoLb)):
            tempLb = ttkCustomWidget.CustomTtkLabel(master, text=tempInfoLb[i], font=textSetting.textList["font2"])
            tempLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            varTemp = tkinter.IntVar()
            if self.mode == "modify":
                tempInfo = self.tempList[self.index]
                varTemp.set(tempInfo[i])
            self.varList.append(varTemp)
            tempEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            tempEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(tempInfoLb))
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
