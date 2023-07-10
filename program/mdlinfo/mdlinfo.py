import os
import tkinter
import traceback

from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd

from program.mdlinfo.importPy.decrypt import MdlDecrypt
from program.mdlinfo.importPy.tkinterScrollbarTreeviewMdlinfo import ScrollbarTreeviewMdlinfo
from program.mdlinfo.importPy.tkinterClass import TreeViewDialog, ImageDialog, SmfDetailDialog, BinFileOrFlagEditDialog, CopyMdlDialog, PasteDialog

from program.smf.importPy.decrypt import SmfDecrypt

root = None
v_fileName = None
v_select = None
v_search = None
searchEt = None
mdlInfoLf = None
getMdlDetailBtn = None
getMdlImageBtn = None
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


def openFile():
    global v_fileName
    global copyAnotherBtn
    global readSMFBtn
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[("MDLINFO", "*.BIN")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのMDLINFOではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            del decryptFile
            decryptFile = None
            filename = os.path.basename(file_path)
            v_fileName.set(filename)

            decryptFile = MdlDecrypt(file_path)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return

            deleteWidget()
            createWidget()
            viewData(decryptFile.allInfoList)
            copyAnotherBtn["state"] = "normal"
            readSMFBtn["state"] = "normal"
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


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
    global getMdlImageBtn
    global getSmfDetailBtn
    global getBinOrFlagBtn
    global deleteMdlInfoBtn
    global copyInfoBtn
    global frame

    v_search.set("")
    searchEt["state"] = "normal"

    btnList = [
        getMdlDetailBtn,
        getMdlImageBtn,
        getSmfDetailBtn,
        getBinOrFlagBtn,
        deleteMdlInfoBtn,
        copyInfoBtn
    ]

    frame = ScrollbarTreeviewMdlinfo(mdlInfoLf, v_select, btnList)

    col_tuple = ("番号", "smf", "イメージ数", "smf要素数", "binファイル", "フラグ")
    frame.tree['columns'] = col_tuple

    frame.tree.column("#0", width=0, stretch=False)
    frame.tree.column("番号", anchor=tkinter.CENTER, width=60, stretch=False)
    frame.tree.column("smf", anchor=tkinter.CENTER)
    frame.tree.column("イメージ数", anchor=tkinter.CENTER, width=60, stretch=False)
    frame.tree.column("smf要素数", anchor=tkinter.CENTER, width=80, stretch=False)
    frame.tree.column("binファイル", anchor=tkinter.CENTER)
    frame.tree.column("フラグ", anchor=tkinter.CENTER, width=60, stretch=False)

    frame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
    frame.tree.heading("smf", text="smf", anchor=tkinter.CENTER)
    frame.tree.heading("イメージ数", text="イメージ数", anchor=tkinter.CENTER)
    frame.tree.heading("smf要素数", text="smf要素数", anchor=tkinter.CENTER)
    frame.tree.heading("binファイル", text="binファイル", anchor=tkinter.CENTER)
    frame.tree.heading("フラグ", text="フラグ", anchor=tkinter.CENTER)

    frame.tree["displaycolumns"] = col_tuple


def viewData(allInfoList):
    index = 0
    for mdlInfo in allInfoList:
        binName = "-"
        if mdlInfo["binInfo"][0]:
            binName = mdlInfo["binInfo"][0]
        data = (index + 1, mdlInfo["smfName"])
        data += (len(mdlInfo["imgList"]),)
        data += (len(mdlInfo["smfDetailList"]),)
        data += (binName, mdlInfo["binInfo"][1])
        frame.tree.insert(parent='', index='end', iid=index, values=data)
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
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"]) - 1
    TreeViewDialog(root, "モデルの詳細情報", num, decryptFile)


def getMdlImage():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"]) - 1
    ImageDialog(root, "モデルのイメージ情報", num, decryptFile)

    allDeleteTreeview()
    decryptFile = decryptFile.reload()
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)


def getSmfDetail():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"]) - 1
    SmfDetailDialog(root, "smf要素情報", num, decryptFile)

    allDeleteTreeview()
    decryptFile = decryptFile.reload()
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)


def getBinOrFlag():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"]) - 1
    BinFileOrFlagEditDialog(root, "バイナリファイルとフラグ情報", num, decryptFile)

    allDeleteTreeview()
    decryptFile = decryptFile.reload()
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)


def copyAnother():
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[("MDLINFO", "MDLINFO*.BIN")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのMDLINFOではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            tempDecryptFile = MdlDecrypt(file_path)
            if not tempDecryptFile.open():
                tempDecryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return

            result = CopyMdlDialog(root, "コピー", tempDecryptFile)
            if result.dirtyFlag:
                copyByteArr = result.copyByteArr
                del tempDecryptFile
                tempDecryptFile = None

                if not decryptFile.copy(copyByteArr):
                    decryptFile.printError()
                    mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                    return
                mb.showinfo(title="成功", message="コピーしました")

                allDeleteTreeview()
                decryptFile = decryptFile.reload()
                viewData(decryptFile.allInfoList)
                frame.tree.selection_set(len(decryptFile.allInfoList) - 1)

        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def deleteMdlInfo():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"]) - 1

    warnMsg = "{0}番のモデル情報を削除しますか？".format(num + 1)
    result = mb.askokcancel(message=warnMsg, icon="warning")
    if result:
        if not decryptFile.delete(num):
            decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
        mb.showinfo(title="成功", message="モデル要素情報を修正しました")

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
    num = int(selectItem["番号"]) - 1
    index = decryptFile.allInfoList[num]["smfIndex"]
    if num + 1 < len(decryptFile.allInfoList):
        nextIndex = decryptFile.allInfoList[num + 1]["smfIndex"]
        copyInfoByteArr = decryptFile.byteArr[index:nextIndex]
    else:
        copyInfoByteArr = decryptFile.byteArr[index:]

    mb.showinfo(title="成功", message="コピーしました")
    pasteInfoBtn["state"] = "normal"


def pasteInfo():
    global decryptFile
    global frame
    global copyInfoByteArr
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])
    result = PasteDialog(root, "MDLINFO情報コピー", decryptFile, num, copyInfoByteArr)
    if result.reloadFlag:
        allDeleteTreeview()
        decryptFile = decryptFile.reload()
        viewData(decryptFile.allInfoList)
        frame.tree.selection_set(num)


def readSMF():
    global decryptFile

    num = None
    if len(frame.tree.selection()) > 0:
        selectId = frame.tree.selection()[0]
        selectItem = frame.tree.set(selectId)
        num = int(selectItem["番号"]) - 1
    file_path = fd.askopenfilename(filetypes=[("SELENE MODEL", "*.SMF")])
    if file_path:
        errorMsg = "予想外のエラーが出ました。\n電車でDのSMFではない、またはファイルが壊れた可能性があります。"
        smfDecryptFile = SmfDecrypt(file_path, writeFlag=False)
        if not smfDecryptFile.open():
            smfDecryptFile.printError()
            mb.showerror(title="エラー", message=errorMsg)
            return

        meshInfoList = smfDecryptFile.meshList
        filename = os.path.basename(file_path)
        if not decryptFile.readSMFSave(filename, meshInfoList):
            decryptFile.printError()
            mb.showerror(title="エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="モデル要素情報を修正しました")

        allDeleteTreeview()
        decryptFile = decryptFile.reload()
        viewData(decryptFile.allInfoList)
        frame.tree.selection_set(len(decryptFile.allInfoList) - 1)


def call_mdlinfo(rootTk, programFrame):
    global root
    global v_fileName
    global v_select
    global v_search
    global searchEt
    global mdlInfoLf
    global getMdlDetailBtn
    global getMdlImageBtn
    global getSmfDetailBtn
    global getBinOrFlagBtn
    global copyAnotherBtn
    global deleteMdlInfoBtn
    global copyInfoBtn
    global pasteInfoBtn
    global readSMFBtn

    root = rootTk
    v_fileName = tkinter.StringVar()
    fileNameEt = ttk.Entry(programFrame, textvariable=v_fileName, font=("", 14), width=23, state="readonly", justify="center")
    fileNameEt.place(relx=0.053, rely=0.03)

    selectLb = ttk.Label(programFrame, text="選択した行番号：", font=("", 14))
    selectLb.place(relx=0.05, rely=0.09)

    v_select = tkinter.StringVar()
    selectEt = ttk.Entry(programFrame, textvariable=v_select, font=("", 14), width=6, state="readonly", justify="center")
    selectEt.place(relx=0.22, rely=0.09)

    searchLb = ttk.Label(programFrame, text="モデル検索：", font=("", 14))
    searchLb.place(relx=0.05, rely=0.15)

    v_search = tkinter.StringVar()
    searchEt = ttk.Entry(programFrame, textvariable=v_search, font=("", 14), state="readonly", justify="center")
    searchEt.place(relx=0.18, rely=0.15, relwidth=0.20)
    searchEt.bind("<KeyRelease>", filterModelList)

    mdlInfoLf = ttk.LabelFrame(programFrame, text="MDLINFO内容")
    mdlInfoLf.place(relx=0.03, rely=0.20, relwidth=0.95, relheight=0.77)

    getMdlDetailBtn = ttk.Button(programFrame, text="選択したモデルの詳細情報", width=25, state="disabled", command=getMdlDetail)
    getMdlDetailBtn.place(relx=0.43, rely=0.03)

    getMdlImageBtn = ttk.Button(programFrame, text="選択したモデルのイメージ情報", width=25, state="disabled", command=getMdlImage)
    getMdlImageBtn.place(relx=0.62, rely=0.03)

    getSmfDetailBtn = ttk.Button(programFrame, text="選択したモデルのsmf要素情報", width=25, state="disabled", command=getSmfDetail)
    getSmfDetailBtn.place(relx=0.81, rely=0.03)

    getBinOrFlagBtn = ttk.Button(programFrame, text="binファイル、フラグ修正", width=25, state="disabled", command=getBinOrFlag)
    getBinOrFlagBtn.place(relx=0.43, rely=0.09)

    copyAnotherBtn = ttk.Button(programFrame, text="別のMDLINFOからコピーする", width=25, state="disabled", command=copyAnother)
    copyAnotherBtn.place(relx=0.62, rely=0.09)

    deleteMdlInfoBtn = ttk.Button(programFrame, text="選択したモデル情報を削除する", width=25, state="disabled", command=deleteMdlInfo)
    deleteMdlInfoBtn.place(relx=0.81, rely=0.09)

    copyInfoBtn = ttk.Button(programFrame, text="選択した行をコピーする", width=25, state="disabled", command=copyInfo)
    copyInfoBtn.place(relx=0.43, rely=0.15)

    pasteInfoBtn = ttk.Button(programFrame, text="選択した行に貼り付けする", width=25, state="disabled", command=pasteInfo)
    pasteInfoBtn.place(relx=0.62, rely=0.15)

    readSMFBtn = ttk.Button(programFrame, text="SMF情報でモデル追加", width=25, state="disabled", command=readSMF)
    readSMFBtn.place(relx=0.81, rely=0.15)
