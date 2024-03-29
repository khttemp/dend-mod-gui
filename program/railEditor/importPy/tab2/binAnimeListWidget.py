from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import program.textSetting as textSetting


class BinAnimeListWidget:
    def __init__(self, frame, decryptFile, binAnimeList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.binAnimeList = binAnimeList
        self.reloadFunc = reloadFunc
        self.varList = []

        self.eleLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["editBaseBinAnimeLabel"])
        self.eleLf.pack(anchor=tkinter.NW, padx=10)

        self.txtFrame = ttk.Frame(self.eleLf)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.varBinAnimeCnt = tkinter.IntVar()
        self.varBinAnimeCnt.set(len(self.binAnimeList))
        self.binAnimeCntTextLb = tkinter.Label(self.txtFrame, text=textSetting.textList["railEditor"]["animeCntLabel"], font=textSetting.textList["font6"], width=9, borderwidth=1, relief="solid")
        self.binAnimeCntTextLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.binAnimeCntLb = tkinter.Label(self.txtFrame, textvariable=self.varBinAnimeCnt, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
        self.binAnimeCntLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.binAnimeCntBtn = tkinter.Button(self.txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=lambda: self.editBinAnimeCnt(self.varBinAnimeCnt.get()))
            self.binAnimeCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.txtFrame2 = ttk.Frame(self.eleLf)
        self.txtFrame2.pack(anchor=tkinter.NW, pady=5)

        binAnimeHeaderLb = textSetting.textList["railEditor"]["editBinAnimeHeaderList"]
        for i in range(len(binAnimeHeaderLb)):
            self.headerLb = tkinter.Label(self.txtFrame2, text=binAnimeHeaderLb[i], font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
            self.headerLb.grid(row=0, column=i, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.binAnimeList)):
            binAnimeInfo = self.binAnimeList[i]
            for j in range(len(binAnimeInfo)):
                self.varTemph = tkinter.IntVar()
                self.varTemph.set(int(binAnimeInfo[j]))
                self.temphTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemph, font=textSetting.textList["font6"], width=7, borderwidth=1, relief="solid")
                self.temphTextLb.grid(row=i + 1, column=j, sticky=tkinter.W + tkinter.E)
            self.temphBtn = tkinter.Button(self.txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], font=textSetting.textList["font7"], command=partial(self.editBinAnime, i, binAnimeInfo))
            self.temphBtn.grid(row=i + 1, column=len(binAnimeInfo), sticky=tkinter.W + tkinter.E)

    def editBinAnimeCnt(self, val):
        result = EditBinAnimeCntWidget(self.frame, textSetting.textList["railEditor"]["editAnimeCntLabel"], self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveBinAnimeCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I73"])
            self.reloadFunc()

    def editBinAnime(self, i, binAnimeInfo):
        result = EditBinAnimeWidget(self.frame, textSetting.textList["railEditor"]["editAnimeCntLabel"], self.decryptFile, binAnimeInfo)
        if result.reloadFlag:
            self.binAnimeList[i] = result.resultValueList
            if not self.decryptFile.saveBinAnime(self.binAnimeList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I74"])
            self.reloadFunc()


class EditBinAnimeCntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditBinAnimeCntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        self.valLb.pack()

        self.varBinAnimeCnt = tkinter.IntVar()
        self.varBinAnimeCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varBinAnimeCnt, font=textSetting.textList["font2"], width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varBinAnimeCnt.get())
                    if res < 0:
                        errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                        return False
                    self.resultValue = res
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E60"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return False
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

            if self.resultValue < self.val:
                msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
                result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True


class EditBinAnimeWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, binAnimeInfo):
        self.decryptFile = decryptFile
        self.binAnimeInfo = binAnimeInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditBinAnimeWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        binAnimeInfoLbList = textSetting.textList["railEditor"]["editBinAnimeHeaderList"]
        for i in range(len(self.binAnimeInfo)):
            self.binAnimeInfoLb = ttk.Label(master, text=binAnimeInfoLbList[i], font=textSetting.textList["font2"])
            self.binAnimeInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.varBinAnime = tkinter.IntVar()
            self.varBinAnime.set(self.binAnimeInfo[i])
            self.varList.append(self.varBinAnime)
            self.binAnimeEt = ttk.Entry(master, textvariable=self.varBinAnime, font=textSetting.textList["font2"])
            self.binAnimeEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        res = int(self.varList[i].get())
                        self.resultValueList.append(res)
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
