import os
import tkinter
import traceback

from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.errorLogClass import ErrorLogObj

from program.mdlinfo.importPy.decrypt import MdlDecrypt
from program.mdlinfo.importPy.tkinterScrollbarTreeviewMdlinfo import ScrollbarTreeviewMdlinfo
from program.mdlinfo.importPy.tkinterClass import TreeViewDialog, SmfTypeDialog, SmfDetailDialog, BinFileOrFlagEditDialog, CopyMdlDialog, PasteDialog

from program.smf.importPy.decrypt import SmfDecrypt

root = None
rootFrameAppearance = None
v_fileName = None
v_select = None
v_search = None
searchEt = None
mdlInfoLf = None
getMdlDetailBtn = None
getMdlTypeBtn = None
getSmfDetailBtn = None
getBinOrFlagBtn = None
copyAnotherBtn = None
deleteMdlInfoBtn = None
copyInfoBtn = None
pasteInfoBtn = None
readSMFBtn = None
decryptFile = None
frame = None
copyInfoByteArr = None
errObj = ErrorLogObj


def openFile():
    global v_fileName
    global copyAnotherBtn
    global readSMFBtn
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["mdlinfo"]["fileType"], "MDLINFO*.BIN")])

    errorMsg = textSetting.textList["errorList"]["E18"]
    if file_path:
        try:
            del decryptFile
            decryptFile = None
            filename = os.path.basename(file_path)
            v_fileName.set(filename)

            decryptFile = MdlDecrypt(file_path)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            deleteWidget()
            createWidget()
            viewData(decryptFile.allInfoList)
            copyAnotherBtn["state"] = "normal"
            readSMFBtn["state"] = "normal"
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def deleteWidget():
    global v_select
    global mdlInfoLf

    children = mdlInfoLf.winfo_children()
    for child in children:
        child.destroy()

    v_select.set("")


def createWidget():
    global v_select
    global v_search
    global searchEt
    global mdlInfoLf
    global getMdlDetailBtn
    global getMdlTypeBtn
    global getSmfDetailBtn
    global getBinOrFlagBtn
    global deleteMdlInfoBtn
    global copyInfoBtn
    global frame

    v_search.set("")
    searchEt["state"] = "normal"

    btnList = [
        getMdlDetailBtn,
        getMdlTypeBtn,
        getSmfDetailBtn,
        getBinOrFlagBtn,
        deleteMdlInfoBtn,
        copyInfoBtn
    ]

    frame = ScrollbarTreeviewMdlinfo(mdlInfoLf, v_select, btnList)

    col_tuple = (
        "treeNum",
        "treeSmf",
        "treeSmfType",
        "treeSmfEleNum",
        "binFileLabel",
        "binFileFlag"
    )
    frame.tree["columns"] = col_tuple

    frame.tree.column("#0", width=0, stretch=False)
    frame.tree.column("treeNum", anchor=tkinter.CENTER, width=60, stretch=False)
    frame.tree.column("treeSmf", anchor=tkinter.CENTER)
    frame.tree.column("treeSmfType", anchor=tkinter.CENTER, width=60, stretch=False)
    frame.tree.column("treeSmfEleNum", anchor=tkinter.CENTER, width=80, stretch=False)
    frame.tree.column("binFileLabel", anchor=tkinter.CENTER)
    frame.tree.column("binFileFlag", anchor=tkinter.CENTER, width=60, stretch=False)

    frame.tree.heading("treeNum", text=textSetting.textList["mdlinfo"]["treeNum"], anchor=tkinter.CENTER)
    frame.tree.heading("treeSmf", text=textSetting.textList["mdlinfo"]["treeSmf"], anchor=tkinter.CENTER)
    frame.tree.heading("treeSmfType", text=textSetting.textList["mdlinfo"]["treeSmfType"], anchor=tkinter.CENTER)
    frame.tree.heading("treeSmfEleNum", text=textSetting.textList["mdlinfo"]["treeSmfEleNum"], anchor=tkinter.CENTER)
    frame.tree.heading("binFileLabel", text=textSetting.textList["mdlinfo"]["binFileLabel"], anchor=tkinter.CENTER)
    frame.tree.heading("binFileFlag", text=textSetting.textList["mdlinfo"]["binFileFlag"], anchor=tkinter.CENTER)

    frame.tree["displaycolumns"] = col_tuple


def viewData(allInfoList):
    index = 0
    for mdlInfo in allInfoList:
        binName = "-"
        if mdlInfo["binInfo"][0]:
            binName = mdlInfo["binInfo"][0]
        data = (index + 1, mdlInfo["smfName"])
        data += (mdlInfo["smfType"],)
        data += (len(mdlInfo["smfDetailList"]),)
        data += (binName, mdlInfo["binInfo"][1])
        frame.tree.insert(parent="", index="end", iid=index, values=data)
        index += 1
    filterData()


def filterModelList(event):
    global v_select
    global frame

    v_select.set("")
    if len(frame.tree.selection()) > 0:
        frame.tree.selection_remove(frame.tree.selection())
    filterData()


def filterData():
    global v_search
    global decryptFile
    global frame

    for i in range(len(decryptFile.allInfoList)):
        frame.tree.reattach(i, "", tkinter.END)

    search = v_search.get()
    for i in frame.tree.get_children():
        item = frame.tree.item(i)
        modelName = item["values"][1]
        if search.upper() not in modelName.upper():
            frame.tree.detach(i)


def allDeleteTreeview():
    global decryptFile
    global frame

    for i in range(len(decryptFile.allInfoList)):
        if frame.tree.exists(i):
            frame.tree.delete(i)


def getMdlDetail():
    global rootFrameAppearance
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1
    TreeViewDialog(root, textSetting.textList["mdlinfo"]["detailModelInfo"], num, decryptFile, rootFrameAppearance)


def getMdlType():
    global rootFrameAppearance
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1
    SmfTypeDialog(root, textSetting.textList["mdlinfo"]["detailModelTypeInfo"], num, decryptFile, rootFrameAppearance)

    allDeleteTreeview()
    decryptFile = decryptFile.reload()
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)


def getSmfDetail():
    global rootFrameAppearance
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1
    SmfDetailDialog(root, textSetting.textList["mdlinfo"]["smfInfo"], num, decryptFile, rootFrameAppearance)

    allDeleteTreeview()
    decryptFile = decryptFile.reload()
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)


def getBinOrFlag():
    global rootFrameAppearance
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1
    BinFileOrFlagEditDialog(root, textSetting.textList["mdlinfo"]["binFileOrFlagLabel"], num, decryptFile, rootFrameAppearance)

    allDeleteTreeview()
    decryptFile = decryptFile.reload()
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)


def copyAnother():
    global rootFrameAppearance
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["mdlinfo"]["fileType"], "MDLINFO*.BIN")])

    errorMsg = textSetting.textList["errorList"]["E18"]
    if file_path:
        try:
            tempDecryptFile = MdlDecrypt(file_path)
            if not tempDecryptFile.open():
                tempDecryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            result = CopyMdlDialog(root, textSetting.textList["mdlinfo"]["copyAnotherMdlinfo"], tempDecryptFile, rootFrameAppearance)
            if result.dirtyFlag:
                copyByteArr = result.copyByteArr
                del tempDecryptFile
                tempDecryptFile = None

                if not decryptFile.copy(copyByteArr):
                    decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])

                allDeleteTreeview()
                decryptFile = decryptFile.reload()
                viewData(decryptFile.allInfoList)
                frame.tree.selection_set(len(decryptFile.allInfoList) - 1)

        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def deleteMdlInfo():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1

    warnMsg = textSetting.textList["infoList"]["I25"].format(num + 1)
    result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
    if result:
        if not decryptFile.delete(num):
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])

        allDeleteTreeview()
        decryptFile = decryptFile.reload()
        viewData(decryptFile.allInfoList)

        num -= 1
        if num >= 0:
            frame.tree.selection_set(num)
        else:
            frame.tree.selection_set(0)


def copyInfo():
    global pasteInfoBtn
    global frame
    global decryptFile
    global copyInfoByteArr

    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1
    index = decryptFile.allInfoList[num]["smfIndex"]
    if num + 1 < len(decryptFile.allInfoList):
        nextIndex = decryptFile.allInfoList[num + 1]["smfIndex"]
        copyInfoByteArr = decryptFile.byteArr[index:nextIndex]
    else:
        copyInfoByteArr = decryptFile.byteArr[index:]

    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
    pasteInfoBtn["state"] = "normal"


def pasteInfo():
    global rootFrameAppearance
    global decryptFile
    global frame
    global copyInfoByteArr
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"])
    result = PasteDialog(root, textSetting.textList["mdlinfo"]["copyModelLabel"], decryptFile, num, copyInfoByteArr, rootFrameAppearance)
    if result.reloadFlag:
        allDeleteTreeview()
        decryptFile = decryptFile.reload()
        viewData(decryptFile.allInfoList)
        frame.tree.selection_set(num)


def readSMF():
    global decryptFile

    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["smf"]["fileType"], "*.SMF")])
    if file_path:
        errorMsg = textSetting.textList["errorList"]["E19"]
        smfDecryptFile = SmfDecrypt(file_path, writeFlag=False)
        if not smfDecryptFile.open():
            smfDecryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        meshInfoList = smfDecryptFile.meshList
        filename = os.path.basename(file_path)
        if not decryptFile.readSMFSave(filename, meshInfoList):
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])

        allDeleteTreeview()
        decryptFile = decryptFile.reload()
        viewData(decryptFile.allInfoList)
        frame.tree.selection_set(len(decryptFile.allInfoList) - 1)


def call_mdlinfo(rootTk, appearance):
    global root
    global rootFrameAppearance
    global v_fileName
    global v_select
    global v_search
    global searchEt
    global mdlInfoLf
    global getMdlDetailBtn
    global getMdlTypeBtn
    global getSmfDetailBtn
    global getBinOrFlagBtn
    global copyAnotherBtn
    global deleteMdlInfoBtn
    global copyInfoBtn
    global pasteInfoBtn
    global readSMFBtn

    root = rootTk
    rootFrameAppearance = appearance

    headerFrame = ttkCustomWidget.CustomTtkFrame(root)
    headerFrame.pack(fill=tkinter.BOTH, padx=40, pady=(20, 0))

    selectLbFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
    selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

    v_fileName = tkinter.StringVar()
    fileNameEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
    fileNameEt.grid(columnspan=5, row=0, column=0, pady=(0, 15), sticky=tkinter.EW)

    selectLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["mdlinfo"]["selectNum"], font=textSetting.textList["font2"])
    selectLb.grid(columnspan=4, row=1, column=0, pady=(0, 15), sticky=tkinter.EW)

    v_select = tkinter.StringVar()
    selectEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
    selectEt.grid(row=1, column=4, pady=(0, 15), sticky=tkinter.E)

    searchLb = ttkCustomWidget.CustomTtkLabel(selectLbFrame, text=textSetting.textList["mdlinfo"]["searchModel"], font=textSetting.textList["font2"])
    searchLb.grid(columnspan=2, row=2, column=0, pady=(0, 15), sticky=tkinter.E)

    v_search = tkinter.StringVar()
    searchEt = ttkCustomWidget.CustomTtkEntry(selectLbFrame, textvariable=v_search, font=textSetting.textList["font2"], state="readonly", justify="center")
    searchEt.grid(columnspan=6, row=2, column=3, pady=(0, 15), sticky=tkinter.EW)
    searchEt.bind("<KeyRelease>", filterModelList)

    btnFrame = ttkCustomWidget.CustomTtkFrame(headerFrame)
    btnFrame.pack(fill=tkinter.BOTH, padx=(40, 0))

    getMdlDetailBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlDetailLabel"], width=25, state="disabled", command=getMdlDetail)
    getMdlDetailBtn.grid(row=0, column=0, padx=10, pady=(0, 20))

    getMdlTypeBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlTypeLabel"], width=25, state="disabled", command=getMdlType)
    getMdlTypeBtn.grid(row=0, column=1, padx=10, pady=(0, 20))

    getSmfDetailBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlSmfEleLabel"], width=25, state="disabled", command=getSmfDetail)
    getSmfDetailBtn.grid(row=0, column=2, padx=10, pady=(0, 20))

    getBinOrFlagBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["binFileFlagLabel"], width=25, state="disabled", command=getBinOrFlag)
    getBinOrFlagBtn.grid(row=1, column=0, padx=10, pady=(0, 20))

    copyAnotherBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["copyAnotherMdlinfoLabel"], width=25, state="disabled", command=copyAnother)
    copyAnotherBtn.grid(row=1, column=1, padx=10, pady=(0, 20))

    deleteMdlInfoBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlinfoDeleteLabel"], width=25, state="disabled", command=deleteMdlInfo)
    deleteMdlInfoBtn.grid(row=1, column=2, padx=10, pady=(0, 20))

    copyInfoBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlinfoCopyLabel"], width=25, state="disabled", command=copyInfo)
    copyInfoBtn.grid(row=2, column=0, padx=10, pady=(0, 20))

    pasteInfoBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["mdlinfoPasteLabel"], width=25, state="disabled", command=pasteInfo)
    pasteInfoBtn.grid(row=2, column=1, padx=10, pady=(0, 20))

    readSMFBtn = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["mdlinfo"]["addSmfModelLabel"], width=25, state="disabled", command=readSMF)
    readSMFBtn.grid(row=2, column=2, padx=10, pady=(0, 20))

    btnFrame.grid_columnconfigure(0, weight=1)
    btnFrame.grid_columnconfigure(1, weight=1)
    btnFrame.grid_columnconfigure(2, weight=1)

    mdlInfoLf = ttkCustomWidget.CustomTtkLabelFrame(root, text=textSetting.textList["mdlinfo"]["scriptLabel"])
    mdlInfoLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))
