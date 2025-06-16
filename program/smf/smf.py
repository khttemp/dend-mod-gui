import os
import codecs
import shutil
import copy
import re
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

from program.smf.importPy.decrypt import SmfDecrypt
from program.smf.importPy.tkinterEditClass import SwapDialog, SwapMeshDialog, FrameInfoDialog
from program.smf.importPy.tkinterEditFbxClass import SwapFbxMeshDialog
from program.smf.importPy.tkinterScrollbarTreeviewSmf import ScrollbarTreeviewSmf
from program.smf.importPy.extractFbx import FbxObject
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
copyAndPasteFrameButton = None
extract3dObjButton = None
turnModelMeshButton = None
swapModelMeshButton = None
editInfoFrameButton = None

v_framePosX = None
v_framePosY = None
v_framePosZ = None
v_frameRotX = None
v_frameRotY = None
v_frameRotZ = None

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
    global copyAndPasteFrameButton
    global extract3dObjButton
    global turnModelMeshButton
    global swapModelMeshButton
    global editInfoFrameButton
    global decryptFile

    btnList = [
        swapFrameButton,
        deleteFrameButton,
        copyAndPasteFrameButton,
        editInfoFrameButton
    ]
    meshBtnList = [
        turnModelMeshButton,
        swapModelMeshButton
    ]

    frame = ScrollbarTreeviewSmf(scriptLf, btnList, meshBtnList, getFrameInfo)
    frame.tree.heading("#0", text=decryptFile.filename, anchor=tkinter.CENTER)

    for idx, frameObj in enumerate(decryptFile.frameList):
        fName = frameObj["name"]
        meshNo = frameObj["meshNo"]
        tags = ""
        if meshNo != -1:
            fName += textSetting.textList["smf"]["treeMeshNumFormat"].format(meshNo)
            tags = "mesh"
        parentFrameNo = frameObj["parentFrameNo"]
        frame.tree.insert("", str(idx), "item{0}".format(idx), text=fName, tags=tags, open=True)
        if parentFrameNo != -1:
            frame.tree.move("item{0}".format(idx), "item{0}".format(parentFrameNo), "end")

    standardButton["state"] = "normal"
    extract3dObjButton["state"] = "normal"
    turnModelMeshButton["state"] = "disabled"
    swapModelMeshButton["state"] = "disabled"


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
        if decryptFile.detectMuTrack():
            if not decryptFile.createStandardGauge(None):
                if decryptFile.error != "":
                    mb.showerror(title=textSetting.textList["error"], message=decryptFile.error)
                    return
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
        else:
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

    result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=root)
    if result:
        errorMsg = textSetting.textList["errorList"]["E4"]
        if not decryptFile.deleteFrame(frameIdx, -1):
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
        reloadWidget()


def copyAndPasteFrame():
    global root
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    frameIdx = int(selectId[4:])
    parentIdx = decryptFile.frameList[frameIdx]["parentFrameNo"]
    selectName = frame.tree.item(selectId)["text"]
    warnMsg = textSetting.textList["infoList"]["I127"].format(selectName)

    result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=root)
    if result:
        errorMsg = textSetting.textList["errorList"]["E4"]
        if not decryptFile.addFrame(frameIdx, parentIdx):
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
        reloadWidget()


def editInfoFrame():
    global root
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    frameIdx = int(selectId[4:])
    result = FrameInfoDialog(root, textSetting.textList["smf"]["editInfoFrame"], frameIdx, decryptFile, rootFrameAppearance)
    if result.reloadFlag:
        reloadWidget()


def extract3d():
    global decryptFile
    saveName = os.path.splitext(os.path.basename(decryptFile.filename))[0]
    file_path = fd.asksaveasfilename(
        initialfile=saveName,
        filetypes=[
            (textSetting.textList["smf"]["fbxFile"], "*.fbx"),
            (textSetting.textList["smf"]["xFile"], "*.x"),
            (textSetting.textList["smf"]["x3dFile"], "*.x3d")
        ],
        defaultextension=".fbx")

    if file_path:
        errorMsg = textSetting.textList["errorList"]["E4"]
        ext = os.path.splitext(os.path.basename(file_path))[1].lower()
        if ext == ".fbx":
            fbxObj = FbxObject(file_path, decryptFile)
            if not fbxObj.makeFbxFile():
                fbxObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I123"])
        elif ext == ".x":
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


def turnModelMesh():
    global decryptFile
    global frame

    warnMsg = textSetting.textList["infoList"]["I124"]
    result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=root)
    if result:
        errorMsg = textSetting.textList["errorList"]["E4"]
        selectId = frame.tree.selection()[0]
        selectName = frame.tree.item(selectId)["text"]
        meshNo = re.findall("Mesh No.(\d+)", selectName)[0]
        if not decryptFile.turnModelMesh(int(meshNo)):
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I125"])
        reloadWidget()


def swapModelMesh():
    global root
    global rootFrameAppearance
    global frame
    global decryptFile

    file_path = fd.askopenfilename(
        filetypes=[
            (textSetting.textList["smf"]["fileType"], "*.SMF"),
            (textSetting.textList["smf"]["fbxFile"], "*.fbx")
        ]
    )
    if file_path:
        ext = os.path.splitext(os.path.basename(file_path))[1].lower()
        if ext == ".smf":
            swapDecryptFile = SmfDecrypt(file_path, False, False, False, False, v_process, processBar, False)
            if not swapDecryptFile.open():
                swapDecryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E74"])
                return
            selectId = frame.tree.selection()[0]
            selectName = frame.tree.item(selectId)["text"]
            meshNo = re.findall("Mesh No.(\d+)", selectName)[0]
            result = SwapMeshDialog(root, textSetting.textList["smf"]["swapMesh"], decryptFile, swapDecryptFile, rootFrameAppearance, int(meshNo))
            if result.reloadFlag:
                reloadWidget()
        elif ext == ".fbx":
            selectId = frame.tree.selection()[0]
            selectName = frame.tree.item(selectId)["text"]
            meshNo = re.findall("Mesh No.(\d+)", selectName)[0]
            result = SwapFbxMeshDialog(root, textSetting.textList["smf"]["swapMesh"], decryptFile, file_path, rootFrameAppearance, int(meshNo))
            if result.reloadFlag:
                reloadWidget()


def getFrameInfo():
    global v_framePosX
    global v_framePosY
    global v_framePosZ
    global v_frameRotX
    global v_frameRotY
    global v_frameRotZ
    global frame
    global decryptFile

    selectId = frame.tree.selection()[0]
    idx = int(selectId.strip("item"))
    frameObj = decryptFile.frameList[idx]
    matrix = frameObj["matrix"]
    pos = decryptFile.matrixToPosInfo(matrix)
    v_framePosX.set(round(pos[0], 5))
    v_framePosY.set(round(pos[1], 5))
    v_framePosZ.set(round(pos[2], 5))
    q = decryptFile.matrixToEulerAngleInfo(matrix)
    v_frameRotX.set(round(q[0], 5))
    v_frameRotY.set(round(q[1], 5))
    v_frameRotZ.set(round(q[2], 5))


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
    global copyAndPasteFrameButton
    global extract3dObjButton
    global turnModelMeshButton
    global swapModelMeshButton
    global editInfoFrameButton

    global v_framePosX
    global v_framePosY
    global v_framePosZ
    global v_frameRotX
    global v_frameRotY
    global v_frameRotZ

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
    processScriptFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=25, pady=15)
    rightFrame = ttkCustomWidget.CustomTtkFrame(root)
    rightFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=5, pady=5)
    buttonListFrame = ttkCustomWidget.CustomTtkFrame(rightFrame)
    buttonListFrame.pack(expand=True, fill=tkinter.BOTH)
    smfInfoLabelFrame = ttkCustomWidget.CustomTtkFrame(rightFrame)
    smfInfoLabelFrame.pack(expand=True, fill=tkinter.BOTH)
    smfImageSearchFrame = ttkCustomWidget.CustomTtkFrame(rightFrame)
    smfImageSearchFrame.pack(expand=True, fill=tkinter.BOTH)

    processBar = ttk.Progressbar(processScriptFrame, orient=tkinter.HORIZONTAL, variable=v_process, maximum=100, length=400, mode="determinate")
    processBar.pack(fill=tkinter.X)

    scriptLf = ttkCustomWidget.CustomTtkLabelFrame(processScriptFrame, text=textSetting.textList["smf"]["scriptLabel"])
    scriptLf.pack(expand=True, fill=tkinter.BOTH, pady=15)
    frame = ScrollbarTreeviewSmf(scriptLf, None, None)

    frameEditButtonFrame = ttkCustomWidget.CustomTtkFrame(buttonListFrame)
    frameEditButtonFrame.grid(row=0, column=0, pady=10)
    copyAndPasteFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["copyAndPasteFrameLabel"], width=25, command=copyAndPasteFrame, state="disabled")
    copyAndPasteFrameButton.grid(row=0, column=0, padx=30, pady=5)
    deleteFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["deleteFrameLabel"], width=25, command=deleteFrame, state="disabled")
    deleteFrameButton.grid(row=0, column=1, padx=30, pady=5)
    editInfoFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["editInfoFrameLabel"], width=25, command=editInfoFrame, state="disabled")
    editInfoFrameButton.grid(row=1, column=0, padx=30, pady=5)
    swapFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["swapFrameLabel"], width=25, command=swapFrame, state="disabled")
    swapFrameButton.grid(row=1, column=1, padx=30, pady=5)

    meshEditButtonFrame = ttkCustomWidget.CustomTtkFrame(buttonListFrame)
    meshEditButtonFrame.grid(row=1, column=0, pady=10)
    turnModelMeshButton = ttkCustomWidget.CustomTtkButton(meshEditButtonFrame, text=textSetting.textList["smf"]["turnModelMeshLabel"], width=25, command=turnModelMesh, state="disabled")
    turnModelMeshButton.grid(row=0, column=0, padx=30, pady=5)
    swapModelMeshButton = ttkCustomWidget.CustomTtkButton(meshEditButtonFrame, text=textSetting.textList["smf"]["swapModelMeshLabel"], width=25, command=swapModelMesh, state="disabled")
    swapModelMeshButton.grid(row=0, column=1, padx=30, pady=5)

    elseEditButtonFrame = ttkCustomWidget.CustomTtkFrame(buttonListFrame)
    elseEditButtonFrame.grid(row=2, column=0, pady=10)
    standardButton = ttkCustomWidget.CustomTtkButton(elseEditButtonFrame, text=textSetting.textList["smf"]["createStandardLabel"], width=25, command=createStandardGaugeButton, state="disabled")
    standardButton.grid(row=0, column=0, padx=30, pady=5)
    extract3dObjButton = ttkCustomWidget.CustomTtkButton(elseEditButtonFrame, text=textSetting.textList["smf"]["extract3dLabel"], width=25, command=extract3d, state="disabled")
    extract3dObjButton.grid(row=0, column=1, padx=30, pady=5)

    framePosInfoLf = ttkCustomWidget.CustomTtkLabelFrame(smfInfoLabelFrame, text=textSetting.textList["smf"]["framePosInfoLabel"])
    framePosInfoLf.grid(row=0, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

    v_framePosX = tkinter.DoubleVar()
    framePosXEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=v_framePosX, width=12, state="readonly")
    framePosXEt.grid(row=0, column=0, padx=10, pady=5)

    v_framePosY = tkinter.DoubleVar()
    framePosYEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=v_framePosY, width=12, state="readonly")
    framePosYEt.grid(row=0, column=1, padx=10, pady=5)

    v_framePosZ = tkinter.DoubleVar()
    framePosZEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=v_framePosZ, width=12, state="readonly")
    framePosZEt.grid(row=0, column=2, padx=10, pady=5)


    frameRotInfoLf = ttkCustomWidget.CustomTtkLabelFrame(smfInfoLabelFrame, text=textSetting.textList["smf"]["frameRotInfoLabel"])
    frameRotInfoLf.grid(row=1, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

    v_frameRotX = tkinter.DoubleVar()
    frameRotXEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=v_frameRotX, width=12, state="readonly")
    frameRotXEt.grid(row=0, column=0, padx=10, pady=5)

    v_frameRotY = tkinter.DoubleVar()
    frameRotYEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=v_frameRotY, width=12, state="readonly")
    frameRotYEt.grid(row=0, column=1, padx=10, pady=5)

    v_frameRotZ = tkinter.DoubleVar()
    frameRotZEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=v_frameRotZ, width=12, state="readonly")
    frameRotZEt.grid(row=0, column=2, padx=10, pady=5)


    scanSmfImageButton = ttkCustomWidget.CustomTtkButton(smfImageSearchFrame, text=textSetting.textList["smf"]["scanSmfImageLabel"], width=72, command=scanSmfImage)
    scanSmfImageButton.grid(row=0, column=0, sticky=tkinter.EW, padx=30, pady=5)

    v_modelCount = tkinter.StringVar()
    modelCountEntry = ttkCustomWidget.CustomTtkEntry(smfImageSearchFrame, textvariable=v_modelCount, font=textSetting.textList["defaultFont"], justify="center", state="readonly")
    modelCountEntry.grid(row=1, column=0, sticky=tkinter.EW, padx=30, pady=5)

    noImageListbox = tkinter.Listbox(smfImageSearchFrame, selectmode="single", height=8, font=textSetting.textList["font2"], bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
    noImageListbox.grid(row=2, column=0, sticky=tkinter.EW, padx=30, pady=5)

    v_modelPath = tkinter.StringVar()
    modelPathEntry = ttkCustomWidget.CustomTtkEntry(smfImageSearchFrame, textvariable=v_modelPath, font=textSetting.textList["defaultFont"], state="readonly")
    modelPathEntry.grid(row=3, column=0, sticky=tkinter.EW, padx=30, pady=5)

    copyImageButton = ttkCustomWidget.CustomTtkButton(smfImageSearchFrame, text=textSetting.textList["smf"]["copyImageLabel"], width=50, command=copyImage, state="disabled")
    copyImageButton.grid(row=4, column=0, sticky=tkinter.EW, padx=30, pady=5)
