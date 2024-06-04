import os
import codecs
import sys
import tkinter
import copy
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

import program.orgInfoEditor.importPy.gameDefine as gameDefine
from program.orgInfoEditor.importPy.tkinterTab import tab1AllWidget, tab2AllWidget, tab3AllWidget
from program.orgInfoEditor.importPy.tkinterStageWidget import EditStageInfo

from program.orgInfoEditor.dendDecrypt import LSdecrypt as dendLs
from program.orgInfoEditor.dendDecrypt import BSdecrypt as dendBs
from program.orgInfoEditor.dendDecrypt import CSdecrypt as dendCs
from program.orgInfoEditor.dendDecrypt import RSdecrypt as dendRs
from program.orgInfoEditor.dendDecrypt import SSdecrypt as dendSs

root = None
gameCb = None
trainCb = None
menuCb = None
v_edit = None
edit_stage_train_button = None
tabFrame = None
rootFrameAppearance = None
decryptFile = None
varList = []
btnList = []
defaultData = []
gameDefine.load()


def resource_path(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(os.path.abspath(os.path.dirname(__file__)), "dendData"))
    return os.path.join(bundle_dir, relative_path)


def defaultDataRead(game):
    global defaultData

    defaultData = []
    path = ""
    if game == gameDefine.SS:
        path = resource_path("train_org_data.den")
        defaultDecryptFile = dendSs.SSdecrypt(path)
        errorMsg = textSetting.textList["errorList"]["E4"]
        if not defaultDecryptFile.open():
            defaultDecryptFile.printError()
            if defaultDecryptFile.error != "":
                errorMsg = defaultDecryptFile.error
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return
        trainOrgInfoList = defaultDecryptFile.trainInfoList
        for trainOrgInfo in trainOrgInfoList:
            speedList = trainOrgInfo[0]
            notchCnt = len(speedList) // defaultDecryptFile.notchContentCnt
            perfList = trainOrgInfo[1]
            rainList = trainOrgInfo[2]
            carbList = trainOrgInfo[3]
            otherList = trainOrgInfo[4]
            hurikoList = trainOrgInfo[5]
            oneWheelList = trainOrgInfo[6]
            defaultData.append(
                {
                    "notch": speedList[0:notchCnt],
                    "tlk": speedList[notchCnt:notchCnt*2],
                    "soundNum": speedList[notchCnt*2:notchCnt*3],
                    "add": speedList[notchCnt*3:notchCnt*4],
                    "att": perfList,
                    "rain": rainList,
                    "carb": carbList,
                    "other": otherList,
                    "huriko": hurikoList,
                    "oneWheel": oneWheelList
                })
    else:
        if game == gameDefine.LS:
            path = resource_path("LSdata.txt")
        elif game == gameDefine.BS:
            path = resource_path("BSdata.txt")
        elif game == gameDefine.CS:
            path = resource_path("CSdata.txt")
        elif game == gameDefine.RS:
            path = resource_path("RSdata.txt")

        f = codecs.open(path, "r", "utf-8", "ignore")
        lines = f.readlines()
        f.close()

        count = 1
        mdlCnt = int(lines[0])
        for i in range(mdlCnt):
            name = lines[count].split("\t")[0]
            count += 1

            notchs = [round(float(f), 4) for f in lines[count].split("\t")]
            count += 3

            tlks = [round(float(f), 4) for f in lines[count].split("\t")]
            count += 3

            if game in [gameDefine.CS, gameDefine.RS]:
                soundNums = [int(i) for i in lines[count].split("\t")]
                count += 1
                adds = [round(float(f), 4) for f in lines[count].split("\t")]
                count += 3

            count += 1
            atts = [round(float(f), 5) for f in lines[count].split("\t")]
            count += 3

            if game in [gameDefine.CS, gameDefine.RS]:
                hurikos = [int(i) for i in lines[count].split("\t")]
                count += 1

            if game in [gameDefine.CS, gameDefine.RS]:
                defaultData.append(
                    {
                        "name": name,
                        "notch": notchs,
                        "tlk": tlks,
                        "soundNum": soundNums,
                        "add": adds,
                        "att": atts,
                        "huriko": hurikos,
                    })
            else:
                defaultData.append(
                    {
                        "name": name,
                        "notch": notchs,
                        "tlk": tlks,
                        "att": atts,
                    })


def openFile():
    global gameCb
    global decryptFile

    if gameCb.current() == gameDefine.LS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA.BIN")])
        if file_path:
            del decryptFile
            decryptFile = dendLs.LSdecrypt(file_path)
            defaultDataRead(gameDefine.LS)
    elif gameCb.current() == gameDefine.BS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA2ND.BIN")])
        if file_path:
            del decryptFile
            decryptFile = dendBs.BSdecrypt(file_path)
            defaultDataRead(gameDefine.BS)
    elif gameCb.current() == gameDefine.CS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA3RD.BIN")])
        if file_path:
            del decryptFile
            decryptFile = dendCs.CSdecrypt(file_path)
            defaultDataRead(gameDefine.CS)
    elif gameCb.current() == gameDefine.RS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = dendRs.RSdecrypt(file_path)
            defaultDataRead(gameDefine.RS)
    elif gameCb.current() == gameDefine.SS:
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["orgInfoEditor"]["fileType"], "train_org_data.den")])
        if file_path:
            del decryptFile
            decryptFile = dendSs.SSdecrypt(file_path)
            defaultDataRead(gameDefine.SS)

    errorMsg = textSetting.textList["errorList"]["E4"]
    if file_path:
        if not decryptFile.open():
            decryptFile.printError()
            if decryptFile.error != "":
                errorMsg = decryptFile.error
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        deleteWidget()
        initSelect()


def initSelect():
    global gameCb
    global trainCb
    global menuCb
    global decryptFile
    global defaultData

    trainCb["values"] = modifiedTrainNameList()
    trainCb.current(0)
    trainCb["state"] = "readonly"

    if gameCb.current() > gameDefine.SS:
        menuCb["values"] = textSetting.textList["orgInfoEditor"]["menuComboValues"]
    else:
        menuCb["values"] = textSetting.textList["orgInfoEditor"]["menuComboSSValues"]
    menuCb.current(0)
    menuCb["state"] = "readonly"
    selectInfo(trainCb.current(), menuCb.current())

    edit_stage_train_button["state"] = "normal"


def selectTrain(idx):
    global menuCb
    global decryptFile

    try:
        selectInfo(idx, menuCb.current())
    except Exception:
        errorMsg = textSetting.textList["errorList"]["E14"]
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def selectInfo(trainIdx, index):
    global gameCb
    global trainCb
    global menuCb
    global v_edit
    global edit_stage_train_button
    global tabFrame
    global decryptFile
    global rootFrameAppearance
    deleteWidget()

    widgetList = [
        v_edit,
        trainCb,
        menuCb,
        edit_stage_train_button
    ]
    game = gameCb.current()

    if index == 0:
        tab1AllWidget(tabFrame, decryptFile, trainIdx, game, varList, btnList, defaultData, widgetList, rootFrameAppearance, reloadFile)
    elif index == 1:
        tab2AllWidget(tabFrame, decryptFile, trainIdx, game, defaultData, widgetList, rootFrameAppearance, reloadFile)
    elif index == 2:
        tab3AllWidget(tabFrame, decryptFile, trainIdx, game, widgetList, rootFrameAppearance, reloadFile)


def deleteWidget():
    global tabFrame
    global varList
    global btnList

    children = tabFrame.winfo_children()
    for child in children:
        child.destroy()

    varList = []
    btnList = []


def reloadFile():
    global trainCb
    global decryptFile

    errorMsg = textSetting.textList["errorList"]["E4"]
    if not decryptFile.open():
        decryptFile.printError()
        if decryptFile.error != "":
            errorMsg = decryptFile.error
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        return

    deleteWidget()
    idx = trainCb.current()
    trainCb["values"] = modifiedTrainNameList()
    trainCb.current(idx)
    selectTrain(trainCb.current())


def selectGame():
    global gameCb
    global trainCb
    global menuCb
    global edit_stage_train_button

    deleteWidget()
    trainCb["state"] = "disabled"
    trainCb["values"] = []
    trainCb.set("")

    menuCb["state"] = "disabled"
    menuCb["values"] = []
    menuCb.set("")

    if gameCb.current() in [gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        edit_stage_train_button.grid(row=0, column=3)
        edit_stage_train_button["state"] = "disabled"
    else:
        edit_stage_train_button.grid_remove()


def editStageTrain():
    global root
    global gameCb
    global decryptFile
    global rootFrameAppearance

    index = decryptFile.stageIdx
    if index == -1:
        errorMsg = textSetting.textList["errorList"]["E69"]
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        return

    game = gameCb.current()
    EditStageInfo(root, textSetting.textList["orgInfoEditor"]["editStageLabel"], game, decryptFile, rootFrameAppearance)


def modifiedTrainNameList():
    global gameCb
    global decryptFile
    global defaultData

    copyTrainNameList = copy.deepcopy(decryptFile.trainNameList)
    for index, trainName in enumerate(copyTrainNameList):
        trainOrgInfo = decryptFile.trainInfoList[index]
        if trainOrgInfo is None:
            copyTrainNameList[index] = trainName + textSetting.textList["orgInfoEditor"]["dataCorrupted"]
            continue
        editFlag = False

        speedList = trainOrgInfo[0]
        notchCnt = len(speedList) // decryptFile.notchContentCnt
        defNotchCnt = len(defaultData[index]["notch"])
        if notchCnt != defNotchCnt:
            editFlag = True
        else:
            for i in range(len(speedList)):
                speed = speedList[i]
                if i >= 0 and i < notchCnt:
                    defSpeed = defaultData[index]["notch"][i]
                elif i >= notchCnt and i < notchCnt*2:
                    defSpeed = defaultData[index]["tlk"][i - notchCnt]
                elif i >= notchCnt*2 and i < notchCnt*3:
                    defSpeed = defaultData[index]["soundNum"][i - notchCnt*2]
                elif i >= notchCnt*3 and i < notchCnt*4:
                    defSpeed = defaultData[index]["add"][i - notchCnt*3]
                if speed != defSpeed:
                    editFlag = True
                    break

        perfList = trainOrgInfo[1]
        for i in range(len(perfList)):
            perf = perfList[i]
            defPerf = defaultData[index]["att"][i]
            if perf != defPerf:
                editFlag = True
                break

        if gameCb.current() in [gameDefine.CS, gameDefine.RS]:
            hurikoList = trainOrgInfo[2]
            for i in range(len(hurikoList)):
                huriko = hurikoList[i]
                defHuriko = defaultData[index]["huriko"][i]
                if huriko != defHuriko:
                    editFlag = True
                    break

        if gameCb.current() == gameDefine.SS:
            rainList = trainOrgInfo[2]
            for i in range(len(rainList)):
                rain = rainList[i]
                defRain = defaultData[index]["rain"][i]
                if rain != defRain:
                    editFlag = True
                    break

            carbList = trainOrgInfo[3]
            for i in range(len(carbList)):
                carb = carbList[i]
                defCarb = defaultData[index]["carb"][i]
                if carb != defCarb:
                    editFlag = True
                    break

            otherList = trainOrgInfo[4]
            for i in range(len(otherList)):
                other = otherList[i]
                defOther = defaultData[index]["other"][i]
                if other != defOther:
                    editFlag = True
                    break

            hurikoList = trainOrgInfo[5]
            if hurikoList is not None:
                if defaultData[index]["huriko"] is not None:
                    for i in range(len(hurikoList)):
                        huriko = hurikoList[i]
                        defHuriko = defaultData[index]["huriko"][i]
                        if huriko != defHuriko:
                            editFlag = True
                            break
                else:
                    editFlag = True
            else:
                if defaultData[index]["huriko"] is not None:
                    editFlag = True

            oneWheelList = trainOrgInfo[6]
            if oneWheelList is not None:
                if defaultData[index]["oneWheel"] is not None:
                    for i in range(len(oneWheelList)):
                        oneWheel = oneWheelList[i]
                        defOneWheel = defaultData[index]["oneWheel"][i]
                        if oneWheel != defOneWheel:
                            editFlag = True
                            break
            else:
                if defaultData[index]["oneWheel"] is not None:
                    editFlag = True

        if editFlag:
            copyTrainNameList[index] = trainName + textSetting.textList["orgInfoEditor"]["modified"]

    return copyTrainNameList


def call_orgInfoEditor(rootTk, appearance):
    global root
    global gameCb
    global trainCb
    global menuCb
    global v_edit
    global edit_stage_train_button
    global tabFrame
    global rootFrameAppearance

    root = rootTk
    rootFrameAppearance = appearance

    headerFrame = ttkCustomWidget.CustomTtkFrame(root)
    headerFrame.pack(fill=tkinter.X, padx=40, pady=(25, 0))

    gameCb = ttkCustomWidget.CustomTtkCombobox(headerFrame, width=23, state="readonly", values=gameDefine.gameList)
    gameCb.bind("<<ComboboxSelected>>", lambda e: selectGame())
    gameCb.grid(row=0, column=0, padx=15, pady=(0, 15))
    gameCb.current(0)

    trainCb = ttkCustomWidget.CustomTtkCombobox(headerFrame, width=40, state="disabled")
    trainCb.bind("<<ComboboxSelected>>", lambda e: selectTrain(trainCb.current()))
    trainCb.grid(row=0, column=1, padx=20, pady=(0, 15))

    menuCb = ttkCustomWidget.CustomTtkCombobox(headerFrame, width=30, state="disabled")
    menuCb.bind("<<ComboboxSelected>>", lambda e: selectInfo(trainCb.current(), menuCb.current()))
    menuCb.grid(row=0, column=2, padx=20, pady=(0, 15))

    v_edit = tkinter.StringVar()

    edit_stage_train_button = ttkCustomWidget.CustomTtkButton(headerFrame, text=textSetting.textList["orgInfoEditor"]["editStageDefaultTrain"], width=23, command=editStageTrain, state="disabled")
    edit_stage_train_button.grid(row=0, column=3, padx=20, pady=(0, 10))

    tabFrame = ttkCustomWidget.CustomTtkFrame(root, borderwidth=1, relief="solid")
    tabFrame.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 20))

    selectGame()
