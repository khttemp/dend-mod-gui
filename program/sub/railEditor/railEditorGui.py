import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

import tkinter

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

        v_radio = tkinter.IntVar()
        v_radio.set(self.RS)

        lsRb = ttkCustomWidget.CustomTtkRadiobutton(root, text="Lightning Stage", command=selectGame, variable=v_radio, value=LS)
        lsRb.place(relx=0.32, rely=0.02)
        lsTrialRb = ttkCustomWidget.CustomTtkRadiobutton(root, text="Lightning Stage(体験版)", command=selectGame, variable=v_radio, value=LSTrial)
        lsTrialRb.place(relx=0.32, rely=0.05)
        bsRb = ttkCustomWidget.CustomTtkRadiobutton(root, text="Burning Stage", command=selectGame, variable=v_radio, value=BS)
        bsRb.place(relx=0.50, rely=0.02)
        csRb = ttkCustomWidget.CustomTtkRadiobutton(root, text="Climax Stage", command=selectGame, variable=v_radio, value=CS)
        csRb.place(relx=0.68, rely=0.02)
        rsRb = ttkCustomWidget.CustomTtkRadiobutton(root, text="Rising Stage", command=selectGame, variable=v_radio, value=RS, state="selected")
        rsRb.place(relx=0.86, rely=0.02)

        excelExtractBtn = ttkCustomWidget.CustomTtkButton(root, text=textSetting.textList["railEditor"]["railDataExtractExcel"], width=30, state="disabled")
        excelExtractBtn.place(relx=0.40, rely=0.08)
        excelSaveBtn = ttkCustomWidget.CustomTtkButton(root, text=textSetting.textList["railEditor"]["railDataSaveExcel"], width=30, state="disabled")
        excelSaveBtn.place(relx=0.70, rely=0.08)

        v_filename = tkinter.StringVar()
        filenameEt = ttkCustomWidget.CustomTtkEntry(root, textvariable=v_filename, font=textSetting.textList["font2"], width=20, state="readonly", justify="center")
        filenameEt.place(relx=0.05, rely=0.02)

        cb = ttkCustomWidget.CustomTtkCombobox(root, width=20, font=textSetting.textList["font2"], values=info, state="disabled")
        cb.bind("<<ComboboxSelected>>", lambda e: selectInfo(cb.current()))
        cb.place(relx=0.05, rely=0.08)

        tabFrame = ttkCustomWidget.CustomTtkFrame(root, borderwidth=1, relief="solid")
        tabFrame.place(relx=0.03, rely=0.13, relwidth=0.95, relheight=0.84)