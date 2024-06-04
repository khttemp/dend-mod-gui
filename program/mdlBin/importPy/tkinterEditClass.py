import copy

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class InputDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, cmdList, num, section, cmdItem=None):
        self.v_paramList = []
        self.decryptFile = decryptFile
        self.ver = decryptFile.ver
        self.cmdList = cmdList
        self.num = num
        self.cmdItem = cmdItem
        self.section = section
        self.reloadFlag = False
        if self.cmdItem is not None:
            self.mode = "edit"
            self.info = textSetting.textList["infoList"]["I1"]
            self.p_cmd = self.cmdItem["treeName"]
            self.p_cnt = len(self.cmdItem) - 5
        else:
            self.mode = "insert"
            self.info = textSetting.textList["infoList"]["I2"]
            self.p_cmd = None
            self.p_cnt = None
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        delayLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["treeDelay"], width=12, font=textSetting.textList["font2"])
        delayLb.grid(row=0, column=0, sticky=tkinter.N+tkinter.S)
        self.v_delay = tkinter.StringVar()
        if self.cmdItem is not None:
            self.v_delay.set(self.cmdItem["treeDelay"])
        else:
            self.v_delay.set(0)
        delayEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_delay, width=27, font=textSetting.textList["font2"])
        delayEt.grid(row=0, column=1, sticky=tkinter.N+tkinter.S, pady=10)

        cmdLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["treeName"], width=12, font=textSetting.textList["font2"])
        cmdLb.grid(row=1, column=0, sticky=tkinter.N+tkinter.S)
        self.v_cmd = tkinter.StringVar()
        cmdCopy = copy.deepcopy(self.cmdList)
        cmdCopy.sort()
        cmdCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_cmd, width=25, font=textSetting.textList["font2"], state="readonly", value=cmdCopy)
        cmdCb.grid(row=1, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        if self.p_cmd is not None:
            self.v_cmd.set(self.p_cmd)
        else:
            self.v_cmd.set(cmdCopy[0])

        paramCntLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["paramLabel"], width=12, font=textSetting.textList["font2"])
        paramCntLb.grid(row=2, column=0, sticky=tkinter.N+tkinter.S)
        self.v_paramCnt = tkinter.IntVar()
        paramCntList = [cnt for cnt in range(0, 16)]
        self.paramCntCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_paramCnt, width=25, font=textSetting.textList["font2"], state="readonly", value=paramCntList)
        self.paramCntCb.grid(row=2, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        if self.p_cnt is not None:
            self.v_paramCnt.set(self.p_cnt)
        else:
            self.v_paramCnt.set(0)

        if self.cmdItem is None:
            positionLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], width=12, font=textSetting.textList["font2"])
            positionLb.grid(row=3, column=0, sticky=tkinter.N+tkinter.S)
            self.v_position = tkinter.StringVar()
            positionList = textSetting.textList["mdlBin"]["posValue"]
            self.positionCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_position, width=25, font=textSetting.textList["font2"], state="readonly", value=positionList)
            self.positionCb.grid(row=3, column=1, sticky=tkinter.N+tkinter.S, pady=10)
            self.v_position.set(positionList[0])

        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(columnspan=2, row=4, column=0, sticky=tkinter.E + tkinter.W, pady=10)

        self.paramFrame = ttkCustomWidget.CustomTtkFrame(master)
        self.paramFrame.grid(columnspan=2, row=5, column=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        if self.ver == 2:
            cmdCb.bind("<<ComboboxSelected>>", lambda e: self.cmdLock())
            self.cmdLock()

        self.paramCntCb.bind("<<ComboboxSelected>>", lambda e: self.selectParam(self.v_paramCnt.get(), self.paramFrame))
        if self.p_cnt != 0:
            self.selectParam(self.v_paramCnt.get(), self.paramFrame, self.cmdItem)
        super().body(master)

    def selectParam(self, paramCnt, frame, cmdItem=None):
        self.v_paramList = []
        children = frame.winfo_children()
        for child in children:
            child.destroy()

        if paramCnt == 0:
            paramLb = ttkCustomWidget.CustomTtkLabel(frame)
            paramLb.grid(row=0, column=0)

        for i in range(paramCnt):
            paramLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1), width=12, font=textSetting.textList["font2"])
            paramLb.grid(row=i, column=0, sticky=tkinter.N+tkinter.S)
            v_param = tkinter.StringVar()
            self.v_paramList.append(v_param)
            paramEt = ttkCustomWidget.CustomTtkEntry(frame, textvariable=v_param, width=27, font=textSetting.textList["font2"])
            paramEt.grid(row=i, column=1, sticky=tkinter.N+tkinter.S)
        if cmdItem is not None:
            for i in range(len(self.v_paramList)):
                self.v_paramList[i].set(cmdItem[textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)])

    def cmdLock(self):
        if self.ver == 2:
            if self.v_cmd.get() in ["MDL_GETINDEX", "SET_LENSFLEAR_MT"]:
                self.paramCntCb["state"] = "disabled"
                self.paramCntCb.current(2)
                self.selectParam(self.v_paramCnt.get(), self.paramFrame)
            else:
                self.paramCntCb["state"] = "normal"

    def validate(self):
        editParamList = []
        textParamList = []
        paramIdx = 0
        floatFlag = True
        errorFlag = False
        for var in self.v_paramList:
            num = 0
            if floatFlag:
                try:
                    num = float(var.get())
                except Exception:
                    floatFlag = False
                    if self.ver < 3:
                        if self.ver == 2:
                            if self.v_cmd.get() not in ["MDL_GETINDEX", "SET_LENSFLEAR_MT"]:
                                errorFlag = True
                            else:
                                if paramIdx != 1:
                                    errorFlag = True
                        else:
                            errorFlag = True

            if self.ver == 2:
                if self.v_cmd.get() in ["MDL_GETINDEX", "SET_LENSFLEAR_MT"] and paramIdx == 1:
                    floatFlag = False

            if floatFlag:
                editParamList.append(num)
            else:
                editParamList.append(var.get())
                textParamList.append(paramIdx)
            paramIdx += 1

        if errorFlag:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
            return False

        msg = ""
        infoMsg = self.info
        for param in textParamList:
            msg += textSetting.textList["mdlBin"]["paramNumLabel"].format(param + 1)
            msg += "\n"

        if len(textParamList) > 0:
            msg += textSetting.textList["infoList"]["I17"]
            infoMsg = msg + self.info

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=infoMsg, parent=self)
        if result:
            scriptData = []
            scriptData.append(int(self.v_delay.get()))
            scriptData.append(self.cmdList.index(self.v_cmd.get()))
            scriptData.append(self.v_paramCnt.get())
            if len(textParamList) == 0:
                scriptData.append(0xFF)
            else:
                scriptData.append(len(textParamList))

            for i in range(self.v_paramCnt.get()):
                scriptData.append(editParamList[i])

            sectionList = self.section.split(",")
            num = int(sectionList[0])
            listNum = int(sectionList[1])
            cmdDiff = int(sectionList[2])

            if self.mode == "insert":
                if self.positionCb.current() == 0:
                    cmdDiff += 1

            if not self.decryptFile.saveFile(num, listNum, cmdDiff, self.mode, scriptData):
                self.decryptFile.printError()
                errorMsg = textSetting.textList["errorList"]["E4"]
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
        self.reloadFlag = True


class PasteDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, cmdList, num, section, copyScriptData):
        self.decryptFile = decryptFile
        self.cmdList = cmdList
        self.num = num
        self.section = section
        self.copyScriptData = copyScriptData
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
        self.frontBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlBin"]["pasteFront"], style="custom.paste.TButton", width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlBin"]["pasteBack"], style="custom.paste.TButton", width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = ttkCustomWidget.CustomTtkButton(self.box, text=textSetting.textList["mdlBin"]["pasteCancel"], style="custom.paste.TButton", width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)

    def frontInsert(self):
        self.ok()
        sectionList = self.section.split(",")
        num = int(sectionList[0])
        listNum = int(sectionList[1])
        cmdDiff = int(sectionList[2])
        if not self.decryptFile.saveFile(num, listNum, cmdDiff, "insert", self.copyScriptData):
            self.decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        sectionList = self.section.split(",")
        num = int(sectionList[0])
        listNum = int(sectionList[1])
        cmdDiff = int(sectionList[2])
        if not self.decryptFile.saveFile(num, listNum, cmdDiff + 1, "insert", self.copyScriptData):
            self.decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
        self.reloadFlag = True


class HeaderDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.master = master
        self.selectListNum = -1
        self.selectIndexNum = -1
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False
        self.reloadFlag = False
        self.imgList = copy.deepcopy(self.decryptFile.imgList)
        self.imgSizeList = copy.deepcopy(self.decryptFile.imgSizeList)
        self.smfList = copy.deepcopy(self.decryptFile.smfList)
        self.wavList = copy.deepcopy(self.decryptFile.wavList)
        self.tgaList = copy.deepcopy(self.decryptFile.tgaList)
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(True, True)
        btnFrame = ttkCustomWidget.CustomTtkFrame(master)
        btnFrame.pack(pady=5)
        listFrame = ttkCustomWidget.CustomTtkFrame(master)
        listFrame.pack()

        listHeight = 8

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W+tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W+tkinter.E)
        ###
        imgListLb = ttkCustomWidget.CustomTtkLabel(listFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlBin"]["imgInfo"])
        imgListLb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)

        copyImgList = self.setListboxInfo(0, self.imgList)
        self.v_imgList = tkinter.StringVar(value=copyImgList)
        imgListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=30, height=listHeight, listvariable=self.v_imgList, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        imgListListbox.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        imgListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 0, imgListListbox, imgListListbox.curselection()))
        ###
        padLb = ttkCustomWidget.CustomTtkLabel(listFrame, width=3)
        padLb.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)
        ###
        imgSizeListLb = ttkCustomWidget.CustomTtkLabel(listFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlBin"]["imgSizeInfo"])
        imgSizeListLb.grid(row=0, column=2, sticky=tkinter.W+tkinter.E)

        copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
        self.v_imgSize = tkinter.StringVar(value=copyImgSizeList)
        imgSizeListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=30, height=listHeight, listvariable=self.v_imgSize, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        imgSizeListbox.grid(row=1, column=2, sticky=tkinter.W+tkinter.E)
        imgSizeListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 1, imgSizeListbox, imgSizeListbox.curselection()))
        ###
        smfListLb = ttkCustomWidget.CustomTtkLabel(listFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlBin"]["smfInfo"])
        smfListLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)

        copySmfList = self.setListboxInfo(2, self.smfList)
        self.v_smfList = tkinter.StringVar(value=copySmfList)
        smfListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=30, height=listHeight, listvariable=self.v_smfList, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        smfListListbox.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
        smfListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 2, smfListListbox, smfListListbox.curselection()))
        ###
        padLb = ttkCustomWidget.CustomTtkLabel(listFrame, width=3)
        padLb.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)
        ###
        wavListLb = ttkCustomWidget.CustomTtkLabel(listFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlBin"]["seInfo"])
        wavListLb.grid(row=2, column=2, sticky=tkinter.W+tkinter.E)

        copyWavList = self.setListboxInfo(3, self.wavList)
        self.v_wavList = tkinter.StringVar(value=copyWavList)
        wavListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=30, height=listHeight, listvariable=self.v_wavList, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        wavListListbox.grid(row=3, column=2, sticky=tkinter.W+tkinter.E)
        wavListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 3, wavListListbox, wavListListbox.curselection()))
        ###
        if self.decryptFile.ver != 1:
            tgaListLb = ttkCustomWidget.CustomTtkLabel(listFrame, font=textSetting.textList["font2"], text=textSetting.textList["mdlBin"]["tgaInfo"])
            tgaListLb.grid(row=4, column=0, columnspan=3, sticky=tkinter.W+tkinter.E)

            copyTgaList = self.setListboxInfo(4, self.tgaList)
            self.v_tgaList = tkinter.StringVar(value=copyTgaList)
            tgaListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], height=listHeight, listvariable=self.v_tgaList, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
            tgaListListbox.grid(row=5, column=0, columnspan=3, sticky=tkinter.W+tkinter.E)
            tgaListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 4, tgaListListbox, tgaListListbox.curselection()))
        super().body(master)

    def buttonActive(self, event, num, listbox, value):
        if len(value) == 0:
            return
        self.selectListNum = num
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["mdlBin"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def setListboxInfo(self, index, listboxInfo):
        if index == 0:
            self.imgList = listboxInfo
            copyImgList = copy.deepcopy(self.imgList)
            if len(copyImgList) > 0:
                for i in range(len(copyImgList)):
                    imgName = copyImgList[i]["imgName"]
                    if self.decryptFile.ver == 4:
                        copyImgList[i] = "{0:02d}→{1}, {2}".format(i, imgName, copyImgList[i]["imgElse"])
                    else:
                        copyImgList[i] = "{0:02d}→{1}".format(i, imgName)
            else:
                copyImgList = [textSetting.textList["mdlBin"]["noList"]]

            return copyImgList
        elif index == 1:
            self.imgSizeList = listboxInfo
            copyImgSizeList = copy.deepcopy(self.imgSizeList)
            if len(copyImgSizeList) > 0:
                for i in range(len(copyImgSizeList)):
                    copyImgSizeList[i] = "{0:02d}→img{1:02d}, {2}".format(i, copyImgSizeList[i][0], copyImgSizeList[i][1])
            else:
                copyImgSizeList = [textSetting.textList["mdlBin"]["noList"]]

            return copyImgSizeList
        elif index == 2:
            self.smfList = listboxInfo
            copySmfList = copy.deepcopy(self.smfList)
            if len(copySmfList) > 0:
                for i in range(len(copySmfList)):
                    copySmfList[i] = "{0:02d}→{1}".format(i, copySmfList[i])
            else:
                copySmfList = [textSetting.textList["mdlBin"]["noList"]]

            return copySmfList
        elif index == 3:
            self.wavList = listboxInfo
            copyWavList = copy.deepcopy(self.wavList)
            if len(copyWavList) > 0:
                for i in range(len(copyWavList)):
                    copyWavList[i] = "{0:02d}→{1}, {2}".format(i, copyWavList[i][0], copyWavList[i][1])
            else:
                copyWavList = [textSetting.textList["mdlBin"]["noList"]]

            return copyWavList
        elif index == 4:
            self.tgaList = listboxInfo
            copyTgaList = copy.deepcopy(self.tgaList)
            if len(copyTgaList) > 0:
                for i in range(len(copyTgaList)):
                    copyTgaList[i] = "{0:02d}→{1}, {2}".format(i, copyTgaList[i]["tgaInfo"], copyTgaList[i]["tgaElse"])
            else:
                copyTgaList = [textSetting.textList["mdlBin"]["noList"]]

            return copyTgaList

    def modify(self):
        selectList = None
        if self.selectListNum == 0:
            selectList = self.imgList
        elif self.selectListNum == 1:
            selectList = self.imgSizeList
        elif self.selectListNum == 2:
            selectList = self.smfList
        elif self.selectListNum == 3:
            selectList = self.wavList
        elif self.selectListNum == 4:
            selectList = self.tgaList
        result = HeaderEditDialog(self.master, textSetting.textList["mdlBin"]["headerModify"], self.decryptFile.ver, "modify", self.selectListNum, self.selectIndexNum, selectList, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.dirtyFlag = True
            if self.selectListNum == 0:
                copyImgList = self.setListboxInfo(0, self.imgList)
                self.v_imgList.set(copyImgList)
            elif self.selectListNum == 1:
                copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
                self.v_imgSize.set(copyImgSizeList)
            elif self.selectListNum == 2:
                copySmfList = self.setListboxInfo(2, self.smfList)
                self.v_smfList.set(copySmfList)
            elif self.selectListNum == 3:
                copyWavList = self.setListboxInfo(3, self.wavList)
                self.v_wavList.set(copyWavList)
            elif self.selectListNum == 4:
                copyTgaList = self.setListboxInfo(4, self.tgaList)
                self.v_tgaList.set(copyTgaList)

    def insert(self):
        selectList = None
        if self.selectListNum == 0:
            selectList = self.imgList
        elif self.selectListNum == 1:
            selectList = self.imgSizeList
        elif self.selectListNum == 2:
            selectList = self.smfList
        elif self.selectListNum == 3:
            selectList = self.wavList
        elif self.selectListNum == 4:
            selectList = self.tgaList
        result = HeaderEditDialog(self.master, textSetting.textList["mdlBin"]["headerInsert"], self.decryptFile.ver, "insert", self.selectListNum, self.selectIndexNum, selectList, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.dirtyFlag = True
            if self.selectListNum == 0:
                copyImgList = self.setListboxInfo(0, self.imgList)
                self.v_imgList.set(copyImgList)
            elif self.selectListNum == 1:
                copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
                self.v_imgSize.set(copyImgSizeList)
            elif self.selectListNum == 2:
                copySmfList = self.setListboxInfo(2, self.smfList)
                self.v_smfList.set(copySmfList)
            elif self.selectListNum == 3:
                copyWavList = self.setListboxInfo(3, self.wavList)
                self.v_wavList.set(copyWavList)
            elif self.selectListNum == 4:
                copyTgaList = self.setListboxInfo(4, self.tgaList)
                self.v_tgaList.set(copyTgaList)

    def delete(self):
        msg = ""
        if self.selectListNum == 0:
            msg += textSetting.textList["mdlBin"]["imgInfo"]
        elif self.selectListNum == 1:
            msg += textSetting.textList["mdlBin"]["imgSizeInfo"]
        elif self.selectListNum == 2:
            msg += textSetting.textList["mdlBin"]["smfInfo"]
        elif self.selectListNum == 3:
            msg += textSetting.textList["mdlBin"]["seInfo"]
        elif self.selectListNum == 4:
            msg += textSetting.textList["mdlBin"]["tgaInfo"]

        msg += textSetting.textList["infoList"]["I6"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
        if result:
            self.dirtyFlag = True
            if self.selectListNum == 0:
                self.imgList.pop(self.selectIndexNum)
                copyImgList = self.setListboxInfo(0, self.imgList)
                self.v_imgList.set(copyImgList)
            elif self.selectListNum == 1:
                self.imgSizeList.pop(self.selectIndexNum)
                copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
                self.v_imgSize.set(copyImgSizeList)
            elif self.selectListNum == 2:
                self.smfList.pop(self.selectIndexNum)
                copySmfList = self.setListboxInfo(2, self.smfList)
                self.v_smfList.set(copySmfList)
            elif self.selectListNum == 3:
                self.wavList.pop(self.selectIndexNum)
                copyWavList = self.setListboxInfo(3, self.wavList)
                self.v_wavList.set(copyWavList)
            elif self.selectListNum == 4:
                self.tgaList.pop(self.selectIndexNum)
                copyTgaList = self.setListboxInfo(4, self.tgaList)
                self.v_tgaList.set(copyTgaList)
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def validate(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I7"], icon="warning", parent=self)
            if result:
                if not self.decryptFile.saveHeader(self.imgList, self.imgSizeList, self.smfList, self.wavList, self.tgaList):
                    self.decryptFile.printError()
                    errorMsg = textSetting.textList["errorList"]["E4"]
                    mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                    return False
            else:
                self.dirtyFlag = False
        return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I8"])
            self.reloadFlag = True


class HeaderEditDialog(CustomSimpleDialog):
    def __init__(self, master, title, ver, mode, selectListNum, selectIndexNum, selectList, rootFrameAppearance):
        self.ver = ver
        self.mode = mode
        self.selectListNum = selectListNum
        self.selectIndexNum = selectIndexNum
        self.selectList = selectList
        self.dirtyFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        if self.selectListNum == 0:
            imgNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgLabel"], font=textSetting.textList["font2"])
            imgNameLb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
            self.v_imgName = tkinter.StringVar()
            imgNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_imgName)
            imgNameEt.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

            if self.ver == 4:
                imgElse1Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["else"] + "1", font=textSetting.textList["font2"])
                imgElse1Lb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
                self.v_imgElse1 = tkinter.StringVar()
                self.imgElseCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_imgElse1, values=textSetting.textList["mdlBin"]["headerElse1Value"])
                self.imgElseCb.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
                self.imgElseCb.current(0)
                self.imgElseCb.bind("<<ComboboxSelected>>", self.imgElseCbChange)

                imgElse2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["else"] + "2", font=textSetting.textList["font2"])
                imgElse2Lb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
                self.v_imgElse2 = tkinter.StringVar()
                self.imgElseEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_imgElse2, state="disabled")
                self.imgElseEt.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_imgName.set(self.selectList[self.selectIndexNum]["imgName"])

                if self.ver == 4:
                    imgElse1 = self.selectList[self.selectIndexNum]["imgElse"][0]
                    self.imgElseCb.current(imgElse1)
                    if imgElse1 == 0:
                        self.imgElseEt["state"] = "disabled"
                        self.v_imgElse2.set("")
                    else:
                        imgElse2 = self.selectList[self.selectIndexNum]["imgElse"][1]
                        self.imgElseEt["state"] = "normal"
                        self.v_imgElse2.set(imgElse2)
            else:
                if self.ver == 4:
                    self.setInsertWidget(master, 3)
                else:
                    self.setInsertWidget(master, 1)
        elif self.selectListNum == 1:
            imgIndexLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgIndex"], font=textSetting.textList["font2"])
            imgIndexLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
            imgIndex_xLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgX"], font=textSetting.textList["font2"])
            imgIndex_xLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
            imgIndex_yLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgY"], font=textSetting.textList["font2"])
            imgIndex_yLb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
            imgIndex_widthLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgWidth"], font=textSetting.textList["font2"])
            imgIndex_widthLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)
            imgIndex_heightLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgHeight"], font=textSetting.textList["font2"])
            imgIndex_heightLb.grid(row=5, column=0, sticky=tkinter.W+tkinter.E)

            self.v_imgIndex = tkinter.IntVar()
            self.v_imgIndex_x = tkinter.DoubleVar()
            self.v_imgIndex_y = tkinter.DoubleVar()
            self.v_imgIndex_width = tkinter.DoubleVar()
            self.v_imgIndex_height = tkinter.DoubleVar()
            imgIndexEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex, font=textSetting.textList["font2"])
            imgIndexEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
            imgIndex_xEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_x, font=textSetting.textList["font2"])
            imgIndex_xEt.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)
            imgIndex_yEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_y, font=textSetting.textList["font2"])
            imgIndex_yEt.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)
            imgIndex_widthEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_width, font=textSetting.textList["font2"])
            imgIndex_widthEt.grid(row=4, column=1, sticky=tkinter.W+tkinter.E)
            imgIndex_heightEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_height, font=textSetting.textList["font2"])
            imgIndex_heightEt.grid(row=5, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_imgIndex.set(int(self.selectList[self.selectIndexNum][0]))
                self.v_imgIndex_x.set(float(self.selectList[self.selectIndexNum][1][0]))
                self.v_imgIndex_y.set(float(self.selectList[self.selectIndexNum][1][1]))
                self.v_imgIndex_width.set(float(self.selectList[self.selectIndexNum][1][2]))
                self.v_imgIndex_height.set(float(self.selectList[self.selectIndexNum][1][3]))
            else:
                self.setInsertWidget(master, 6)
        elif self.selectListNum == 2:
            smfNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerSmfLabel"], font=textSetting.textList["font2"])
            smfNameLb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
            self.v_smfName = tkinter.StringVar()
            smfNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_smfName)
            smfNameEt.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_smfName.set(self.selectList[self.selectIndexNum])
            else:
                self.setInsertWidget(master, 1)
        elif self.selectListNum == 3:
            wavNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerSELabel"], font=textSetting.textList["font2"])
            wavNameLb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
            self.v_wavName = tkinter.StringVar()
            wavNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_wavName)
            wavNameEt.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

            wavCntLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerSEGroup"], font=textSetting.textList["font2"])
            wavCntLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
            self.v_wavCnt = tkinter.IntVar()
            wavCntEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_wavCnt)
            wavCntEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_wavName.set(self.selectList[self.selectIndexNum][0])
                self.v_wavCnt.set(int(self.selectList[self.selectIndexNum][1]))
            else:
                self.setInsertWidget(master, 2)
        elif self.selectListNum == 4:
            tgaName1Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaLabel"] + "1", font=textSetting.textList["font2"])
            tgaName1Lb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaName1 = tkinter.StringVar()
            tgaName1Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaName1)
            tgaName1Et.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

            tgaName2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaLabel"] + "2", font=textSetting.textList["font2"])
            tgaName2Lb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaName2 = tkinter.StringVar()
            tgaName2Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaName2)
            tgaName2Et.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

            tgaEle1Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["else"] + "1", font=textSetting.textList["font2"])
            tgaEle1Lb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaEle1 = tkinter.DoubleVar()
            tgaEle1Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaEle1)
            tgaEle1Et.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)

            tgaEle2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["else"] + "2", font=textSetting.textList["font2"])
            tgaEle2Lb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaEle2 = tkinter.DoubleVar()
            tgaEle2Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaEle2)
            tgaEle2Et.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)

            xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
            xLine.grid(row=4, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

            tgaElseB1Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaB"] + "1", font=textSetting.textList["font2"])
            tgaElseB1Lb.grid(row=5, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaElseB1 = tkinter.IntVar()
            tgaElseB1Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaElseB1)
            tgaElseB1Et.grid(row=5, column=1, sticky=tkinter.W+tkinter.E)

            tgaElseB2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaB"] + "2", font=textSetting.textList["font2"])
            tgaElseB2Lb.grid(row=6, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaElseB2 = tkinter.IntVar()
            tgaElseB2Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaElseB2)
            tgaElseB2Et.grid(row=6, column=1, sticky=tkinter.W+tkinter.E)

            tgaElseB3Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaB"] + "3", font=textSetting.textList["font2"])
            tgaElseB3Lb.grid(row=7, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaElseB3 = tkinter.IntVar()
            tgaElseB3Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaElseB3)
            tgaElseB3Et.grid(row=7, column=1, sticky=tkinter.W+tkinter.E)

            tgaElseB4Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaB"] + "4", font=textSetting.textList["font2"])
            tgaElseB4Lb.grid(row=8, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaElseB4 = tkinter.IntVar()
            tgaElseB4Et = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaElseB4)
            tgaElseB4Et.grid(row=8, column=1, sticky=tkinter.W+tkinter.E)

            tgaElsePerLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaPer"], font=textSetting.textList["font2"])
            tgaElsePerLb.grid(row=9, column=0, sticky=tkinter.W+tkinter.E)
            self.v_tgaElsePer = tkinter.IntVar()
            tgaElsePerEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_tgaElsePer)
            tgaElsePerEt.grid(row=9, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_tgaName1.set(self.selectList[self.selectIndexNum]["tgaInfo"][0])
                self.v_tgaName2.set(self.selectList[self.selectIndexNum]["tgaInfo"][1])
                self.v_tgaEle1.set(self.selectList[self.selectIndexNum]["tgaInfo"][2])
                self.v_tgaEle2.set(self.selectList[self.selectIndexNum]["tgaInfo"][3])
                self.v_tgaElseB1.set(self.selectList[self.selectIndexNum]["tgaElse"][0])
                self.v_tgaElseB2.set(self.selectList[self.selectIndexNum]["tgaElse"][1])
                self.v_tgaElseB3.set(self.selectList[self.selectIndexNum]["tgaElse"][2])
                self.v_tgaElseB4.set(self.selectList[self.selectIndexNum]["tgaElse"][3])
                self.v_tgaElsePer.set(self.selectList[self.selectIndexNum]["tgaElse"][4])
            else:
                self.setInsertWidget(master, 10)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["mdlBin"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def imgElseCbChange(self, event):
        imgElse1 = self.imgElseCb.current()
        if imgElse1 == 0:
            self.imgElseEt["state"] = "disabled"
            self.v_imgElse2.set("")
        else:
            self.imgElseEt["state"] = "normal"

    def validate(self):
        msg = ""
        if self.mode == "modify":
            msg = textSetting.textList["infoList"]["I1"]
        else:
            msg = textSetting.textList["infoList"]["I2"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=msg, parent=self)
        if result:
            if self.selectListNum == 0:
                try:
                    imgInfo = {}
                    imgInfo["imgName"] = self.v_imgName.get()
                    imgInfo["imgElse"] = []
                    if self.ver == 4:
                        imgElse1 = self.imgElseCb.current()
                        imgInfo["imgElse"].append(imgElse1)
                        if imgElse1 != 0:
                            imgElse2 = int(self.v_imgElse2.get())
                            imgInfo["imgElse"].append(imgElse2)

                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = imgInfo
                    else:
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, imgInfo)
                        else:
                            self.selectList.insert(self.selectIndexNum, imgInfo)
                    return True
                except Exception:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
                    return False
            elif self.selectListNum == 1:
                try:
                    imgSizeInfo = []
                    imgSizeInfo.append(int(self.v_imgIndex.get()))

                    imgSize = []
                    imgSize.append(float(self.v_imgIndex_x.get()))
                    imgSize.append(float(self.v_imgIndex_y.get()))
                    imgSize.append(float(self.v_imgIndex_width.get()))
                    imgSize.append(float(self.v_imgIndex_height.get()))
                    imgSizeInfo.append(imgSize)

                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = imgSizeInfo
                    else:
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, imgSizeInfo)
                        else:
                            self.selectList.insert(self.selectIndexNum, imgSizeInfo)
                    return True
                except Exception:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
                    return False
            elif self.selectListNum == 2:
                try:
                    smfName = self.v_smfName.get()

                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = smfName
                    else:
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, smfName)
                        else:
                            self.selectList.insert(self.selectIndexNum, smfName)
                    return True
                except Exception:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
                    return False
            elif self.selectListNum == 3:
                try:
                    wavInfo = []

                    wavName = self.v_wavName.get()
                    wavInfo.append(wavName)
                    wavCnt = int(self.v_wavCnt.get())
                    wavInfo.append(wavCnt)

                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = wavInfo
                    else:
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, wavInfo)
                        else:
                            self.selectList.insert(self.selectIndexNum, wavInfo)
                    return True
                except Exception:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
                    return False
            elif self.selectListNum == 4:
                try:
                    tgaInfo = {}
                    tgaInfo["tgaInfo"] = []
                    tgaInfo["tgaInfo"].append(self.v_tgaName1.get())
                    tgaInfo["tgaInfo"].append(self.v_tgaName2.get())
                    tgaInfo["tgaInfo"].append(float(self.v_tgaEle1.get()))
                    tgaInfo["tgaInfo"].append(float(self.v_tgaEle2.get()))

                    tgaInfo["tgaElse"] = []
                    tgaInfo["tgaElse"].append(int(self.v_tgaElseB1.get()))
                    tgaInfo["tgaElse"].append(int(self.v_tgaElseB2.get()))
                    tgaInfo["tgaElse"].append(int(self.v_tgaElseB3.get()))
                    tgaInfo["tgaElse"].append(int(self.v_tgaElseB4.get()))
                    tgaInfo["tgaElse"].append(int(self.v_tgaElsePer.get()))

                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = tgaInfo
                    else:
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, tgaInfo)
                        else:
                            self.selectList.insert(self.selectIndexNum, tgaInfo)
                    return True
                except Exception:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
                    return False

    def apply(self):
        self.dirtyFlag = True


class ListNumModifyDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, num, curVal):
        self.decryptFile = decryptFile
        self.num = num
        self.curVal = curVal
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        listLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I18"].format(self.num), font=textSetting.textList["font2"])
        listLb.grid(row=0, column=0)

        self.v_listNum = tkinter.IntVar()
        self.v_listNum.set(self.curVal)
        sp = ttkCustomWidget.CustomTtkSpinbox(master, textvariable=self.v_listNum, font=textSetting.textList["font2"], from_=1, to=100, width=5)
        sp.grid(row=0, column=1, padx=10)

        list2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I19"], font=textSetting.textList["font2"])
        list2Lb.grid(row=0, column=2)
        super().body(master)

    def validate(self):
        if self.v_listNum.get() < self.curVal:
            warnMsg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        else:
            infoMsg = textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=infoMsg, parent=self)

        if result:
            if not self.decryptFile.saveFile(int(self.num), 0, -1, "list", self.v_listNum.get()):
                self.decryptFile.printError()
                errorMsg = textSetting.textList["errorList"]["E4"]
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I22"])
        self.reloadFlag = True


class ListHeaderModifyDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, num, listNum, headerInfo):
        self.decryptFile = decryptFile
        self.num = num
        self.listNum = listNum
        self.headerInfo = headerInfo
        self.v_paramList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        for i in range(3):
            paramLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1), font=textSetting.textList["font2"])
            paramLb.grid(row=i, column=0, sticky=tkinter.N + tkinter.S)
            self.v_paramList.append(tkinter.IntVar(value=self.headerInfo[i]))
            paramEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_paramList[i], width=20, font=textSetting.textList["font2"])
            paramEt.grid(row=i, column=1, sticky=tkinter.N + tkinter.S)
        super().body(master)

    def validate(self):
        headerList = []
        try:
            for i in range(3):
                param = self.v_paramList[i].get()
                param = int(param)
                headerList.append(param)

            infoMsg = textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=infoMsg, parent=self)

            if result:
                if not self.decryptFile.saveListHeader(self.num, self.listNum, headerList):
                    self.decryptFile.printError()
                    errorMsg = textSetting.textList["errorList"]["E4"]
                    mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                    return False
                return True
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E5"])
            return False

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I23"])
        self.reloadFlag = True


class NumModifyDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, curVal):
        self.decryptFile = decryptFile
        self.curVal = curVal
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        numLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I24"], font=textSetting.textList["font2"])
        numLb.grid(row=0, column=0)

        self.v_num = tkinter.IntVar()
        self.v_num.set(self.curVal)
        sp = ttkCustomWidget.CustomTtkSpinbox(master, textvariable=self.v_num, font=textSetting.textList["font2"], from_=1, to=100, width=5)
        sp.grid(row=0, column=1, padx=10)

        self.num2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I19"], font=textSetting.textList["font2"])
        self.num2Lb.grid(row=0, column=2)
        super().body(master)

    def validate(self):
        if self.v_num.get() < self.curVal:
            warnMsg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        else:
            infoMsg = textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=infoMsg, parent=self)

        if result:
            if not self.decryptFile.saveNumFile(self.v_num.get()):
                self.decryptFile.printError()
                errorMsg = textSetting.textList["errorList"]["E4"]
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I23"])
        self.reloadFlag = True
