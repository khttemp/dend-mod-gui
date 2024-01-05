import os
import copy
import codecs
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting

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
    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["comicscript"]["fileType"], "*.BIN")])

    errorMsg = textSetting.textList["errorList"]["E6"]
    if file_path:
        try:
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            del decryptFile
            decryptFile = ComicDecrypt(file_path, cmdList)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            deleteWidget()
            createWidget()
        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


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

    col_tuple = (
        "treeNum",
        "comicScriptName"
    )
    paramList = []
    for i in range(decryptFile.max_param):
        paramList.append(textSetting.textList["comicscript"]["paramNumLabel"].format(i+1))
    col_tuple = col_tuple + tuple(paramList)

    frame.tree["columns"] = col_tuple
    frame.tree.column("#0", width=0, stretch=False)

    frame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column("comicScriptName", anchor=tkinter.CENTER, width=150, minwidth=150)
    frame.tree.heading("treeNum", text=textSetting.textList["comicscript"]["treeNum"], anchor=tkinter.CENTER)
    frame.tree.heading("comicScriptName", text=textSetting.textList["comicscript"]["treeName"], anchor=tkinter.CENTER)

    for i in range(decryptFile.max_param):
        col_name = textSetting.textList["comicscript"]["paramNumLabel"].format(i+1)
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
        frame.tree.insert(parent="", index="end", iid=num, values=data)
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
    v_btnList[3]["state"] = "disabled"


def editLine():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, textSetting.textList["comicscript"]["cmdModify"], decryptFile, int(selectItem["treeNum"]), selectItem)
    if result.reloadFlag:
        reloadFile()


def insertLine():
    global root
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, textSetting.textList["comicscript"]["cmdInsert"], decryptFile, int(selectItem["treeNum"]))
    if result.reloadFlag:
        reloadFile()


def deleteLine():
    global frame
    selectId = int(frame.tree.selection()[0])
    warnMsg = textSetting.textList["infoList"]["I9"]
    result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
    if result:
        if not decryptFile.saveFile("delete", selectId, None):
            decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
        reloadFile()


def copyLine():
    global v_btnList
    global frame
    global copyComicData
    comicData = []
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    comicData.append(selectItem["comicScriptName"])
    paramCnt = len(selectItem)-2
    comicData.append(paramCnt)
    for i in range(paramCnt):
        f = float(selectItem[textSetting.textList["comicscript"]["paramNumLabel"].format(i+1)])
        comicData.append(f)
    copyComicData = copy.deepcopy(comicData)

    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
    v_btnList[4]["state"] = "normal"


def pasteLine():
    global root
    global decryptFile
    global frame
    global copyComicData
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"])
    result = PasteDialog(root, textSetting.textList["comicscript"]["cmdPaste"], decryptFile, num, copyComicData)
    if result.reloadFlag:
        reloadFile()


def reloadFile():
    global v_select
    global decryptFile
    global frame

    errorMsg = textSetting.textList["errorList"]["E6"]
    if decryptFile.filePath:
        try:
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
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
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def csvExtract():
    global v_fileName
    global decryptFile
    file = v_fileName.get()
    filename = os.path.splitext(os.path.basename(file))[0]
    file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("comicscript_csv", "*.csv")])
    errorMsg = textSetting.textList["errorList"]["E7"]
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
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def csvLoadAndSave():
    global decryptFile
    file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("comicscript_csv", "*.csv")])
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
            errorMsg = textSetting.textList["errorList"]["E8"].format(i+1, cmdName)
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        comicDataParaList = []
        for j in range(1, len(arr)):
            if arr[j] == "":
                break
            try:
                comicDataParaList.append(float(arr[j]))
            except Exception:
                w = codecs.open("error.log", "a", "utf-8", "strict")
                w.write(traceback.format_exc())
                w.close()
                errorMsg = textSetting.textList["errorList"]["E9"].format(i+1, arr[j])
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

        csvComicData.append(cmdName)
        cmdParaCnt = len(comicDataParaList)
        csvComicData.append(cmdParaCnt)
        for j in range(len(comicDataParaList)):
            csvComicData.append(comicDataParaList[j])

        csvComicDataList.append(csvComicData)
    warnMsg = textSetting.textList["infoList"]["I11"]
    result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")

    if result:
        if not decryptFile.saveComicList(csvComicDataList):
            decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
        reloadFile()


def headerFileEdit():
    global root
    global decryptFile
    result = HeaderFileInfo(root, textSetting.textList["comicscript"]["headerInfo"], decryptFile)
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
    fileNameEt = ttk.Entry(programFrame, textvariable=v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
    fileNameEt.place(relx=0.053, rely=0.03)

    selectLb = ttk.Label(programFrame, text=textSetting.textList["comicscript"]["selectNum"], font=textSetting.textList["font2"])
    selectLb.place(relx=0.05, rely=0.09)

    v_select = tkinter.StringVar()
    selectEt = ttk.Entry(programFrame, textvariable=v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
    selectEt.place(relx=0.22, rely=0.09)

    buttonWidth = 25

    v_btnList = []

    editLineBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["editLineLabel"], width=buttonWidth, state="disabled", command=editLine)
    editLineBtn.place(relx=0.43, rely=0.03)
    v_btnList.append(editLineBtn)

    insertLineBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["insertLineLabel"], width=buttonWidth, state="disabled", command=insertLine)
    insertLineBtn.place(relx=0.62, rely=0.03)
    v_btnList.append(insertLineBtn)

    deleteLineBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["deleteLineLabel"], width=buttonWidth, state="disabled", command=deleteLine)
    deleteLineBtn.place(relx=0.81, rely=0.03)
    v_btnList.append(deleteLineBtn)

    copyLineBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["copyLineLabel"], width=buttonWidth, state="disabled", command=copyLine)
    copyLineBtn.place(relx=0.43, rely=0.09)
    v_btnList.append(copyLineBtn)

    pasteLineBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["pasteLineLabel"], width=buttonWidth, state="disabled", command=pasteLine)
    pasteLineBtn.place(relx=0.62, rely=0.09)
    v_btnList.append(pasteLineBtn)

    csvExtractBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["csvExtractLabel"], width=buttonWidth, state="disabled", command=csvExtract)
    csvExtractBtn.place(relx=0.43, rely=0.15)
    v_btnList.append(csvExtractBtn)

    csvLoadAndSaveBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["csvSaveLabel"], width=buttonWidth, state="disabled", command=csvLoadAndSave)
    csvLoadAndSaveBtn.place(relx=0.62, rely=0.15)
    v_btnList.append(csvLoadAndSaveBtn)

    headerFileEditBtn = ttk.Button(programFrame, text=textSetting.textList["comicscript"]["headerEditLabel"], width=buttonWidth, state="disabled", command=headerFileEdit)
    headerFileEditBtn.place(relx=0.81, rely=0.15)
    v_btnList.append(headerFileEditBtn)

    scriptLf = ttk.LabelFrame(programFrame, text=textSetting.textList["comicscript"]["scriptLabel"])
    scriptLf.place(relx=0.03, rely=0.20, relwidth=0.95, relheight=0.77)
