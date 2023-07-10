import os
import copy
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from program.cmdList import cmdList

from program.comicscript.importPy.tkinterScrollbarTreeviewComicscript import ScrollbarTreeviewComicscript
from program.comicscript.importPy.tkinterEditClass import InputDialog, PasteDialog, HeaderFileInfo
from program.comicscript.importPy.decrypt import ComicDecrypt

root = None
v_fileName = None
v_select = None
v_btnList = []
decryptFile = None
scriptLf = None
frame = None
copyComicData = None


def openFile():
    global v_fileName
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[("COMIC_SCRIPT", "*.BIN")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのコミックスクリプトではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            del decryptFile
            decryptFile = ComicDecrypt(file_path, cmdList)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return
            deleteWidget()
            createWidget()
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def createWidget():
    global v_select
    global v_btnList
    global scriptLf
    global decryptFile
    global frame

    btnList = [
        v_btnList[0],
        v_btnList[1],
        v_btnList[2],
        v_btnList[3],
        v_btnList[5],
        v_btnList[6],
        v_btnList[7]
    ]
    frame = ScrollbarTreeviewComicscript(scriptLf, v_select, btnList)

    col_tuple = ('番号', 'コマンド名')
    paramList = []
    for i in range(decryptFile.max_param):
        paramList.append("param{0}".format(i+1))
    col_tuple = col_tuple + tuple(paramList)

    frame.tree['columns'] = col_tuple
    frame.tree.column('#0', width=0, stretch=False)

    frame.tree.column('番号', anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column('コマンド名', anchor=tkinter.CENTER, width=150, minwidth=150)
    frame.tree.heading('番号', text='番号', anchor=tkinter.CENTER)
    frame.tree.heading('コマンド名', text='コマンド名', anchor=tkinter.CENTER)

    for i in range(decryptFile.max_param):
        col_name = "param{0}".format(i+1)
        frame.tree.column(col_name, anchor=tkinter.CENTER, width=100, minwidth=100)
        frame.tree.heading(col_name, text=col_name, anchor=tkinter.CENTER)

    num = 0
    for comicData in decryptFile.comicDataList:
        data = (num, comicData[0])
        paramCnt = comicData[1]
        paramList = []
        for i in range(paramCnt):
            paramList.append(comicData[2+i])
        data = data + tuple(paramList)
        frame.tree.insert(parent='', index='end', iid=num, values=data)
        num += 1
    return num


def deleteWidget():
    global v_select
    global v_btnList
    global scriptLf

    children = scriptLf.winfo_children()
    for child in children:
        child.destroy()

    v_select.set("")
    v_btnList[0]["state"] = "disabled"
    v_btnList[1]["state"] = "disabled"
    v_btnList[2]["state"] = "disabled"


def editLine():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "コマンド修正", decryptFile, int(selectItem["番号"]), selectItem)
    if result.reloadFlag:
        reloadFile()


def insertLine():
    global root
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "コマンド挿入", decryptFile, int(selectItem["番号"]))
    if result.reloadFlag:
        reloadFile()


def deleteLine():
    global frame
    selectId = int(frame.tree.selection()[0])
    warnMsg = "選択した行を削除します。\nそれでもよろしいですか？"
    result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")
    if result:
        if not decryptFile.saveFile("delete", selectId, None):
            decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="スクリプトを改造しました")
        reloadFile()


def copyLine():
    global v_btnList
    global frame
    global copyComicData
    comicData = []
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    comicData.append(selectItem["コマンド名"])
    paramCnt = len(selectItem)-2
    comicData.append(paramCnt)
    for i in range(paramCnt):
        f = float(selectItem["param{0}".format(i+1)])
        comicData.append(f)
    copyComicData = copy.deepcopy(comicData)

    mb.showinfo(title="成功", message="コピーしました")
    v_btnList[4]["state"] = "normal"


def pasteLine():
    global root
    global decryptFile
    global frame
    global copyComicData
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])
    result = PasteDialog(root, "コマンドコピー", decryptFile, num, copyComicData)
    if result.reloadFlag:
        reloadFile()


def reloadFile():
    global v_select
    global decryptFile
    global frame

    errorMsg = "予想外のエラーが出ました。\n電車でDのコミックスクリプトではない、またはファイルが壊れた可能性があります。"
    if decryptFile.filePath:
        try:
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return

            selectId = None
            if v_select.get() != "":
                selectId = int(v_select.get())

            deleteWidget()
            maxIndex = createWidget()
            if selectId is not None:
                if selectId >= maxIndex:
                    selectId = maxIndex - 1
                if selectId - 3 < 0:
                    frame.tree.see(0)
                else:
                    frame.tree.see(selectId - 3)
                frame.tree.selection_set(selectId)
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def csvExtract():
    global v_fileName
    global decryptFile
    file = v_fileName.get()
    filename = os.path.splitext(os.path.basename(file))[0]
    file_path = fd.asksaveasfilename(initialfile=filename, defaultextension='csv', filetypes=[('comicscript_csv', '*.csv')])
    errorMsg = "CSVで取り出す機能が失敗しました。\n権限問題の可能性があります。"
    if file_path:
        try:
            w = open(file_path, "w")
            for comicData in decryptFile.comicDataList:
                w.write("{0},".format(comicData[0]))
                cmdParaCnt = comicData[1]
                for i in range(cmdParaCnt):
                    w.write("{0}".format(comicData[2 + i]))
                    if i < cmdParaCnt-1:
                        w.write(",")
                w.write("\n")
            w.close()
            mb.showinfo(title="成功", message="CSVで取り出しました")
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def csvLoadAndSave():
    global decryptFile
    file_path = fd.askopenfilename(defaultextension='csv', filetypes=[("comicscript_csv", "*.csv")])
    if not file_path:
        return
    f = open(file_path)
    csvLines = f.readlines()
    f.close()

    csvComicDataList = []
    for i in range(len(csvLines)):
        csvComicData = []
        csvLine = csvLines[i].strip()
        arr = csvLine.split(",")
        cmdName = arr[0]
        if cmdName not in cmdList:
            errorMsg = "{0}行目のコマンド[{1}]は\n存在しないコマンドです".format(i+1, cmdName)
            mb.showerror(title="エラー", message=errorMsg)
            return

        comicDataParaList = []
        for j in range(1, len(arr)):
            if arr[j] == "":
                break
            try:
                comicDataParaList.append(float(arr[j]))
            except Exception:
                w = open("error.log", "a")
                w.write(traceback.format_exc())
                w.close()
                errorMsg = "{0}行目のコマンドに\n数字に変換できない要素[{1}]が入ってます".format(i+1, arr[j])
                mb.showerror(title="エラー", message=errorMsg)
                return

        csvComicData.append(cmdName)
        cmdParaCnt = len(comicDataParaList)
        csvComicData.append(cmdParaCnt)
        for j in range(len(comicDataParaList)):
            csvComicData.append(comicDataParaList[j])

        csvComicDataList.append(csvComicData)
    warnMsg = "選択したCSVで上書きします。\nそれでもよろしいですか？"
    result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")

    if result:
        if not decryptFile.saveComicList(csvComicDataList):
            decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="スクリプトを改造しました")
        reloadFile()


def headerFileEdit():
    global root
    global decryptFile
    result = HeaderFileInfo(root, "ヘッダー情報", decryptFile)
    if result.reloadFlag:
        reloadFile()


def call_comicscript(rootTk, programFrame):
    global root
    global v_fileName
    global v_select
    global v_btnList
    global scriptLf
    root = rootTk

    v_fileName = tkinter.StringVar()
    fileNameEt = ttk.Entry(programFrame, textvariable=v_fileName, font=("", 14), width=23, state="readonly", justify="center")
    fileNameEt.place(relx=0.053, rely=0.03)

    selectLb = ttk.Label(programFrame, text="選択した行番号：", font=("", 14))
    selectLb.place(relx=0.05, rely=0.09)

    v_select = tkinter.StringVar()
    selectEt = ttk.Entry(programFrame, textvariable=v_select, font=("", 14), width=6, state="readonly", justify="center")
    selectEt.place(relx=0.22, rely=0.09)

    buttonWidth = 25

    v_btnList = []

    editLineBtn = ttk.Button(programFrame, text="選択した行を修正する", width=buttonWidth, state="disabled", command=editLine)
    editLineBtn.place(relx=0.43, rely=0.03)
    v_btnList.append(editLineBtn)

    insertLineBtn = ttk.Button(programFrame, text="選択した行に挿入する", width=buttonWidth, state="disabled", command=insertLine)
    insertLineBtn.place(relx=0.62, rely=0.03)
    v_btnList.append(insertLineBtn)

    deleteLineBtn = ttk.Button(programFrame, text="選択した行を削除する", width=buttonWidth, state="disabled", command=deleteLine)
    deleteLineBtn.place(relx=0.81, rely=0.03)
    v_btnList.append(deleteLineBtn)

    copyLineBtn = ttk.Button(programFrame, text="選択した行をコピーする", width=buttonWidth, state="disabled", command=copyLine)
    copyLineBtn.place(relx=0.43, rely=0.09)
    v_btnList.append(copyLineBtn)

    pasteLineBtn = ttk.Button(programFrame, text="選択した行に貼り付けする", width=buttonWidth, state="disabled", command=pasteLine)
    pasteLineBtn.place(relx=0.62, rely=0.09)
    v_btnList.append(pasteLineBtn)

    csvExtractBtn = ttk.Button(programFrame, text="CSVで取り出す", width=buttonWidth, state="disabled", command=csvExtract)
    csvExtractBtn.place(relx=0.43, rely=0.15)
    v_btnList.append(csvExtractBtn)

    csvLoadAndSaveBtn = ttk.Button(programFrame, text="CSVで上書きする", width=buttonWidth, state="disabled", command=csvLoadAndSave)
    csvLoadAndSaveBtn.place(relx=0.62, rely=0.15)
    v_btnList.append(csvLoadAndSaveBtn)

    headerFileEditBtn = ttk.Button(programFrame, text="ヘッダー情報を修正する", width=buttonWidth, state="disabled", command=headerFileEdit)
    headerFileEditBtn.place(relx=0.81, rely=0.15)
    v_btnList.append(headerFileEditBtn)

    scriptLf = ttk.LabelFrame(programFrame, text="スクリプト内容")
    scriptLf.place(relx=0.03, rely=0.20, relwidth=0.95, relheight=0.77)
