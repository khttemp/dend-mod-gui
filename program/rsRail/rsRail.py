import os
import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from program.rsRail.getMemory.getMemory import GetMemory
from program.tkinterScrollbarFrameClass import ScrollbarFrame


root = None
v_railNo = None
v_ambNo = None
v_fileName = None
contentsLf = None
frame = None
memoryObj = None
railValList = None
railElementList = None
ambValList = None
ambElementList = None
ambChildValList = None
ambChildElementList = None
ambChildModelLf = None


def deleteAllWidget():
    global contentsLf

    for children in contentsLf.winfo_children():
        children.destroy()


def createWidget():
    global v_railNo
    global v_ambNo
    global contentsLf
    global railValList
    global railElementList
    global ambValList
    global ambElementList
    global ambChildModelLf

    railValList = []
    railElementList = []

    railNoFrame = ttk.Frame(contentsLf)
    railNoFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

    railNoLb = ttk.Label(railNoFrame, text="レールNo", font=("", 14))
    railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
    v_railNo = tkinter.IntVar()
    railNoEt = ttk.Entry(railNoFrame, textvariable=v_railNo, font=("", 14), width=7, justify="center")
    railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
    railElementList.append(railNoEt)
    searchBtn = ttk.Button(railNoFrame, text="照会", command=lambda: searchRail())
    searchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)
    railElementList.append(searchBtn)
    modifyBtn = ttk.Button(railNoFrame, text="変更", command=lambda: modifyRail(), state="disabled")
    modifyBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=30)
    railElementList.append(modifyBtn)

    sidePackFrame = ttk.Frame(contentsLf)
    sidePackFrame.pack(anchor=tkinter.NW, padx=20)

    xyzFrame = ttk.LabelFrame(sidePackFrame, text="向きXYZ情報")
    xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
    xLb = ttk.Label(xyzFrame, text="xの向き", font=("", 14))
    xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_x = tkinter.DoubleVar()
    railValList.append(v_x)
    xEt = ttk.Entry(xyzFrame, textvariable=v_x, font=("", 14), width=7, justify="center", state="readonly")
    xEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(xEt)

    yLb = ttk.Label(xyzFrame, text="yの向き", font=("", 14))
    yLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_y = tkinter.DoubleVar()
    railValList.append(v_y)
    yEt = ttk.Entry(xyzFrame, textvariable=v_y, font=("", 14), width=7, justify="center", state="readonly")
    yEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(yEt)

    zLb = ttk.Label(xyzFrame, text="zの向き", font=("", 14))
    zLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_z = tkinter.DoubleVar()
    railValList.append(v_z)
    zEt = ttk.Entry(xyzFrame, textvariable=v_z, font=("", 14), width=7, justify="center", state="readonly")
    zEt.grid(row=0, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(zEt)

    perFrame = ttk.LabelFrame(sidePackFrame, text="モデルのPER")
    perFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)

    perLb = ttk.Label(perFrame, text="per", font=("", 14))
    perLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_per = tkinter.DoubleVar()
    railValList.append(v_per)
    perEt = ttk.Entry(perFrame, textvariable=v_per, font=("", 14), width=7, justify="center", state="readonly")
    perEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(perEt)

    ambValList = []
    ambElementList = []

    ambNoFrame = ttk.Frame(contentsLf)
    ambNoFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

    ambNoLb = ttk.Label(ambNoFrame, text="AMB No", font=("", 14))
    ambNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
    v_ambNo = tkinter.IntVar()
    ambNoEt = ttk.Entry(ambNoFrame, textvariable=v_ambNo, font=("", 14), width=7, justify="center")
    ambNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
    ambElementList.append(ambNoEt)
    ambSearchBtn = ttk.Button(ambNoFrame, text="照会", command=lambda: searchAMB())
    ambSearchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)
    ambElementList.append(ambSearchBtn)
    ambModifyBtn = ttk.Button(ambNoFrame, text="変更", command=lambda: modifyAMB(), state="disabled")
    ambModifyBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=30)
    ambElementList.append(ambModifyBtn)

    ambContentsFrame = ttk.Frame(contentsLf)
    ambContentsFrame.pack(anchor=tkinter.NW, padx=5, fill=tkinter.BOTH, expand=True)

    ambScroll = ScrollbarFrame(ambContentsFrame)
    ambScrollFrame = ambScroll.frame

    ambParentInfoFrame = ttk.Frame(ambScrollFrame)
    ambParentInfoFrame.pack(anchor=tkinter.NW)

    ambParentInfoLf = ttk.LabelFrame(ambParentInfoFrame, text="AMB情報")
    ambParentInfoLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=15, pady=10)

    lengthLb = ttk.Label(ambParentInfoLf, text="長さ", font=("", 14))
    lengthLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_length = tkinter.DoubleVar()
    ambValList.append(v_length)
    lengthEt = ttk.Entry(ambParentInfoLf, textvariable=v_length, font=("", 14), width=7, justify="center", state="readonly")
    lengthEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(lengthEt)

    railNoLb = ttk.Label(ambParentInfoLf, text="配置レールNo", font=("", 14))
    railNoLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambRailNo = tkinter.IntVar()
    ambValList.append(v_ambRailNo)
    ambRailNoEt = ttk.Entry(ambParentInfoLf, textvariable=v_ambRailNo, font=("", 14), width=7, justify="center", state="readonly")
    ambRailNoEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(ambRailNoEt)

    railPosLb = ttk.Label(ambParentInfoLf, text="オフセット", font=("", 14))
    railPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambRailPos = tkinter.IntVar()
    ambValList.append(v_ambRailPos)
    ambRailPosEt = ttk.Entry(ambParentInfoLf, textvariable=v_ambRailPos, font=("", 14), width=7, justify="center", state="readonly")
    ambRailPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(ambRailPosEt)

    ambxyzFrameLf = ttk.LabelFrame(ambParentInfoFrame, text="BASE距離、向きXYZ情報")
    ambxyzFrameLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, pady=15)

    xPosLb = ttk.Label(ambxyzFrameLf, text="xの距離", font=("", 14))
    xPosLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambxPos = tkinter.DoubleVar()
    ambValList.append(v_ambxPos)
    xPosEt = ttk.Entry(ambxyzFrameLf, textvariable=v_ambxPos, font=("", 14), width=7, justify="center", state="readonly")
    xPosEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(xPosEt)

    yPosLb = ttk.Label(ambxyzFrameLf, text="yの距離", font=("", 14))
    yPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambyPos = tkinter.DoubleVar()
    ambValList.append(v_ambyPos)
    yPosEt = ttk.Entry(ambxyzFrameLf, textvariable=v_ambyPos, font=("", 14), width=7, justify="center", state="readonly")
    yPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(yPosEt)

    zPosLb = ttk.Label(ambxyzFrameLf, text="zの距離", font=("", 14))
    zPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambzPos = tkinter.DoubleVar()
    ambValList.append(v_ambzPos)
    zPosEt = ttk.Entry(ambxyzFrameLf, textvariable=v_ambzPos, font=("", 14), width=7, justify="center", state="readonly")
    zPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(zPosEt)

    xRotLb = ttk.Label(ambxyzFrameLf, text="xの向き", font=("", 14))
    xRotLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambxRot = tkinter.DoubleVar()
    ambValList.append(v_ambxRot)
    xRotEt = ttk.Entry(ambxyzFrameLf, textvariable=v_ambxRot, font=("", 14), width=7, justify="center", state="readonly")
    xRotEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(xRotEt)

    yRotLb = ttk.Label(ambxyzFrameLf, text="yの向き", font=("", 14))
    yRotLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambyRot = tkinter.DoubleVar()
    ambValList.append(v_ambyRot)
    yRotEt = ttk.Entry(ambxyzFrameLf, textvariable=v_ambyRot, font=("", 14), width=7, justify="center", state="readonly")
    yRotEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(yRotEt)

    zRotLb = ttk.Label(ambxyzFrameLf, text="zの向き", font=("", 14))
    zRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambzRot = tkinter.DoubleVar()
    ambValList.append(v_ambzRot)
    zRotEt = ttk.Entry(ambxyzFrameLf, textvariable=v_ambzRot, font=("", 14), width=7, justify="center", state="readonly")
    zRotEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(zRotEt)

    ambModelLf = ttk.LabelFrame(ambScrollFrame, text="AMBモデル情報")
    ambModelLf.pack(anchor=tkinter.NW, padx=15, pady=15)
    setAmbModel(ambModelLf, True)

    ambChildModelLf = ttk.LabelFrame(ambScrollFrame, text="AMB子モデル情報")
    ambChildModelLf.pack(anchor=tkinter.NW, padx=15, pady=15)
    ambBlankLb = ttk.Label(ambChildModelLf)
    ambBlankLb.pack()


def setAmbModel(ambModelLf, flag):
    global ambValList
    global ambElementList
    global ambChildValList
    global ambChildElementList

    xyzFrame = ttk.Frame(ambModelLf)
    xyzFrame.pack(anchor=tkinter.NW)
    xMdlPosLb = ttk.Label(xyzFrame, text="xの距離", font=("", 14))
    xMdlPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_xMdlPos = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_xMdlPos)
    else:
        ambChildValList.append(v_xMdlPos)
    xMdlPosEt = ttk.Entry(xyzFrame, textvariable=v_xMdlPos, font=("", 14), width=7, justify="center", state="readonly")
    xMdlPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(xMdlPosEt)
    else:
        ambChildElementList.append(xMdlPosEt)

    yMdlPosLb = ttk.Label(xyzFrame, text="yの距離", font=("", 14))
    yMdlPosLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_yMdlPos = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_yMdlPos)
    else:
        ambChildValList.append(v_yMdlPos)
    yMdlPosEt = ttk.Entry(xyzFrame, textvariable=v_yMdlPos, font=("", 14), width=7, justify="center", state="readonly")
    yMdlPosEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(yMdlPosEt)
    else:
        ambChildElementList.append(yMdlPosEt)

    zMdlPosLb = ttk.Label(xyzFrame, text="zの距離", font=("", 14))
    zMdlPosLb.grid(row=1, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_zMdlPos = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_zMdlPos)
    else:
        ambChildValList.append(v_zMdlPos)
    zMdlPosEt = ttk.Entry(xyzFrame, textvariable=v_zMdlPos, font=("", 14), width=7, justify="center", state="readonly")
    zMdlPosEt.grid(row=1, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(zMdlPosEt)
    else:
        ambChildElementList.append(zMdlPosEt)

    xMdlRotLb = ttk.Label(xyzFrame, text="xの向き", font=("", 14))
    xMdlRotLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_xMdlRot = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_xMdlRot)
    else:
        ambChildValList.append(v_xMdlRot)
    xMdlRotEt = ttk.Entry(xyzFrame, textvariable=v_xMdlRot, font=("", 14), width=7, justify="center", state="readonly")
    xMdlRotEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(xMdlRotEt)
    else:
        ambChildElementList.append(xMdlRotEt)

    yMdlRotLb = ttk.Label(xyzFrame, text="yの向き", font=("", 14))
    yMdlRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_yMdlRot = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_yMdlRot)
    else:
        ambChildValList.append(v_yMdlRot)
    yMdlRotEt = ttk.Entry(xyzFrame, textvariable=v_yMdlRot, font=("", 14), width=7, justify="center", state="readonly")
    yMdlRotEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(yMdlRotEt)
    else:
        ambChildElementList.append(yMdlRotEt)

    zMdlRotLb = ttk.Label(xyzFrame, text="zの向き", font=("", 14))
    zMdlRotLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_zMdlRot = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_zMdlRot)
    else:
        ambChildValList.append(v_zMdlRot)
    zMdlRotEt = ttk.Entry(xyzFrame, textvariable=v_zMdlRot, font=("", 14), width=7, justify="center", state="readonly")
    zMdlRotEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(zMdlRotEt)
    else:
        ambChildElementList.append(zMdlRotEt)

    xMdlRot2Lb = ttk.Label(xyzFrame, text="xの向き(終端)", font=("", 14))
    xMdlRot2Lb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_xMdlRot2 = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_xMdlRot2)
    else:
        ambChildValList.append(v_xMdlRot2)
    xMdlRot2Et = ttk.Entry(xyzFrame, textvariable=v_xMdlRot2, font=("", 14), width=7, justify="center", state="readonly")
    xMdlRot2Et.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(xMdlRot2Et)
    else:
        ambChildElementList.append(xMdlRot2Et)

    yMdlRot2Lb = ttk.Label(xyzFrame, text="yの向き(終端)", font=("", 14))
    yMdlRot2Lb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_yMdlRot2 = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_yMdlRot2)
    else:
        ambChildValList.append(v_yMdlRot2)
    yMdlRot2Et = ttk.Entry(xyzFrame, textvariable=v_yMdlRot2, font=("", 14), width=7, justify="center", state="readonly")
    yMdlRot2Et.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(yMdlRot2Et)
    else:
        ambChildElementList.append(yMdlRot2Et)

    zMdlRot2Lb = ttk.Label(xyzFrame, text="zの向き(終端)", font=("", 14))
    zMdlRot2Lb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_zMdlRot2 = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_zMdlRot2)
    else:
        ambChildValList.append(v_zMdlRot2)
    zMdlRot2Et = ttk.Entry(xyzFrame, textvariable=v_zMdlRot2, font=("", 14), width=7, justify="center", state="readonly")
    zMdlRot2Et.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(zMdlRot2Et)
    else:
        ambChildElementList.append(zMdlRot2Et)

    perLb = ttk.Label(xyzFrame, text="per", font=("", 14))
    perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_per = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_per)
    else:
        ambChildValList.append(v_per)
    perEt = ttk.Entry(xyzFrame, textvariable=v_per, font=("", 14), width=7, justify="center", state="readonly")
    perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(perEt)
    else:
        ambChildElementList.append(perEt)


def searchRail():
    global v_railNo
    global memoryObj

    valList = memoryObj.getRailMemory(v_railNo.get())
    if valList is None:
        errorMsg = "レールのメモリーを参照できません。\nステージを選択してから実行してください"
        mb.showerror(title="エラー", message=errorMsg)
        return
    updateRailValue(valList)


def updateRailValue(valList):
    global railValList
    global railElementList

    modifyBtn = railElementList[2]
    modifyBtn["state"] = "normal"

    for i in range(4):
        railValList[i].set(round(valList[i], 5))


def modifyRail():
    global v_railNo
    global railElementList

    railNoEt = railElementList[0]
    railNoEt["state"] = "disabled"

    searchBtn = railElementList[1]
    searchBtn["state"] = "disabled"

    modifyBtn = railElementList[2]
    modifyBtn["text"] = "保存"
    modifyBtn["command"] = lambda: saveRail(v_railNo.get())

    for i in range(4):
        railElementList[3 + i]["state"] = "normal"


def saveRail(railNo):
    global railValList
    global railElementList
    global memoryObj

    message = "レール{0}のメモリー情報を変更しますか？\nいいえを押すと変更をやめ、検索モードへ移行します。\n(権限問題で上書き失敗することもあります)".format(railNo)
    result = mb.askyesnocancel(title="確認", message=message, icon="warning")
    if result is None:
        return

    railNoEt = railElementList[0]
    railNoEt["state"] = "normal"

    searchBtn = railElementList[1]
    searchBtn["state"] = "normal"

    modifyBtn = railElementList[2]
    modifyBtn["text"] = "変更"
    modifyBtn["command"] = lambda: modifyRail()

    for i in range(4):
        railElementList[3 + i]["state"] = "readonly"

    if result:
        valList = []
        for i in range(4):
            valList.append(railValList[i].get())

        if not memoryObj.saveMemory(railNo, valList):
            memoryObj.printError()
            errorMsg = "レールのメモリーを参照できません。"
            mb.showerror(title="エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="レール{0}のメモリー情報を変更しました。".format(railNo))
    else:
        searchRail()


def searchAMB():
    global v_ambNo
    global memoryObj

    valList = memoryObj.getAMBMemory(v_ambNo.get())
    if valList is None:
        errorMsg = "AMBのメモリーを参照できません。\nステージを選択してから実行してください"
        mb.showerror(title="エラー", message=errorMsg)
        return
    updateAMBValue(valList)


def updateAMBValue(valList):
    global ambValList
    global ambElementList
    global ambChildValList
    global ambChildElementList
    global ambChildModelLf

    ambModifyBtn = ambElementList[2]
    ambModifyBtn["state"] = "normal"

    for i in range(len(ambValList)):
        if i in [1, 2]:
            ambValList[i].set(valList[i])
        else:
            ambValList[i].set(round(valList[i], 5))

    ambChildValList = []
    ambChildElementList = []
    for children in ambChildModelLf.winfo_children():
        children.destroy()

    childIdx = 0
    for childValInfo in valList[-1]:
        setAmbModel(ambChildModelLf, False)
        separator = ttk.Separator(ambChildModelLf, orient="horizontal")
        separator.pack(fill=tkinter.X)

        for i in range(10):
            ambChildValList[childIdx + i].set(round(childValInfo[i], 5))
        childIdx += 10


def modifyAMB():
    global v_ambNo
    global ambElementList
    global ambChildElementList

    ambRailNoEt = ambElementList[0]
    ambRailNoEt["state"] = "disabled"

    ambSearchBtn = ambElementList[1]
    ambSearchBtn["state"] = "disabled"

    ambMmodifyBtn = ambElementList[2]
    ambMmodifyBtn["text"] = "保存"
    ambMmodifyBtn["command"] = lambda: saveAMB(v_ambNo.get())

    for i in range(len(ambElementList) - 3):
        ambElementList[3 + i]["state"] = "normal"

    for i in range(len(ambChildElementList)):
        ambChildElementList[i]["state"] = "normal"


def saveAMB(ambNo):
    global ambValList
    global ambElementList
    global ambChildValList
    global memoryObj

    message = "AMB {0}のメモリー情報を変更しますか？\nいいえを押すと変更をやめ、検索モードへ移行します。\n(権限問題で上書き失敗することもあります)".format(ambNo)
    result = mb.askyesnocancel(title="確認", message=message, icon="warning")
    if result is None:
        return

    ambRailNoEt = ambElementList[0]
    ambRailNoEt["state"] = "normal"

    ambSearchBtn = ambElementList[1]
    ambSearchBtn["state"] = "normal"

    ambModifyBtn = ambElementList[2]
    ambModifyBtn["text"] = "変更"
    ambModifyBtn["command"] = lambda: modifyAMB()

    for i in range(len(ambElementList) - 3):
        ambElementList[3 + i]["state"] = "readonly"

    for i in range(len(ambChildElementList)):
        ambChildElementList[i]["state"] = "readonly"

    if result:
        valList = []
        for i in range(len(ambValList)):
            valList.append(ambValList[i].get())

        childCount = len(ambChildValList) // 10
        childList = []
        offIdx = 0
        for i in range(childCount):
            childInfo = []
            for j in range(10):
                childInfo.append(ambChildValList[offIdx + j].get())
            childList.append(childInfo)
            offIdx += 10
        valList.append(childList)

        if not memoryObj.saveAMBMemory(ambNo, valList):
            memoryObj.printError()
            errorMsg = "AMBのメモリーを参照できません。"
            mb.showerror(title="エラー", message=errorMsg)
            return
        mb.showinfo(title="成功", message="AMB {0}のメモリー情報を変更しました。".format(ambNo))
    else:
        searchAMB()


def openFile():
    global v_fileName
    global memoryObj

    file_path = fd.askopenfilename(filetypes=[("DEND_RS_EXE", "*.exe")])
    if file_path:
        filename = os.path.basename(file_path)
        v_fileName.set(filename)
        del memoryObj
        memoryObj = GetMemory(file_path)
        if not memoryObj.open():
            memoryObj.printError()
            mb.showerror(title="エラー", message=memoryObj.error)
            return
        deleteAllWidget()
        createWidget()


def call_rsRail(rootTk, programFrame):
    global root
    global v_railNo
    global v_fileName
    global contentsLf

    root = rootTk

    v_fileName = tkinter.StringVar()
    fileNameEt = ttk.Entry(programFrame, textvariable=v_fileName, font=("", 14), width=23, state="readonly", justify="center")
    fileNameEt.place(relx=0.053, rely=0.03)

    contentsLf = ttk.LabelFrame(programFrame, text="内容")
    contentsLf.place(relx=0.03, rely=0.07, relwidth=0.95, relheight=0.90)
