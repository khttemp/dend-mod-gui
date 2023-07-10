import os
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from program.smf.importPy.decrypt import SmfDecrypt
from program.smf.importPy.tkinterEditClass import SwapDialog
from program.smf.importPy.tkinterScrollbarTreeviewSmf import ScrollbarTreeviewSmf

root = None
frame = None
v_process = None
processBar = None
scriptLf = None
standardButton = None
swapFrameButton = None
deleteFrameButton = None
decryptFile = None


def openFile(frameCheck, meshCheck, xyzCheck, mtrlCheck):
    global v_process
    global processBar
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[("SELENE MODEL", "*.SMF")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのSMFではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            frameFlag = False
            if frameCheck == 1:
                frameFlag = True
            meshFlag = False
            if meshCheck == 1:
                meshFlag = True
            xyzFlag = False
            if xyzCheck == 1:
                xyzFlag = True
            mtrlFlag = False
            if mtrlCheck == 1:
                mtrlFlag = True
            decryptFile = SmfDecrypt(file_path, frameFlag, meshFlag, xyzFlag, mtrlFlag, v_process, processBar)
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
    global processBar
    global scriptLf
    global swapFrameButton
    global deleteFrameButton

    children = processBar.winfo_children()
    for child in children:
        child.destroy()

    children = scriptLf.winfo_children()
    for child in children:
        child.destroy()

    btnList = [
        swapFrameButton,
        deleteFrameButton
    ]
    for btn in btnList:
        btn["state"] = "disabled"


def createWidget():
    global frame
    global scriptLf
    global standardButton
    global swapFrameButton
    global deleteFrameButton
    global decryptFile

    btnList = [
        swapFrameButton,
        deleteFrameButton
    ]

    frame = ScrollbarTreeviewSmf(scriptLf, btnList)
    frame.tree.heading('#0', text=decryptFile.filename, anchor=tkinter.CENTER)

    for idx, frameInfo in enumerate(decryptFile.frameList):
        fName = frameInfo[1].rstrip("\x00")
        meshNo = frameInfo[2]
        if meshNo != -1:
            fName += "(Mesh No.{0})".format(meshNo)
        parentFrameNo = frameInfo[3]
        frame.tree.insert("", str(idx), "item{0}".format(idx), text=fName, open=True)
        if parentFrameNo != -1:
            frame.tree.move("item{0}".format(idx), "item{0}".format(parentFrameNo), "end")

    standardButton["state"] = "normal"


def reloadWidget():
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのSMFではない、またはファイルが壊れた可能性があります。"
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title="エラー", message=errorMsg)
        return
    deleteWidget()
    createWidget()


def createStandardGaugeButton():
    global decryptFile
    global v_process
    global processBar

    if not decryptFile.detectGauge():
        if decryptFile.error == "":
            msg = "下記のモデルのみ出来ます"
            for model in decryptFile.standardGuageList:
                msg += "\n" + model
            mb.showerror(title="エラー", message=msg)
            return
    else:
        modelIndex = decryptFile.standardGuageList.index(decryptFile.filename)
        modelName = decryptFile.d4NarrowGuageList[modelIndex]
        msg = modelName + "を読み込んでください"
        mb.showinfo(title="ファイル", message=msg)
        file_path = fd.askopenfilename(filetypes=[("SELENE MODEL", "*.SMF")])
        if file_path:
            filename = os.path.basename(file_path)
            if filename.upper() != modelName:
                msg = "モデルが違います"
                mb.showerror(title="エラー", message=msg)
                return
            d4DecryptFile = SmfDecrypt(file_path, False, False, False, False, v_process, processBar, False)
            if not d4DecryptFile.open():
                d4DecryptFile.printError()
                mb.showerror(title="エラー", message="読み込みエラーです")
                return

            if not decryptFile.createStandardGauge(d4DecryptFile):
                if d4DecryptFile.error != "":
                    mb.showerror(title="エラー", message=d4DecryptFile.error)
                    return
                decryptFile.printError()
                mb.showerror(title="エラー", message="エラーです")
                return
        else:
            return
        mb.showinfo(title="成功", message="標準軌を作成しました")
        reloadWidget()


def swapFrame():
    global root
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    result = SwapDialog(root, "フレーム入れ替え", decryptFile, selectId)
    if result.reloadFlag:
        reloadWidget()


def deleteFrame():
    global root
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    frameIdx = int(selectId[4:])
    selectName = frame.tree.item(selectId)["text"]
    warnMsg = "{0}を消します。\nこの要素の全ての子要素に影響が及びます。\nこのまま消してもよろしいですか？".format(selectName)

    result = mb.askokcancel(title="確認", message=warnMsg, parent=root)
    if result:
        errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
        if not decryptFile.deleteFrame(frameIdx, -1):
            decryptFile.printError()
            mb.showerror(title="保存エラー", message=errorMsg)
        mb.showinfo(title="成功", message="SMFを修正しました")
        reloadWidget()


def call_smf(rootTk, programFrame):
    global root
    global v_process
    global processBar
    global scriptLf
    global standardButton
    global swapFrameButton
    global deleteFrameButton

    root = rootTk

    v_process = tkinter.IntVar()
    v_process.set(0)
    processBar = ttk.Progressbar(programFrame, orient=tkinter.HORIZONTAL, variable=v_process, maximum=100, length=400, mode="determinate")
    processBar.place(relx=0.03, rely=0.03)

    scriptLf = ttk.LabelFrame(programFrame, text="構成")
    scriptLf.place(relx=0.03, rely=0.08, relwidth=0.45, relheight=0.89)

    standardButton = ttk.Button(programFrame, text="標準軌を作成する", width=25, command=createStandardGaugeButton, state="disabled")
    standardButton.place(relx=0.55, rely=0.03)

    swapFrameButton = ttk.Button(programFrame, text="フレームの位置を入れ替える", width=25, command=swapFrame, state="disabled")
    swapFrameButton.place(relx=0.78, rely=0.03)

    deleteFrameButton = ttk.Button(programFrame, text="フレームを消す", width=25, command=deleteFrame, state="disabled")
    deleteFrameButton.place(relx=0.55, rely=0.07)
