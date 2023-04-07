import os
import sys
import codecs
import configparser
import tkinter
from tkinter import ttk

from tkinter import messagebox as mb

import program.comicscript.comicscript as comicscriptProgram
import program.mdlBin.mdlBin as mdlBinProgram
import program.mdlinfo.mdlinfo as mdlinfoProgram
import program.lbcrEditor.lbcrEditor as lbcrEditorProgram
import program.musicEditor.musicEditor as musicEditorProgram
import program.fvtMaker.fvtMaker as fvtMakerProgram
import program.railEditor.railEditor as railEditorProgram


def clearProgramFrame():
    children = programFrame.winfo_children()
    for child in children:
        child.destroy()


def callProgram(programName):
    global selectedProgram

    clearProgramFrame()
    selectedProgram = programName
    if selectedProgram == "lbcrEditor":
        lbcrEditorProgram.call_lbcrEditor(root, programFrame)
    elif selectedProgram == "mdlBin":
        mdlBinProgram.call_mdlBin(root, programFrame)
    elif selectedProgram == "mdlinfo":
        mdlinfoProgram.call_mdlinfo(root, programFrame)
    elif selectedProgram == "comicscript":
        comicscriptProgram.call_comicscript(root, programFrame)
    elif selectedProgram == "musicEditor":
        musicEditorProgram.call_musicEditor(root, programFrame)
    elif selectedProgram == "fvtMaker":
        fvtMakerProgram.call_fvtMaker(root, programFrame)
    elif selectedProgram == "railEditor":
        railEditorProgram.call_railEditor(root, programFrame)

    if selectedProgram == "railEditor":
        add_railCsvOptionMenu()
    else:
        delete_railCsvOptionMenu()


def loadFile():
    global v_railCsvRadio
    global v_ambCsvRadio
    global selectedProgram

    if selectedProgram == "lbcrEditor":
        lbcrEditorProgram.openFile()
    elif selectedProgram == "mdlBin":
        mdlBinProgram.openFile()
    elif selectedProgram == "mdlinfo":
        mdlinfoProgram.openFile()
    elif selectedProgram == "comicscript":
        comicscriptProgram.openFile()
    elif selectedProgram == "musicEditor":
        musicEditorProgram.openFile()
    elif selectedProgram == "fvtMaker":
        fvtMakerProgram.openFile()
    elif selectedProgram == "railEditor":
        railEditorProgram.openFile(v_railCsvRadio.get(), v_ambCsvRadio.get())
    else:
        mb.showerror(title="エラー", message="プログラムを選択してください")


def add_railCsvOptionMenu():
    global config_ini_path
    global configRead
    global v_railCsvRadio
    global v_ambCsvRadio
    global menubar

    if not os.path.exists(config_ini_path):
        writeDefaultConfig()

    configRead = configparser.ConfigParser()
    configRead.read(config_ini_path, encoding="utf-8")

    if menubar.entryconfig(tkinter.END) == menubar.entryconfig(2):
        v_railCsvRadio = tkinter.IntVar()
        v_railCsvRadio.set(int(configRead.get("RAIL_CSV", "mode")))
        v_ambCsvRadio = tkinter.IntVar()
        v_ambCsvRadio.set(int(configRead.get("AMB_CSV", "mode")))
        railCsvOptionMenu = tkinter.Menu(menubar, tearoff=False)
        railCsvOptionMenu.add_radiobutton(label="レールCSVを常に確認", variable=v_railCsvRadio, value=0, command=writeConfig)
        railCsvOptionMenu.add_radiobutton(label="レールCSVを常に上書きする", variable=v_railCsvRadio, value=1, command=writeConfig)
        railCsvOptionMenu.add_radiobutton(label="レールCSVを上書きしない", variable=v_railCsvRadio, value=2, command=writeConfig)
        railCsvOptionMenu.add_separator()
        railCsvOptionMenu.add_radiobutton(label="AMBのCSVを常に確認", variable=v_ambCsvRadio, value=0, command=writeConfig)
        railCsvOptionMenu.add_radiobutton(label="AMBのCSVを常に上書きする", variable=v_ambCsvRadio, value=1, command=writeConfig)
        railCsvOptionMenu.add_radiobutton(label="AMBのCSVを上書きしない", variable=v_ambCsvRadio, value=2, command=writeConfig)
        menubar.add_cascade(label="CSVオプション", menu=railCsvOptionMenu)


def delete_railCsvOptionMenu():
    global menubar

    menubar.delete(3)


def writeDefaultConfig():
    global config_ini_path

    config = configparser.RawConfigParser()
    config.add_section("RAIL_CSV")
    config.set("RAIL_CSV", "mode", 0)
    config.add_section("AMB_CSV")
    config.set("AMB_CSV", "mode", 0)
    f = codecs.open(config_ini_path, "w", "utf-8", "strict")
    config.write(f)
    f.close()


def writeConfig():
    global v_railCsvRadio
    global v_ambCsvRadio
    global config_ini_path
    global configRead

    configRead.set("RAIL_CSV", "mode", str(v_railCsvRadio.get()))
    configRead.set("AMB_CSV", "mode", str(v_ambCsvRadio.get()))

    config = configparser.RawConfigParser()
    config.add_section("RAIL_CSV")
    config.set("RAIL_CSV", "mode", int(configRead.get("RAIL_CSV", "mode")))
    config.add_section("AMB_CSV")
    config.set("AMB_CSV", "mode", int(configRead.get("AMB_CSV", "mode")))
    f = codecs.open(config_ini_path, "w", "utf-8", "strict")
    config.write(f)
    f.close()


config_ini_path = "config.ini"
configRead = None
v_railCsvRadio = None
v_ambCsvRadio = None
selectedProgram = None

root = tkinter.Tk()
root.title("電車でD 改造 統合版 1.0.2")
root.geometry("1024x768")

menubar = tkinter.Menu(root)

v_prog = tkinter.IntVar()

progmenu = tkinter.Menu(menubar, tearoff=False)
progmenu.add_radiobutton(label="車両性能", value=1, variable=v_prog, command=lambda: callProgram("lbcrEditor"))
progmenu.add_radiobutton(label="モデルバイナリ", value=2, variable=v_prog, command=lambda: callProgram("mdlBin"))
progmenu.add_radiobutton(label="MDLINFO", value=3, variable=v_prog, command=lambda: callProgram("mdlinfo"))
progmenu.add_separator()
progmenu.add_radiobutton(label="コミックスクリプト", value=4, variable=v_prog, command=lambda: callProgram("comicscript"))
progmenu.add_radiobutton(label="BGMリスト", value=5, variable=v_prog, command=lambda: callProgram("musicEditor"))
progmenu.add_radiobutton(label="FVT作成", value=6, variable=v_prog, command=lambda: callProgram("fvtMaker"))
progmenu.add_separator()
progmenu.add_radiobutton(label="レールエディター", value=7, variable=v_prog, command=lambda: callProgram("railEditor"))
progmenu.add_separator()
progmenu.add_radiobutton(label="終了", value=8, variable=v_prog, command=sys.exit)

filemenu = tkinter.Menu(menubar, tearoff=False)
filemenu.add_command(label="ファイルを開く", command=loadFile)

menubar.add_cascade(label="改造プログラム", menu=progmenu)
menubar.add_cascade(label="ファイル", menu=filemenu)

root.config(menu=menubar)

programFrame = ttk.Frame(root)
programFrame.pack(fill=tkinter.BOTH, expand=True)

if not os.path.exists(config_ini_path):
    writeDefaultConfig()

root.mainloop()
