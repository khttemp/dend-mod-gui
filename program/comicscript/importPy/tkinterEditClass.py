import copy

import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb


class InputDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, cmdItem=None):
        self.decryptFile = decryptFile
        self.num = num
        self.cmdItem = cmdItem
        self.v_paramList = []
        self.reloadFlag = False
        if self.cmdItem is not None:
            self.mode = "modify"
            self.infoMsg = "このまま修正してもよろしいですか？"
            self.p_cmd = self.cmdItem["コマンド名"]
            self.p_cnt = len(self.cmdItem)-2
        else:
            self.mode = "insert"
            self.infoMsg = "このまま挿入してもよろしいですか？"
            self.p_cmd = None
            self.p_cnt = None
        super(InputDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.cmdLb = ttk.Label(master, text="コマンド名", width=12, font=("", 12))
        self.cmdLb.grid(row=0, column=0, sticky=tkinter.N+tkinter.S)
        self.v_cmd = tkinter.StringVar()
        cmdCopy = copy.deepcopy(self.decryptFile.cmdList)
        cmdCopy.sort()
        self.cmdCb = ttk.Combobox(master, font=("", 12), textvariable=self.v_cmd, width=25, state="readonly", value=cmdCopy)
        self.cmdCb.grid(row=0, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        if self.p_cmd is not None:
            self.v_cmd.set(self.p_cmd)
        else:
            self.v_cmd.set(cmdCopy[0])

        self.paramCntLb = ttk.Label(master, text="パラメータ数", width=12, font=("", 12))
        self.paramCntLb.grid(row=1, column=0, sticky=tkinter.N+tkinter.S)
        self.v_paramCnt = tkinter.IntVar()
        paramCntList = [cnt for cnt in range(0, 16)]
        self.paramCntCb = ttk.Combobox(master, font=("", 12), textvariable=self.v_paramCnt, width=25, state="readonly", value=paramCntList)
        self.paramCntCb.grid(row=1, column=1, sticky=tkinter.N+tkinter.S, pady=10)
        if self.p_cnt is not None:
            self.v_paramCnt.set(self.p_cnt)
        else:
            self.v_paramCnt.set(0)

        if self.cmdItem is None:
            self.position = ttk.Label(master, text="挿入する位置", width=12, font=("", 12))
            self.position.grid(row=2, column=0, sticky=tkinter.N+tkinter.S)
            self.v_position = tkinter.StringVar()
            positionList = ["後", "前"]
            self.positionCb = ttk.Combobox(master, font=("", 12), textvariable=self.v_position, width=25, state="readonly", value=positionList)
            self.positionCb.grid(row=2, column=1, sticky=tkinter.N+tkinter.S, pady=10)
            self.v_position.set(positionList[0])

        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(columnspan=2, row=3, column=0, sticky=tkinter.E+tkinter.W, pady=10)

        self.paramFrame = ttk.tkinter.Frame(master)
        self.paramFrame.grid(columnspan=2, row=4, column=0, sticky=tkinter.N+tkinter.E+tkinter.W+tkinter.S)

        self.paramLb = ttk.Label(self.paramFrame)
        self.paramLb.grid(row=0, column=0)

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
            self.paramLb = ttk.Label(frame, text="param{0}".format(i+1), width=12, font=("", 12))
            self.paramLb.grid(row=i, column=0, sticky=tkinter.N+tkinter.S)
            v_param = tkinter.DoubleVar()
            self.v_paramList.append(v_param)
            self.paramEt = ttk.Entry(frame, font=("", 12), textvariable=v_param, width=27)
            self.paramEt.grid(row=i, column=1, sticky=tkinter.N+tkinter.S)
        if cmdItem is not None:
            for i in range(len(self.v_paramList)):
                self.v_paramList[i].set(cmdItem["param{0}".format(i+1)])

    def validate(self):
        editParamList = []
        try:
            for var in self.v_paramList:
                num = float(var.get())
                editParamList.append(num)
        except Exception:
            errorMsg = "数字で入力してください。"
            mb.showerror(title="数字エラー", message=errorMsg, parent=self)
            return False

        result = mb.askokcancel(title="確認", message=self.infoMsg, parent=self)
        if result:
            comicData = []
            comicData.append(self.v_cmd.get())
            comicData.append(self.v_paramCnt.get())
            for i in range(self.v_paramCnt.get()):
                comicData.append(editParamList[i])

            if self.mode == "insert":
                position = self.v_position.get()
                if position == "後":
                    self.num += 1

            if not self.decryptFile.saveFile(self.mode, self.num, comicData):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="スクリプトを改造しました")
        self.reloadFlag = True


class PasteDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, comicData):
        self.decryptFile = decryptFile
        self.num = num
        self.comicData = comicData
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
        if not self.decryptFile.saveFile("insert", self.num, self.comicData):
            self.decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        self.ok()
        mb.showinfo(title="成功", message="貼り付けしました")
        self.reloadFlag = True

    def backInsert(self):
        if not self.decryptFile.saveFile("insert", self.num + 1, self.comicData):
            self.decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        self.ok()
        mb.showinfo(title="成功", message="貼り付けしました")
        self.reloadFlag = True


class HeaderFileInfo(sd.Dialog):
    def __init__(self, master, title, decryptFile):
        self.master = master
        self.decryptFile = decryptFile
        self.imgList = copy.deepcopy(decryptFile.imgList)
        self.imgSizeList = copy.deepcopy(decryptFile.imgSizeList)
        self.seList = copy.deepcopy(decryptFile.seList)
        self.bgmList = copy.deepcopy(decryptFile.bgmList)
        self.selectListNum = -1
        self.selectIndexNum = -1
        self.dirtyFlag = False
        self.reloadFlag = False
        super(HeaderFileInfo, self).__init__(parent=master, title=title)

    def body(self, master):
        self.btnFrame = tkinter.Frame(master, pady=5)
        self.btnFrame.pack()
        self.listFrame = tkinter.Frame(master)
        self.listFrame.pack()

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W+tkinter.E)
        self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W+tkinter.E)

        self.imgListLb = tkinter.Label(self.listFrame, font=("", 14), text="画像情報")
        self.imgListLb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)

        copyImgList = self.setListboxInfo(0, self.imgList)

        self.v_imgList = tkinter.StringVar(value=copyImgList)
        self.imgListBox = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_imgList)
        self.imgListBox.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.imgListBox.bind('<<ListboxSelect>>', lambda e:  self.buttonActive(e, self.imgListBox, 0, self.imgListBox.curselection()))

        self.padLb = tkinter.Label(self.listFrame, width=3)
        self.padLb.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

        self.imgSizeListLb = tkinter.Label(self.listFrame, font=("", 14), width=40, text="画像サイズ情報")
        self.imgSizeListLb.grid(row=0, column=2, sticky=tkinter.W+tkinter.E)

        copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
        self.v_imgSizeList = tkinter.StringVar(value=copyImgSizeList)
        self.imgSizeListBox = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_imgSizeList)
        self.imgSizeListBox.grid(row=1, column=2, sticky=tkinter.W+tkinter.E)
        self.imgSizeListBox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, self.imgSizeListBox, 1, self.imgSizeListBox.curselection()))

        self.seListLb = tkinter.Label(self.listFrame, font=("", 14), text="SE情報")
        self.seListLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)

        copySeList = self.setListboxInfo(2, self.seList)
        self.v_seList = tkinter.StringVar(value=copySeList)
        self.seListBox = tkinter.Listbox(self.listFrame, font=("", 14), width=40, listvariable=self.v_seList)
        self.seListBox.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
        self.seListBox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, self.seListBox, 2, self.seListBox.curselection()))

        self.padLb = tkinter.Label(self.listFrame, width=3)
        self.padLb.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)

        self.bgmListLb = tkinter.Label(self.listFrame, font=("", 14), text="BGM情報")
        self.bgmListLb.grid(row=2, column=2, sticky=tkinter.W+tkinter.E)

        copyBgmList = self.setListboxInfo(3, self.bgmList)
        self.v_bgmList = tkinter.StringVar(value=copyBgmList)
        self.bgmListBox = tkinter.Listbox(self.listFrame, font=("", 14), listvariable=self.v_bgmList)
        self.bgmListBox.grid(row=3, column=2, sticky=tkinter.W+tkinter.E)
        self.bgmListBox.bind('<<ListboxSelect>>', lambda e: self.buttonActive(e, self.bgmListBox, 3, self.bgmListBox.curselection()))

    def setListboxInfo(self, index, listboxInfo):
        if index == 0:
            if len(listboxInfo) > 0:
                copyImgList = copy.deepcopy(listboxInfo)
                for i in range(len(copyImgList)):
                    copyImgList[i] = "{0:02d}→{1}".format(i, copyImgList[i])
            else:
                copyImgList = ["(なし)"]
            return copyImgList
        elif index == 1:
            if len(listboxInfo) > 0:
                copyImgSizeList = copy.deepcopy(listboxInfo)
                for i in range(len(copyImgSizeList)):
                    copyImgSizeList[i] = "{0:02d}→img{1:02d}, {2}".format(i, copyImgSizeList[i][0], copyImgSizeList[i][1])
            else:
                copyImgSizeList = ["(なし)"]
            return copyImgSizeList
        elif index == 2:
            if len(listboxInfo) > 0:
                copySeList = copy.deepcopy(listboxInfo)
                for i in range(len(copySeList)):
                    copySeList[i] = "{0:02d}→{1} [{2}]".format(i, copySeList[i][0], copySeList[i][1])
            else:
                copySeList = ["(なし)"]
            return copySeList
        elif index == 3:
            if len(listboxInfo) > 0:
                copyBgmList = copy.deepcopy(listboxInfo)
                for i in range(len(copyBgmList)):
                    copyBgmList[i] = "{0:02d}→{1} [{2}], [{3}, {4}]".format(i, copyBgmList[i][0], copyBgmList[i][1], copyBgmList[i][2], copyBgmList[i][3])
            else:
                copyBgmList = ["(なし)"]
            return copyBgmList

    def buttonActive(self, event, listbox, num, value):
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

    def modify(self):
        selectList = None
        if self.selectListNum == 0:
            selectList = self.imgList
        elif self.selectListNum == 1:
            selectList = self.imgSizeList
        elif self.selectListNum == 2:
            selectList = self.seList
        elif self.selectListNum == 3:
            selectList = self.bgmList

        result = HeaderFileEdit(self.master, "ヘッダー情報修正", "modify", self.selectListNum, self.selectIndexNum, selectList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            if self.selectListNum == 0:
                copyImgList = self.setListboxInfo(0, self.imgList)
                self.v_imgList.set(copyImgList)
            elif self.selectListNum == 1:
                copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
                self.v_imgSizeList.set(copyImgSizeList)
            elif self.selectListNum == 2:
                copySeList = self.setListboxInfo(2, self.seList)
                self.v_seList.set(copySeList)
            elif self.selectListNum == 3:
                copyBgmList = self.setListboxInfo(3, self.bgmList)
                self.v_bgmList.set(copyBgmList)

    def insert(self):
        selectList = None
        if self.selectListNum == 0:
            selectList = self.imgList
        elif self.selectListNum == 1:
            selectList = self.imgSizeList
        elif self.selectListNum == 2:
            selectList = self.seList
        elif self.selectListNum == 3:
            selectList = self.bgmList

        result = HeaderFileEdit(self.master, "ヘッダー情報修正", "insert", self.selectListNum, self.selectIndexNum, selectList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            if self.selectListNum == 0:
                copyImgList = self.setListboxInfo(0, self.imgList)
                self.v_imgList.set(copyImgList)
            elif self.selectListNum == 1:
                copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
                self.v_imgSizeList.set(copyImgSizeList)
            elif self.selectListNum == 2:
                copySeList = self.setListboxInfo(2, self.seList)
                self.v_seList.set(copySeList)
            elif self.selectListNum == 3:
                copyBgmList = self.setListboxInfo(3, self.bgmList)
                self.v_bgmList.set(copyBgmList)

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
                if len(self.imgList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
                copyImgList = self.setListboxInfo(0, self.imgList)
                self.v_imgList.set(copyImgList)
            elif self.selectListNum == 1:
                self.imgSizeList.pop(self.selectIndexNum)
                if len(self.imgSizeList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
                copyImgSizeList = self.setListboxInfo(1, self.imgSizeList)
                self.v_imgSizeList.set(copyImgSizeList)
            elif self.selectListNum == 2:
                self.seList.pop(self.selectIndexNum)
                if len(self.seList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
                copySeList = self.setListboxInfo(2, self.seList)
                self.v_seList.set(copySeList)
            elif self.selectListNum == 3:
                self.bgmList.pop(self.selectIndexNum)
                if len(self.bgmList) == 0:
                    self.modifyBtn["state"] = "disabled"
                    self.deleteBtn["state"] = "disabled"
                copyBgmList = self.setListboxInfo(3, self.bgmList)
                self.v_bgmList.set(copyBgmList)

    def validate(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title="警告", message="変更を保存しますか？", icon="warning", parent=self)
            if result:
                if not self.decryptFile.saveHeader(self.imgList, self.imgSizeList, self.seList, self.bgmList):
                    self.decryptFile.printError()
                    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return
                return True
        else:
            return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title="成功", message="ヘッダー情報を改造しました")
            self.reloadFlag = True


class HeaderFileEdit(sd.Dialog):
    def __init__(self, master, title, mode, selectListNum, selectIndexNum, selectList):
        self.mode = mode
        self.selectListNum = selectListNum
        self.selectIndexNum = selectIndexNum
        self.selectList = selectList
        self.dirtyFlag = False
        super(HeaderFileEdit, self).__init__(parent=master, title=title)

    def body(self, master):
        if self.selectListNum == 0:
            self.imgLb = ttk.Label(master, text="画像ファイル名", font=("", 12))
            self.imgLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
            self.v_img = tkinter.StringVar()
            self.imgEt = ttk.Entry(master, textvariable=self.v_img, font=("", 12))
            self.imgEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
            if self.mode == "modify":
                self.v_img.set(self.selectList[self.selectIndexNum])
            else:
                self.setInsertWidget(master, 2)
        elif self.selectListNum == 1:
            self.imgIndexLb = ttk.Label(master, text="画像ファイル\nINDEX", font=("", 12))
            self.imgIndexLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
            self.imgIndex_xLb = ttk.Label(master, text="x座標", font=("", 12))
            self.imgIndex_xLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
            self.imgIndex_yLb = ttk.Label(master, text="y座標", font=("", 12))
            self.imgIndex_yLb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
            self.imgIndex_widthLb = ttk.Label(master, text="横長さ", font=("", 12))
            self.imgIndex_widthLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)
            self.imgIndex_heightLb = ttk.Label(master, text="縦長さ", font=("", 12))
            self.imgIndex_heightLb.grid(row=5, column=0, sticky=tkinter.W+tkinter.E)

            self.v_imgIndex = tkinter.IntVar()
            self.v_imgIndex_x = tkinter.DoubleVar()
            self.v_imgIndex_y = tkinter.DoubleVar()
            self.v_imgIndex_width = tkinter.DoubleVar()
            self.v_imgIndex_height = tkinter.DoubleVar()
            self.imgIndexEt = ttk.Entry(master, textvariable=self.v_imgIndex, font=("", 12))
            self.imgIndexEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
            self.imgIndex_xEt = ttk.Entry(master, textvariable=self.v_imgIndex_x, font=("", 12))
            self.imgIndex_xEt.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)
            self.imgIndex_yEt = ttk.Entry(master, textvariable=self.v_imgIndex_y, font=("", 12))
            self.imgIndex_yEt.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)
            self.imgIndex_widthEt = ttk.Entry(master, textvariable=self.v_imgIndex_width, font=("", 12))
            self.imgIndex_widthEt.grid(row=4, column=1, sticky=tkinter.W+tkinter.E)
            self.imgIndex_heightEt = ttk.Entry(master, textvariable=self.v_imgIndex_height, font=("", 12))
            self.imgIndex_heightEt.grid(row=5, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_imgIndex.set(int(self.selectList[self.selectIndexNum][0]))
                self.v_imgIndex_x.set(float(self.selectList[self.selectIndexNum][1][0]))
                self.v_imgIndex_y.set(float(self.selectList[self.selectIndexNum][1][1]))
                self.v_imgIndex_width.set(float(self.selectList[self.selectIndexNum][1][2]))
                self.v_imgIndex_height.set(float(self.selectList[self.selectIndexNum][1][3]))
            else:
                self.setInsertWidget(master, 6)
        elif self.selectListNum == 2:
            self.seLb = ttk.Label(master, text="SEファイル", font=("", 12))
            self.seLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
            self.seFileCntLb = ttk.Label(master, text="グループ取得数", font=("", 12))
            self.seFileCntLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)

            self.v_se = tkinter.StringVar()
            self.v_seFileCnt = tkinter.IntVar()
            self.seEt = ttk.Entry(master, textvariable=self.v_se, font=("", 12))
            self.seEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
            self.seFileCntEt = ttk.Entry(master, textvariable=self.v_seFileCnt, font=("", 12))
            self.seFileCntEt.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_se.set(self.selectList[self.selectIndexNum][0])
                self.v_seFileCnt.set(int(self.selectList[self.selectIndexNum][1]))
            else:
                self.setInsertWidget(master, 3)
        elif self.selectListNum == 3:
            self.bgmLb = ttk.Label(master, text="BGMファイル", font=("", 12))
            self.bgmLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
            self.bgmLoopFlagLb = ttk.Label(master, text="BGMループフラグ", font=("", 12))
            self.bgmLoopFlagLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
            self.bgmStartLb = ttk.Label(master, text="BGM Start位置", font=("", 12))
            self.bgmStartLb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
            self.bgmLoopStartLb = ttk.Label(master, text="BGM Loop Start位置", font=("", 12))
            self.bgmLoopStartLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)

            self.v_bgm = tkinter.StringVar()
            self.v_bgmLoopFlag = tkinter.IntVar()
            self.v_bgmStart = tkinter.DoubleVar()
            self.v_bgmLoopStart = tkinter.DoubleVar()
            self.bgmEt = ttk.Entry(master, textvariable=self.v_bgm, font=("", 12))
            self.bgmEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
            self.bgmLoopFlagCb = ttk.Combobox(master, width=24, state="readonly", value=["ループしない", "ループする"])
            self.bgmLoopFlagCb.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)
            self.bgmLoopFlagCb.current(self.v_bgmLoopFlag.get())
            self.bgmStartEt = ttk.Entry(master, textvariable=self.v_bgmStart, font=("", 12))
            self.bgmStartEt.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)
            self.bgmLoopStartEt = ttk.Entry(master, textvariable=self.v_bgmLoopStart, font=("", 12))
            self.bgmLoopStartEt.grid(row=4, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.v_bgm.set(self.selectList[self.selectIndexNum][0])
                self.bgmLoopFlagCb.current(int(self.selectList[self.selectIndexNum][1]))
                self.v_bgmStart.set(self.selectList[self.selectIndexNum][2])
                self.v_bgmLoopStart.set(self.selectList[self.selectIndexNum][3])
            else:
                self.setInsertWidget(master, 5)

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text="挿入する位置", font=("", 12))
        self.insertLb.grid(row=index+1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=("", 12), textvariable=self.v_insert, values=["後", "前"])
        self.insertCb.grid(row=index+1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

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
                    imgName = self.v_img.get()
                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = imgName
                    elif self.mode == "insert":
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, imgName)
                        else:
                            self.selectList.insert(self.selectIndexNum, imgName)
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
                    elif self.mode == "insert":
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, imgSizeInfo)
                        else:
                            self.selectList.insert(self.selectIndexNum, imgSizeInfo)
                    return True
                except Exception:
                    errorMsg = "不正な値があります"
                    mb.showerror(title="エラー", message=errorMsg)
                    return False
            elif self.selectListNum == 2:
                try:
                    seList = []
                    seList.append(self.v_se.get())
                    seList.append(int(self.v_seFileCnt.get()))
                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = seList
                    elif self.mode == "insert":
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, seList)
                        else:
                            self.selectList.insert(self.selectIndexNum, seList)
                    return True
                except Exception:
                    errorMsg = "不正な値があります"
                    mb.showerror(title="エラー", message=errorMsg)
                    return False
            elif self.selectListNum == 3:
                try:
                    bgmList = []
                    bgmList.append(self.v_bgm.get())
                    bgmList.append(int(self.bgmLoopFlagCb.current()))
                    bgmList.append(float(self.v_bgmStart.get()))
                    bgmList.append(float(self.v_bgmLoopStart.get()))
                    if self.mode == "modify":
                        self.selectList[self.selectIndexNum] = bgmList
                    elif self.mode == "insert":
                        insertIdx = self.insertCb.current()
                        if insertIdx == 0:
                            self.selectList.insert(self.selectIndexNum + 1, bgmList)
                        else:
                            self.selectList.insert(self.selectIndexNum, bgmList)
                    return True
                except Exception:
                    errorMsg = "不正な値があります"
                    mb.showerror(title="エラー", message=errorMsg)
                    return False

    def apply(self):
        self.dirtyFlag = True
