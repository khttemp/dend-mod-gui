import os
import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

from program.railEditor.importPy.tkinterTab import tab1AllWidget, tab2AllWidget, tab3AllWidget, tab4AllWidget, tab5AllWidget, tab6AllWidget, tab7AllWidget, tab8AllWidget, tab9AllWidget, tab10AllWidget, tab11AllWidget
from program.railEditor.importPy.excelWidget import ExcelWidget
import program.railEditor.dendDecrypt.RSdecrypt as dendRs
import program.railEditor.dendDecrypt.CSdecrypt as dendCs
import program.railEditor.dendDecrypt.BSdecrypt as dendBs
import program.railEditor.dendDecrypt.LSdecrypt as dendLs
import program.railEditor.dendDecrypt.LSTrialDecrypt as dendLsTrial

LSTrial = -1
LS = 0
BS = 1
CS = 2
RS = 3

v_radio = None
v_filename = None
cb = None
tabFrame = None
decryptFile = None
excelWidget = None
excelExtractBtn = None
excelSaveBtn = None
configPath = None
rootFrameAppearance = None
info = textSetting.textList["railEditor"]["railComboValue"]
lsInfo = textSetting.textList["railEditor"]["railLsComboValue"]


def openFile():
    global v_radio
    global v_filename
    global cb
    global lsInfo
    global info
    global decryptFile
    global excelWidget
    global excelExtractBtn
    global excelSaveBtn
    global configPath

    errorMsg = textSetting.textList["errorList"]["E21"]
    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["railEditor"]["fileType"], "*.BIN")])
    if file_path:
        filename = os.path.basename(file_path)
        v_filename.set(filename)
        del decryptFile
        decryptFile = None

        if v_radio.get() == RS:
            decryptFile = dendRs.RailDecrypt(file_path)
        elif v_radio.get() == CS:
            decryptFile = dendCs.RailDecrypt(file_path)
        elif v_radio.get() == BS:
            decryptFile = dendBs.RailDecrypt(file_path)
        elif v_radio.get() == LS:
            decryptFile = dendLs.RailDecrypt(file_path)
        elif v_radio.get() == LSTrial:
            decryptFile = dendLsTrial.RailDecrypt(file_path)

        if not decryptFile.open():
            if decryptFile.error == "":
                errorMsg = textSetting.textList["errorList"]["E76"].format(decryptFile.game)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            else:
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        deleteAllWidget()
        if v_radio.get() in [LS, LSTrial]:
            cb["values"] = lsInfo
        else:
            cb["values"] = info
        cb.current(0)
        cb["state"] = "readonly"
        excelWidget = ExcelWidget(decryptFile, reloadWidget, configPath)
        excelExtractBtn["command"] = excelWidget.extract
        excelSaveBtn["command"] = excelWidget.save
        excelExtractBtn["state"] = "normal"
        excelSaveBtn["state"] = "normal"
        selectInfo(cb.current())


def deleteAllWidget():
    global tabFrame
    children = tabFrame.winfo_children()
    for child in children:
        child.destroy()


def selectInfo(index, selectId=None):
    global root
    global tabFrame
    global decryptFile
    global rootFrameAppearance
    deleteAllWidget()

    if index == 0:
        tab1AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget)
    elif index == 1:
        tab2AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget)
    elif index == 2:
        tab3AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget, selectId)
    elif index == 3:
        tab4AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget, selectId)
    elif index == 4:
        tab5AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget)
    elif index == 5:
        tab6AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget, selectId)
    elif index == 6:
        tab7AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget)
    elif index == 7:
        tab8AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadWidget)
    elif index == 8:
        tab9AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget, selectId)
    elif index == 9:
        tab10AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadWidget)
    elif index == 10:
        tab11AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadWidget)


def reloadWidget(*selectId):
    global cb
    global decryptFile
    decryptFile = decryptFile.reload()
    deleteAllWidget()
    selId = None
    if selectId and selectId[0] is not None:
        selId = int(selectId[0])
    selectInfo(cb.current(), selId)


def selectGame():
    global v_filename
    global cb
    global excelWidget
    global excelExtractBtn
    global excelSaveBtn

    v_filename.set("")
    cb.set("")
    cb["state"] = "disabled"
    excelWidget = None
    excelExtractBtn["state"] = "disabled"
    excelSaveBtn["state"] = "disabled"
    deleteAllWidget()


def call_railEditor(rootTk, config_ini_path, appearance):
    global root
    global info
    global v_radio
    global v_filename
    global cb
    global tabFrame
    global excelExtractBtn
    global excelSaveBtn
    global configPath
    global rootFrameAppearance

    configPath = config_ini_path
    rootFrameAppearance = appearance

    root = rootTk
    v_radio = tkinter.IntVar()
    v_radio.set(RS)

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
