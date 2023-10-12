import os
import codecs
import shutil
import copy
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
scanSmfImageButton = None
v_modelCount = None
noImageListbox = None
v_modelPath = None
copyImageButton = None
noTexList = []
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


def scanSmfImage():
    global root
    global v_modelCount
    global noImageListbox
    global v_modelPath
    global noTexList
    global copyImageButton

    errorMsg = textSetting.textList["errorList"]["E4"]
    fileList = fd.askopenfilenames(filetypes=[(textSetting.textList["smf"]["fileListType"], "*.SMF")])
    if fileList:
        dirPath = os.path.dirname(fileList[0])
        v_modelPath.set(dirPath)
        allTexSet = set()
        modelCountFormat = "{0}/{1}"
        for idx, file in enumerate(fileList):
            v_modelCount.set(modelCountFormat.format(idx + 1, len(fileList)))
            root.update()

            decryptFile = SmfDecrypt(file, writeFlag=False)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            allTexSet |= decryptFile.texList
        allTexList = list(allTexSet)
        noTexList = []

        noImageListbox.delete(0, tkinter.END)
        for tex in allTexList:
            if not os.path.exists(os.path.join(dirPath, tex)):
                noTexList.append(tex)
                noImageListbox.insert(tkinter.END, "「{0}」がありません".format(tex))

        if len(noTexList) > 0:
            copyImageButton["state"] = "normal"
        else:
            copyImageButton["state"] = "disabled"


def copyImage():
    global root
    global v_modelPath
    global noTexList
    global noImageListbox
    global copyImageButton

    folderPath = fd.askdirectory()
    if folderPath:
        newNoTexList = []
        noImageListbox.delete(0, tkinter.END)
        root.update()

        modelCountFormat = "{0}/{1}"
        for idx, tex in enumerate(noTexList):
            v_modelCount.set(modelCountFormat.format(idx + 1, len(noTexList)))
            imagePath = os.path.join(folderPath, tex)
            if os.path.exists(imagePath):
                shutil.copy(imagePath, v_modelPath.get())
                noImageListbox.insert(tkinter.END, "{0}をコピーしました".format(tex))
            else:
                newNoTexList.append(tex)
                noImageListbox.insert(0, "「{0}」が存在しません".format(tex))
            root.update()
        noTexList = copy.deepcopy(newNoTexList)
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I118"])
        if len(noTexList) > 0:
            copyImageButton["state"] = "normal"
        else:
            copyImageButton["state"] = "disabled"


def call_smf(rootTk, programFrame):
    global root
    global frame
    global v_process
    global processBar
    global scriptLf
    global standardButton
    global swapFrameButton
    global deleteFrameButton
    global scanSmfImageButton
    global v_modelCount
    global noImageListbox
    global v_modelPath
    global copyImageButton

    root = rootTk

    v_process = tkinter.IntVar()
    v_process.set(0)

    processScriptFrame = ttk.Frame(programFrame)
    processScriptFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=30, pady=15)
    buttonListFrame = ttk.Frame(programFrame)
    buttonListFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=5, pady=5)

    processBar = ttk.Progressbar(processScriptFrame, orient=tkinter.HORIZONTAL, variable=v_process, maximum=100, length=400, mode="determinate")
    processBar.pack(fill=tkinter.X)

    scriptLf = ttk.LabelFrame(processScriptFrame, text=textSetting.textList["smf"]["scriptLabel"])
    scriptLf.pack(expand=True, fill=tkinter.BOTH, pady=15)
    frame = ScrollbarTreeviewSmf(scriptLf, None)

    standardButton = ttk.Button(buttonListFrame, text=textSetting.textList["smf"]["createStandardLabel"], width=25, command=createStandardGaugeButton, state="disabled")
    standardButton.grid(row=0, column=0, padx=30, pady=5)

    swapFrameButton = ttk.Button(buttonListFrame, text=textSetting.textList["smf"]["swapFrameLabel"], width=25, command=swapFrame, state="disabled")
    swapFrameButton.grid(row=0, column=1, padx=30, pady=5)

    deleteFrameButton = ttk.Button(buttonListFrame, text=textSetting.textList["smf"]["deleteFrameLabel"], width=25, command=deleteFrame, state="disabled")
    deleteFrameButton.grid(row=1, column=0, padx=30, pady=5)

    scanSmfImageButton = ttk.Button(buttonListFrame, text=textSetting.textList["smf"]["scanSmfImageLabel"], width=50, command=scanSmfImage)
    scanSmfImageButton.grid(row=2, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

    v_modelCount = tkinter.StringVar()
    modelCountEntry = ttk.Entry(buttonListFrame, textvariable=v_modelCount, font=textSetting.textList["defaultFont"], justify="center", state="readonly")
    modelCountEntry.grid(row=3, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)

    noImageListbox = tkinter.Listbox(buttonListFrame, selectmode="single", font=textSetting.textList["font2"])
    noImageListbox.grid(row=4, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)

    v_modelPath = tkinter.StringVar()
    modelPathEntry = ttk.Entry(buttonListFrame, textvariable=v_modelPath, font=textSetting.textList["defaultFont"], state="readonly")
    modelPathEntry.grid(row=5, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)

    copyImageButton = ttk.Button(buttonListFrame, text=textSetting.textList["smf"]["copyImageLabel"], width=50, command=copyImage, state="disabled")
    copyImageButton.grid(row=6, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)
