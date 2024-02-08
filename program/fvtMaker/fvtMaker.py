import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting

from program.tkinterScrollbarFrameClass import ScrollbarFrame
from program.fvtMaker.importPy.tkinterWidgetClass import CsvWidget, DescWidget
from program.fvtMaker.importPy.fvtConvert import FvtConvert

root = None
v_radio = None
csvLf = None
descLf = None
content = -1
fvtConvertFile = None

LS = 0
BS = 1
CS = 2
RS = 3


def openFile():
    global root
    global fvtConvertFile
    global content

    if content == -1:
        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E13"])
        return

    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["fvtMaker"]["fileType"], "*.csv")])

    if file_path:
        del fvtConvertFile
        fvtConvertFile = FvtConvert(file_path, content)
        if not fvtConvertFile.open():
            mb.showerror(title=textSetting.textList["error"], message=fvtConvertFile.error)
            return

        warnMsg = textSetting.textList["infoList"]["I13"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=root)
        if result:
            try:
                fvtConvertFile.write()
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I14"])
            except Exception:
                w = open("error.log", "w")
                w.write(traceback.format_exc())
                w.close()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E14"])


def selectGame():
    global v_radio
    global csvLf
    global descLf
    global content
    deleteWidget()

    content = v_radio.get()
    frame = ScrollbarFrame(csvLf, True)
    frame.pack(expand=True, fill=tkinter.BOTH)
    CsvWidget(frame.interior, content)
    frame2 = ScrollbarFrame(descLf, True)
    frame2.pack(expand=True, fill=tkinter.BOTH)
    DescWidget(frame2.interior, content)


def deleteWidget():
    global csvLf
    global descLf
    children = csvLf.winfo_children()
    for child in children:
        child.destroy()

    children = descLf.winfo_children()
    for child in children:
        child.destroy()


def call_fvtMaker(rootTk, programFrame):
    global root
    global v_radio
    global csvLf
    global descLf
    global content

    root = rootTk
    content = -1

    v_radio = tkinter.IntVar()
    v_radio.set(-1)

    lsRb = tkinter.Radiobutton(programFrame, text="Lightning Stage", command=selectGame, variable=v_radio, value=LS)
    lsRb.place(relx=0.05, rely=0.02)

    bsRb = tkinter.Radiobutton(programFrame, text="Burning Stage", command=selectGame, variable=v_radio, value=BS)
    bsRb.place(relx=0.3, rely=0.02)

    csRb = tkinter.Radiobutton(programFrame, text="Climax Stage", command=selectGame, variable=v_radio, value=CS)
    csRb.place(relx=0.55, rely=0.02)

    rsRb = tkinter.Radiobutton(programFrame, text="Rising Stage", command=selectGame, variable=v_radio, value=RS)
    rsRb.place(relx=0.8, rely=0.02)

    csvLf = ttk.LabelFrame(programFrame, text=textSetting.textList["fvtMaker"]["csvLfLabel"])
    csvLf.place(relx=0.03, rely=0.07, relwidth=0.95, relheight=0.3)

    descLf = ttk.LabelFrame(programFrame, text=textSetting.textList["fvtMaker"]["howWrite"])
    descLf.place(relx=0.03, rely=0.38, relwidth=0.95, relheight=0.59)
