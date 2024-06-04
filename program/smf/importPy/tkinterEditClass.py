import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class SwapDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, selectId):
        self.decryptFile = decryptFile
        self.selectId = selectId
        self.itemList = []
        self.v_itemList = []
        self.entryList = []
        self.swapFrameList = []
        self.reloadFlag = False
        self.infoMsg = textSetting.textList["infoList"]["I102"]

        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["smf"]["locationParentFrame"], font=textSetting.textList["font2"])
        swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        frameIdx = int(self.selectId[4:])
        self.swapFrameList = []
        swapFrameCbList = []
        for index, frameInfo in enumerate(self.decryptFile.frameList):
            if index == frameIdx:
                continue
            self.swapFrameList.append([index, frameInfo[1]])
            swapFrameCbList.append("%02d(%s)" % (index, frameInfo[1]))

        self.v_swap = tkinter.StringVar()
        self.v_swap.set(swapFrameCbList[0])
        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=20, state="readonly", font=textSetting.textList["font2"], value=swapFrameCbList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        self.swapCb.set(swapFrameCbList[0])
        super().body(master)

    def validate(self):
        swapCbIdx = self.swapCb.current()
        parentIdx = self.swapFrameList[swapCbIdx][0]
        parentName = self.swapFrameList[swapCbIdx][1]
        frameIdx = int(self.selectId[4:])
        frameName = self.decryptFile.frameList[frameIdx][1]
        self.warnMsg = textSetting.textList["infoList"]["I103"].format(frameName, parentName) + self.infoMsg

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=self.warnMsg, parent=self)
        if result:
            errorMsg = textSetting.textList["errorList"]["E4"]
            if not self.decryptFile.saveSwap(frameIdx, parentIdx):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
        self.reloadFlag = True
