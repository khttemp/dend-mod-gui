from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class StationWidget:
    def __init__(self, root, frame, decryptFile, stationList, rootFrameAppearance, reloadFunc):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.stationList = stationList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        stationLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["stationInfoLabel"])
        stationLf.pack(anchor=tkinter.NW, padx=10, pady=5)

        txtFrame = ttkCustomWidget.CustomTtkFrame(stationLf)
        txtFrame.pack(anchor=tkinter.NW)

        stationCntLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["railEditor"]["stationInfoCntLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=12, borderwidth=1, relief="solid")
        stationCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varStationCnt = tkinter.IntVar()
        self.varStationCnt.set(len(self.decryptFile.stationList))
        stationCntTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varStationCnt, font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        stationCntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        stationCntBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=lambda: self.editStationCnt(self.varStationCnt.get()))
        stationCntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        txtFrame2 = ttkCustomWidget.CustomTtkFrame(stationLf)
        txtFrame2.pack(anchor=tkinter.NW)

        if len(self.decryptFile.stationList) > 0:
            constLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["stationConst0Label"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            constLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
            ambLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["stationAmbNoLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=9, borderwidth=1, relief="solid")
            ambLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
            ambChildLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["stationAmbChildNoLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=10, borderwidth=1, relief="solid")
            ambChildLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
            eleLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["stationElementLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
            eleLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)
            pngNumLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, text=textSetting.textList["railEditor"]["stationImgNoLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=9, borderwidth=1, relief="solid")
            pngNumLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)

        self.stationVarList = []
        self.stationVarCnt = 0
        for i in range(len(self.decryptFile.stationList)):
            stationInfo = self.decryptFile.stationList[i]
            for j in range(len(stationInfo)):
                self.stationVarList.append(tkinter.IntVar(value=stationInfo[j]))
                varStationLb = ttkCustomWidget.CustomTtkLabel(txtFrame2, textvariable=self.stationVarList[self.stationVarCnt], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                varStationLb.grid(row=i + 1, column=j, sticky=tkinter.W + tkinter.E)
                self.stationVarCnt += 1
            varBtn = ttkCustomWidget.CustomTtkButton(txtFrame2, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editStation, i, stationInfo))
            varBtn.grid(row=i + 1, column=len(stationInfo), sticky=tkinter.W + tkinter.E)

    def editStationCnt(self, val):
        result = EditStationCntWidget(self.root, textSetting.textList["railEditor"]["editStationCntLabel"], self.decryptFile, val, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveStationCnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I77"])
            self.reloadFunc()

    def editStation(self, i, stationInfo):
        result = EditStationWidget(self.root, textSetting.textList["railEditor"]["editStationInfoLabel"], self.decryptFile, stationInfo, self.rootFrameAppearance)
        if result.reloadFlag:
            self.stationList[i] = result.resultValueList
            if not self.decryptFile.saveStation(self.stationList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I78"])
            self.reloadFunc()


class EditStationCntWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, val, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.val = val
        self.rootFrameAppearance = rootFrameAppearance
        self.resultValue = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.pack()

        self.varStationCnt = tkinter.IntVar()
        self.varStationCnt.set(self.val)
        valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varStationCnt, font=textSetting.textList["font2"], width=16)
        valEt.pack()
        super().body(master)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                try:
                    res = int(self.varStationCnt.get())
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


class EditStationWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, stationInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.stationInfo = stationInfo
        self.rootFrameAppearance = rootFrameAppearance
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        stationInfoLbList = textSetting.textList["railEditor"]["editStationInfoLabelList"]
        for i in range(len(self.stationInfo)):
            stationLb = ttkCustomWidget.CustomTtkLabel(master, text=stationInfoLbList[i], font=textSetting.textList["font2"])
            stationLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            varStation = tkinter.IntVar()
            varStation.set(self.stationInfo[i])
            self.varList.append(varStation)
            stationEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            stationEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
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
