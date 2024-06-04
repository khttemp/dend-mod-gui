from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class BinAnimeListWidget:
    def __init__(self, root, frame, decryptFile, binAnimeList, rootFrameAppearance, reloadFunc):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.binAnimeList = binAnimeList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        eleLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["editBaseBinAnimeLabel"])
        eleLf.pack(anchor=tkinter.NW, padx=10, pady=5)

        txtFrame = ttkCustomWidget.CustomTtkFrame(eleLf)
        txtFrame.pack(anchor=tkinter.NW)

        self.varBinAnimeCnt = tkinter.IntVar()
        self.varBinAnimeCnt.set(len(self.binAnimeList))
        binAnimeCntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["railEditor"]["animeCntLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=9, borderwidth=1, relief="solid")
        binAnimeCntTextLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        binAnimeCntLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varBinAnimeCnt, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        binAnimeCntLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            binAnimeCntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editBinAnimeCnt(self.varBinAnimeCnt.get()))
            binAnimeCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        txtFrame2 = ttkCustomWidget.CustomTtkFrame(eleLf)
        txtFrame2.pack(anchor=tkinter.NW, pady=5)

        binAnimeHeaderLb = textSetting.textList["railEditor"]["editBinAnimeHeaderList"]
        for i in range(len(binAnimeHeaderLb)):
            headerLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=binAnimeHeaderLb[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            headerLb.grid(row=0, column=i, sticky=tkinter.W + tkinter.E)

        self.varList = []
        self.varCnt = 0
        for i in range(len(self.binAnimeList)):
            binAnimeInfo = self.binAnimeList[i]
            for j in range(len(binAnimeInfo)):
                self.varList.append(tkinter.IntVar(value=int(binAnimeInfo[j])))
                temphTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, textvariable=self.varList[self.varCnt], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
                temphTextLb.grid(row=i + 1, column=j, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
            temphBtn = ttkCustomWidget.CustomTtkButton(txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editBinAnime, i, binAnimeInfo))
            temphBtn.grid(row=i + 1, column=len(binAnimeInfo), sticky=tkinter.W + tkinter.E)

    def editBinAnimeCnt(self, val):
        result = EditBinAnimeCntWidget(self.root, textSetting.textList["railEditor"]["editAnimeCntLabel"], self.decryptFile, val, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveBinAnimeCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I73"])
            self.reloadFunc()

    def editBinAnime(self, i, binAnimeInfo):
        result = EditBinAnimeWidget(self.root, textSetting.textList["railEditor"]["editAnimeCntLabel"], self.decryptFile, binAnimeInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.binAnimeList[i] = result.resultValueList
            if not self.decryptFile.saveBinAnime(self.binAnimeList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I74"])
            self.reloadFunc()


class EditBinAnimeCntWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, val, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()

        self.varBinAnimeCnt = tkinter.IntVar()
        self.varBinAnimeCnt.set(self.val)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varBinAnimeCnt, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

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


class EditBinAnimeWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, binAnimeInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.binAnimeInfo = binAnimeInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        binAnimeInfoLbList = textSetting.textList["railEditor"]["editBinAnimeHeaderList"]
        for i in range(len(self.binAnimeInfo)):
            binAnimeInfoLb = ttkCustomWidget.CustomTtkLabel(master, text=binAnimeInfoLbList[i], font=textSetting.textList["font2"])
            binAnimeInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            self.varList.append(tkinter.IntVar(value=self.binAnimeInfo[i]))
            binAnimeEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            binAnimeEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

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
