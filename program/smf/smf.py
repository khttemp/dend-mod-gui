import os
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from program.smf.importPy.decrypt import SmfDecrypt
from program.smf.importPy.tkinterScrollbarFrame import ScrollbarFrame

root = None
frame = None
v_process = None
processBar = None
scriptLf = None
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

    children = processBar.winfo_children()
    for child in children:
        child.destroy()

    children = scriptLf.winfo_children()
    for child in children:
        child.destroy()


def createWidget():
    global frame
    global scriptLf
    global decryptFile

    frame = ScrollbarFrame(scriptLf, None, None)
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


def reloadWidget():
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのSMFではない、またはファイルが壊れた可能性があります。"
    if not decryptFile.open():
        print("error" + decryptFile.error)
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
            d4DecryptFile = SmfDecrypt(file_path, False, False, False, False, v_process, processBar)
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


def call_smf(rootTk, programFrame):
    global root
    global v_process
    global processBar
    global scriptLf

    root = rootTk

    v_process = tkinter.IntVar()
    v_process.set(0)
    processBar = ttk.Progressbar(programFrame, orient=tkinter.HORIZONTAL, variable=v_process, maximum=100, length=400, mode="determinate")
    processBar.place(relx=0.03, rely=0.03)

    scriptLf = ttk.LabelFrame(programFrame, text="構成")
    scriptLf.place(relx=0.03, rely=0.08, relwidth=0.45, relheight=0.89)

    bButton = ttk.Button(programFrame, text="標準軌を作成する", width=25, command=createStandardGaugeButton)
    bButton.place(relx=0.5, rely=0.03)
