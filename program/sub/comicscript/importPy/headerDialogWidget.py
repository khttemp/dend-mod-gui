import copy

import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class ImageListWidget(ttkCustomWidget.CustomTtkLabelFrame):
    def __init__(self, master, groupBoxTitle, imgList, rootFrameAppearance):
        super().__init__(master, text=groupBoxTitle)
        self.master = master
        self.groupBoxTitle = groupBoxTitle
        self.imgList = imgList
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
            for i, imgName in enumerate(imgList):
                dipslayImageInfo = "{0:02d}→{1}".format(i, imgName)
                displayImageList.append(dipslayImageInfo)
        else:
            displayImageList = [textSetting.textList["comicscript"]["noList"]]
        return displayImageList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["comicscript"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.imgList[self.selectIndexNum]
        result = EditImageListDialog(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.imgList[self.selectIndexNum] = result.resultValue
            displayImageList = self.setListboxInfo(self.imgList)
            self.v_imgList.set(displayImageList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditImageListDialog(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.imgList.insert(self.selectIndexNum + result.insertPos, result.resultValue)
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

        imgNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerImgLabel"], font=textSetting.textList["font2"])
        imgNameLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_imgName = tkinter.StringVar()
        imgNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_imgName)
        imgNameEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

        if self.mode == "modify":
            self.v_imgName.set(self.item)

        if self.mode == "insert":
            self.setInsertWidget(master, 2)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["comicscript"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValue = ""
        if not self.v_imgName.get():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["comicscript"]["headerImgLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValue = self.v_imgName.get()

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
            displayImageSizeList = [textSetting.textList["comicscript"]["noList"]]
        return displayImageSizeList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["comicscript"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.imgSizeList[self.selectIndexNum]
        result = EditImageSizeListDialog(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.imgSizeList[self.selectIndexNum] = result.resultValueList
            displayImageSizeList = self.setListboxInfo(self.imgSizeList)
            self.v_imgSizeList.set(displayImageSizeList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditImageSizeListDialog(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
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

        imgIndexLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerImgIndex"], font=textSetting.textList["font2"])
        imgIndexLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_xLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerImgX"], font=textSetting.textList["font2"])
        imgIndex_xLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_yLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerImgY"], font=textSetting.textList["font2"])
        imgIndex_yLb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_widthLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerImgWidth"], font=textSetting.textList["font2"])
        imgIndex_widthLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)
        imgIndex_heightLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerImgHeight"], font=textSetting.textList["font2"])
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

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["comicscript"]["posValue"])
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
            displayWavList = [textSetting.textList["comicscript"]["noList"]]
        return displayWavList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["comicscript"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.wavList[self.selectIndexNum]
        result = EditWavListWidget(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.wavList[self.selectIndexNum] = result.resultValueList
            displayWavList = self.setListboxInfo(self.wavList)
            self.v_wavList.set(displayWavList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditWavListWidget(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
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
        self.resultValueList = []
        self.insertPos = 0
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
        valLb.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        wavNameLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerSELabel"], font=textSetting.textList["font2"])
        wavNameLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_wavName = tkinter.StringVar()
        wavNameEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.v_wavName)
        wavNameEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

        wavCntLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerSEGroup"], font=textSetting.textList["font2"])
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

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["comicscript"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueList = []
        if not self.v_wavName.get():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["comicscript"]["headerSELabel"])
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


class BgmListWidget(ttkCustomWidget.CustomTtkLabelFrame):
    def __init__(self, master, groupBoxTitle, bgmList, rootFrameAppearance):
        super().__init__(master, text=groupBoxTitle)
        self.master = master
        self.groupBoxTitle = groupBoxTitle
        self.bgmList = bgmList
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
        displayBgmList = self.setListboxInfo(bgmList)
        self.v_bgmList = tkinter.StringVar(value=displayBgmList)
        self.bgmListListbox = tkinter.Listbox(listFrame, selectmode="single", font=textSetting.textList["font2"], width=23, height=8, listvariable=self.v_bgmList, bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.bgmListListbox.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.bgmListListbox.bind("<<ListboxSelect>>", lambda e: self.buttonActive(self.bgmListListbox, self.bgmListListbox.curselection()))

    def setListboxInfo(self, bgmList):
        displayBgmList = []
        if len(bgmList) > 0:
            for i in range(len(bgmList)):
                dipslayBgmInfo = "{0:02d}→{1} [{2}], [{3}, {4}]".format(i, bgmList[i][0], bgmList[i][1], bgmList[i][2], bgmList[i][3])
                displayBgmList.append(dipslayBgmInfo)
        else:
            displayBgmList = [textSetting.textList["comicscript"]["noList"]]
        return displayBgmList

    def buttonActive(self, listbox, value):
        if len(value) == 0:
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
            return
        self.selectIndexNum = value[0]

        if listbox.get(value[0]) == textSetting.textList["comicscript"]["noList"]:
            self.modifyBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"
        else:
            self.modifyBtn["state"] = "normal"
            self.deleteBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"

    def modify(self):
        item = self.bgmList[self.selectIndexNum]
        result = EditBgmListWidget(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item, self.rootFrameAppearance)
        if result.reloadFlag:
            self.bgmList[self.selectIndexNum] = result.resultValueList
            displayBgmList = self.setListboxInfo(self.bgmList)
            self.v_bgmList.set(displayBgmList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def insert(self):
        result = EditBgmListWidget(self.master, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert", None, self.rootFrameAppearance)
        if result.reloadFlag:
            self.bgmList.insert(self.selectIndexNum + result.insertPos, result.resultValueList)
            displayBgmList = self.setListboxInfo(self.bgmList)
            self.v_bgmList.set(displayBgmList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"

    def delete(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndexNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            self.bgmList.pop(self.selectIndexNum)
            displayBgmList = self.setListboxInfo(self.bgmList)
            self.v_bgmList.set(displayBgmList)
            self.dirtyFlag = True
            self.modifyBtn["state"] = "disabled"
            self.insertBtn["state"] = "disabled"
            self.deleteBtn["state"] = "disabled"


class EditBgmListWidget(CustomSimpleDialog):
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

        bgmLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerBGMLabel"], font=textSetting.textList["font2"])
        bgmLb.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        bgmLoopFlagLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerBGMLoopFlag"], font=textSetting.textList["font2"])
        bgmLoopFlagLb.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
        bgmStartLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerBGMStart"], font=textSetting.textList["font2"])
        bgmStartLb.grid(row=3, column=0, sticky=tkinter.W+tkinter.E)
        bgmLoopStartLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["headerBGMLoopStart"], font=textSetting.textList["font2"])
        bgmLoopStartLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)

        self.v_bgm = tkinter.StringVar()
        self.v_bgmLoopFlag = tkinter.IntVar()
        self.v_bgmStart = tkinter.DoubleVar()
        self.v_bgmLoopStart = tkinter.DoubleVar()
        bgmEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_bgm, font=textSetting.textList["font2"])
        bgmEt.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)
        self.bgmLoopFlagCb = ttkCustomWidget.CustomTtkCombobox(master, width=24, font=textSetting.textList["font2"], state="readonly", value=textSetting.textList["comicscript"]["headerBGMLoopLabelInfo"])
        self.bgmLoopFlagCb.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)
        self.bgmLoopFlagCb.current(self.v_bgmLoopFlag.get())
        bgmStartEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_bgmStart, font=textSetting.textList["font2"])
        bgmStartEt.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)
        bgmLoopStartEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_bgmLoopStart, font=textSetting.textList["font2"])
        bgmLoopStartEt.grid(row=4, column=1, sticky=tkinter.W+tkinter.E)

        if self.mode == "modify":
            self.v_bgm.set(self.item[0])
            self.bgmLoopFlagCb.current(self.item[1])
            self.v_bgmStart.set(self.item[2])
            self.v_bgmLoopStart.set(self.item[3])
        else:
            self.setInsertWidget(master, 5)
        super().body(master)

    def setInsertWidget(self, master, index):
        xLine = ttkCustomWidget.CustomTtkSeparator(master, orient=tkinter.HORIZONTAL)
        xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, pady=10)

        insertLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["comicscript"]["posLabel"], font=textSetting.textList["font2"])
        insertLb.grid(row=index + 1, column=0, sticky=tkinter.W+tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttkCustomWidget.CustomTtkCombobox(master, state="readonly", font=textSetting.textList["font2"], textvariable=self.v_insert, values=textSetting.textList["comicscript"]["posValue"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W+tkinter.E)
        self.insertCb.current(0)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.resultValueList = []
        if not self.v_bgm.get():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["comicscript"]["headerBGMLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValueList.append(self.v_bgm.get())
        self.resultValueList.append(self.bgmLoopFlagCb.current())

        try:
            float(self.v_bgmStart.get())
            float(self.v_bgmLoopStart.get())
        except Exception:
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return

        self.resultValueList.append(self.v_bgmStart.get())
        self.resultValueList.append(self.v_bgmLoopStart.get())

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
        self.seList = copy.deepcopy(decryptFile.seList)
        self.bgmList = copy.deepcopy(decryptFile.bgmList)
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        # imageList
        self.imageSimpleList = ImageListWidget(master, textSetting.textList["comicscript"]["imgInfo"], self.imgList, self.rootFrameAppearance)
        self.imageSimpleList.grid(row=0, column=0, padx=(0, 5))
        # imageSizeList
        self.imageSizeSimpleList = ImageSizeListWidget(master, textSetting.textList["comicscript"]["imgSizeInfo"], self.imgSizeList, self.rootFrameAppearance)
        self.imageSizeSimpleList.grid(row=0, column=1, padx=5)
        # listLayout - wavList
        self.wavSimpleList = WavListWidget(master, textSetting.textList["comicscript"]["seInfo"], self.seList, self.rootFrameAppearance)
        self.wavSimpleList.grid(row=0, column=2, padx=5)
        # listLayout - bgmList
        self.bgmSimpleList = BgmListWidget(master, textSetting.textList["comicscript"]["bgmInfo"], self.bgmList, self.rootFrameAppearance)
        self.bgmSimpleList.grid(row=0, column=3, padx=5)
        super().body(master)

    def validate(self):
        self.dirtyFlag = False
        self.dirtyFlag |= self.imageSimpleList.dirtyFlag
        self.dirtyFlag |= self.imageSizeSimpleList.dirtyFlag
        self.dirtyFlag |= self.wavSimpleList.dirtyFlag
        self.dirtyFlag |= self.bgmSimpleList.dirtyFlag

        if self.dirtyFlag:
            result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I7"], icon="warning")
            if result:
                newImgList = self.imageSimpleList.imgList
                newImgSizeList = self.imageSizeSimpleList.imgSizeList
                newWavList = self.wavSimpleList.wavList
                newBgmList = self.bgmSimpleList.bgmList
                if not self.decryptFile.saveHeader(newImgList, newImgSizeList, newWavList, newBgmList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return
                return True
        return True

    def apply(self):
        if self.dirtyFlag:
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I8"])
            self.reloadFlag = True
