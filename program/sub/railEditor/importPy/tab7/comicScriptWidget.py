import copy

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class ComicScriptWidget:
    def __init__(self, root, frame, decryptFile, comicScriptList, rootFrameAppearance, reloadFunc):
        self.root = root
        self.frame = frame
        self.decryptFile = decryptFile
        self.comicScriptList = comicScriptList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.selectIndexNum = -1

        comicScriptLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["comicScriptLabel"])
        comicScriptLf.pack(anchor=tkinter.NW, padx=10, side=tkinter.LEFT, fill=tkinter.Y)

        btnFrame = ttkCustomWidget.CustomTtkFrame(comicScriptLf)
        btnFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, style="custom.listbox.TButton", text=textSetting.textList["modify"], state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, style="custom.listbox.TButton", text=textSetting.textList["insert"], state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, style="custom.listbox.TButton", text=textSetting.textList["delete"], state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

        listFrame = ttkCustomWidget.CustomTtkFrame(comicScriptLf)
        listFrame.pack()

        copyComicScriptList = self.setListboxInfo(self.comicScriptList)
        self.v_comicScriptList = tkinter.StringVar(value=copyComicScriptList)
        listWidth = 25
        if self.decryptFile.game in ["LS", "LSTrial"]:
            listWidth = 80
        comicScriptListListbox = tkinter.Listbox(listFrame, selectmode="single", height=22, font=textSetting.textList["font2"], width=listWidth, listvariable=self.v_comicScriptList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        comicScriptListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        comicScriptListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(comicScriptListListbox, comicScriptListListbox.curselection()))

    def buttonActive(self, listbox, value):
        if self.decryptFile.game == "LSTrial":
            if not (self.decryptFile.readFlag or self.decryptFile.filenameNum == 7):
                self.modifyBtn["state"] = "disabled"
                self.insertBtn["state"] = "disabled"
                self.deleteBtn["state"] = "disabled"
                return

        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["railEditor"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def setListboxInfo(self, listboxInfo):
        self.comicScriptList = listboxInfo
        copyComicScriptList = copy.deepcopy(self.comicScriptList)
        if len(copyComicScriptList) > 0:
            for i in range(len(copyComicScriptList)):
                comicScriptInfo = copyComicScriptList[i]
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    copyComicScriptList[i] = "{0:02d}→{1}, [{2}, {3}]".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2])
                elif self.decryptFile.game == "LS":
                    copyComicScriptList[i] = "{0:02d}→{1}, [{2}, {3}], {4}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2], comicScriptInfo[3])
                elif self.decryptFile.game == "LSTrial":
                    if self.decryptFile.readFlag:
                        copyComicScriptList[i] = "{0:02d}→{1}, [{2}, {3}], {4}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2], comicScriptInfo[3])
                    else:
                        copyComicScriptList[i] = "{0:02d}→{1}, [{2}], {3}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2])
        else:
            copyComicScriptList = [textSetting.textList["railEditor"]["noList"]]

        return copyComicScriptList

    def modify(self):
        result = EditComicScriptListWidget(self.root, textSetting.textList["railEditor"]["modifyComicScriptLabel"], self.decryptFile, "modify", self.selectIndexNum, self.comicScriptList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.comicScriptList[self.selectIndexNum] = result.resultValueList
            if not self.decryptFile.saveComicScriptList(self.comicScriptList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I85"])
            self.reloadFunc()

    def insert(self):
        result = EditComicScriptListWidget(self.root, textSetting.textList["railEditor"]["insertComicScriptLabel"], self.decryptFile, "insert", self.selectIndexNum, self.comicScriptList, self.rootFrameAppearance)
        if result.reloadFlag:
            if result.insert == 0:
                self.selectIndexNum += 1
            self.comicScriptList.insert(self.selectIndexNum, result.resultValueList)
            if not self.decryptFile.saveComicScriptList(self.comicScriptList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I85"])
            self.reloadFunc()

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.comicScriptList.pop(self.selectIndexNum)
            if not self.decryptFile.saveComicScriptList(self.comicScriptList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I85"])
            self.reloadFunc()


class EditComicScriptListWidget(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, mode, index, comicScriptList, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.index = index
        self.comicScriptList = comicScriptList
        self.varList = []
        self.varCnt = 0
        self.resultValueList = []
        self.insert = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.comicScriptLb = copy.deepcopy(textSetting.textList["railEditor"]["editComicScriptLabelList"])
        if self.decryptFile.game == "LSTrial" and self.decryptFile.filenameNum == 7:
            self.comicScriptLb.pop()

        for i in range(len(self.comicScriptLb)):
            tempNameLb = ttkCustomWidget.CustomTtkLabel(master, text=self.comicScriptLb[i], font=textSetting.textList["font2"], width=15)
            tempNameLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            varTemp = tkinter.IntVar()
            self.varList.append(varTemp)
            txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
            txtEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
            if self.mode == "modify":
                comicScriptInfo = self.comicScriptList[self.index]
                varTemp.set(comicScriptInfo[i])
            self.varCnt += 1

        if self.decryptFile.game in ["LS", "LSTrial"]:
            xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
            xLine.grid(row=len(self.comicScriptLb), column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

            for i in range(9):
                tempNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["editLsComicScriptFLabel"].format(i + 1), font=textSetting.textList["font2"], width=15)
                tempNameLb.grid(row=len(self.comicScriptLb) + i + 1, column=0, sticky=tkinter.W + tkinter.E)
                varTemp = tkinter.IntVar()
                self.varList.append(varTemp)
                txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                txtEt.grid(row=len(self.comicScriptLb) + i + 1, column=1, sticky=tkinter.W + tkinter.E)
                if self.mode == "modify":
                    comicScriptInfo = self.comicScriptList[self.index]
                    if self.decryptFile.filenameNum == 7:
                        varTemp.set(comicScriptInfo[2][i])
                    else:
                        varTemp.set(comicScriptInfo[3][i])
                self.varCnt += 1

        if self.mode == "insert":
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                self.setInsertWidget(master, len(self.comicScriptLb))
            else:
                self.setInsertWidget(master, len(self.comicScriptLb) + 10)
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
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

        if result:
            try:
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    for i in range(len(self.varList)):
                        try:
                            res = int(self.varList[i].get())
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E60"]
                            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                elif self.decryptFile.game == "LS":
                    tempList = []
                    for i in range(len(self.varList)):
                        try:
                            if i in [0, 1, 2]:
                                res = int(self.varList[i].get())
                                self.resultValueList.append(res)
                            else:
                                tempList.append(float(self.varList[i].get()))
                        except Exception:
                            errorMsg = textSetting.textList["errorList"]["E3"]
                            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                            return False
                    self.resultValueList.append(tempList)
                elif self.decryptFile.game == "LSTrial":
                    if self.decryptFile.readFlag:
                        tempList = []
                        for i in range(len(self.varList)):
                            try:
                                if i in [0, 1, 2]:
                                    res = int(self.varList[i].get())
                                    self.resultValueList.append(res)
                                else:
                                    tempList.append(float(self.varList[i].get()))
                            except Exception:
                                errorMsg = textSetting.textList["errorList"]["E3"]
                                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                                return False
                    else:
                        tempList = []
                        for i in range(len(self.varList)):
                            try:
                                if i in [0, 1]:
                                    res = int(self.varList[i].get())
                                    self.resultValueList.append(res)
                                else:
                                    tempList.append(float(self.varList[i].get()))
                            except Exception:
                                errorMsg = textSetting.textList["errorList"]["E3"]
                                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                                return False
                    self.resultValueList.append(tempList)

                if self.mode == "insert":
                    self.insert = self.insertCb.current()
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
