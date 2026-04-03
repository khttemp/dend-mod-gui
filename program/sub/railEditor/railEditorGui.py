import os

import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

import program.sub.railEditor.dendDecrypt.RSdecrypt as dendRs
import program.sub.railEditor.dendDecrypt.CSdecrypt as dendCs
import program.sub.railEditor.dendDecrypt.BSdecrypt as dendBs
import program.sub.railEditor.dendDecrypt.LSdecrypt as dendLs
import program.sub.railEditor.dendDecrypt.LSTrialDecrypt as dendLsTrial

import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb

class RailEditorWindow(tkinter.Frame):
    def __init__(self, master, importDict):
        super().__init__(master)
        self.importDict = importDict
        self.decryptFile = None
        self.LSTrial = -1
        self.LS = 0
        self.BS = 1
        self.CS = 2
        self.RS = 3

        self.v_radio = tkinter.IntVar()
        self.v_radio.set(self.RS)

        lsRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Lightning Stage", command=self.selectGame, variable=self.v_radio, value=self.LS)
        lsRb.place(relx=0.32, rely=0.02)
        lsTrialRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Lightning Stage(体験版)", command=self.selectGame, variable=self.v_radio, value=self.LSTrial)
        lsTrialRb.place(relx=0.32, rely=0.05)
        bsRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Burning Stage", command=self.selectGame, variable=self.v_radio, value=self.BS)
        bsRb.place(relx=0.50, rely=0.02)
        csRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Climax Stage", command=self.selectGame, variable=self.v_radio, value=self.CS)
        csRb.place(relx=0.68, rely=0.02)
        rsRb = ttkCustomWidget.CustomTtkRadiobutton(master, text="Rising Stage", command=self.selectGame, variable=self.v_radio, value=self.RS, state="selected")
        rsRb.place(relx=0.86, rely=0.02)

        self.excelExtractBtn = ttkCustomWidget.CustomTtkButton(master, text=textSetting.textList["railEditor"]["railDataExtractExcel"], width=30, state="disabled")
        self.excelExtractBtn.place(relx=0.40, rely=0.08)
        self.excelSaveBtn = ttkCustomWidget.CustomTtkButton(master, text=textSetting.textList["railEditor"]["railDataSaveExcel"], width=30, state="disabled")
        self.excelSaveBtn.place(relx=0.70, rely=0.08)

        self.v_filename = tkinter.StringVar()
        filenameEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_filename, font=textSetting.textList["font2"], width=20, state="readonly", justify="center")
        filenameEt.place(relx=0.05, rely=0.02)

        self.cb = ttkCustomWidget.CustomTtkCombobox(master, width=20, font=textSetting.textList["font2"], values=textSetting.textList["railEditor"]["railComboValue"], state="disabled")
        self.cb.bind("<<ComboboxSelected>>", lambda e: self.selectInfo(cb.current()))
        self.cb.place(relx=0.05, rely=0.08)

        self.tabFrame = ttkCustomWidget.CustomTtkFrame(master, borderwidth=1, relief="solid")
        self.tabFrame.place(relx=0.03, rely=0.13, relwidth=0.95, relheight=0.84)

    def selectGame(self):
        self.v_filename.set("")
        self.cb.set("")
        self.cb["state"] = "disabled"

        self.excelExtractBtn["state"] = "disabled"
        self.excelSaveBtn["state"] = "disabled"
        self.deleteAllWidget()

    def deleteAllWidget(self):
        children = self.tabFrame.winfo_children()
        for child in children:
            child.destroy()

    def selectInfo(self, selectId=None):
        pass

    def openFile(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["railEditor"]["fileType"], "*.BIN")])
        if file_path:
            filename = os.path.basename(file_path)
            self.fileNameLabel.setText(filename)
            del self.decryptFile
            self.decryptFile = None

            selectedRadioId = self.v_radio.get()
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
                self.cb["values"] = textSetting.textList["railEditor"]["railLsComboValue"]
            else:
                self.cb["values"] = textSetting.textList["railEditor"]["railComboValue"]
            self.cb.current(0)
            self.cb["state"] = "readonly"

            self.excelExtractBtn["state"] = "normal"
            self.excelSaveBtn["state"] = "normal"
            self.selectInfo(self.tabCombo.currentIndex())
