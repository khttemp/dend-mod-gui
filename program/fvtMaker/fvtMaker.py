import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

from program.tkinterScrollbarFrameClass import ScrollbarFrame
from program.fvtMaker.importPy.tkinterWidgetClass import CsvWidget, DescWidget
from program.fvtMaker.importPy.fvtConvert import FvtConvert

root = None
v_radio = None
csvLf = None
descLf = None
content = -1
fvtConvertFile = None
rootFrameAppearance = None

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
            fvtConvertFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E124"])
            return

        warnMsg = textSetting.textList["infoList"]["I13"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=root)
        if result:
            if not fvtConvertFile.write():
                fvtConvertFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I14"])


def selectGame():
    global v_radio
    global csvLf
    global descLf
    global content
    global rootFrameAppearance
    deleteWidget()

    content = v_radio.get()
    frame = ScrollbarFrame(csvLf, True, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    CsvWidget(frame.interior, content)
    frame2 = ScrollbarFrame(descLf, True, bgColor=rootFrameAppearance.bgColor)
    frame2.pack(expand=True, fill=tkinter.BOTH)
    DescWidget(frame2.interior, content, rootFrameAppearance)


def deleteWidget():
    global csvLf
    global descLf
    children = csvLf.winfo_children()
    for child in children:
        child.destroy()

    children = descLf.winfo_children()
    for child in children:
        child.destroy()


def call_fvtMaker(rootTk, appearance):
    global root
    global v_radio
    global csvLf
    global descLf
    global content
    global rootFrameAppearance

    root = rootTk
    rootFrameAppearance = appearance
    content = -1

    headerFrame = ttkCustomWidget.CustomTtkFrame(root)
    headerFrame.pack(fill=tkinter.X, padx=40, pady=25)

    v_radio = tkinter.IntVar()
    v_radio.set(-1)

    lsRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Lightning Stage", command=selectGame, variable=v_radio, value=LS)
    lsRb.grid(row=0, column=0, padx=10)

    bsRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Burning Stage", command=selectGame, variable=v_radio, value=BS)
    bsRb.grid(row=0, column=1, padx=10)

    csRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Climax Stage", command=selectGame, variable=v_radio, value=CS)
    csRb.grid(row=0, column=2, padx=10)

    rsRb = ttkCustomWidget.CustomTtkRadiobutton(headerFrame, text="Rising Stage", command=selectGame, variable=v_radio, value=RS)
    rsRb.grid(row=0, column=3, padx=10)

    headerFrame.grid_columnconfigure(0, weight=1)
    headerFrame.grid_columnconfigure(1, weight=1)
    headerFrame.grid_columnconfigure(2, weight=1)
    headerFrame.grid_columnconfigure(3, weight=1)

    bodyFrame = ttkCustomWidget.CustomTtkFrame(root)
    bodyFrame.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))

    csvLf = ttkCustomWidget.CustomTtkLabelFrame(bodyFrame, text=textSetting.textList["fvtMaker"]["csvLfLabel"], height=250)
    csvLf.pack(fill=tkinter.BOTH)
    csvLf.pack_propagate(False)

    descLf = ttkCustomWidget.CustomTtkLabelFrame(bodyFrame, text=textSetting.textList["fvtMaker"]["howWrite"])
    descLf.pack(expand=True, fill=tkinter.BOTH)
