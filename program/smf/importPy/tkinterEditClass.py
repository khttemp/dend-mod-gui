import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb


class SwapDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, selectId):
        self.decryptFile = decryptFile
        self.selectId = selectId
        self.itemList = []
        self.v_itemList = []
        self.entryList = []
        self.swapFrameList = []
        self.reloadFlag = False
        self.infoMsg = "このまま移してもよろしいですか？"

        super(SwapDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.swapLb = ttk.Label(master, text="移動先親フレーム", font=("", 14))
        self.swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

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
        self.swapCb = ttk.Combobox(master, textvariable=self.v_swap, width=20, state="readonly", font=("", 14), value=swapFrameCbList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        self.swapCb.set(swapFrameCbList[0])

    def validate(self):
        swapCbIdx = self.swapCb.current()
        parentIdx = self.swapFrameList[swapCbIdx][0]
        parentName = self.swapFrameList[swapCbIdx][1]
        frameIdx = int(self.selectId[4:])
        frameName = self.decryptFile.frameList[frameIdx][1]
        self.warnMsg = "{0}を{1}の子に移します。\nこの要素の全ての子要素に影響が及びます。\n".format(frameName, parentName) + self.infoMsg

        result = mb.askokcancel(title="確認", message=self.warnMsg, parent=self)
        if result:
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            if not self.decryptFile.saveSwap(frameIdx, parentIdx):
                self.decryptFile.printError()
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="SMFを修正しました")
        self.reloadFlag = True
