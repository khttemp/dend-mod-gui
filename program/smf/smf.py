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
import program.appearance.ttkCustomWidget as ttkCustomWidget

from program.smf.importPy.decrypt import SmfDecrypt
from program.smf.importPy.tkinterEditClass import SwapDialog
from program.smf.importPy.tkinterScrollbarTreeviewSmf import ScrollbarTreeviewSmf
from program.smf.importPy.extractX import XObject
from program.smf.importPy.extractX3d import X3dObject

root = None
rootFrameAppearance = None
frame = None
v_process = None
processBar = None
scriptLf = None
standardButton = None
swapFrameButton = None
deleteFrameButton = None
extract3dObjButton = None

v_framePosX = None
v_framePosY = None
v_framePosZ = None
v_frameRotX = None
v_frameRotY = None
v_frameRotZ = None
v_frameRotW = None

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
    global extract3dObjButton
    global decryptFile

    btnList = [
        swapFrameButton,
        deleteFrameButton
    ]

    frame = ScrollbarTreeviewSmf(scriptLf, btnList, getFrameInfo)
    frame.tree.heading("#0", text=decryptFile.filename, anchor=tkinter.CENTER)

    for idx, frameObj in enumerate(decryptFile.frameList):
        fName = frameObj["name"]
        meshNo = frameObj["meshNo"]
        if meshNo != -1:
            fName += textSetting.textList["smf"]["treeMeshNumFormat"].format(meshNo)
        parentFrameNo = frameObj["parentFrameNo"]
        frame.tree.insert("", str(idx), "item{0}".format(idx), text=fName, open=True)
        if parentFrameNo != -1:
            frame.tree.move("item{0}".format(idx), "item{0}".format(parentFrameNo), "end")

    standardButton["state"] = "normal"
    extract3dObjButton["state"] = "normal"


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
    global rootFrameAppearance
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    result = SwapDialog(root, textSetting.textList["smf"]["swapFrame"], decryptFile, rootFrameAppearance, selectId)
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
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
        reloadWidget()


def extract3d():
    global decryptFile
    saveName = os.path.splitext(os.path.basename(decryptFile.filename))[0]
    file_path = fd.asksaveasfilename(initialfile=saveName, filetypes=[(textSetting.textList["smf"]["xFile"], "*.x"), (textSetting.textList["smf"]["x3dFile"], "*.x3d")], defaultextension=".x")

    if file_path:
        errorMsg = textSetting.textList["errorList"]["E4"]
        ext = os.path.splitext(os.path.basename(file_path))[1].lower()
        if ext == ".x":
            xObj = XObject(file_path, decryptFile)
            if not xObj.makeXFile():
                xObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I122"])
        elif ext == ".x3d":
            x3dObj = X3dObject(file_path, decryptFile)
            if not x3dObj.makeX3d():
                x3dObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I121"])


def getFrameInfo():
    global v_framePosX
    global v_framePosY
    global v_framePosZ
    global v_frameRotX
    global v_frameRotY
    global v_frameRotZ
    global v_frameRotW
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    idx = int(selectId.strip("item"))
    frameObj = decryptFile.frameList[idx]
    matrix = frameObj["matrix"]
    pos = decryptFile.matrixToPos(matrix).split()
    v_framePosX.set(round(float(pos[0]), 5))
    v_framePosY.set(round(float(pos[1]), 5))
    v_framePosZ.set(round(float(pos[2]), 5))
    q = decryptFile.matrixToRot(matrix).split()
    v_frameRotX.set(round(float(q[0]), 5))
    v_frameRotY.set(round(float(q[1]), 5))
    v_frameRotZ.set(round(float(q[2]), 5))
    v_frameRotW.set(round(float(q[3]), 5))


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


def call_smf(rootTk, appearance):
    global root
    global rootFrameAppearance
    global frame
    global v_process
    global processBar
    global scriptLf
    global standardButton
    global swapFrameButton
    global deleteFrameButton
    global extract3dObjButton

    global v_framePosX
    global v_framePosY
    global v_framePosZ
    global v_frameRotX
    global v_frameRotY
    global v_frameRotZ
    global v_frameRotW

    global scanSmfImageButton
    global v_modelCount
    global noImageListbox
    global v_modelPath
    global copyImageButton

    root = rootTk
    rootFrameAppearance = appearance

    v_process = tkinter.IntVar()
    v_process.set(0)

    processScriptFrame = ttkCustomWidget.CustomTtkFrame(root)
    processScriptFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=30, pady=15)
    buttonListFrame = ttkCustomWidget.CustomTtkFrame(root)
    buttonListFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=5, pady=5)

    processBar = ttk.Progressbar(processScriptFrame, orient=tkinter.HORIZONTAL, variable=v_process, maximum=100, length=400, mode="determinate")
    processBar.pack(fill=tkinter.X)

    scriptLf = ttkCustomWidget.CustomTtkLabelFrame(processScriptFrame, text=textSetting.textList["smf"]["scriptLabel"])
    scriptLf.pack(expand=True, fill=tkinter.BOTH, pady=15)
    frame = ScrollbarTreeviewSmf(scriptLf, None)

    standardButton = ttkCustomWidget.CustomTtkButton(buttonListFrame, text=textSetting.textList["smf"]["createStandardLabel"], width=25, command=createStandardGaugeButton, state="disabled")
    standardButton.grid(row=0, column=0, padx=30, pady=5)

    swapFrameButton = ttkCustomWidget.CustomTtkButton(buttonListFrame, text=textSetting.textList["smf"]["swapFrameLabel"], width=25, command=swapFrame, state="disabled")
    swapFrameButton.grid(row=0, column=1, padx=30, pady=5)

    deleteFrameButton = ttkCustomWidget.CustomTtkButton(buttonListFrame, text=textSetting.textList["smf"]["deleteFrameLabel"], width=25, command=deleteFrame, state="disabled")
    deleteFrameButton.grid(row=1, column=0, padx=30, pady=5)

    extract3dObjButton = ttkCustomWidget.CustomTtkButton(buttonListFrame, text=textSetting.textList["smf"]["extract3dLabel"], width=25, command=extract3d, state="disabled")
    extract3dObjButton.grid(row=1, column=1, padx=30, pady=5)

    framePosInfoLf = ttkCustomWidget.CustomTtkLabelFrame(buttonListFrame, text=textSetting.textList["smf"]["framePosInfoLabel"])
    framePosInfoLf.grid(row=2, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

    v_framePosX = tkinter.DoubleVar()
    framePosXEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=v_framePosX, width=10, state="readonly")
    framePosXEt.grid(row=0, column=0, padx=10, pady=5)

    v_framePosY = tkinter.DoubleVar()
    framePosYEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=v_framePosY, width=10, state="readonly")
    framePosYEt.grid(row=0, column=1, padx=10, pady=5)

    v_framePosZ = tkinter.DoubleVar()
    framePosZEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=v_framePosZ, width=10, state="readonly")
    framePosZEt.grid(row=0, column=2, padx=10, pady=5)


    frameRotInfoLf = ttkCustomWidget.CustomTtkLabelFrame(buttonListFrame, text=textSetting.textList["smf"]["frameRotInfoLabel"])
    frameRotInfoLf.grid(row=3, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

    v_frameRotX = tkinter.DoubleVar()
    frameRotXEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=v_frameRotX, width=10, state="readonly")
    frameRotXEt.grid(row=0, column=0, padx=10, pady=5)

    v_frameRotY = tkinter.DoubleVar()
    frameRotYEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=v_frameRotY, width=10, state="readonly")
    frameRotYEt.grid(row=0, column=1, padx=10, pady=5)

    v_frameRotZ = tkinter.DoubleVar()
    frameRotZEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=v_frameRotZ, width=10, state="readonly")
    frameRotZEt.grid(row=0, column=2, padx=10, pady=5)

    v_frameRotW = tkinter.DoubleVar()
    frameRotWEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=v_frameRotW, width=10, state="readonly")
    frameRotWEt.grid(row=1, column=0, padx=10, pady=5)


    scanSmfImageButton = ttkCustomWidget.CustomTtkButton(buttonListFrame, text=textSetting.textList["smf"]["scanSmfImageLabel"], width=50, command=scanSmfImage)
    scanSmfImageButton.grid(row=4, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

    v_modelCount = tkinter.StringVar()
    modelCountEntry = ttkCustomWidget.CustomTtkEntry(buttonListFrame, textvariable=v_modelCount, font=textSetting.textList["defaultFont"], justify="center", state="readonly")
    modelCountEntry.grid(row=5, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)

    noImageListbox = tkinter.Listbox(buttonListFrame, selectmode="single", font=textSetting.textList["font2"], bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
    noImageListbox.grid(row=6, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)

    v_modelPath = tkinter.StringVar()
    modelPathEntry = ttkCustomWidget.CustomTtkEntry(buttonListFrame, textvariable=v_modelPath, font=textSetting.textList["defaultFont"], state="readonly")
    modelPathEntry.grid(row=7, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)

    copyImageButton = ttkCustomWidget.CustomTtkButton(buttonListFrame, text=textSetting.textList["smf"]["copyImageLabel"], width=50, command=copyImage, state="disabled")
    copyImageButton.grid(row=8, column=0, columnspan=2, sticky=tkinter.EW, padx=30, pady=5)
