import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

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
        mb.showerror(title="エラー", message="ゲームを選択してください")
        return

    file_path = fd.askopenfilename(filetypes=[("CSVファイル", "*.csv")])

    if file_path:
        del fvtConvertFile
        fvtConvertFile = FvtConvert(file_path, content)
        if not fvtConvertFile.open():
            mb.showerror(title="エラー", message=fvtConvertFile.error)
            return

        warnMsg = "変換準備ができました。\n既存のファイルは上書きされます。\nそれでもよろしいですか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=root)
        if result:
            try:
                fvtConvertFile.write()
                mb.showinfo(title="成功", message="全てのリストを書込みしました")
            except Exception:
                w = open("error.log", "w")
                w.write(traceback.format_exc())
                w.close()
                mb.showerror(title="保存エラー", message="予想外のエラーです。変換失敗しました")


def selectGame():
    global v_radio
    global csvLf
    global descLf
    global content
    deleteWidget()

    content = v_radio.get()
    frame = ScrollbarFrame(csvLf, True, False)
    CsvWidget(frame.frame, content)
    frame2 = ScrollbarFrame(descLf, True, False)
    DescWidget(frame2.frame, content)


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

    csvLf = ttk.LabelFrame(programFrame, text="CSVの様式（CSVの1行目はヘッダー扱いになり、読み込みを省略する）")
    csvLf.place(relx=0.03, rely=0.07, relwidth=0.95, relheight=0.3)

    descLf = ttk.LabelFrame(programFrame, text="作成方法")
    descLf.place(relx=0.03, rely=0.38, relwidth=0.95, relheight=0.59)
