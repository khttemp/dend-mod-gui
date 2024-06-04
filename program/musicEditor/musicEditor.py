import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

from program.musicEditor.dendMusicDecrypt import BSMusicDecrypt as dendBs
from program.musicEditor.dendMusicDecrypt import CSMusicDecrypt as dendCs
from program.musicEditor.dendMusicDecrypt import RSMusicDecrypt as dendRs

from program.musicEditor.importPy.tkinterScrollbarTreeviewMusicEditor import ScrollbarTreeviewMusicEditor
from program.musicEditor.importPy.tkinterEditClass import InputDialog

v_edit = None
v_swap = None
edit_button = None
swap_button = None
v_radio = None
bgmLf = None
decryptFile = None
frame = None
rootFrameAppearance = None

BS = 1
CS = 2
RS = 3


def openFile():
    global v_radio
    global decryptFile

    if v_radio.get() == BS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["musicEditor"]["fileType"], "LS_INFO.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendBs.BSMusicDecrypt(file_path)
    elif v_radio.get() == CS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["musicEditor"]["fileType"], "SOUNDTRACK_INFO.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendCs.CSMusicDecrypt(file_path)
    elif v_radio.get() == RS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["musicEditor"]["fileType"], "SOUNDTRACK_INFO_4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendRs.RSMusicDecrypt(file_path)

    errorMsg = textSetting.textList["errorList"]["E21"]
    if file_path:
        deleteWidget()
        if not decryptFile.open():
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        createWidget()


def createWidget():
    global edit_button
    global swap_button
    global v_radio
    global decryptFile
    global bgmLf
    global frame

    content = v_radio.get()
    btnList = [
        edit_button,
        swap_button
    ]
    frame = ScrollbarTreeviewMusicEditor(bgmLf, content, btnList)

    treeHeaderList = []

    for i in range(len(decryptFile.headerList)):
        treeHeaderList.append(decryptFile.headerList[i][0])

    frame.tree["columns"] = tuple(treeHeaderList)

    frame.tree.column("#0", width=0, stretch="no")
    for i in range(len(decryptFile.headerList)):
        frame.tree.column(decryptFile.headerList[i][0], anchor=tkinter.CENTER, width=decryptFile.headerList[i][1])

    for i in range(len(decryptFile.headerList)):
        frame.tree.heading(decryptFile.headerList[i][0], text=decryptFile.headerList[i][0], anchor=tkinter.CENTER)

    for i in range(len(decryptFile.musicList)):
        data = tuple([i]) + tuple(decryptFile.musicList[i])
        frame.tree.insert(parent="", index="end", iid=i, values=data)


def editMusic():
    global root
    global rootFrameAppearance
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, textSetting.textList["musicEditor"]["bgmModify"], decryptFile, rootFrameAppearance, int(selectItem[textSetting.textList["musicEditor"]["bgmNo"]]), selectItem)
    if result.reloadFlag:
        reloadFile()


def swapMusic():
    global root
    global rootFrameAppearance
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, textSetting.textList["musicEditor"]["bgmSwap"], decryptFile, rootFrameAppearance, int(selectItem[textSetting.textList["musicEditor"]["bgmNo"]]))
    if result.reloadFlag:
        reloadFile()


def reloadFile():
    global edit_button
    global swap_button
    global decryptFile

    errorMsg = textSetting.textList["errorList"]["E21"]
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        return

    deleteWidget()
    createWidget()
    edit_button["state"] = "disabled"
    swap_button["state"] = "disabled"


def deleteWidget():
    global edit_button
    global swap_button
    global bgmLf

    children = bgmLf.winfo_children()
    for child in children:
        child.destroy()

    edit_button["state"] = "disabled"
    swap_button["state"] = "disabled"


def call_musicEditor(rootTk, appearance):
    global root
    global rootFrameAppearance
    global v_edit
    global v_swap
    global edit_button
    global swap_button
    global v_radio
    global bgmLf

    root = rootTk
    rootFrameAppearance = appearance

    headerFrame = ttkCustomWidget.CustomTtkFrame(root)
    headerFrame.pack(fill=tkinter.X, padx=40, pady=(25, 0))

    radioFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
    radioFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

    v_radio = tkinter.IntVar(value=RS)

    bsRb = ttkCustomWidget.CustomTtkRadiobutton(radioFrame, text="Burning Stage", command=deleteWidget, variable=v_radio, value=BS)
    bsRb.grid(row=0, column=0, padx=(0, 50))

    csRb = ttkCustomWidget.CustomTtkRadiobutton(radioFrame, text="Climax Stage", command=deleteWidget, variable=v_radio, value=CS)
    csRb.grid(row=0, column=1, padx=(0, 50))

    rsRb = ttkCustomWidget.CustomTtkRadiobutton(radioFrame, text="Rising Stage", command=deleteWidget, variable=v_radio, value=RS)
    rsRb.grid(row=0, column=2, padx=(0, 50))

    btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
    btnFrame.pack(fill=tkinter.X)

    v_edit = tkinter.StringVar()
    v_edit.set(textSetting.textList["musicEditor"]["bgmModifyLabel"])
    edit_button = ttkCustomWidget.CustomTtkButton(btnFrame, textvariable=v_edit, width=30, command=editMusic, state="disabled")
    edit_button.grid(row=0, column=0)

    v_swap = tkinter.StringVar()
    v_swap.set(textSetting.textList["musicEditor"]["bgmSwapLabel"])
    swap_button = ttkCustomWidget.CustomTtkButton(btnFrame, textvariable=v_swap, width=30, command=swapMusic, state="disabled")
    swap_button.grid(row=0, column=1)

    btnFrame.grid_columnconfigure(0, weight=1)
    btnFrame.grid_columnconfigure(1, weight=1)

    bgmLf = ttkCustomWidget.CustomTtkLabelFrame(root, text=textSetting.textList["musicEditor"]["scriptLabel"])
    bgmLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))
