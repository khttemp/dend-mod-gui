import os
import codecs
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting

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
    file_path = fd.askopenfilename(filetypes=[(textSetting.textList["smf"]["fileType"], "*.SMF")])

    errorMsg = textSetting.textList["errorList"]["E19"]
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
    frame.tree.heading("#0", text=decryptFile.filename, anchor=tkinter.CENTER)

    for idx, frameInfo in enumerate(decryptFile.frameList):
        fName = frameInfo[1].rstrip("\x00")
        meshNo = frameInfo[2]
        if meshNo != -1:
            fName += textSetting.textList["smf"]["treeMeshNumFormat"].format(meshNo)
        parentFrameNo = frameInfo[3]
        frame.tree.insert("", str(idx), "item{0}".format(idx), text=fName, open=True)
        if parentFrameNo != -1:
            frame.tree.move("item{0}".format(idx), "item{0}".format(parentFrameNo), "end")

    standardButton["state"] = "normal"


def reloadWidget():
    global decryptFile

    errorMsg = textSetting.textList["errorList"]["E19"]
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        return
    deleteWidget()
    createWidget()


def createStandardGaugeButton():
    global decryptFile
    global v_process
    global processBar

    if not decryptFile.detectGauge():
        if decryptFile.error == "":
            msg = textSetting.textList["infoList"]["I105"]
            for model in decryptFile.standardGuageList:
                msg += "\n" + model
            mb.showerror(title=textSetting.textList["error"], message=msg)
            return
    else:
        modelIndex = decryptFile.standardGuageList.index(decryptFile.filename)
        modelName = decryptFile.d4NarrowGuageList[modelIndex]
        msg = textSetting.textList["infoList"]["I106"].format(modelName)
        mb.showinfo(title=textSetting.textList["smf"]["smfFile"], message=msg)
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["smf"]["fileType"], "*.SMF")])
        if file_path:
            filename = os.path.basename(file_path)
            if filename.upper() != modelName:
                msg = textSetting.textList["infoList"]["I107"]
                mb.showerror(title=textSetting.textList["error"], message=msg)
                return
            d4DecryptFile = SmfDecrypt(file_path, False, False, False, False, v_process, processBar, False)
            if not d4DecryptFile.open():
                d4DecryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E74"])
                return

            if not decryptFile.createStandardGauge(d4DecryptFile):
                if d4DecryptFile.error != "":
                    mb.showerror(title=textSetting.textList["error"], message=d4DecryptFile.error)
                    return
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
        else:
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I108"])
        reloadWidget()


def swapFrame():
    global root
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    result = SwapDialog(root, textSetting.textList["smf"]["swapFrame"], decryptFile, selectId)
    if result.reloadFlag:
        reloadWidget()


def deleteFrame():
    global root
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    frameIdx = int(selectId[4:])
    selectName = frame.tree.item(selectId)["text"]
    warnMsg = textSetting.textList["infoList"]["I109"].format(selectName)

    result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, parent=root)
    if result:
        errorMsg = textSetting.textList["errorList"]["E4"]
        if not decryptFile.deleteFrame(frameIdx, -1):
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
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

    scriptLf = ttk.LabelFrame(programFrame, text=textSetting.textList["smf"]["scriptLabel"])
    scriptLf.place(relx=0.03, rely=0.08, relwidth=0.45, relheight=0.89)

    standardButton = ttk.Button(programFrame, text=textSetting.textList["smf"]["createStandardLabel"], width=25, command=createStandardGaugeButton, state="disabled")
    standardButton.place(relx=0.55, rely=0.03)

    swapFrameButton = ttk.Button(programFrame, text=textSetting.textList["smf"]["swapFrameLabel"], width=25, command=swapFrame, state="disabled")
    swapFrameButton.place(relx=0.78, rely=0.03)

    deleteFrameButton = ttk.Button(programFrame, text=textSetting.textList["smf"]["deleteFrameLabel"], width=25, command=deleteFrame, state="disabled")
    deleteFrameButton.place(relx=0.55, rely=0.07)
