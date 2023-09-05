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
listHeaderModifyBtn = None
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
    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["mdlBin"]["fileType"], "*.BIN")])

    errorMsg = textSetting.textList["errorList"]["E6"]
    if file_path:
        try:
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            del decryptFile
            decryptFile = None

            decryptFile = MdlBinDecrypt(file_path, cmdList)
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
    editLineBtn["state"] = "disabled"
    insertLineBtn["state"] = "disabled"
    deleteLineBtn["state"] = "disabled"
    headerFileEditBtn["state"] = "disabled"


def createWidget():
    global v_select
    global editLineBtn
    global insertLineBtn
    global deleteLineBtn
    global copyLineBtn
    global headerFileEditBtn
    global listNumModifyBtn
    global listHeaderModifyBtn
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
        listHeaderModifyBtn,
        numModifyBtn
    ]
    headerFileEditBtn["state"] = "normal"
    csvExtractBtn["state"] = "normal"
    csvLoadAndSaveBtn["state"] = "normal"
    frame = ScrollbarTreeviewMdlBin(scriptLf, v_select, btnList)

    col_tuple = (
        "treeNum",
        "treeDelay",
        "treeName",
        "treeFileFlag",
        "treeSection"
    )
    paramList = []
    for i in range(decryptFile.max_param):
        paramList.append(textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1))
    col_tuple = col_tuple + tuple(paramList)

    frame.tree["columns"] = col_tuple

    frame.tree.column("#0", width=0, stretch=False)
    frame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column("treeDelay", anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column("treeName", anchor=tkinter.CENTER, width=150, minwidth=150)
    frame.tree.column("treeFileFlag", stretch=False)
    frame.tree.column("treeSection", stretch=False)
    for i in range(decryptFile.max_param):
        col_name = textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)
        frame.tree.column(col_name, anchor=tkinter.CENTER, width=100, minwidth=100)

    displayList = []

    frame.tree.heading("treeNum", text=textSetting.textList["mdlBin"]["treeNum"], anchor=tkinter.CENTER)
    frame.tree.heading("treeDelay", text=textSetting.textList["mdlBin"]["treeDelay"], anchor=tkinter.CENTER)
    frame.tree.heading("treeName", text=textSetting.textList["mdlBin"]["treeName"], anchor=tkinter.CENTER)
    for i in range(decryptFile.max_param):
        col_name = textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)
        displayList.append(col_name)
        frame.tree.heading(col_name, text=col_name, anchor=tkinter.CENTER)

    frame.tree["displaycolumns"] = [
        "treeNum",
        "treeDelay",
        "treeName"
    ]
    frame.tree["displaycolumns"] += tuple(displayList)

    index = 0
    num = 0
    sectionNum = 0
    for scriptDataInfoList in decryptFile.scriptDataAllInfoList:
        listNum = 0
        for scriptDataInfo in scriptDataInfoList:
            headerInfo = (index, "-", "---#{0}, {1}#---".format(num, listNum), "-", "{0},{1},{2}".format(num, listNum, sectionNum))
            headerInfo += (",".join(str(n) for n in scriptDataInfo[0]), )
            frame.tree.insert(parent="", index="end", iid=index, values=headerInfo)
            index += 1
            sectionNum = 1
            for scriptData in scriptDataInfo[1:]:
                data = (index, scriptData[0], cmdList[scriptData[1]], scriptData[3], "{0},{1},{2}".format(num, listNum, sectionNum))
                paramCnt = scriptData[2]
                paramList = []
                for i in range(paramCnt):
                    paramList.append(scriptData[4 + i])
                data = data + tuple(paramList)
                frame.tree.insert(parent="", index="end", iid=index, values=data)
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
    result = InputDialog(root, textSetting.textList["mdlBin"]["cmdModify"], decryptFile, cmdList, int(selectItem["treeNum"]), selectItem["treeSection"], selectItem)
    if result.reloadFlag:
        reloadFile()


def insertLine():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, textSetting.textList["mdlBin"]["cmdInsert"], decryptFile, cmdList, int(selectItem["treeNum"]), selectItem["treeSection"])
    if result.reloadFlag:
        reloadFile()


def deleteLine():
    global decryptFile
    global frame
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    warnMsg = textSetting.textList["infoList"]["I9"]
    result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
    if result:
        sectionList = selectItem["treeSection"].split(",")
        num = int(sectionList[0])
        listNum = int(sectionList[1])
        cmdDiff = int(sectionList[2])
        if not decryptFile.saveFile(num, listNum, cmdDiff, "delete"):
            decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
        reloadFile()


def copyLine():
    global pasteLineBtn
    global frame
    global copyScriptData

    scriptData = []
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    scriptData.append(int(selectItem["treeDelay"]))
    scriptData.append(cmdList.index(selectItem["treeName"]))
    paramCnt = len(selectItem) - 5
    scriptData.append(paramCnt)
    scriptData.append(int(selectItem["treeFileFlag"]))
    for i in range(paramCnt):
        try:
            temp = float(selectItem[textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)])
        except Exception:
            temp = selectItem[textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)]
        scriptData.append(temp)
    copyScriptData = copy.deepcopy(scriptData)

    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
    pasteLineBtn["state"] = "normal"


def pasteLine():
    global root
    global decryptFile
    global frame
    global copyScriptData
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"])
    result = PasteDialog(root, textSetting.textList["mdlBin"]["cmdPaste"], decryptFile, cmdList, num, selectItem["treeSection"], copyScriptData)
    if result.reloadFlag:
        reloadFile()


def headerFileEdit():
    global root
    global decryptFile
    global frame
    result = HeaderDialog(root, textSetting.textList["mdlBin"]["headerInfo"], decryptFile)
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
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def listNumModify():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    arr = selectItem["treeName"].split(", ")
    num = arr[0].strip("-").strip("#")

    scriptDataInfoList = decryptFile.scriptDataAllInfoList[int(num)]
    result = ListNumModifyDialog(root, textSetting.textList["mdlBin"]["listNumModifyLabel"], decryptFile, num, len(scriptDataInfoList))
    if result.reloadFlag:
        reloadFile()


def listHeaderModify():
    global root
    global decryptFile
    global frame
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    arr = selectItem["treeName"].split(", ")
    num = arr[0].strip("-").strip("#")
    listNum = arr[1].strip("-").strip("#")
    headerInfo = [int(n) for n in selectItem["param1"].split(",")]

    result = ListHeaderModifyDialog(root, textSetting.textList["mdlBin"]["listHeaderModifyLabel"], decryptFile, int(num), int(listNum), headerInfo)
    if result.reloadFlag:
        reloadFile()


def numModify():
    global root
    global decryptFile
    global frame

    scriptDataAllInfoList = decryptFile.scriptDataAllInfoList
    result = NumModifyDialog(root, textSetting.textList["mdlBin"]["numModifyLabel"], decryptFile, len(scriptDataAllInfoList))
    if result.reloadFlag:
        reloadFile()


def csvExtract():
    global v_fileName
    global decryptFile

    file = v_fileName.get()
    filename = os.path.splitext(os.path.basename(file))[0]
    file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("mdlbin_csv", "*.csv")])
    errorMsg = textSetting.textList["errorList"]["E7"]
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
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def csvLoadAndSave():
    global decryptFile
    file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("mdlbin_csv", "*.csv")])
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
                    errorMsg = textSetting.textList["errorList"]["E8"].format(i + 1, cmdName)
                    mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                    return
                csvScriptData.append(arr)
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E15"].format(i + 1)
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

    msg = textSetting.textList["infoList"]["I15"].format(i + 1)
    result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")

    if result:
        if not decryptFile.saveCsv(csvScriptDataAllInfoList):
            decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I16"])
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
    global listHeaderModifyBtn
    global numModifyBtn
    global csvExtractBtn
    global csvLoadAndSaveBtn
    global scriptLf

    root = rootTk
    v_fileName = tkinter.StringVar()
    fileNameEt = ttk.Entry(programFrame, textvariable=v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
    fileNameEt.place(relx=0.053, rely=0.03)

    selectLb = ttk.Label(programFrame, text=textSetting.textList["mdlBin"]["selectNum"], font=textSetting.textList["font2"])
    selectLb.place(relx=0.05, rely=0.09)

    v_select = tkinter.StringVar()
    selectEt = ttk.Entry(programFrame, textvariable=v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
    selectEt.place(relx=0.22, rely=0.09)

    editLineBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["editLineLabel"], width=25, state="disabled", command=editLine)
    editLineBtn.place(relx=0.43, rely=0.03)

    insertLineBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["insertLineLabel"], width=25, state="disabled", command=insertLine)
    insertLineBtn.place(relx=0.62, rely=0.03)

    deleteLineBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["deleteLineLabel"], width=25, state="disabled", command=deleteLine)
    deleteLineBtn.place(relx=0.81, rely=0.03)

    copyLineBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["copyLineLabel"], width=25, state="disabled", command=copyLine)
    copyLineBtn.place(relx=0.43, rely=0.09)

    pasteLineBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["pasteLineLabel"], width=25, state="disabled", command=pasteLine)
    pasteLineBtn.place(relx=0.62, rely=0.09)

    headerFileEditBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["headerEditLabel"], width=25, state="disabled", command=headerFileEdit)
    headerFileEditBtn.place(relx=0.81, rely=0.09)

    listNumModifyBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["listNumModifyBtnLabel"], width=25, state="disabled", command=listNumModify)
    listNumModifyBtn.place(relx=0.43, rely=0.15)

    listHeaderModifyBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["listHeaderModifyBtnLabel"], width=25, state="disabled", command=listHeaderModify)
    listHeaderModifyBtn.place(relx=0.62, rely=0.15)

    numModifyBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["numModifyBtnLabel"], width=25, state="disabled", command=numModify)
    numModifyBtn.place(relx=0.81, rely=0.15)

    csvExtractBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["csvExtractLabel"], width=25, state="disabled", command=csvExtract)
    csvExtractBtn.place(relx=0.05, rely=0.15)

    csvLoadAndSaveBtn = ttk.Button(programFrame, text=textSetting.textList["mdlBin"]["csvSaveLabel"], width=25, state="disabled", command=csvLoadAndSave)
    csvLoadAndSaveBtn.place(relx=0.22, rely=0.15)

    scriptLf = ttk.LabelFrame(programFrame, text=textSetting.textList["mdlBin"]["scriptLabel"])
    scriptLf.place(relx=0.03, rely=0.20, relwidth=0.95, relheight=0.77)
