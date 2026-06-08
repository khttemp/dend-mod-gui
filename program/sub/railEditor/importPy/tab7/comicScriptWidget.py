import copy

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class ComicScriptWidget:
    def __init__(self, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.comicScriptList = decryptFile.comicScriptList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.selectIndexNum = -1

        if self.decryptFile.game == "LSTrial":
            if not (self.decryptFile.readFlag or self.decryptFile.filenameNum == 7):
                return

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
        comicScriptListListbox = tkinter.Listbox(listFrame, selectmode="single", height=20, font=textSetting.textList["font2"], width=listWidth, listvariable=self.v_comicScriptList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        comicScriptListListbox.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        comicScriptListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(comicScriptListListbox, comicScriptListListbox.curselection()))

    def setListboxInfo(self, comicScriptList):
        displayComicScriptList = []
        if len(comicScriptList) > 0:
            for i in range(len(comicScriptList)):
                comicScriptInfo = comicScriptList[i]
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    displayComicScriptList.append("{0:02d}→{1}, [{2}, {3}]".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2]))
                elif self.decryptFile.game == "LS":
                    comicScriptTempList = [round(x, 3) for x in comicScriptInfo[3]]
                    displayComicScriptList.append("{0:02d}→{1}, [{2}, {3}], {4}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2], comicScriptTempList))
                elif self.decryptFile.game == "LSTrial":
                    if self.decryptFile.readFlag:
                        comicScriptTempList = [round(x, 3) for x in comicScriptInfo[3]]
                        displayComicScriptList.append("{0:02d}→{1}, [{2}, {3}], {4}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2], comicScriptTempList))
                    else:
                        comicScriptTempList = [round(x, 3) for x in comicScriptInfo[2]]
                        displayComicScriptList.append("{0:02d}→{1}, [{2}], {3}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptTempList))
        else:
            displayComicScriptList = [textSetting.textList["railEditor"]["noList"]]
        return displayComicScriptList

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

    def modify(self):
        item = self.comicScriptList[self.selectIndexNum]
        result = EditComicScriptListWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["modifyComicScriptLabel"], self.decryptFile, "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.comicScriptList[self.selectIndexNum] = result.resultValueList
            if not self.decryptFile.saveComicScriptList(self.comicScriptList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I85"])
            self.reloadFunc()

    def insert(self):
        result = EditComicScriptListWidget(self.frame.winfo_toplevel(), textSetting.textList["railEditor"]["insertComicScriptLabel"], self.decryptFile, "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.comicScriptList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
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
    def __init__(self, master, title, decryptFile, mode, item, rootFrameAppearance):
        self.decryptFile = decryptFile
        self.mode = mode
        self.item = item
        self.rootFrameAppearance = rootFrameAppearance
        self.varList = []
        self.varCnt = 0
        self.resultValueList = []
        self.insertPos = None
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
            tempNameLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E)
            varTemp = tkinter.IntVar()
            self.varList.append(varTemp)
            txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
            txtEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            if self.mode == "modify":
                varTemp.set(self.item[i])
            self.varCnt += 1

        if self.decryptFile.game in ["LS", "LSTrial"]:
            xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
            xLine.grid(row=len(self.comicScriptLb) + 1, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

            for i in range(9):
                tempNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["railEditor"]["editLsComicScriptFLabel"].format(i + 1), font=textSetting.textList["font2"], width=15)
                tempNameLb.grid(row=len(self.comicScriptLb) + i + 2, column=0, sticky=tkinter.W + tkinter.E)
                varTemp = tkinter.DoubleVar()
                self.varList.append(varTemp)
                txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
                txtEt.grid(row=len(self.comicScriptLb) + i + 2, column=1, sticky=tkinter.W + tkinter.E)
                if self.mode == "modify":
                    if self.decryptFile.game == "LSTrial" and self.decryptFile.filenameNum == 7:
                        varTemp.set(round(float(self.item[2][i]), 3))
                    else:
                        varTemp.set(round(float(self.item[3][i]), 3))
                self.varCnt += 1

        if self.mode == "insert":
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                self.setInsertWidget(master, len(self.comicScriptLb) + 1)
            else:
                self.setInsertWidget(master, len(self.comicScriptLb) + 11)
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
                    self.insertPos = 1
                    if self.insertCb.current() == 1:
                        self.insertPos = 0
                return True
            except Exception:
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
