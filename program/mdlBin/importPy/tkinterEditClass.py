import copy

import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb


class InputDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, cmdList, num, section, cmdItem=None):
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
            self.info = "このまま修正してもよろしいですか？"
            self.p_cmd = self.cmdItem["コマンド名"]
            self.p_cnt = len(self.cmdItem) - 5
        else:
            self.mode = "insert"
            self.info = "このまま挿入してもよろしいですか？"
            self.p_cmd = None
            self.p_cnt = None
        super(InputDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.idxLb = ttk.Label(master, text="delay", width=12, font=("", 14))
        self.idxLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)
        self.v_delay = tkinter.StringVar()
        if self.cmdItem is not None:
            self.v_delay.set(self.cmdItem["delay"])
        else:
            self.v_delay.set(0)
        self.idxEt = ttk.Entry(master, textvariable=self.v_delay, width=33)
        self.idxEt.grid(row=0, column=1, sticky=tkinter.N + tkinter.S, pady=10)

        self.cmdLb = ttk.Label(master, text="コマンド名", width=12, font=("", 14))
        self.cmdLb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S)
        self.v_cmd = tkinter.StringVar()
        cmdCopy = copy.deepcopy(self.cmdList)
        cmdCopy.sort()
        self.cmdCb = ttk.Combobox(master, textvariable=self.v_cmd, width=30, state="readonly", value=cmdCopy)
        self.cmdCb.grid(row=1, column=1, sticky=tkinter.N + tkinter.S, pady=10)
        if self.p_cmd is not None:
            self.v_cmd.set(self.p_cmd)
        else:
            self.v_cmd.set(cmdCopy[0])

        self.paramCntLb = ttk.Label(master, text="パラメータ数", width=12, font=("", 14))
        self.paramCntLb.grid(row=2, column=0, sticky=tkinter.N + tkinter.S)
        self.v_paramCnt = tkinter.IntVar()
        paramCntList = [cnt for cnt in range(0, 16)]
        self.paramCntCb = ttk.Combobox(master, textvariable=self.v_paramCnt, width=30, state="readonly", value=paramCntList)
        self.paramCntCb.grid(row=2, column=1, sticky=tkinter.N + tkinter.S, pady=10)
        if self.p_cnt is not None:
            self.v_paramCnt.set(self.p_cnt)
        else:
            self.v_paramCnt.set(0)

        if self.cmdItem is None:
            self.position = ttk.Label(master, text="挿入する位置", width=12, font=("", 14))
            self.position.grid(row=3, column=0, sticky=tkinter.N + tkinter.S)
            self.v_position = tkinter.StringVar()
            positionList = ["後", "前"]
            self.positionCb = ttk.Combobox(master, textvariable=self.v_position, width=30, state="readonly", value=positionList)
            self.positionCb.grid(row=3, column=1, sticky=tkinter.N + tkinter.S, pady=10)
            self.v_position.set(positionList[0])

        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(columnspan=2, row=4, column=0, sticky=tkinter.E + tkinter.W, pady=10)

        self.paramFrame = ttk.Frame(master)
        self.paramFrame.grid(columnspan=2, row=5, column=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        self.paramLb = ttk.Label(self.paramFrame)
        self.paramLb.grid(row=0, column=0)

        if self.ver == 2:
            self.cmdCb.bind('<<ComboboxSelected>>', lambda e: self.cmdLock())
            self.cmdLock()

        self.paramCntCb.bind('<<ComboboxSelected>>', lambda e: self.selectParam(self.v_paramCnt.get(), self.paramFrame))
        if self.p_cnt != 0:
            self.selectParam(self.v_paramCnt.get(), self.paramFrame, self.cmdItem)

    def selectParam(self, paramCnt, frame, cmdItem=None):
        self.v_paramList = []
        children = frame.winfo_children()
        for child in children:
            child.destroy()

        if paramCnt == 0:
            self.paramLb = ttk.Label(frame)
            self.paramLb.grid(row=0, column=0)

        for i in range(paramCnt):
            self.paramLb = ttk.Label(frame, text="param{0}".format(i + 1), font=("", 14))
            self.paramLb.grid(row=i, column=0, sticky=tkinter.N + tkinter.S)
            v_param = tkinter.StringVar()
            self.v_paramList.append(v_param)
            self.paramEt = ttk.Entry(frame, textvariable=v_param, width=30)
            self.paramEt.grid(row=i, column=1, sticky=tkinter.N + tkinter.S)
        if cmdItem is not None:
            for i in range(len(self.v_paramList)):
                self.v_paramList[i].set(cmdItem["param{0}".format(i + 1)])

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
            mb.showerror(title="エラー", message="不正な値があります")
            return False

        msg = ""
        infoMsg = self.info
        for param in textParamList:
            msg += "param{0}\n".format(param + 1)

        if len(textParamList) > 0:
            msg += "※上記のparamは文字として保存されます\n\n"
            infoMsg = msg + self.info

        result = mb.askokcancel(title="確認", message=infoMsg, parent=self)
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
                if self.v_position.get() == "後":
                    cmdDiff += 1

            if not self.decryptFile.saveFile(num, listNum, cmdDiff, self.mode, scriptData):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="スクリプトを改造しました")
        self.reloadFlag = True


class PasteDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, cmdList, num, section, copyScriptData):
        self.decryptFile = decryptFile
        self.cmdList = cmdList
        self.num = num
        self.section = section
        self.copyScriptData = copyScriptData
        self.reloadFlag = False
        super(PasteDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.posLb = ttk.Label(master, text="挿入する位置を選んでください", font=("", 14))
        self.posLb.pack(padx=10, pady=10)

    def buttonbox(self):
        box = tkinter.Frame(self, padx=5, pady=5)
        self.frontBtn = tkinter.Button(box, text="前", font=("", 12), width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = tkinter.Button(box, text="後", font=("", 12), width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = tkinter.Button(box, text="Cancel", font=("", 12), width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)
        box.pack()

    def frontInsert(self):
        self.ok()
        sectionList = self.section.split(",")
        num = int(sectionList[0])
        listNum = int(sectionList[1])
        cmdDiff = int(sectionList[2])
        if not self.decryptFile.saveFile(num, listNum, cmdDiff, "insert", self.copyScriptData):
            self.decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="スクリプトを改造しました")
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        sectionList = self.section.split(",")
        num = int(sectionList[0])
        listNum = int(sectionList[1])
        cmdDiff = int(sectionList[2])
        if not self.decryptFile.saveFile(num, listNum, cmdDiff + 1, "insert", self.copyScriptData):
            self.decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="スクリプトを改造しました")
        self.reloadFlag = True


class HeaderDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile):
        self.master = master
        self.selectListNum = -1
        self.selectIndexNum = -1
        self.decryptFile = decryptFile
        self.dirtyFlag = False
        self.reloadFlag = False
        self.imgList = copy.deepcopy(self.decryptFile.imgList)
        self.imgSizeList = copy.deepcopy(self.decryptFile.imgSizeList)
        self.smfList = copy.deepcopy(self.decryptFile.smfList)
        self.wavList = copy.deepcopy(self.decryptFile.wavList)
        self.tgaList = copy.deepcopy(self.decryptFile.tgaList)
        super(HeaderDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(True, True)
        self.btnFrame = tkinter.Frame(master, pady=5)
        self.btnFrame.pack()
        self.listFrame = tkinter.Frame(master)
        self.listFrame.pack()

        listHeight = 8

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)
        ###
        self.imgListLb = tkinter.Label(self.listFrame, font=("", 14), text="画像情報")
        self.imgListLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        copyImgList = self.setListboxInfo(0, self.imgList)
        self.v_imgList = tkinter.StringVar(value=copyImgList)
        self.imgListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), width=30, height=listHeight, listvariable=self.v_imgList)
        self.imgListListbox.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.imgListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 0, self.imgListListbox, self.imgListListbox.curselection()))
        ###
        self.padLb = tkinter.Label(self.listFrame, width=3)
        self.padLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        ###
        self.imgSizeListLb = tkinter.Label(self.listFrame, font=("", 14), text="画像サイズ情報")
        self.imgSizeListLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
        self.v_imgSize = tkinter.StringVar(value=copyImgSizeList)
        self.imgSizeListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), width=30, height=listHeight, listvariable=self.v_imgSize)
        self.imgSizeListbox.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)
        self.imgSizeListbox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 1, self.imgSizeListbox, self.imgSizeListbox.curselection()))
        ###
        self.smfListLb = tkinter.Label(self.listFrame, font=("", 14), text="smf情報")
        self.smfListLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)

        copySmfList = self.setListboxInfo(2, self.smfList)
        self.v_smfList = tkinter.StringVar(value=copySmfList)
        self.smfListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), width=30, height=listHeight, listvariable=self.v_smfList)
        self.smfListListbox.grid(row=3, column=0, sticky=tkinter.W + tkinter.E)
        self.smfListListbox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 2, self.smfListListbox, self.smfListListbox.curselection()))
        ###
        self.padLb = tkinter.Label(self.listFrame, width=3)
        self.padLb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)
        ###
        self.wavListLb = tkinter.Label(self.listFrame, font=("", 14), text="SE情報")
        self.wavListLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E)

        copyWavList = self.setListboxInfo(3, self.wavList)
        self.v_wavList = tkinter.StringVar(value=copyWavList)
        self.wavListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), width=30, height=listHeight, listvariable=self.v_wavList)
        self.wavListListbox.grid(row=3, column=2, sticky=tkinter.W + tkinter.E)
        self.wavListListbox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 3, self.wavListListbox, self.wavListListbox.curselection()))
        ###
        if self.decryptFile.ver != 1:
            self.tgaListLb = tkinter.Label(self.listFrame, font=("", 14), text="tga情報")
            self.tgaListLb.grid(row=4, column=0, columnspan=3, sticky=tkinter.W + tkinter.E)

            copyTgaList = self.setListboxInfo(4, self.tgaList)
            self.v_tgaList = tkinter.StringVar(value=copyTgaList)
            self.tgaListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), height=listHeight, listvariable=self.v_tgaList)
            self.tgaListListbox.grid(row=5, column=0, columnspan=3, sticky=tkinter.W + tkinter.E)
            self.tgaListListbox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, 4, self.tgaListListbox, self.tgaListListbox.curselection()))

    def buttonActive(self, event, num, listbox, value):
        if len(value) == 0:
            return
        self.selectListNum = num
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == "(なし)":
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
                copyImgList = ["(なし)"]

            return copyImgList
        elif index == 1:
            self.imgSizeList = listboxInfo
            copyImgSizeList = copy.deepcopy(self.imgSizeList)
            if len(copyImgSizeList) > 0:
                for i in range(len(copyImgSizeList)):
                    copyImgSizeList[i] = "{0:02d}→img{1:02d}, {2}".format(i, copyImgSizeList[i][0], copyImgSizeList[i][1])
            else:
                copyImgSizeList = ["(なし)"]

            return copyImgSizeList
        elif index == 2:
            self.smfList = listboxInfo
            copySmfList = copy.deepcopy(self.smfList)
            if len(copySmfList) > 0:
                for i in range(len(copySmfList)):
                    copySmfList[i] = "{0:02d}→{1}".format(i, copySmfList[i])
            else:
                copySmfList = ["(なし)"]

            return copySmfList
        elif index == 3:
            self.wavList = listboxInfo
            copyWavList = copy.deepcopy(self.wavList)
            if len(copyWavList) > 0:
                for i in range(len(copyWavList)):
                    copyWavList[i] = "{0:02d}→{1}, {2}".format(i, copyWavList[i][0], copyWavList[i][1])
            else:
                copyWavList = ["(なし)"]

            return copyWavList
        elif index == 4:
            self.tgaList = listboxInfo
            copyTgaList = copy.deepcopy(self.tgaList)
            if len(copyTgaList) > 0:
                for i in range(len(copyTgaList)):
                    copyTgaList[i] = "{0:02d}→{1}, {2}".format(i, copyTgaList[i]["tgaInfo"], copyTgaList[i]["tgaElse"])
            else:
                copyTgaList = ["(なし)"]

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
        result = HeaderEditDialog(self.master, "ヘッダー情報修正", self.decryptFile.ver, "modify", self.selectListNum, self.selectIndexNum, selectList)
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
        result = HeaderEditDialog(self.master, "ヘッダー情報挿入", self.decryptFile.ver, "insert", self.selectListNum, self.selectIndexNum, selectList)
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
            msg += "画像情報の"
        elif self.selectListNum == 1:
            msg += "画像サイズ情報の"
        elif self.selectListNum == 2:
            msg += "smf情報の"
        elif self.selectListNum == 3:
            msg += "SE情報の"
        elif self.selectListNum == 4:
            msg += "tga情報の"

        msg += "{0}番目を削除します。\nそれでもよろしいですか？".format(self.selectIndexNum + 1)
        result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
        if result:
            self.dirtyFlag = True
            if self.selectListNum == 0:
                self.imgList.pop(self.selectIndexNum)
                copyImgList = self.setListboxInfo(0, self.imgList)
                self.v_imgList.set(copyImgList)
                if len(self.imgList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
            elif self.selectListNum == 1:
                self.imgSizeList.pop(self.selectIndexNum)
                copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
                self.v_imgSize.set(copyImgSizeList)
                if len(self.imgSizeList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
            elif self.selectListNum == 2:
                self.smfList.pop(self.selectIndexNum)
                copySmfList = self.setListboxInfo(2, self.smfList)
                self.v_smfList.set(copySmfList)
                if len(self.smfList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
            elif self.selectListNum == 3:
                self.wavList.pop(self.selectIndexNum)
                copyWavList = self.setListboxInfo(3, self.wavList)
                self.v_wavList.set(copyWavList)
                if len(self.wavList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
            elif self.selectListNum == 4:
                self.tgaList.pop(self.selectIndexNum)
                copyTgaList = self.setListboxInfo(4, self.tgaList)
                self.v_tgaList.set(copyTgaList)
                if len(self.tgaList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"

    def validate(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title="警告", message="変更を保存しますか？", icon="warning", parent=self)
            if result:
                if not self.decryptFile.saveHeader(self.imgList, self.imgSizeList, self.smfList, self.wavList, self.tgaList):
                    self.decryptFile.printError()
                    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False
            else:
                self.dirtyFlag = False
        return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title="成功", message="ヘッダー情報を改造しました")
            self.reloadFlag = True


class HeaderEditDialog(sd.Dialog):
    def __init__(self, master, title, ver, mode, selectListNum, selectIndexNum, selectList):
        self.ver = ver
        self.mode = mode
        self.selectListNum = selectListNum
        self.selectIndexNum = selectIndexNum
        self.selectList = selectList
        self.dirtyFlag = False
        super(HeaderEditDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        if self.selectListNum == 0:
            self.imgNameLb = ttk.Label(master, text="イメージ名", font=("", 12))
            self.imgNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.v_imgName = tkinter.StringVar()
            self.imgNameEt = ttk.Entry(master, font=("", 12), textvariable=self.v_imgName)
            self.imgNameEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

            if self.ver == 4:
                self.imgElse1Lb = ttk.Label(master, text="要素1", font=("", 12))
                self.imgElse1Lb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
                self.v_imgElse1 = tkinter.StringVar()
                self.imgElseCb = ttk.Combobox(master, state="readonly", font=("", 12), textvariable=self.v_imgElse1, values=[0, 1])
                self.imgElseCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)
                self.imgElseCb.current(0)
                self.imgElseCb.bind("<<ComboboxSelected>>", self.imgElseCbChange)

                self.imgElse2Lb = ttk.Label(master, text="要素2", font=("", 12))
                self.imgElse2Lb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
                self.v_imgElse2 = tkinter.StringVar()
                self.imgElseEt = ttk.Entry(master, font=("", 12), textvariable=self.v_imgElse2, state="disabled")
                self.imgElseEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)

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
            self.imgIndexLb = ttk.Label(master, text="画像ファイル\nINDEX", font=("", 12))
            self.imgIndexLb.grid(row=1, column=0)
            self.imgIndex_xLb = ttk.Label(master, text="x座標", font=("", 12))
            self.imgIndex_xLb.grid(row=2, column=0)
            self.imgIndex_yLb = ttk.Label(master, text="y座標", font=("", 12))
            self.imgIndex_yLb.grid(row=3, column=0)
            self.imgIndex_widthLb = ttk.Label(master, text="横長さ", font=("", 12))
            self.imgIndex_widthLb.grid(row=4, column=0)
            self.imgIndex_heightLb = ttk.Label(master, text="縦長さ", font=("", 12))
            self.imgIndex_heightLb.grid(row=5, column=0)

            self.v_imgIndex = tkinter.IntVar()
            self.v_imgIndex_x = tkinter.DoubleVar()
            self.v_imgIndex_y = tkinter.DoubleVar()
            self.v_imgIndex_width = tkinter.DoubleVar()
            self.v_imgIndex_height = tkinter.DoubleVar()
            self.imgIndexEt = ttk.Entry(master, textvariable=self.v_imgIndex, font=("", 12))
            self.imgIndexEt.grid(row=1, column=1)
            self.imgIndex_xEt = ttk.Entry(master, textvariable=self.v_imgIndex_x, font=("", 12))
            self.imgIndex_xEt.grid(row=2, column=1)
            self.imgIndex_yEt = ttk.Entry(master, textvariable=self.v_imgIndex_y, font=("", 12))
            self.imgIndex_yEt.grid(row=3, column=1)
            self.imgIndex_widthEt = ttk.Entry(master, textvariable=self.v_imgIndex_width, font=("", 12))
            self.imgIndex_widthEt.grid(row=4, column=1)
            self.imgIndex_heightEt = ttk.Entry(master, textvariable=self.v_imgIndex_height, font=("", 12))
            self.imgIndex_heightEt.grid(row=5, column=1)

            if self.mode == "modify":
                self.v_imgIndex.set(int(self.selectList[self.selectIndexNum][0]))
                self.v_imgIndex_x.set(float(self.selectList[self.selectIndexNum][1][0]))
                self.v_imgIndex_y.set(float(self.selectList[self.selectIndexNum][1][1]))
                self.v_imgIndex_width.set(float(self.selectList[self.selectIndexNum][1][2]))
                self.v_imgIndex_height.set(float(self.selectList[self.selectIndexNum][1][3]))
            else:
                self.setInsertWidget(master, 6)
        elif self.selectListNum == 2:
            self.smfNameLb = ttk.Label(master, text="smfファイル名", font=("", 12))
            self.smfNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.v_smfName = tkinter.StringVar()
            self.smfNameEt = ttk.Entry(master, font=("", 12), textvariable=self.v_smfName)
            self.smfNameEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

            if self.mode == "modify":
                self.v_smfName.set(self.selectList[self.selectIndexNum])
            else:
                self.setInsertWidget(master, 1)
        elif self.selectListNum == 3:
            self.wavNameLb = ttk.Label(master, text="SEファイル名", font=("", 12))
            self.wavNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.v_wavName = tkinter.StringVar()
            self.wavNameEt = ttk.Entry(master, font=("", 12), textvariable=self.v_wavName)
            self.wavNameEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

            self.wavCntLb = ttk.Label(master, text="グループ取得数", font=("", 12))
            self.wavCntLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
            self.v_wavCnt = tkinter.IntVar()
            self.wavCntEt = ttk.Entry(master, font=("", 12), textvariable=self.v_wavCnt)
            self.wavCntEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)

            if self.mode == "modify":
                self.v_wavName.set(self.selectList[self.selectIndexNum][0])
                self.v_wavCnt.set(int(self.selectList[self.selectIndexNum][1]))
            else:
                self.setInsertWidget(master, 2)
        elif self.selectListNum == 4:
            self.tgaName1Lb = ttk.Label(master, text="TGAファイル名1", font=("", 12))
            self.tgaName1Lb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaName1 = tkinter.StringVar()
            self.tgaName1Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaName1)
            self.tgaName1Et.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

            self.tgaName2Lb = ttk.Label(master, text="TGAファイル名2", font=("", 12))
            self.tgaName2Lb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaName2 = tkinter.StringVar()
            self.tgaName2Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaName2)
            self.tgaName2Et.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)

            self.tgaEle1Lb = ttk.Label(master, text="要素1", font=("", 12))
            self.tgaEle1Lb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaEle1 = tkinter.DoubleVar()
            self.tgaEle1Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaEle1)
            self.tgaEle1Et.grid(row=2, column=1, sticky=tkinter.W + tkinter.E)

            self.tgaEle2Lb = ttk.Label(master, text="要素2", font=("", 12))
            self.tgaEle2Lb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaEle2 = tkinter.DoubleVar()
            self.tgaEle2Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaEle2)
            self.tgaEle2Et.grid(row=3, column=1, sticky=tkinter.W + tkinter.E)

            self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
            self.xLine.grid(row=4, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

            self.tgaElseB1Lb = ttk.Label(master, text="B1", font=("", 12))
            self.tgaElseB1Lb.grid(row=5, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaElseB1 = tkinter.IntVar()
            self.tgaElseB1Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaElseB1)
            self.tgaElseB1Et.grid(row=5, column=1, sticky=tkinter.W + tkinter.E)

            self.tgaElseB2Lb = ttk.Label(master, text="B2", font=("", 12))
            self.tgaElseB2Lb.grid(row=6, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaElseB2 = tkinter.IntVar()
            self.tgaElseB2Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaElseB2)
            self.tgaElseB2Et.grid(row=6, column=1, sticky=tkinter.W + tkinter.E)

            self.tgaElseB3Lb = ttk.Label(master, text="B3", font=("", 12))
            self.tgaElseB3Lb.grid(row=7, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaElseB3 = tkinter.IntVar()
            self.tgaElseB3Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaElseB3)
            self.tgaElseB3Et.grid(row=7, column=1, sticky=tkinter.W + tkinter.E)

            self.tgaElseB4Lb = ttk.Label(master, text="B4", font=("", 12))
            self.tgaElseB4Lb.grid(row=8, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaElseB4 = tkinter.IntVar()
            self.tgaElseB4Et = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaElseB4)
            self.tgaElseB4Et.grid(row=8, column=1, sticky=tkinter.W + tkinter.E)

            self.tgaElsePerLb = ttk.Label(master, text="per", font=("", 12))
            self.tgaElsePerLb.grid(row=9, column=0, sticky=tkinter.W + tkinter.E)
            self.v_tgaElsePer = tkinter.IntVar()
            self.tgaElsePerEt = ttk.Entry(master, font=("", 12), textvariable=self.v_tgaElsePer)
            self.tgaElsePerEt.grid(row=9, column=1, sticky=tkinter.W + tkinter.E)

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

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text="挿入する位置", font=("", 12))
        self.insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=("", 12), textvariable=self.v_insert, values=["後", "前"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
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
            msg = "このまま修正してもよろしいですか？"
        else:
            msg = "このまま挿入してもよろしいですか？"
        result = mb.askokcancel(title="確認", message=msg, parent=self)
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
                    mb.showerror(title="エラー", message="不正な値があります")
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
                    mb.showerror(title="エラー", message="不正な値があります")
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
                    mb.showerror(title="エラー", message="不正な値があります")
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
                    mb.showerror(title="エラー", message="不正な値があります")
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
                    mb.showerror(title="エラー", message="不正な値があります")
                    return False

    def apply(self):
        self.dirtyFlag = True


class ListNumModifyDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, curVal):
        self.decryptFile = decryptFile
        self.num = num
        self.curVal = curVal
        self.reloadFlag = False
        super(ListNumModifyDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.listLb = ttk.Label(master, text="セクション{0}の数を".format(self.num), font=("", 14))
        self.listLb.grid(row=0, column=0)

        self.v_listNum = tkinter.IntVar()
        self.v_listNum.set(self.curVal)
        self.sp = ttk.Spinbox(master, textvariable=self.v_listNum, font=("", 12), from_=1, to=100, width=5)
        self.sp.grid(row=0, column=1, padx=10)

        self.list2Lb = ttk.Label(master, text="に修正する", font=("", 14))
        self.list2Lb.grid(row=0, column=2)

    def validate(self):
        if self.v_listNum.get() < self.curVal:
            warnMsg = "選択した数は現在より少なく設定してます\nこの数で修正しますか？"
            result = mb.askokcancel(title="確認", message=warnMsg, icon="warning", parent=self)
        else:
            infoMsg = "この数で修正しますか？"
            result = mb.askokcancel(title="確認", message=infoMsg, parent=self)

        if result:
            if not self.decryptFile.saveFile(int(self.num), 0, -1, "list", self.v_listNum.get()):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="セクションの数を改造しました")
        self.reloadFlag = True


class ListHeaderModifyDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, listNum, headerInfo):
        self.decryptFile = decryptFile
        self.num = num
        self.listNum = listNum
        self.headerInfo = headerInfo
        self.v_paramList = []
        self.reloadFlag = False
        super(ListHeaderModifyDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        for i in range(3):
            self.paramLb = ttk.Label(master, text="param{0}".format(i + 1), font=("", 14))
            self.paramLb.grid(row=i, column=0, sticky=tkinter.N + tkinter.S)
            self.v_param = tkinter.IntVar()
            self.v_param.set(self.headerInfo[i])
            self.v_paramList.append(self.v_param)
            self.paramEt = ttk.Entry(master, textvariable=self.v_param, width=30)
            self.paramEt.grid(row=i, column=1, sticky=tkinter.N + tkinter.S)

    def validate(self):
        headerList = []
        try:
            for i in range(3):
                param = self.v_paramList[i].get()
                param = int(param)
                headerList.append(param)

            infoMsg = "この数で修正しますか？"
            result = mb.askokcancel(title="確認", message=infoMsg, parent=self)

            if result:
                if not self.decryptFile.saveListHeader(self.num, self.listNum, headerList):
                    self.decryptFile.printError()
                    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False
                return True
        except Exception:
            mb.showerror(title="エラー", message="不正な値があります")
            return False

    def apply(self):
        mb.showinfo(title="成功", message="リストの数を改造しました")
        self.reloadFlag = True


class NumModifyDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, curVal):
        self.decryptFile = decryptFile
        self.curVal = curVal
        self.reloadFlag = False
        super(NumModifyDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.numLb = ttk.Label(master, text="リストの数を", font=("", 14))
        self.numLb.grid(row=0, column=0)

        self.v_num = tkinter.IntVar()
        self.v_num.set(self.curVal)
        self.sp = ttk.Spinbox(master, textvariable=self.v_num, font=("", 12), from_=1, to=100, width=5)
        self.sp.grid(row=0, column=1, padx=10)

        self.num2Lb = ttk.Label(master, text="に修正する", font=("", 14))
        self.num2Lb.grid(row=0, column=2)

    def validate(self):
        if self.v_num.get() < self.curVal:
            warnMsg = "選択した数は現在より少なく設定してます\nこの数で修正しますか？"
            result = mb.askokcancel(title="確認", message=warnMsg, icon="warning", parent=self)
        else:
            infoMsg = "この数で修正しますか？"
            result = mb.askokcancel(title="確認", message=infoMsg, parent=self)

        if result:
            if not self.decryptFile.saveNumFile(self.v_num.get()):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="リストの数を改造しました")
        self.reloadFlag = True
