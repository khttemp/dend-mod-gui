import os
import copy
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from program.cmdList import cmdList

from program.mdlBin.importPy.tkinterScrollbarTreeviewMdlBin import ScrollbarTreeviewMdlBin
from program.mdlBin.importPy.tkinterEditClass import InputDialog, PasteDialog, HeaderDialog, ListNumModifyDialog, ListHeaderModifyDialog, NumModifyDialog
from program.mdlBin.importPy.decrypt import MdlBinDecrypt

root = None
v_fileName = None
v_select = None
editLineBtn = None
insertLineBtn = None
deleteLineBtn = None
copyLineBtn = None
pasteLineBtn = None
headerFileEditBtn = None
listNumModifyBtn = None
listHeadeModifyBtn = None
numModifyBtn = None
csvExtractBtn = None
csvLoadAndSaveBtn = None
scriptLf = None
decryptFile = None
frame = None
copyScriptData = None


def openFile():
    global v_fileName
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[("MODEL_SCRIPT", "*.BIN")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのモデルバイナリではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            del decryptFile
            decryptFile = None

            decryptFile = MdlBinDecrypt(file_path, cmdList)
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


def deleteWidget():
    global v_select
    global editLineBtn
    global insertLineBtn
    global deleteLineBtn
    global headerFileEditBtn
    global scriptLf

    children = scriptLf.winfo_children()
    for child in children:
        child.destroy()

    v_select.set("")
    editLineBtn['state'] = 'disabled'
    insertLineBtn['state'] = 'disabled'
    deleteLineBtn['state'] = 'disabled'
    headerFileEditBtn['state'] = 'disabled'


def createWidget():
    global v_select
    global editLineBtn
    global insertLineBtn
    global deleteLineBtn
    global copyLineBtn
    global headerFileEditBtn
    global listNumModifyBtn
    global listHeadeModifyBtn
    global numModifyBtn
    global csvExtractBtn
    global csvLoadAndSaveBtn
    global scriptLf
    global decryptFile
    global frame

    btnList = [
        editLineBtn,
        insertLineBtn,
        deleteLineBtn,
        copyLineBtn,
        listNumModifyBtn,
        listHeadeModifyBtn,
        numModifyBtn
    ]
    headerFileEditBtn['state'] = 'normal'
    csvExtractBtn['state'] = 'normal'
    csvLoadAndSaveBtn['state'] = 'normal'
    frame = ScrollbarTreeviewMdlBin(scriptLf, v_select, btnList)

    col_tuple = ('番号', 'delay', 'コマンド名', 'ファイルフラグ', 'セクション')
    paramList = []
    for i in range(decryptFile.max_param):
        paramList.append("param{0}".format(i + 1))
    col_tuple = col_tuple + tuple(paramList)

    frame.tree['columns'] = col_tuple

    frame.tree.column('#0', width=0, stretch=False)
    frame.tree.column('番号', anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column('delay', anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column('コマンド名', anchor=tkinter.CENTER, width=150, minwidth=150)
    frame.tree.column('ファイルフラグ', stretch=False)
    frame.tree.column('セクション', stretch=False)
    for i in range(decryptFile.max_param):
        col_name = "param{0}".format(i + 1)
        frame.tree.column(col_name, anchor=tkinter.CENTER, width=100, minwidth=100)

    displayList = []

    frame.tree.heading('番号', text='番号', anchor=tkinter.CENTER)
    frame.tree.heading('delay', text='delay', anchor=tkinter.CENTER)
    frame.tree.heading('コマンド名', text='コマンド名', anchor=tkinter.CENTER)
    for i in range(decryptFile.max_param):
        col_name = "param{0}".format(i + 1)
        displayList.append(col_name)
        frame.tree.heading(col_name, text=col_name, anchor=tkinter.CENTER)

    frame.tree["displaycolumns"] = ["番号", "delay", "コマンド名"]
    frame.tree["displaycolumns"] += tuple(displayList)

    index = 0
    num = 0
    sectionNum = 0
    for scriptDataInfoList in decryptFile.scriptDataAllInfoList:
        listNum = 0
        for scriptDataInfo in scriptDataInfoList:
            headerInfo = (index, "-", "---#{0}, {1}#---".format(num, listNum), "-", "{0},{1},{2}".format(num, listNum, sectionNum))
            headerInfo += (",".join(str(n) for n in scriptDataInfo[0]), )
            frame.tree.insert(parent='', index='end', iid=index, values=headerInfo)
            index += 1
            sectionNum = 1
            for scriptData in scriptDataInfo[1:]:
                data = (index, scriptData[0], cmdList[scriptData[1]], scriptData[3], "{0},{1},{2}".format(num, listNum, sectionNum))
                paramCnt = scriptData[2]
                paramList = []
                for i in range(paramCnt):
                    paramList.append(scriptData[4 + i])
                data = data + tuple(paramList)
                frame.tree.insert(parent='', index='end', iid=index, values=data)
                index += 1
                sectionNum += 1
            listNum += 1
            sectionNum = 0
        num += 1
    return index


def editLine():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "コマンド修正", decryptFile, cmdList, int(selectItem["番号"]), selectItem["セクション"], selectItem)
    if result.reloadFlag:
        reloadFile()


def insertLine():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "コマンド挿入", decryptFile, cmdList, int(selectItem["番号"]), selectItem["セクション"])
    if result.reloadFlag:
        reloadFile()


def deleteLine():
    global decryptFile
    global frame
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    warnMsg = "選択した行を削除します。\nそれでもよろしいですか？"
    result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")
    if result:
        sectionList = selectItem["セクション"].split(",")
        num = int(sectionList[0])
        listNum = int(sectionList[1])
        cmdDiff = int(sectionList[2])
        if not decryptFile.saveFile(num, listNum, cmdDiff, "delete"):
            decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
        mb.showinfo(title="成功", message="スクリプトを改造しました")
        reloadFile()


def copyLine():
    global pasteLineBtn
    global frame
    global copyScriptData

    scriptData = []
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    scriptData.append(int(selectItem["delay"]))
    scriptData.append(cmdList.index(selectItem["コマンド名"]))
    paramCnt = len(selectItem) - 5
    scriptData.append(paramCnt)
    scriptData.append(int(selectItem["ファイルフラグ"]))
    for i in range(paramCnt):
        try:
            temp = float(selectItem["param{0}".format(i + 1)])
        except Exception:
            temp = selectItem["param{0}".format(i + 1)]
        scriptData.append(temp)
    copyScriptData = copy.deepcopy(scriptData)

    mb.showinfo(title="成功", message="コピーしました")
    pasteLineBtn['state'] = 'normal'


def pasteLine():
    global root
    global decryptFile
    global frame
    global copyScriptData
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])
    result = PasteDialog(root, "コマンド貼り付け", decryptFile, cmdList, num, selectItem["セクション"], copyScriptData)
    if result.reloadFlag:
        reloadFile()


def headerFileEdit():
    global root
    global decryptFile
    global frame
    result = HeaderDialog(root, "ヘッダー情報", decryptFile)
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

            selectId = -1
            if v_select.get() != "":
                selectId = int(v_select.get())
            deleteWidget()
            maxIndex = createWidget()
            if selectId >= maxIndex:
                selectId = maxIndex - 1

            if selectId - 3 < 0:
                frame.tree.see(0)
            else:
                frame.tree.see(selectId - 3)

            if selectId >= 0:
                frame.tree.selection_set(selectId)
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def listNumModify():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    arr = selectItem["コマンド名"].split(", ")
    num = arr[0].strip("-").strip("#")

    scriptDataInfoList = decryptFile.scriptDataAllInfoList[int(num)]
    result = ListNumModifyDialog(root, "セクションの数変更", decryptFile, num, len(scriptDataInfoList))
    if result.reloadFlag:
        reloadFile()


def listHeadeModify():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    arr = selectItem["コマンド名"].split(", ")
    num = arr[0].strip("-").strip("#")
    listNum = arr[1].strip("-").strip("#")
    headerInfo = [int(n) for n in selectItem["param1"].split(",")]

    result = ListHeaderModifyDialog(root, "セクションの内容変更", decryptFile, int(num), int(listNum), headerInfo)
    if result.reloadFlag:
        reloadFile()


def numModify():
    global root
    global decryptFile
    global frame

    scriptDataAllInfoList = decryptFile.scriptDataAllInfoList
    result = NumModifyDialog(root, "リストの数変更", decryptFile, len(scriptDataAllInfoList))
    if result.reloadFlag:
        reloadFile()


def csvExtract():
    global v_fileName
    global decryptFile

    file = v_fileName.get()
    filename = os.path.splitext(os.path.basename(file))[0]
    file_path = fd.asksaveasfilename(initialfile=filename, defaultextension='csv', filetypes=[('mdlbin_csv', '*.csv')])
    errorMsg = "CSVで取り出す機能が失敗しました。\n権限問題の可能性があります。"
    if file_path:
        try:
            w = open(file_path, "w")
            num = 0
            for scriptDataInfoList in decryptFile.scriptDataAllInfoList:
                listNum = 0
                for scriptDataInfo in scriptDataInfoList:
                    headerInfo = "#{0}-{1},".format(num, listNum)
                    headerInfo += ",".join(str(n) for n in scriptDataInfo[0])
                    headerInfo += "\n"
                    w.write(headerInfo)
                    for scriptData in scriptDataInfo[1:]:
                        data = "{0},{1},".format(scriptData[0], cmdList[scriptData[1]])
                        paramCnt = scriptData[2]
                        paramList = []
                        for i in range(paramCnt):
                            paramList.append(scriptData[4 + i])
                        data += ",".join(str(p) for p in paramList)
                        data += "\n"
                        w.write(data)
                    listNum += 1
                num += 1
            w.close()
            mb.showinfo(title="成功", message="CSVで取り出しました")
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def csvLoadAndSave():
    global decryptFile
    file_path = fd.askopenfilename(defaultextension='csv', filetypes=[("mdlbin_csv", "*.csv")])
    if not file_path:
        return
    f = open(file_path)
    csvLines = f.readlines()
    f.close()

    csvScriptDataAllInfoList = []
    csvScriptDataInfoList = []
    csvScriptDataInfo = []
    csvScriptData = []
    curNum = -1
    curListNum = -1
    for i in range(len(csvLines)):
        try:
            csvLine = csvLines[i].strip()
            arr = csvLine.split(",")

            if "#" in arr[0]:
                section = arr[0].strip("#").split("-")
                num = int(section[0])
                listNum = int(section[1])

                if curNum != num:
                    curNum = num
                    curListNum = listNum
                    csvScriptDataInfoList = []
                    csvScriptDataAllInfoList.append(csvScriptDataInfoList)
                    csvScriptDataInfo = []
                    csvScriptDataInfoList.append(csvScriptDataInfo)
                elif curListNum != listNum:
                    curListNum = listNum
                    csvScriptDataInfo = []
                    csvScriptDataInfoList.append(csvScriptDataInfo)
                csvScriptDataInfo.append(arr[1:])
                csvScriptData = []
                csvScriptDataInfo.append(csvScriptData)
            else:
                cmdName = arr[1]
                if cmdName not in cmdList:
                    errorMsg = "{0}行のコマンドは存在しません [{1}]".format(i + 1, cmdName)
                    mb.showerror(title="読み込みエラー", message=errorMsg)
                    return
                csvScriptData.append(arr)
        except Exception:
            errorMsg = "{0}行のデータを読み込み失敗しました。".format(i + 1)
            mb.showerror(title="読み込みエラー", message=errorMsg)
            return

    msg = "{0}行のデータを読み込みしました。\n上書きしますか？".format(i + 1)
    result = mb.askokcancel(title="警告", message=msg, icon="warning")

    if result:
        if not decryptFile.saveCsv(csvScriptDataAllInfoList):
            decryptFile.printError()
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            mb.showerror(title="保存エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="CSVで上書きしました")
        reloadFile()


def call_mdlBin(rootTk, programFrame):
    global root
    global v_fileName
    global v_select
    global editLineBtn
    global insertLineBtn
    global deleteLineBtn
    global copyLineBtn
    global pasteLineBtn
    global headerFileEditBtn
    global listNumModifyBtn
    global listHeadeModifyBtn
    global numModifyBtn
    global csvExtractBtn
    global csvLoadAndSaveBtn
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

    editLineBtn = ttk.Button(programFrame, text="選択した行を修正する", width=25, state="disabled", command=editLine)
    editLineBtn.place(relx=0.43, rely=0.03)

    insertLineBtn = ttk.Button(programFrame, text="選択した行に挿入する", width=25, state="disabled", command=insertLine)
    insertLineBtn.place(relx=0.62, rely=0.03)

    deleteLineBtn = ttk.Button(programFrame, text="選択した行を削除する", width=25, state="disabled", command=deleteLine)
    deleteLineBtn.place(relx=0.81, rely=0.03)

    copyLineBtn = ttk.Button(programFrame, text="選択した行をコピーする", width=25, state="disabled", command=copyLine)
    copyLineBtn.place(relx=0.43, rely=0.09)

    pasteLineBtn = ttk.Button(programFrame, text="選択した行に貼り付けする", width=25, state="disabled", command=pasteLine)
    pasteLineBtn.place(relx=0.62, rely=0.09)

    headerFileEditBtn = ttk.Button(programFrame, text="ヘッダー情報を修正する", width=25, state="disabled", command=headerFileEdit)
    headerFileEditBtn.place(relx=0.81, rely=0.09)

    listNumModifyBtn = ttk.Button(programFrame, text="セクションの数を修正する", width=25, state="disabled", command=listNumModify)
    listNumModifyBtn.place(relx=0.43, rely=0.15)

    listHeadeModifyBtn = ttk.Button(programFrame, text="セクションの内容を修正する", width=25, state="disabled", command=listHeadeModify)
    listHeadeModifyBtn.place(relx=0.62, rely=0.15)

    numModifyBtn = ttk.Button(programFrame, text="リストの数を修正する", width=25, state="disabled", command=numModify)
    numModifyBtn.place(relx=0.81, rely=0.15)

    csvExtractBtn = ttk.Button(programFrame, text="CSVで取り出す", width=25, state="disabled", command=csvExtract)
    csvExtractBtn.place(relx=0.05, rely=0.15)

    csvLoadAndSaveBtn = ttk.Button(programFrame, text="CSVで上書きする", width=25, state="disabled", command=csvLoadAndSave)
    csvLoadAndSaveBtn.place(relx=0.22, rely=0.15)

    scriptLf = ttk.LabelFrame(programFrame, text="スクリプト内容")
    scriptLf.place(relx=0.03, rely=0.20, relwidth=0.95, relheight=0.77)
