import copy
import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class MusicWidget:
    def __init__(self, root, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        txtFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        txtFrame.pack(anchor=tkinter.NW, padx=10, pady=5)

        musicLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["railEditor"]["bgmNum"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        musicLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varMusic = tkinter.IntVar()
        self.varMusic.set(self.decryptFile.musicCnt)
        musicTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varMusic, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        musicTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game in ["CS", "RS"]:
            musicBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editVar(self.varMusic.get()))
            musicBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        else:
            musicBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editMusicList())
            musicBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditMusicCnt(self.root, textSetting.textList["railEditor"]["editBgmNumLabel"], self.decryptFile, value, self.rootFrameAppearance)

        if result.reloadFlag:
            if not self.decryptFile.saveMusic(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I69"])

            self.reloadFunc()

    def editMusicList(self):
        result = EditMusicList(self.root, textSetting.textList["railEditor"]["editBgmListLabel"], self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveMusicList(result.musicList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I69"])
            self.reloadFunc()


class EditMusicCnt(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, val, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = val
        self.reloadFlag = False
        self.resultValue = 0
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()

        self.varMusicCnt = tkinter.IntVar()
        self.varMusicCnt.set(self.val)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varMusicCnt, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varMusicCnt.get())
                    if res <= 0:
                        errorMsg = textSetting.textList["errorList"]["E61"].format(1)
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
                    self.resultValue = res
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


class EditMusicList(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.musicList = copy.deepcopy(decryptFile.musicList)
        self.dirtyFlag = False
        self.reloadFlag = False
        self.resultList = []
        self.rootFrameAppearance = rootFrameAppearance
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.frame = master
        self.resizable(False, False)

        btnFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        btnFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)

        if self.decryptFile.game != "LS":
            self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
            self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
            self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        listFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        listFrame.pack()

        copyMusicList = self.setListboxInfo(self.musicList)
        self.v_musicList = tkinter.StringVar(value=copyMusicList)
        musicListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=55, height=6, listvariable=self.v_musicList, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
        musicListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        musicListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(musicListListbox, musicListListbox.curselection()))
        super().body(master)

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            if listbox.get(value[0]) == textSetting.textList["railEditor"]["noList"]:
                self.modifyBtn["state"] = "disabled"
                self.deleteBtn["state"] = "disabled"
            else:
                self.modifyBtn["state"] = "normal"
                self.deleteBtn["state"] = "normal"
            self.insertBtn["state"] = "normal"
        else:
            self.modifyBtn["state"] = "normal"

    def setListboxInfo(self, musicList):
        copyMusicList = copy.deepcopy(musicList)
        if len(copyMusicList) > 0:
            for i in range(len(copyMusicList)):
                musicInfo = copyMusicList[i]
                copyMusicList[i] = "{0:02d}→{1}".format(i, musicInfo)
        else:
            copyMusicList = [textSetting.textList["railEditor"]["noList"]]

        return copyMusicList

    def modify(self):
        result = EditMusicListWidget(self.frame, textSetting.textList["railEditor"]["modifyBgmLabel"], self.decryptFile, "modify", self.selectIndexNum, self.musicList, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.musicList[self.selectIndexNum] = result.resultValueList
            copyMusicList = self.setListboxInfo(self.musicList)
            self.v_musicList.set(copyMusicList)

    def insert(self):
        result = EditMusicListWidget(self.frame, textSetting.textList["railEditor"]["insertBgmLabel"], self.decryptFile, "insert", self.selectIndexNum, self.musicList, self.rootFrameAppearance)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.musicList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
            copyMusicList = self.setListboxInfo(self.musicList)
            self.v_musicList.set(copyMusicList)

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
        if result:
            self.dirtyFlag = True
            self.musicList.pop(self.selectIndexNum)
            copyMusicList = self.setListboxInfo(self.musicList)
            self.v_musicList.set(copyMusicList)
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


class EditMusicListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, index, musicList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.index = index
        self.musicList = musicList
        self.varList = []
        self.resultValueList = []
        self.insertPos = -1
        self.dirtyFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        musicInfoLb = textSetting.textList["railEditor"]["editBgmInfoLabelList"]
        for i in range(len(musicInfoLb)):
            musicLb = ttkCustomWidget.CustomTtkLabel(master, text=musicInfoLb[i], font=textSetting.textList["font2"])
            musicLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i == 2 or i == 3:
                self.varMusic = tkinter.DoubleVar()
                if self.mode == "modify":
                    musicInfo = self.musicList[self.index]
                    self.varMusic.set(musicInfo[i])
            else:
                self.varMusic = tkinter.StringVar()
                if self.mode == "modify":
                    musicInfo = self.musicList[self.index]
                    self.varMusic.set(musicInfo[i])
            self.varList.append(self.varMusic)
            musicEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varMusic, font=textSetting.textList["font2"])
            musicEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(musicInfoLb))
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
                    if i == 2 or i == 3:
                        try:
                            res = float(self.varList[i].get())
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                            return False
                    else:
                        res = str(self.varList[i].get())
                    self.resultValueList.append(res)
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.dirtyFlag = True
