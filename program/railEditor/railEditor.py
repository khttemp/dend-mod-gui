import os
import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting

from program.railEditor.importPy.tkinterTab import tab1AllWidget, tab2AllWidget, tab3AllWidget, tab4AllWidget, tab5AllWidget, tab6AllWidget, tab7AllWidget, tab8AllWidget, tab9AllWidget, tab10AllWidget, tab11AllWidget
import program.railEditor.dendDecrypt.RSdecrypt as dendRs
import program.railEditor.dendDecrypt.CSdecrypt as dendCs
import program.railEditor.dendDecrypt.BSdecrypt as dendBs
import program.railEditor.dendDecrypt.LSdecrypt as dendLs

LS = 0
BS = 1
CS = 2
RS = 3

v_radio = None
v_filename = None
cb = None
tabFrame = None
decryptFile = None
info = textSetting.textList["railEditor"]["railComboValue"]
lsInfo = textSetting.textList["railEditor"]["railLsComboValue"]


def openFile(v_railCsvMode, v_ambCsvMode):
    global v_radio
    global v_filename
    global cb
    global lsInfo
    global info
    global decryptFile

    errorMsg = textSetting.textList["errorList"]["E21"]
    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["railEditor"]["fileType"], "*.BIN")])
    if file_path:
        filename = os.path.basename(file_path)
        v_filename.set(filename)
        del decryptFile
        decryptFile = None

        writeFlag = True
        ambWriteFlag = True

        if v_railCsvMode == 0:
            file = os.path.splitext(os.path.basename(file_path))[0]
            directory = os.path.dirname(file_path)
            if os.path.exists(os.path.join(directory, file + ".csv")):
                result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I96"], icon="warning")
                if result == "no":
                    writeFlag = False
        elif v_railCsvMode == 2:
            file = os.path.splitext(os.path.basename(file_path))[0]
            directory = os.path.dirname(file_path)
            if os.path.exists(os.path.join(directory, file + ".csv")):
                writeFlag = False

        if v_ambCsvMode == 0:
            file = os.path.splitext(os.path.basename(file_path))[0]
            directory = os.path.dirname(file_path)
            if os.path.exists(os.path.join(directory, file + "_amb.csv")):
                result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I97"], icon="warning")
                if result == "no":
                    ambWriteFlag = False
        elif v_ambCsvMode == 2:
            file = os.path.splitext(os.path.basename(file_path))[0]
            directory = os.path.dirname(file_path)
            if os.path.exists(os.path.join(directory, file + ".csv")):
                ambWriteFlag = False

        if v_radio.get() == RS:
            decryptFile = dendRs.RailDecrypt(file_path, writeFlag, ambWriteFlag)
        elif v_radio.get() == CS:
            decryptFile = dendCs.RailDecrypt(file_path, writeFlag, ambWriteFlag)
        elif v_radio.get() == BS:
            decryptFile = dendBs.RailDecrypt(file_path, writeFlag, ambWriteFlag)
        elif v_radio.get() == LS:
            decryptFile = dendLs.RailDecrypt(file_path, writeFlag, ambWriteFlag)

        if not decryptFile.open():
            if decryptFile.error == "":
                errorMsg = textSetting.textList["errorList"]["E76"].format(decryptFile.game)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            else:
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        deleteAllWidget()
        if v_radio.get() == LS:
            cb["values"] = lsInfo
        else:
            cb["values"] = info
        cb.current(0)
        cb["state"] = "readonly"
        selectInfo(cb.current())


def deleteAllWidget():
    global tabFrame
    children = tabFrame.winfo_children()
    for child in children:
        child.destroy()


def selectInfo(index, selectId=None):
    global tabFrame
    global decryptFile
    deleteAllWidget()

    if index == 0:
        tab1AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 1:
        tab2AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 2:
        tab3AllWidget(tabFrame, decryptFile, reloadWidget, selectId)
    elif index == 3:
        tab4AllWidget(tabFrame, decryptFile, reloadWidget, selectId)
    elif index == 4:
        tab5AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 5:
        tab6AllWidget(tabFrame, decryptFile, reloadWidget, selectId)
    elif index == 6:
        tab7AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 7:
        tab8AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 8:
        tab9AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 9:
        tab10AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 10:
        tab11AllWidget(tabFrame, decryptFile, reloadWidget)


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
    v_filename.set("")
    cb.set("")
    cb["state"] = "disabled"
    deleteAllWidget()


def call_railEditor(rootTk, programFrame):
    global root
    global info
    global v_radio
    global v_filename
    global cb
    global tabFrame

    root = rootTk
    v_radio = tkinter.IntVar()
    v_radio.set(RS)

    lsRb = tkinter.Radiobutton(programFrame, text="Lightning Stage", command=selectGame, variable=v_radio, value=LS)
    lsRb.place(relx=0.32, rely=0.02)
    bsRb = tkinter.Radiobutton(programFrame, text="Burning Stage", command=selectGame, variable=v_radio, value=BS)
    bsRb.place(relx=0.50, rely=0.02)
    csRb = tkinter.Radiobutton(programFrame, text="Climax Stage", command=selectGame, variable=v_radio, value=CS)
    csRb.place(relx=0.68, rely=0.02)
    rsRb = tkinter.Radiobutton(programFrame, text="Rising Stage", command=selectGame, variable=v_radio, value=RS)
    rsRb.place(relx=0.86, rely=0.02)
    rsRb.select()

    v_filename = tkinter.StringVar()
    filenameEt = ttk.Entry(programFrame, textvariable=v_filename, font=textSetting.textList["font2"], width=20, state="readonly", justify="center")
    filenameEt.place(relx=0.05, rely=0.02)

    cb = ttk.Combobox(programFrame, width=20, font=textSetting.textList["font2"], values=info, state="disabled")
    cb.bind("<<ComboboxSelected>>", lambda e: selectInfo(cb.current()))
    cb.place(relx=0.05, rely=0.08)

    tabFrame = ttk.Frame(programFrame, borderwidth=1, relief="solid")
    tabFrame.place(relx=0.03, rely=0.13, relwidth=0.95, relheight=0.84)
