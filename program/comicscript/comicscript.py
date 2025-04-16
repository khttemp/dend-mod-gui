import os
import copy
import codecs
import traceback
import sys
import requests
import json
import re

import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

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
rootFrameAppearance = None
copyComicData = None


def resource_path(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(os.path.abspath(os.path.dirname(__file__)), "importPy"))
    return os.path.join(bundle_dir, relative_path)


def openFile(comicCheck):
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
            createWidget(comicCheck)
        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def createWidget(comicCheck):
    global v_select
    global v_btnList
    global scriptLf
    global decryptFile
    global frame

    game = textSetting.textList["menu"]["comicscript"]["gameList"][comicCheck]
    cmdJsonInfo = None
    try:
        url = "https://raw.githubusercontent.com/khttemp/dendData/refs/heads/main/comicscript/js/cmd.json"
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            cmdJsonInfo = json.loads(response.text)
    except Exception:
        pass

    if cmdJsonInfo is None:
        f = codecs.open(resource_path("cmd.json"), "r", "utf-8", "strict")
        cmdJsonInfo = json.load(f)
        f.close()

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

        description = cmdJsonInfo[comicData[0]]["description"]
        availableList = re.findall(r"【.*?】", description)[0]
        if game not in availableList:
            tags = "notAvailable"
        else:
            tags = "available"
        frame.tree.insert(parent="", index="end", iid=num, values=data, tags=tags)
        num += 1

    frame.tree.tag_configure("notAvailable", background="#666666", foreground="red")

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
    global rootFrameAppearance
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, textSetting.textList["comicscript"]["cmdModify"], decryptFile, rootFrameAppearance, int(selectItem["treeNum"]), selectItem)
    if result.reloadFlag:
        reloadFile()


def insertLine():
    global root
    global rootFrameAppearance
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, textSetting.textList["comicscript"]["cmdInsert"], decryptFile, rootFrameAppearance, int(selectItem["treeNum"]))
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
    global rootFrameAppearance
    global decryptFile
    global frame
    global copyComicData
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"])
    result = PasteDialog(root, textSetting.textList["comicscript"]["cmdPaste"], decryptFile, rootFrameAppearance, num, copyComicData)
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
    global rootFrameAppearance
    global decryptFile
    result = HeaderFileInfo(root, textSetting.textList["comicscript"]["headerInfo"], decryptFile, rootFrameAppearance)
    if result.reloadFlag:
        reloadFile()


def call_comicscript(rootTk, appearance):
    global root
    global v_fileName
    global v_select
    global v_btnList
    global scriptLf
    global rootFrameAppearance
    root = rootTk
    rootFrameAppearance = appearance

    headerFrame = ttkCustomWidget.CustomTtkFrame(root)
    headerFrame.pack(fill=tkinter.BOTH, padx=40, pady=(20, 0))

    selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
    selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

    v_fileName = tkinter.StringVar()
    fileNameEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
    fileNameEt.grid(columnspan=5, row=0, column=0, pady=(0, 15), sticky=tkinter.EW)

    selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["comicscript"]["selectNum"], font=textSetting.textList["font2"])
    selectLb.grid(columnspan=4, row=1, column=0, pady=(0, 15), sticky=tkinter.EW)

    v_select = tkinter.StringVar()
    selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
    selectEt.grid(row=1, column=4, pady=(0, 15), sticky=tkinter.E)

    btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
    btnFrame.pack(fill=tkinter.BOTH, padx=(120, 0))

    buttonWidth = 25
    v_btnList = []

    editLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["editLineLabel"], width=buttonWidth, state="disabled", command=editLine)
    editLineBtn.grid(row=0, column=0, padx=10, pady=(0, 20))
    v_btnList.append(editLineBtn)

    insertLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["insertLineLabel"], width=buttonWidth, state="disabled", command=insertLine)
    insertLineBtn.grid(row=0, column=1, padx=10, pady=(0, 20))
    v_btnList.append(insertLineBtn)

    deleteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["deleteLineLabel"], width=buttonWidth, state="disabled", command=deleteLine)
    deleteLineBtn.grid(row=0, column=2, padx=10, pady=(0, 20))
    v_btnList.append(deleteLineBtn)

    copyLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["copyLineLabel"], width=buttonWidth, state="disabled", command=copyLine)
    copyLineBtn.grid(row=1, column=0, padx=10, pady=(0, 20))
    v_btnList.append(copyLineBtn)

    pasteLineBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["pasteLineLabel"], width=buttonWidth, state="disabled", command=pasteLine)
    pasteLineBtn.grid(row=1, column=1, padx=10, pady=(0, 20))
    v_btnList.append(pasteLineBtn)

    csvExtractBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["csvExtractLabel"], width=buttonWidth, state="disabled", command=csvExtract)
    csvExtractBtn.grid(row=2, column=0, padx=10, pady=(0, 20))
    v_btnList.append(csvExtractBtn)

    csvLoadAndSaveBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["csvSaveLabel"], width=buttonWidth, state="disabled", command=csvLoadAndSave)
    csvLoadAndSaveBtn.grid(row=2, column=1, padx=10, pady=(0, 20))
    v_btnList.append(csvLoadAndSaveBtn)

    headerFileEditBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["comicscript"]["headerEditLabel"], width=buttonWidth, state="disabled", command=headerFileEdit)
    headerFileEditBtn.grid(row=2, column=2, padx=10, pady=(0, 20))
    v_btnList.append(headerFileEditBtn)

    btnFrame.grid_columnconfigure(0, weight=1)
    btnFrame.grid_columnconfigure(1, weight=1)
    btnFrame.grid_columnconfigure(2, weight=1)

    scriptLf = ttkCustomWidget.CustomTtkLabelFrame(root, text=textSetting.textList["comicscript"]["scriptLabel"])
    scriptLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))
