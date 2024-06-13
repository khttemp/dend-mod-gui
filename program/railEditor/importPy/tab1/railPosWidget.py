from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class RailPosWidget:
    def __init__(self, root, frame, title, num, decryptFile, trainList, rootFrameAppearance, reloadFunc):
        self.root = root
        self.frame = frame
        self.title = title
        self.railBtnList = []
        self.num = num
        self.decryptFile = decryptFile
        self.trainList = trainList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        railPosLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=title)
        railPosLf.pack(anchor=tkinter.NW, padx=10, pady=5)

        playHeaderLb = ttkCustomWidget.CustomTtkLabel(railPosLf, text=textSetting.textList["railEditor"]["railPosPlayerLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        playHeaderLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        railNoHeaderLb = ttkCustomWidget.CustomTtkLabel(railPosLf, text=textSetting.textList["railEditor"]["railPosRailNoLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        railNoHeaderLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        railPosHeaderLb = ttkCustomWidget.CustomTtkLabel(railPosLf, text=textSetting.textList["railEditor"]["railPosRailPosLabel"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=7, borderwidth=1, relief="solid")
        railPosHeaderLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
        b1HeaderLb = ttkCustomWidget.CustomTtkLabel(railPosLf, text=textSetting.textList["railEditor"]["railPosB1Label"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
        b1HeaderLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)
        if not (self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag):
            f1HeaderLb = ttkCustomWidget.CustomTtkLabel(railPosLf, text=textSetting.textList["railEditor"]["railPosF1Label"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
            f1HeaderLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.trainList)):
            trainInfo = self.trainList[i]
            playLb = ttkCustomWidget.CustomTtkLabel(railPosLf, text=textSetting.textList["railEditor"]["railPosPlayerNameLabel"].format(i + 1), font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            playLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            for j in range(len(trainInfo)):
                valLb = ttkCustomWidget.CustomTtkLabel(railPosLf, text=trainInfo[j], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                valLb.grid(row=i + 1, column=j + 1, sticky=tkinter.W + tkinter.E)

            if self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag and i == 2:
                continue
            railBtn = ttkCustomWidget.CustomTtkButton(railPosLf, text=textSetting.textList["railEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVar, i, trainInfo))
            railBtn.grid(row=i + 1, column=len(trainInfo) + 1, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, trainInfo):
        result = EditRailPosWidget(self.root, self.title + textSetting.textList["railEditor"]["commonModifyLabel"], self.decryptFile, trainInfo, self.rootFrameAppearance)

        if result.reloadFlag:
            self.trainList[i] = result.resultValueList
            if not self.decryptFile.saveRailPos(self.num, self.trainList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=self.title + textSetting.textList["infoList"]["I61"])

            self.reloadFunc()


class EditRailPosWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, trainInfo, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.trainInfo = trainInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        trainInfoLbList = textSetting.textList["railEditor"]["editRailPosLabelList"]
        for i in range(len(self.trainInfo)):
            railLb = ttkCustomWidget.CustomTtkLabel(master, text=trainInfoLbList[i], font=textSetting.textList["font2"])
            railLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            if i == 3:
                varRail = tkinter.DoubleVar()
                varRail.set(self.trainInfo[i])
            else:
                varRail = tkinter.IntVar()
                varRail.set(self.trainInfo[i])
            self.varList.append(varRail)
            railEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[i], font=textSetting.textList["font2"])
            railEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
        super().body(master)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i == 3:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())
                            if res < 0:
                                errorMsg = textSetting.textList["errorList"]["E61"].format(0)
                                mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                                return False
                        self.resultValueList.append(res)
                    return True
                except Exception:
                    errorMsg = textSetting.textList["errorList"]["E3"]
                    mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
                    return False
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
