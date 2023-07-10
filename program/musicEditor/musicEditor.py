import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

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

BS = 1
CS = 2
RS = 3


def openFile():
    global v_radio
    global decryptFile

    if v_radio.get() == BS:
        file_path = fd.askopenfilename(filetypes=[("MUSIC_DATA", "LS_INFO.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendBs.BSMusicDecrypt(file_path)
    elif v_radio.get() == CS:
        file_path = fd.askopenfilename(filetypes=[("MUSIC_DATA", "SOUNDTRACK_INFO.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendCs.CSMusicDecrypt(file_path)
    elif v_radio.get() == RS:
        file_path = fd.askopenfilename(filetypes=[("MUSIC_DATA", "SOUNDTRACK_INFO_4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendRs.RSMusicDecrypt(file_path)

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if file_path:
        deleteWidget()
        if not decryptFile.open():
            decryptFile.printError()
            mb.showerror(title="エラー", message=errorMsg)
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

    frame.tree.column('#0', width=0, stretch='no')
    for i in range(len(decryptFile.headerList)):
        frame.tree.column(decryptFile.headerList[i][0], anchor=tkinter.CENTER, width=decryptFile.headerList[i][1])

    for i in range(len(decryptFile.headerList)):
        frame.tree.heading(decryptFile.headerList[i][0], text=decryptFile.headerList[i][0], anchor=tkinter.CENTER)

    for i in range(len(decryptFile.musicList)):
        data = tuple([i]) + tuple(decryptFile.musicList[i])
        frame.tree.insert(parent='', index='end', iid=i, values=data)


def editMusic():
    global root
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "BGM修正", decryptFile, int(selectItem["No"]), selectItem)
    if result.reloadFlag:
        reloadFile()


def swapMusic():
    global root
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "BGM入れ替え", decryptFile, int(selectItem["No"]))
    if result.reloadFlag:
        reloadFile()


def reloadFile():
    global edit_button
    global swap_button
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title="エラー", message=errorMsg)
        return

    deleteWidget()
    createWidget()
    edit_button['state'] = 'disabled'
    swap_button['state'] = 'disabled'


def deleteWidget():
    global edit_button
    global swap_button
    global bgmLf

    children = bgmLf.winfo_children()
    for child in children:
        child.destroy()

    edit_button['state'] = 'disabled'
    swap_button['state'] = 'disabled'


def call_musicEditor(rootTk, programFrame):
    global root
    global v_edit
    global v_swap
    global edit_button
    global swap_button
    global v_radio
    global bgmLf

    root = rootTk
    v_edit = tkinter.StringVar()
    v_edit.set("このBGMを修正する")
    edit_button = ttk.Button(programFrame, textvariable=v_edit, command=editMusic, state='disabled')
    edit_button.place(relx=0.48, rely=0.02, relwidth=0.2, height=25)

    v_swap = tkinter.StringVar()
    v_swap.set("このBGMを入れ替える")
    swap_button = ttk.Button(programFrame, textvariable=v_swap, command=swapMusic, state='disabled')
    swap_button.place(relx=0.75, rely=0.02, relwidth=0.2, height=25)

    v_radio = tkinter.IntVar()

    bsRb = tkinter.Radiobutton(programFrame, text="Burning Stage", command=deleteWidget, variable=v_radio, value=BS)
    bsRb.place(relx=0.04, rely=0.02)

    csRb = tkinter.Radiobutton(programFrame, text="Climax Stage", command=deleteWidget, variable=v_radio, value=CS)
    csRb.place(relx=0.18, rely=0.02)

    rsRb = tkinter.Radiobutton(programFrame, text="Rising Stage", command=deleteWidget, variable=v_radio, value=RS)
    rsRb.select()
    rsRb.place(relx=0.32, rely=0.02)

    bgmLf = ttk.LabelFrame(programFrame, text="BGMリスト")
    bgmLf.place(relx=0.03, rely=0.07, relwidth=0.95, relheight=0.90)
