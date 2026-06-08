import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog

import program.sub.musicEditor.dendDecrypt.BSMusicDecrypt as dendBs
import program.sub.musicEditor.dendDecrypt.CSMusicDecrypt as dendCs
import program.sub.musicEditor.dendDecrypt.RSMusicDecrypt as dendRs

from program.sub.musicEditor.importPy.tkinterScrollbarTreeviewMusicEditor import ScrollbarTreeviewMusicEditor


class MusicEditorWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict, rootFrameAppearance):
        super().__init__(master)
        self.importDict = importDict
        self.rootFrameAppearance = rootFrameAppearance
        self.decryptFile = None
        self.selectId = None
        self.BS = 1
        self.CS = 2
        self.RS = 3

        headerFrame = ttkCustomWidget.CustomTtkFrame(master)
        headerFrame.pack(fill=tkinter.X, padx=40, pady=(25, 0))

        radioFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        radioFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        self.v_radio = tkinter.IntVar(value=self.RS)

        bsRb = ttkCustomWidget.CustomTtkRadiobutton(radioFrame, text="Burning Stage", command=self.deleteWidget, variable=self.v_radio, value=self.BS)
        bsRb.grid(row=0, column=0, padx=(0, 50))

        csRb = ttkCustomWidget.CustomTtkRadiobutton(radioFrame, text="Climax Stage", command=self.deleteWidget, variable=self.v_radio, value=self.CS)
        csRb.grid(row=0, column=1, padx=(0, 50))

        rsRb = ttkCustomWidget.CustomTtkRadiobutton(radioFrame, text="Rising Stage", command=self.deleteWidget, variable=self.v_radio, value=self.RS)
        rsRb.grid(row=0, column=2, padx=(0, 50))

        btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
        btnFrame.pack(fill=tkinter.X)

        self.edit_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["musicEditor"]["bgmModifyLabel"], width=30, command=self.editMusic, state="disabled")
        self.edit_button.grid(row=0, column=0)

        self.swap_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["musicEditor"]["bgmSwapLabel"], width=30, command=self.swapMusic, state="disabled")
        self.swap_button.grid(row=0, column=1)

        btnFrame.grid_columnconfigure(0, weight=1)
        btnFrame.grid_columnconfigure(1, weight=1)

        self.bgmLf = ttkCustomWidget.CustomTtkLabelFrame(master, text=textSetting.textList["musicEditor"]["scriptLabel"])
        self.bgmLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))

    def deleteWidget(self):
        children = self.bgmLf.winfo_children()
        for child in children:
            child.destroy()

        self.edit_button["state"] = "disabled"
        self.swap_button["state"] = "disabled"

    def createMusicTable(self):
        btnList = [
            self.edit_button,
            self.swap_button
        ]
        self.frame = ScrollbarTreeviewMusicEditor(self.bgmLf, btnList)

        treeHeaderList = []

        for i in range(len(self.decryptFile.headerList)):
            treeHeaderList.append(self.decryptFile.headerList[i][0])

        self.frame.tree["columns"] = tuple(treeHeaderList)

        self.frame.tree.column("#0", width=0, stretch="no")
        for i in range(len(self.decryptFile.headerList)):
            self.frame.tree.column(self.decryptFile.headerList[i][0], anchor=tkinter.CENTER, width=self.decryptFile.headerList[i][1])
            self.frame.tree.heading(self.decryptFile.headerList[i][0], text=self.decryptFile.headerList[i][0], anchor=tkinter.CENTER)

        for i in range(len(self.decryptFile.musicList)):
            data = tuple([i + 1]) + tuple(self.decryptFile.musicList[i])
            self.frame.tree.insert(parent="", index="end", iid=i, values=data)

    def openFile(self):
        if self.v_radio.get() == self.BS:
            fileType = [(textSetting.textList["musicEditor"]["fileType"], "LS_INFO.BIN")]
        elif self.v_radio.get() == self.CS:
            fileType = [(textSetting.textList["musicEditor"]["fileType"], "SOUNDTRACK_INFO.BIN")]
        else:
            fileType = [(textSetting.textList["musicEditor"]["fileType"], "SOUNDTRACK_INFO_4TH.BIN")]

        file_path = fd.askopenfilename(filetypes=fileType)
        if not file_path:
            return

        del self.decryptFile
        if self.v_radio.get() == self.BS:
            self.decryptFile = dendBs.BSMusicDecrypt(file_path)
        elif self.v_radio.get() == self.CS:
            self.decryptFile = dendCs.CSMusicDecrypt(file_path)
        else:
            self.decryptFile = dendRs.RSMusicDecrypt(file_path)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E21"])
            return

        self.deleteWidget()
        self.createMusicTable()
    
    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.decryptFile.musicList):
                self.selectId = len(self.decryptFile.musicList) - 1
            self.frame.tree.selection_set(self.selectId)
            self.frame.tree.see(self.selectId)

    def reloadFile(self):
        self.decryptFile = self.decryptFile.reload()
        self.deleteWidget()
        self.createMusicTable()
        self.jumpToSelect()

    def editMusic(self):
        selectId = self.frame.tree.selection()[0]
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["No"]) - 1

        bgmItem = self.decryptFile.musicList[num][1:]
        headerList = [x[0] for x in self.decryptFile.headerList[2:]]
        result = EditMusicInfoDialog(self.edit_button.winfo_toplevel(), textSetting.textList["musicEditor"]["bgmModify"], bgmItem, headerList, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveMusic(num, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I41"])
            self.selectId = num
            self.reloadFile()

    def swapMusic(self):
        selectId = self.frame.tree.selection()[0]
        selectItem = self.frame.tree.set(selectId)
        num = int(selectItem["No"]) - 1
        result = SwapMusicDialog(self.swap_button.winfo_toplevel(), textSetting.textList["musicEditor"]["bgmSwap"], num, self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.swapMusic(num, result.swapMusicNo):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I41"])
            self.selectId = num
            self.reloadFile()


class EditMusicInfoDialog(CustomSimpleDialog):
    def __init__(self, master, title, bgmItem, headerList, rootFrameAppearance):
        self.bgmItem = bgmItem
        self.headerList = headerList
        self.varList = []
        self.varCnt = 0
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i, header in enumerate(self.headerList):
            eleLb = ttkCustomWidget.CustomTtkLabel(master, text=header, font=textSetting.textList["font2"])
            eleLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            self.varList.append(tkinter.StringVar(value=self.bgmItem[i]))
            eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt])
            eleEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.varCnt += 1
        super().body(master)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueList = []
        for i, var in enumerate(self.varList):
            if i > 1:
                try:
                    float(var.get())
                except ValueError:
                    mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                    return
                self.resultValueList.append(float(var.get()))
            else:
                if not var.get():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E139"].format(self.headerList[i]))
                    return False
                self.resultValueList.append(var.get())
        return True

    def apply(self):
        self.reloadFlag = True


class SwapMusicDialog(CustomSimpleDialog):
    def __init__(self, master, title, num, decryptFile, rootFrameAppearance):
        self.num = num
        self.decryptFile = decryptFile
        self.swapMusicNoList = []
        self.swapMusicNo = -1
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["musicEditor"]["changeBgmNum"], font=textSetting.textList["font2"])
        swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        swapMusicCbList = []
        for index, musicInfo in enumerate(self.decryptFile.musicList):
            if index == self.num:
                continue
            self.swapMusicNoList.append(index)
            swapMusicCbList.append("%02d(%s)" % (index + 1, musicInfo[2]))

        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, width=20, state="readonly", font=textSetting.textList["font2"], value=swapMusicCbList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        self.swapCb.current(0)
        super().body(master)

    def validate(self):
        swapCbIdx = self.swapCb.current()
        self.swapMusicNo = self.swapMusicNoList[swapCbIdx]
        warnMsg = textSetting.textList["infoList"]["I40"].format(self.num + 1, self.swapMusicNo + 1) + textSetting.textList["infoList"]["I39"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            return True

    def apply(self):
        self.reloadFlag = True
