import os

import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.railEditor.importPy.tkinterTab import (
    tab1AllWidget, tab2AllWidget, tab3AllWidget, tab4AllWidget,
    tab5AllWidget, tab6AllWidget, tab7AllWidget,
    tab9AllWidget, tab10AllWidget
)
#     tab8AllWidget
#     tab11AllWidget
# )

import program.sub.railEditor.dendDecrypt.RSdecrypt as dendRs
import program.sub.railEditor.dendDecrypt.CSdecrypt as dendCs
import program.sub.railEditor.dendDecrypt.BSdecrypt as dendBs
import program.sub.railEditor.dendDecrypt.LSdecrypt as dendLs
import program.sub.railEditor.dendDecrypt.LSTrialDecrypt as dendLsTrial

import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb

class RailEditorWindow(tkinter.Frame):
    def __init__(self, master, importDict, appearance):
        super().__init__(master)
        self.root = master
        self.importDict = importDict
        self.rootFrameAppearance = appearance
        self.decryptFile = None
        self.LSTrial = -1
        self.LS = 0
        self.BS = 1
        self.CS = 2
        self.RS = 3

        self.v_radioGroup = tkinter.IntVar()
        self.v_radioGroup.set(self.RS)

        lsRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Lightning Stage", command=self.radioButtonTrigger, variable=self.v_radioGroup, value=self.LS)
        lsRb.place(relx=0.32, rely=0.02)
        lsTrialRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Lightning Stage(体験版)", command=self.radioButtonTrigger, variable=self.v_radioGroup, value=self.LSTrial)
        lsTrialRb.place(relx=0.32, rely=0.05)
        bsRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Burning Stage", command=self.radioButtonTrigger, variable=self.v_radioGroup, value=self.BS)
        bsRb.place(relx=0.50, rely=0.02)
        csRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Climax Stage", command=self.radioButtonTrigger, variable=self.v_radioGroup, value=self.CS)
        csRb.place(relx=0.68, rely=0.02)
        rsRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Rising Stage", command=self.radioButtonTrigger, variable=self.v_radioGroup, value=self.RS, state="selected")
        rsRb.place(relx=0.86, rely=0.02)

        self.excelExtractButton = ttkCustomWidget.CustomTtkButton(master, text=textSetting.textList["railEditor"]["railDataExtractExcel"], width=30, state="disabled")
        self.excelExtractButton.place(relx=0.40, rely=0.08)
        self.excelSaveButton = ttkCustomWidget.CustomTtkButton(master, text=textSetting.textList["railEditor"]["railDataSaveExcel"], width=30, state="disabled")
        self.excelSaveButton.place(relx=0.70, rely=0.08)

        self.v_filename = tkinter.StringVar()
        filenameEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_filename, font=textSetting.textList["font2"], width=20, state="readonly", justify="center")
        filenameEt.place(relx=0.05, rely=0.02)

        self.tabCombo = ttkCustomWidget.CustomTtkCombobox(master, width=20, font=textSetting.textList["font2"], values=textSetting.textList["railEditor"]["railComboValue"], state="disabled")
        self.tabCombo.bind("<<ComboboxSelected>>", lambda e: self.selectInfo(self.tabCombo.current()))
        self.tabCombo.place(relx=0.05, rely=0.08)

        self.tabFrame = ttkCustomWidget.CustomTtkFrame(master, borderwidth=1, relief="solid")
        self.tabFrame.place(relx=0.03, rely=0.13, relwidth=0.95, relheight=0.84)

    def radioButtonTrigger(self):
        self.v_filename.set("")
        self.tabCombo.set("")
        self.tabCombo["state"] = "disabled"

        self.excelExtractButton["state"] = "disabled"
        self.excelSaveButton["state"] = "disabled"
        self.deleteAllWidget()

    def deleteAllWidget(self):
        children = self.tabFrame.winfo_children()
        for child in children:
            child.destroy()

    def selectInfo(self, index, selectId=None):
        self.deleteAllWidget()

        if index == 0:
            tab1AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget)
        elif index == 1:
            tab2AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget)
        elif index == 2:
            tab3AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget, selectId)
        elif index == 3:
            tab4AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget, selectId)
        elif index == 4:
            tab5AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget)
        elif index == 5:
            tab6AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget, selectId)
        elif index == 6:
            tab7AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget)
        # elif index == 7:
        #     tab8AllWidget(self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget)
        elif index == 8:
            tab9AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget, selectId)
        elif index == 9:
            tab10AllWidget(self.root, self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget)
        # elif index == 10:
        #     tab11AllWidget(self.tabFrame, self.decryptFile, self.rootFrameAppearance, self.reloadWidget)

    def reloadWidget(self, *selectId):
        self.decryptFile = self.decryptFile.reload()
        selId = None
        if selectId and selectId[0] is not None:
            selId = int(selectId[0])
        self.selectInfo(self.tabCombo.current(), selId)

    def openFile(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["railEditor"]["fileType"], "*.BIN")])
        if file_path:
            filename = os.path.basename(file_path)
            self.v_filename.set(filename)
            del self.decryptFile
            self.decryptFile = None

            selectedRadioId = self.v_radioGroup.get()
            if selectedRadioId == self.RS:
                self.decryptFile = dendRs.RailDecrypt(file_path)
            elif selectedRadioId == self.CS:
                self.decryptFile = dendCs.RailDecrypt(file_path)
            elif selectedRadioId == self.BS:
                self.decryptFile = dendBs.RailDecrypt(file_path)
            elif selectedRadioId == self.LS:
                self.decryptFile = dendLs.RailDecrypt(file_path)
            elif selectedRadioId == self.LSTrial:
                self.decryptFile = dendLsTrial.RailDecrypt(file_path)

            if not self.decryptFile.open():
                if self.decryptFile.error == "":
                    errorMsg = textSetting.textList["errorList"]["E76"].format(self.decryptFile.game)
                    mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                else:
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E21"])
                return

            self.deleteAllWidget()
            if selectedRadioId in [self.LS, self.LSTrial]:
                self.tabCombo["values"] = textSetting.textList["railEditor"]["railLsComboValue"]
            else:
                self.tabCombo["values"] = textSetting.textList["railEditor"]["railComboValue"]
            self.tabCombo.current(0)
            self.tabCombo["state"] = "readonly"

            self.excelExtractButton["state"] = "normal"
            self.excelSaveButton["state"] = "normal"
            self.selectInfo(self.tabCombo.current())
