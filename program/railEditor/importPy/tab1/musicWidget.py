import copy
import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting


class MusicWidget:
    def __init__(self, frame, decryptFile, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc

        self.txtFrame = tkinter.Frame(self.frame, padx=10, pady=5)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.musicLb = tkinter.Label(self.txtFrame, text=textSetting.textList["railEditor"]["bgmNum"], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.musicLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varMusic = tkinter.IntVar()
        self.varMusic.set(self.decryptFile.musicCnt)
        self.musicTextLb = tkinter.Label(self.txtFrame, textvariable=self.varMusic, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.musicTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game in ["CS", "RS"]:
            self.musicBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editVar(self.varMusic.get()))
            self.musicBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        else:
            self.musicBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editMusicList())
            self.musicBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditMusicCnt(self.frame, textSetting.textList["railEditor"]["editBgmNumLabel"], self.decryptFile, value)

        if result.reloadFlag:
            if not self.decryptFile.saveMusic(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I69"])

            self.reloadFunc()

    def editMusicList(self):
        result = EditMusicList(self.frame, textSetting.textList["railEditor"]["editBgmListLabel"], self.decryptFile)
        if result.reloadFlag:
            if not self.decryptFile.saveMusicList(result.musicList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I69"])
            self.reloadFunc()


class EditMusicCnt(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.reloadFlag = False
        self.resultValue = 0
        super(EditMusicCnt, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.pack()

        self.varMusicCnt = tkinter.IntVar()
        self.varMusicCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varMusicCnt, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()

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


class EditMusicList(sd.Dialog):
    def __init__(self, master, title, decryptFile):
        self.decryptFile = decryptFile
        self.musicList = copy.deepcopy(decryptFile.musicList)
        self.dirtyFlag = False
        self.reloadFlag = False
        self.resultList = []
        super(EditMusicList, self).__init__(parent=master, title=title)

    def body(self, master):
        self.frame = master
        self.resizable(False, False)

        self.btnFrame = ttk.Frame(self.frame)
        self.btnFrame.pack()

        self.modifyBtn = tkinter.Button(self.btnFrame, font=textSetting.textList["font2"], text=textSetting.textList["modify"], state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)

        if self.decryptFile.game != "LS":
            self.insertBtn = tkinter.Button(self.btnFrame, font=textSetting.textList["font2"], text=textSetting.textList["insert"], state="disabled", command=self.insert)
            self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.deleteBtn = tkinter.Button(self.btnFrame, font=textSetting.textList["font2"], text=textSetting.textList["delete"], state="disabled", command=self.delete)
            self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.listFrame = ttk.Frame(self.frame)
        self.listFrame.pack()

        copyMusicList = self.setListboxInfo(self.musicList)
        self.v_musicList = tkinter.StringVar(value=copyMusicList)
        self.musicListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=textSetting.textList["font2"], width=55, listvariable=self.v_musicList)
        self.musicListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.musicListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.musicListListbox, self.musicListListbox.curselection()))

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
        result = EditMusicListWidget(self.frame, textSetting.textList["railEditor"]["modifyBgmLabel"], self.decryptFile, "modify", self.selectIndexNum, self.musicList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.musicList[self.selectIndexNum] = result.resultValueList
            copyMusicList = self.setListboxInfo(self.musicList)
            self.v_musicList.set(copyMusicList)

    def insert(self):
        result = EditMusicListWidget(self.frame, textSetting.textList["railEditor"]["insertBgmLabel"], self.decryptFile, "insert", self.selectIndexNum, self.musicList)
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


class EditMusicListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, index, musicList):
        self.decryptFile = decryptFile
        self.mode = mode
        self.index = index
        self.musicList = musicList
        self.varList = []
        self.resultValueList = []
        self.insertPos = -1
        self.dirtyFlag = False
        super(EditMusicListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        musicInfoLb = textSetting.textList["railEditor"]["editBgmInfoLabelList"]
        for i in range(len(musicInfoLb)):
            self.musicLb = ttk.Label(master, text=musicInfoLb[i], font=textSetting.textList["font2"])
            self.musicLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
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
            self.musicEt = ttk.Entry(master, textvariable=self.varMusic, font=textSetting.textList["font2"])
            self.musicEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(musicInfoLb))

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
