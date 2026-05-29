import copy

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class ImageListWidget(ttkCustomWidget.CustomTtkLabelFrame):
    def __init__(self, master, groupBoxTitle, imgList, ver, rootFrameAppearance):
        super().__init__(master, text=groupBoxTitle)
        self.master = master
        self.groupBoxTitle = groupBoxTitle
        self.imgList = imgList
        self.ver = ver
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False

        btnFrame = ttkCustomWidget.CustomTtkFrame(self)
        btnFrame.pack(pady=5)
        listFrame = ttkCustomWidget.CustomTtkFrame(self)
        listFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W+tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W+tkinter.E)

        self.selectIndexNum = -1
        displayImageList = self.setListboxInfo(imgList)
        self.v_imgList = tkinter.StringVar(value=displayImageList)
        self.imgListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=23, height=8, listvariable=self.v_imgList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.imgListListbox.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.imgListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.imgListListbox, self.imgListListbox.curselection()))

    def setListboxInfo(self, imgList):
        displayImageList = []
        if len(imgList) > 0:
            for i in range(len(imgList)):
                imgName = imgList[i]["imgName"]
                if self.ver == 4:
                    dipslayImageInfo = "{0:02d}→{1}, {2}".format(i, imgName, imgList[i]["imgElse"])
                else:
                    dipslayImageInfo = "{0:02d}→{1}".format(i, imgName)
                displayImageList.append(dipslayImageInfo)
        else:
            displayImageList = [textSetting.textList["mdlBin"]["noList"]]
        return displayImageList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["mdlBin"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.imgList[self.selectIndexNum]
        result = EditImageListDialog(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], self.ver, "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.imgList[self.selectIndexNum] = result.resultValueInfo
            displayImageList = self.setListboxInfo(self.imgList)
            self.v_imgList.set(displayImageList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditImageListDialog(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], self.ver, "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.imgList.insert(self.selectIndexNum + result.insertPos, result.resultValueInfo)
            displayImageList = self.setListboxInfo(self.imgList)
            self.v_imgList.set(displayImageList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.imgList.pop(self.selectIndexNum)
            displayImageList = self.setListboxInfo(self.imgList)
            self.v_imgList.set(displayImageList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"


class EditImageListDialog(CustomSimpleDialog):
    def __init__(self, master, title, ver, mode, item, rootFrameAppearance):
        self.ver = ver
        self.mode = mode
        self.item = item
        self.resultValueInfo = {}
        self.insertPos = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        imgNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgLabel"], font=textSetting.textList["font2"])
        imgNameLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_imgName = tkinter.StringVar()
        imgNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_imgName)
        imgNameEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

        if self.mode == "modify":
            self.v_imgName.set(self.item["imgName"])

        if self.ver == 4:
            imgElse1Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["else"] + "1", font=textSetting.textList["font2"])
            imgElse1Lb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
            self.v_imgElse1 = tkinter.IntVar()
            self.imgElseCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_imgElse1, values=textSetting.textList["mdlBin"]["headerElse1Value"])
            self.imgElseCb.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)
            self.imgElseCb.current(0)
            self.imgElseCb.bind("<<ComboboxSelected>>", self.imgElseCbChange)

            imgElse2Lb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["else"] + "2", font=textSetting.textList["font2"])
            imgElse2Lb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
            self.v_imgElse2 = tkinter.IntVar()
            self.imgElseEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_imgElse2, state="disabled")
            self.imgElseEt.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)

            if self.mode == "modify":
                self.imgElseCb.current(self.item["imgElse"][0])
                if self.item["imgElse"][0] != 0:
                    self.imgElseEt["state"] = "normal"
                    self.v_imgElse2.set(self.item["imgElse"][1])
                else:
                    self.imgElseEt["state"] = "disabled"

        if self.mode == "insert":
            if self.ver == 4:
                self.setInsertWidget(master, 4)
            else:
                self.setInsertWidget(master, 2)
        super().body(master)

    def imgElseCbChange(self, event):
        imgElse1 = self.imgElseCb.current()
        if imgElse1 == 0:
            self.imgElseEt["state"] = "disabled"
        else:
            self.imgElseEt["state"] = "normal"

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["mdlBin"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueInfo = {}
        if not self.v_imgName.get():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["mdlBin"]["headerImgLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValueInfo["imgName"] = self.v_imgName.get()
        self.resultValueInfo["imgElse"] = []

        if self.ver == 4:
            try:
                self.v_imgElse2.get()
            except Exception:
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            self.resultValueInfo["imgElse"].append(self.v_imgElse1.get())
            if self.imgElseCb.current() != 0:
                self.resultValueInfo["imgElse"].append(int(self.v_imgElse2.get()))

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        return True

    def apply(self):
        self.reloadFlag = True


class ImageSizeListWidget(ttkCustomWidget.CustomTtkLabelFrame):
    def __init__(self, master, groupBoxTitle, imgSizeList, rootFrameAppearance):
        super().__init__(master, text=groupBoxTitle)
        self.master = master
        self.groupBoxTitle = groupBoxTitle
        self.imgSizeList = imgSizeList
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False

        btnFrame = ttkCustomWidget.CustomTtkFrame(self)
        btnFrame.pack(pady=5)
        listFrame = ttkCustomWidget.CustomTtkFrame(self)
        listFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W+tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W+tkinter.E)

        self.selectIndexNum = -1
        displayImageSizeList = self.setListboxInfo(imgSizeList)
        self.v_imgSizeList = tkinter.StringVar(value=displayImageSizeList)
        self.imgSizeListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=23, height=8, listvariable=self.v_imgSizeList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.imgSizeListListbox.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.imgSizeListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.imgSizeListListbox, self.imgSizeListListbox.curselection()))

    def setListboxInfo(self, imgSizeList):
        displayImageSizeList = []
        if len(imgSizeList) > 0:
            for i in range(len(imgSizeList)):
                dipslayImageSizeInfo = "{0:02d}→img{1:02d}, {2}".format(i, imgSizeList[i][0], imgSizeList[i][1])
                displayImageSizeList.append(dipslayImageSizeInfo)
        else:
            displayImageSizeList = [textSetting.textList["mdlBin"]["noList"]]
        return displayImageSizeList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["mdlBin"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.imgSizeList[self.selectIndexNum]
        result = EditImageSizeListDialog(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.imgSizeList[self.selectIndexNum] = result.resultValueList
            displayImageSizeList = self.setListboxInfo(self.imgSizeList)
            self.v_imgSizeList.set(displayImageSizeList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditImageSizeListDialog(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.imgSizeList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
            displayImageSizeList = self.setListboxInfo(self.imgSizeList)
            self.v_imgSizeList.set(displayImageSizeList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.imgSizeList.pop(self.selectIndexNum)
            displayImageSizeList = self.setListboxInfo(self.imgSizeList)
            self.v_imgSizeList.set(displayImageSizeList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"


class EditImageSizeListDialog(CustomSimpleDialog):
    def __init__(self, master, title, mode, item, rootFrameAppearance):
        self.mode = mode
        self.item = item
        self.resultValueList = []
        self.insertPos = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        imgIndexLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgIndex"], font=textSetting.textList["font2"])
        imgIndexLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_xLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgX"], font=textSetting.textList["font2"])
        imgIndex_xLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_yLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgY"], font=textSetting.textList["font2"])
        imgIndex_yLb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_widthLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgWidth"], font=textSetting.textList["font2"])
        imgIndex_widthLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_heightLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerImgHeight"], font=textSetting.textList["font2"])
        imgIndex_heightLb.grid(row=5, column=0, sticky=tkinter.W+tkinter.E)

        self.v_imgIndex = tkinter.IntVar()
        self.v_imgIndex_x = tkinter.DoubleVar()
        self.v_imgIndex_y = tkinter.DoubleVar()
        self.v_imgIndex_width = tkinter.DoubleVar()
        self.v_imgIndex_height = tkinter.DoubleVar()
        imgIndexEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex, font=textSetting.textList["font2"])
        imgIndexEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
        imgIndex_xEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_x, font=textSetting.textList["font2"])
        imgIndex_xEt.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)
        imgIndex_yEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_y, font=textSetting.textList["font2"])
        imgIndex_yEt.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)
        imgIndex_widthEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_width, font=textSetting.textList["font2"])
        imgIndex_widthEt.grid(row=4, column=1, sticky=tkinter.W+tkinter.E)
        imgIndex_heightEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_imgIndex_height, font=textSetting.textList["font2"])
        imgIndex_heightEt.grid(row=5, column=1, sticky=tkinter.W+tkinter.E)

        if self.mode == "modify":
            self.v_imgIndex.set(self.item[0])
            self.v_imgIndex_x.set(self.item[1][0])
            self.v_imgIndex_y.set(self.item[1][1])
            self.v_imgIndex_width.set(self.item[1][2])
            self.v_imgIndex_height.set(self.item[1][3])
        else:
            self.v_imgIndex.set(0)
            self.v_imgIndex_x.set(float(-1))
            self.v_imgIndex_y.set(float(-1))
            self.v_imgIndex_width.set(float(-1))
            self.v_imgIndex_height.set(float(-1))
            self.setInsertWidget(master, 6)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["mdlBin"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueList = []
        sizeInfo = []
        try:
            self.resultValueList.append(int(self.v_imgIndex.get()))
            sizeInfo.append(float(self.v_imgIndex_x.get()))
            sizeInfo.append(float(self.v_imgIndex_y.get()))
            sizeInfo.append(float(self.v_imgIndex_width.get()))
            sizeInfo.append(float(self.v_imgIndex_height.get()))
        except Exception:
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        self.resultValueList.append(sizeInfo)

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        return True

    def apply(self):
        self.reloadFlag = True


class SmfNameListWidget(ttkCustomWidget.CustomTtkLabelFrame):
    def __init__(self, master, groupBoxTitle, smfList, rootFrameAppearance):
        super().__init__(master, text=groupBoxTitle)
        self.master = master
        self.groupBoxTitle = groupBoxTitle
        self.smfList = smfList
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False

        btnFrame = ttkCustomWidget.CustomTtkFrame(self)
        btnFrame.pack(pady=5)
        listFrame = ttkCustomWidget.CustomTtkFrame(self)
        listFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W+tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W+tkinter.E)

        self.selectIndexNum = -1
        displaySmfNameList = self.setListboxInfo(smfList)
        self.v_smfList = tkinter.StringVar(value=displaySmfNameList)
        self.smfNameListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=23, height=8, listvariable=self.v_smfList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.smfNameListListbox.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.smfNameListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.smfNameListListbox, self.smfNameListListbox.curselection()))

    def setListboxInfo(self, smfList):
        displaySmfNameList = []
        if len(smfList) > 0:
            for i in range(len(smfList)):
                dipslaySmfNameInfo = "{0:02d}→{1}".format(i, smfList[i])
                displaySmfNameList.append(dipslaySmfNameInfo)
        else:
            displaySmfNameList = [textSetting.textList["mdlBin"]["noList"]]
        return displaySmfNameList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["mdlBin"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.smfList[self.selectIndexNum]
        result = EditSmfNameListDialog(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.smfList[self.selectIndexNum] = result.resultValue
            displaySmfNameList = self.setListboxInfo(self.smfList)
            self.v_smfList.set(displaySmfNameList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditSmfNameListDialog(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.smfList.insert(self.selectIndexNum + result.insertPos, result.resultValue)
            displaySmfNameList = self.setListboxInfo(self.smfList)
            self.v_smfList.set(displaySmfNameList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.smfList.pop(self.selectIndexNum)
            displaySmfNameList = self.setListboxInfo(self.smfList)
            self.v_smfList.set(displaySmfNameList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"


class EditSmfNameListDialog(CustomSimpleDialog):
    def __init__(self, master, title, mode, item, rootFrameAppearance):
        self.mode = mode
        self.item = item
        self.resultValue = ""
        self.insertPos = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        smfNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerSmfLabel"], font=textSetting.textList["font2"])
        smfNameLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_smfName = tkinter.StringVar()
        smfNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_smfName)
        smfNameEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

        if self.mode == "modify":
            self.v_smfName.set(self.item)
        else:
            self.setInsertWidget(master, 2)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["mdlBin"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValue = ""
        if not self.v_smfName.get():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["mdlBin"]["headerSmfLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False

        self.resultValue = self.v_smfName.get()
        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        return True

    def apply(self):
        self.reloadFlag = True


class WavListWidget(ttkCustomWidget.CustomTtkLabelFrame):
    def __init__(self, master, groupBoxTitle, wavList, rootFrameAppearance):
        super().__init__(master, text=groupBoxTitle)
        self.master = master
        self.groupBoxTitle = groupBoxTitle
        self.wavList = wavList
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False

        btnFrame = ttkCustomWidget.CustomTtkFrame(self)
        btnFrame.pack(pady=5)
        listFrame = ttkCustomWidget.CustomTtkFrame(self)
        listFrame.pack()

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W+tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W+tkinter.E)

        self.selectIndexNum = -1
        displayWavList = self.setListboxInfo(wavList)
        self.v_wavList = tkinter.StringVar(value=displayWavList)
        self.wavListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=23, height=8, listvariable=self.v_wavList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.wavListListbox.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.wavListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.wavListListbox, self.wavListListbox.curselection()))

    def setListboxInfo(self, wavList):
        displayWavList = []
        if len(wavList) > 0:
            for i in range(len(wavList)):
                dipslayWavInfo = "{0:02d}→{1}, {2}".format(i, wavList[i][0], wavList[i][1])
                displayWavList.append(dipslayWavInfo)
        else:
            displayWavList = [textSetting.textList["mdlBin"]["noList"]]
        return displayWavList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["mdlBin"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.wavList[self.selectIndexNum]
        result = EditWavListWidget(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.wavList[self.selectIndexNum] = result.resultValueList
            displayWavList = self.setListboxInfo(self.wavList)
            self.v_wavList.set(displayWavList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditWavListWidget(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.wavList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
            displayWavList = self.setListboxInfo(self.wavList)
            self.v_wavList.set(displayWavList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.wavList.pop(self.selectIndexNum)
            displayWavList = self.setListboxInfo(self.wavList)
            self.v_wavList.set(displayWavList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"


class EditWavListWidget(CustomSimpleDialog):
    def __init__(self, master, title, mode, item, rootFrameAppearance):
        self.mode = mode
        self.item = item
        self.resultValue = ""
        self.insertPos = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        wavNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerSELabel"], font=textSetting.textList["font2"])
        wavNameLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_wavName = tkinter.StringVar()
        wavNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_wavName)
        wavNameEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

        wavCntLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerSEGroup"], font=textSetting.textList["font2"])
        wavCntLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
        self.v_wavCnt = tkinter.IntVar()
        wavCntEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_wavCnt)
        wavCntEt.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)

        if self.mode == "modify":
            self.v_wavName.set(self.item[0])
            self.v_wavCnt.set(self.item[1])
        else:
            self.setInsertWidget(master, 3)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["mdlBin"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueList = []
        if not self.v_wavName.get():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["mdlBin"]["headerSELabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValueList.append(self.v_wavName.get())

        try:
            self.resultValueList.append(int(self.v_wavCnt.get()))
        except Exception:
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        return True

    def apply(self):
        self.reloadFlag = True


class TgaListWidget(ttkCustomWidget.CustomTtkLabelFrame):
    def __init__(self, master, groupBoxTitle, tgaList, rootFrameAppearance):
        super().__init__(master, text=groupBoxTitle)
        self.master = master
        self.groupBoxTitle = groupBoxTitle
        self.tgaList = tgaList
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False

        btnFrame = ttkCustomWidget.CustomTtkFrame(self)
        btnFrame.pack(pady=5)
        listFrame = ttkCustomWidget.CustomTtkFrame(self)
        listFrame.pack(expand=True, fill=tkinter.BOTH)

        self.modifyBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.insertBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W+tkinter.E)
        self.deleteBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W+tkinter.E)

        self.selectIndexNum = -1
        displayTgaList = self.setListboxInfo(tgaList)
        self.v_tgaList = tkinter.StringVar(value=displayTgaList)
        self.tgaListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], height=8, listvariable=self.v_tgaList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.tgaListListbox.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.tgaListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.tgaListListbox, self.tgaListListbox.curselection()))

        listFrame.grid_columnconfigure(0, weight=1)

    def setListboxInfo(self, tgaList):
        displayTgaList = []
        if len(tgaList) > 0:
            for i in range(len(tgaList)):
                dipslayTgaInfo = "{0:02d}→{1}, {2}".format(i, tgaList[i]["tgaInfo"], tgaList[i]["tgaElse"])
                displayTgaList.append(dipslayTgaInfo)
        else:
            displayTgaList = [textSetting.textList["mdlBin"]["noList"]]
        return displayTgaList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["mdlBin"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.tgaList[self.selectIndexNum]
        result = EditTgaListWidget(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.tgaList[self.selectIndexNum] = result.resultValueInfo
            displayTgaList = self.setListboxInfo(self.tgaList)
            self.v_tgaList.set(displayTgaList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditTgaListWidget(self.master, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.tgaList.insert(self.selectIndexNum + result.insertPos, result.resultValueInfo)
            displayTgaList = self.setListboxInfo(self.tgaList)
            self.v_tgaList.set(displayTgaList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.tgaList.pop(self.selectIndexNum)
            displayTgaList = self.setListboxInfo(self.tgaList)
            self.v_tgaList.set(displayTgaList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"


class EditTgaListWidget(CustomSimpleDialog):
    def __init__(self, master, title, mode, item, rootFrameAppearance):
        self.mode = mode
        self.item = item
        self.resultValueInfo = {}
        self.varList = []
        self.varCnt = 0
        self.insertPos = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(2):
            tgaNameLb = ttkCustomWidget.CustomTtkLabel(master, text="{0}{1}".format(textSetting.textList["mdlBin"]["headerTgaLabel"], i + 1), font=textSetting.textList["font2"])
            tgaNameLb.grid(row=1 + i, column=0, sticky=tkinter.W+tkinter.E)
            self.varList.append(tkinter.StringVar())
            tgaNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt])
            tgaNameEt.grid(row=1 + i, column=1, sticky=tkinter.W+tkinter.E)
            self.varCnt += 1

        for i in range(2):
            tgaEleLb = ttkCustomWidget.CustomTtkLabel(master, text="{0}{1}".format(textSetting.textList["mdlBin"]["else"], i + 1), font=textSetting.textList["font2"])
            tgaEleLb.grid(row=3 + i, column=0, sticky=tkinter.W+tkinter.E)
            self.varList.append(tkinter.DoubleVar())
            tgaEleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt])
            tgaEleEt.grid(row=3 + i, column=1, sticky=tkinter.W+tkinter.E)
            self.varCnt += 1

        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=5, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        for i in range(4):
            tgaElseBLb = ttkCustomWidget.CustomTtkLabel(master, text="{0}{1}".format(textSetting.textList["mdlBin"]["headerTgaB"], i + 1), font=textSetting.textList["font2"])
            tgaElseBLb.grid(row=6 + i, column=0, sticky=tkinter.W+tkinter.E)
            self.varList.append(tkinter.IntVar())
            tgaElseBEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt])
            tgaElseBEt.grid(row=6 + i, column=1, sticky=tkinter.W+tkinter.E)
            self.varCnt += 1

        tgaElsePerLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["headerTgaPer"], font=textSetting.textList["font2"])
        tgaElsePerLb.grid(row=10, column=0, sticky=tkinter.W+tkinter.E)
        self.varList.append(tkinter.IntVar())
        tgaElsePerEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt])
        tgaElsePerEt.grid(row=10, column=1, sticky=tkinter.W+tkinter.E)
        self.varCnt += 1

        if self.mode == "modify":
            self.varList[0].set(self.item["tgaInfo"][0])
            self.varList[1].set(self.item["tgaInfo"][1])
            self.varList[2].set(self.item["tgaInfo"][2])
            self.varList[3].set(self.item["tgaInfo"][3])
            self.varList[4].set(self.item["tgaElse"][0])
            self.varList[5].set(self.item["tgaElse"][1])
            self.varList[6].set(self.item["tgaElse"][2])
            self.varList[7].set(self.item["tgaElse"][3])
            self.varList[8].set(self.item["tgaElse"][4])
        else:
            self.setInsertWidget(master, 11)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["mdlBin"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["mdlBin"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueInfo = {}
        self.resultValueInfo["tgaInfo"] = []
        self.resultValueInfo["tgaElse"] = []
        for i, var in enumerate(self.varList):
            if i in [0, 1]:
                elementName = "{0}{1}".format(textSetting.textList["mdlBin"]["headerTgaLabel"], i + 1)
                errorMsg = textSetting.textList["errorList"]["E139"].format(elementName)
                if not var.get():
                    mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
                    return False
                self.resultValueInfo["tgaInfo"].append(var.get())
            else:
                try:
                    if i in [2, 3]:
                        self.resultValueInfo["tgaInfo"].append(float(var.get()))
                    else:
                        self.resultValueInfo["tgaElse"].append(int(var.get()))
                except Exception:
                    mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                    return

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCb.current() == 1:
                self.insertPos = 0
        return True

    def apply(self):
        self.reloadFlag = True


class HeaderDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance):
        self.master = master
        self.decryptFile = decryptFile
        self.rootFrameAppearance = rootFrameAppearance
        self.dirtyFlag = False
        self.reloadFlag = False
        self.imgList = copy.deepcopy(decryptFile.imgList)
        self.imgSizeList = copy.deepcopy(decryptFile.imgSizeList)
        self.smfList = copy.deepcopy(decryptFile.smfList)
        self.wavList = copy.deepcopy(decryptFile.wavList)
        self.tgaList = copy.deepcopy(decryptFile.tgaList)
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        # imageList
        self.imageSimpleList = ImageListWidget(master, textSetting.textList["mdlBin"]["imgInfo"], self.imgList, self.decryptFile.ver, self.rootFrameAppearance)
        self.imageSimpleList.grid(row=0, column=0, padx=(0, 5))
        # imageSizeList
        self.imageSizeSimpleList = ImageSizeListWidget(master, textSetting.textList["mdlBin"]["imgSizeInfo"], self.imgSizeList, self.rootFrameAppearance)
        self.imageSizeSimpleList.grid(row=0, column=1, padx=5)
        # smfList
        self.smfSimpleList = SmfNameListWidget(master, textSetting.textList["mdlBin"]["smfInfo"], self.smfList, self.rootFrameAppearance)
        self.smfSimpleList.grid(row=0, column=2, padx=5)
        # wavList
        self.wavSimpleList = WavListWidget(master, textSetting.textList["mdlBin"]["seInfo"], self.wavList, self.rootFrameAppearance)
        self.wavSimpleList.grid(row=0, column=3, padx=5)
        # ###
        if self.decryptFile.ver != 1:
            # tgaList
            self.tgaSimpleList = TgaListWidget(master, textSetting.textList["mdlBin"]["tgaInfo"], self.tgaList, self.rootFrameAppearance)
            self.tgaSimpleList.grid(columnspan=4, row=1, column=0, sticky=tkinter.W+tkinter.E)
        super().body(master)

    def validate(self):
        self.dirtyFlag = False
        self.dirtyFlag |= self.imageSimpleList.dirtyFlag
        self.dirtyFlag |= self.imageSizeSimpleList.dirtyFlag
        self.dirtyFlag |= self.smfSimpleList.dirtyFlag
        self.dirtyFlag |= self.wavSimpleList.dirtyFlag
        if self.decryptFile.ver != 1:
            self.dirtyFlag |= self.tgaSimpleList.dirtyFlag

        if self.dirtyFlag:
            result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I7"], icon="warning", parent=self)
            if result:
                newImgList = self.imageSimpleList.imgList
                newImgSizeList = self.imageSizeSimpleList.imgSizeList
                newSmfList = self.smfSimpleList.smfList
                newWavList = self.wavSimpleList.wavList
                if self.decryptFile.ver != 1:
                    newTgaList = self.tgaSimpleList.tgaList
                else:
                    newTgaList = self.tgaList

                if not self.decryptFile.saveHeader(newImgList, newImgSizeList, newSmfList, newWavList, newTgaList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return False
                return True
        return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I8"])
            self.reloadFlag = True
