import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class InputDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, num, bgmItem=None):
        self.decryptFile = decryptFile
        self.num = num
        self.bgmItem = bgmItem
        self.itemList = []
        self.v_itemList = []
        self.entryList = []
        self.reloadFlag = False
        if self.bgmItem is not None:
            self.mode = "edit"
            self.infoMsg = textSetting.textList["infoList"]["I1"]
        else:
            self.mode = "swap"
            self.infoMsg = ""
            self.swapInfoMsg = textSetting.textList["infoList"]["I39"]

        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        maxLen = 0

        if self.bgmItem is not None:
            for i in range(2, len(self.decryptFile.headerList)):
                editBgmLb = ttkCustomWidget.CustomTtkLabel(master, text=self.decryptFile.headerList[i][0], font=textSetting.textList["font2"])
                editBgmLb.grid(row=i, column=0, sticky=tkinter.N + tkinter.S)

                idxName = self.decryptFile.headerList[i][0]
                item = self.bgmItem[idxName]
                self.itemList.append(item)
                if maxLen < len(item):
                    maxLen = len(item)
                v_item = tkinter.StringVar()
                self.v_itemList.append(v_item)
                editBgmEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=v_item, font=textSetting.textList["font2"])
                editBgmEt.grid(row=i, column=1, sticky=tkinter.N + tkinter.S)
                self.entryList.append(editBgmEt)

            for i in range(2, len(self.decryptFile.headerList)):
                self.v_itemList[i - 2].set(self.itemList[i - 2])
                self.entryList[i - 2].config(width=maxLen + 5)
        else:
            swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["musicEditor"]["changeBgmNum"], font=textSetting.textList["font2"])
            swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

            swapBgmList = []
            for bgm in range(len(self.decryptFile.musicList)):
                if bgm == self.num:
                    continue
                swapBgmList.append("%02d(%s)" % (bgm, self.decryptFile.musicList[bgm][2]))

            self.v_swap = tkinter.StringVar()
            self.v_swap.set(swapBgmList[0])
            swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=30, font=textSetting.textList["font2"], state="readonly", value=swapBgmList)
            swapCb.grid(row=0, column=1, sticky=tkinter.N + tkinter.S, pady=10)
            swapCb.set(swapBgmList[0])
        super().body(master)

    def validate(self):
        if self.bgmItem is not None:
            title = textSetting.textList["musicEditor"]["commonTitle"]
            for i in range(2, len(self.decryptFile.headerList)):
                if self.decryptFile.headerList[i][0] in [title[0], title[1], title[2]]:
                    try:
                        self.itemList[i - 2] = float(self.v_itemList[i - 2].get())
                    except Exception:
                        errorMsg = textSetting.textList["errorList"]["E3"]
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg, parent=self)
                        return
                else:
                    self.itemList[i - 2] = self.v_itemList[i - 2].get()
                    if len(self.itemList[i - 2].encode("shift-jis")) > 0xFF:
                        errorMsg = textSetting.textList["errorList"]["E20"]
                        mb.showerror(title=textSetting.textList["numberError"], message=errorMsg, parent=self)
                        return
        else:
            comboName = self.v_swap.get()
            bgmNo = int(comboName[0:2])
            self.infoMsg = textSetting.textList["infoList"]["I40"].format(self.num, bgmNo) + self.swapInfoMsg

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=self.infoMsg, parent=self)
        if result:
            musicList = self.decryptFile.musicList[self.num]
            if self.bgmItem is not None:
                for i in range(2, len(self.decryptFile.headerList)):
                    musicList[i - 1] = self.itemList[i - 2]
                self.decryptFile.musicList[self.num] = musicList
            else:
                self.decryptFile.musicList[self.num] = self.decryptFile.musicList[bgmNo]
                self.decryptFile.musicList[bgmNo] = musicList

            errorMsg = textSetting.textList["errorList"]["E4"]
            if not self.decryptFile.saveMusic():
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I41"])
        self.reloadFlag = True
