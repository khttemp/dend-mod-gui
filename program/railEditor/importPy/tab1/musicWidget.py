import copy
import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


class MusicWidget:
    def __init__(self, frame, decryptFile, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc

        self.txtFrame = tkinter.Frame(self.frame, padx=10, pady=5)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.musicLb = tkinter.Label(self.txtFrame, text="BGM数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.musicLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varMusic = tkinter.IntVar()
        self.varMusic.set(self.decryptFile.musicCnt)
        self.musicTextLb = tkinter.Label(self.txtFrame, textvariable=self.varMusic, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.musicTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game in ["CS", "RS"]:
            self.musicBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editVar(self.varMusic.get()))
            self.musicBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        else:
            self.musicBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editMusicList())
            self.musicBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditMusicCnt(self.frame, "BGM数変更", self.decryptFile, value)

        if result.reloadFlag:
            if not self.decryptFile.saveMusic(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="BGM情報を修正しました")

            self.reloadFunc()

    def editMusicList(self):
        result = EditMusicList(self.frame, "BGMリスト変更", self.decryptFile)
        if result.reloadFlag:
            if not self.decryptFile.saveMusicList(result.musicList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return False
            mb.showinfo(title="成功", message="BGMリストを修正しました")
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

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varMusicCnt = tkinter.IntVar()
        self.varMusicCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varMusicCnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varMusicCnt.get())
                    if res <= 0:
                        errorMsg = "1以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValue = res
                    return True
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

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

        self.modifyBtn = tkinter.Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)

        if self.decryptFile.game != "LS":
            self.insertBtn = tkinter.Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
            self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
            self.deleteBtn = tkinter.Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
            self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.listFrame = ttk.Frame(self.frame)
        self.listFrame.pack()

        copyMusicList = self.setListboxInfo(self.musicList)
        self.v_musicList = tkinter.StringVar(value=copyMusicList)
        self.musicListListbox = tkinter.Listbox(self.listFrame, selectmode="single", font=("", 14), width=55, listvariable=self.v_musicList)
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
            if listbox.get(value[0]) == "(なし)":
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
            copyMusicList = ["(なし)"]

        return copyMusicList

    def modify(self):
        result = EditMusicListWidget(self.frame, "BGMの変更", self.decryptFile, "modify", self.selectIndexNum, self.musicList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.musicList[self.selectIndexNum] = result.resultValueList
            copyMusicList = self.setListboxInfo(self.musicList)
            self.v_musicList.set(copyMusicList)

    def insert(self):
        result = EditMusicListWidget(self.frame, "BGMの挿入", self.decryptFile, "insert", self.selectIndexNum, self.musicList)
        if result.dirtyFlag:
            self.dirtyFlag = True
            self.musicList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
            copyMusicList = self.setListboxInfo(self.musicList)
            self.v_musicList.set(copyMusicList)

    def delete(self):
        msg = "{0}番目を削除します。\nそれでもよろしいですか？".format(self.selectIndexNum + 1)
        result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
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
            result = mb.askokcancel(title="確認", message="このリストで修正しますか？", parent=self)
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

        musicInfoLb = ["ファイル名", "BGM名", "start", "loopStart"]
        for i in range(len(musicInfoLb)):
            self.musicLb = ttk.Label(master, text=musicInfoLb[i], font=("", 14))
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
            self.musicEt = ttk.Entry(master, textvariable=self.varMusic, font=("", 14))
            self.musicEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

        if self.mode == "insert":
            self.setInsertWidget(master, len(musicInfoLb))

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text="挿入する位置", font=("", 12))
        self.insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=("", 12), textvariable=self.v_insert, values=["後", "前"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        infoMsg = "この値で修正しますか？"
        if self.mode == "insert":
            infoMsg = "この値で挿入しますか？"
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message=infoMsg, parent=self)
        if result:
            try:
                for i in range(len(self.varList)):
                    if i == 2 or i == 3:
                        try:
                            res = float(self.varList[i].get())
                        except Exception:
                            errorMsg = "数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False
                    else:
                        res = str(self.varList[i].get())
                    self.resultValueList.append(res)
                return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.dirtyFlag = True
