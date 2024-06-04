import os
import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

from program.rsRail.getMemory.getMemory import GetMemory
from program.tkinterScrollbarFrameClass import ScrollbarFrame


root = None
rootFrameAppearance = None
v_rail1PRail = None
v_rail1PPos = None
v_rail2PRail = None
v_rail2PPos = None
railPosSearchBtn = None
searchRailFuncId = None
v_railNo = None
v_ambNo = None
v_fileName = None
v_delay = None
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
    global v_rail1PRail
    global v_rail1PPos
    global v_rail2PRail
    global v_rail2PPos
    global railPosSearchBtn
    global v_railNo
    global v_ambNo
    global v_delay
    global contentsLf
    global railValList
    global railElementList
    global ambValList
    global ambElementList
    global ambChildModelLf

    railValList = []
    railElementList = []

    railPosFrame = ttkCustomWidget.CustomTtkFrame(contentsLf)
    railPosFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

    rail1PLf = ttkCustomWidget.CustomTtkLabelFrame(railPosFrame, text=textSetting.textList["rsRail"]["1pRailPos"])
    rail1PLf.pack(anchor=tkinter.NW, side=tkinter.LEFT)

    v_rail1PRail = tkinter.IntVar()
    v_rail1PRail.set(-1)
    rail1PRailLb = ttkCustomWidget.CustomTtkLabel(rail1PLf, textvariable=v_rail1PRail, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
    rail1PRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    v_rail1PPos = tkinter.IntVar()
    v_rail1PPos.set(-1)
    rail1PPosLb = ttkCustomWidget.CustomTtkLabel(rail1PLf, textvariable=v_rail1PPos, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
    rail1PPosLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    rail2PLf = ttkCustomWidget.CustomTtkLabelFrame(railPosFrame, text=textSetting.textList["rsRail"]["2pRailPos"])
    rail2PLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=10)

    v_rail2PRail = tkinter.IntVar()
    v_rail2PRail.set(-1)
    rail2PRailLb = ttkCustomWidget.CustomTtkLabel(rail2PLf, textvariable=v_rail2PRail, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
    rail2PRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    v_rail2PPos = tkinter.IntVar()
    v_rail2PPos.set(-1)
    rail2PPosLb = ttkCustomWidget.CustomTtkLabel(rail2PLf, textvariable=v_rail2PPos, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
    rail2PPosLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    railPosSearchBtn = ttkCustomWidget.CustomTtkButton(railPosFrame, text=textSetting.textList["rsRail"]["trainPosSearchBtnLabel"], command=lambda: searchRailPos())
    railPosSearchBtn.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=10, pady=20)

    railNoFrame = ttkCustomWidget.CustomTtkFrame(contentsLf)
    railNoFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

    railNoLb = ttkCustomWidget.CustomTtkLabel(railNoFrame, text=textSetting.textList["rsRail"]["railNo"], font=textSetting.textList["font2"])
    railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
    v_railNo = tkinter.IntVar()
    railNoEt = ttkCustomWidget.CustomTtkEntry(railNoFrame, textvariable=v_railNo, font=textSetting.textList["font2"], width=7, justify="center")
    railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
    railElementList.append(railNoEt)
    searchBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["rsRail"]["railSearchBtnLabel"], command=lambda: searchRail())
    searchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)
    railElementList.append(searchBtn)
    modifyBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["rsRail"]["railChangeBtnLabel"], command=lambda: modifyRail(), state="disabled")
    modifyBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=30)
    railElementList.append(modifyBtn)

    sidePackFrame = ttkCustomWidget.CustomTtkFrame(contentsLf)
    sidePackFrame.pack(anchor=tkinter.NW, padx=20)

    xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["rsRail"]["railXyzInfo"])
    xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
    xLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["railDirX"], font=textSetting.textList["font2"])
    xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_x = tkinter.DoubleVar()
    railValList.append(v_x)
    xEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_x, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    xEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(xEt)

    yLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["railDirY"], font=textSetting.textList["font2"])
    yLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_y = tkinter.DoubleVar()
    railValList.append(v_y)
    yEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_y, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    yEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(yEt)

    zLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["railDirZ"], font=textSetting.textList["font2"])
    zLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_z = tkinter.DoubleVar()
    railValList.append(v_z)
    zEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_z, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    zEt.grid(row=0, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(zEt)

    perFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["rsRail"]["railModelPer"])
    perFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)

    perLb = ttkCustomWidget.CustomTtkLabel(perFrame, text=textSetting.textList["rsRail"]["railPer"], font=textSetting.textList["font2"])
    perLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_per = tkinter.DoubleVar()
    railValList.append(v_per)
    perEt = ttkCustomWidget.CustomTtkEntry(perFrame, textvariable=v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    perEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    railElementList.append(perEt)

    ambValList = []
    ambElementList = []

    ambNoFrame = ttkCustomWidget.CustomTtkFrame(contentsLf)
    ambNoFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

    ambNoLb = ttkCustomWidget.CustomTtkLabel(ambNoFrame, text=textSetting.textList["rsRail"]["ambNo"], font=textSetting.textList["font2"])
    ambNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
    v_ambNo = tkinter.IntVar()
    ambNoEt = ttkCustomWidget.CustomTtkEntry(ambNoFrame, textvariable=v_ambNo, font=textSetting.textList["font2"], width=7, justify="center")
    ambNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
    ambElementList.append(ambNoEt)
    ambSearchBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, text=textSetting.textList["rsRail"]["ambSearchBtnLabel"], command=lambda: searchAMB())
    ambSearchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)
    ambElementList.append(ambSearchBtn)
    ambModifyBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, text=textSetting.textList["rsRail"]["ambChangeBtnLabel"], command=lambda: modifyAMB(), state="disabled")
    ambModifyBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=30)
    ambElementList.append(ambModifyBtn)

    delayLb = ttkCustomWidget.CustomTtkLabel(ambNoFrame, text=textSetting.textList["rsRail"]["ambRecreateTime"], font=textSetting.textList["font2"])
    delayLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)
    v_delay = tkinter.DoubleVar()
    v_delay.set(0.3)
    delayEt = ttkCustomWidget.CustomTtkEntry(ambNoFrame, textvariable=v_delay, font=textSetting.textList["font2"], width=7, justify="center")
    delayEt.grid(row=0, column=5, sticky=tkinter.W + tkinter.E, padx=10)

    ambContentsFrame = ttkCustomWidget.CustomTtkFrame(contentsLf)
    ambContentsFrame.pack(anchor=tkinter.NW, padx=5, fill=tkinter.BOTH, expand=True)

    ambScroll = ScrollbarFrame(ambContentsFrame)
    ambScroll.pack(expand=True, fill=tkinter.BOTH)
    ambScrollFrame = ambScroll.interior

    ambParentInfoFrame = ttkCustomWidget.CustomTtkFrame(ambScrollFrame)
    ambParentInfoFrame.pack(anchor=tkinter.NW)

    ambParentInfoLf = ttkCustomWidget.CustomTtkLabelFrame(ambParentInfoFrame, text=textSetting.textList["rsRail"]["ambInfoLabel"])
    ambParentInfoLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=15, pady=10)

    lengthLb = ttkCustomWidget.CustomTtkLabel(ambParentInfoLf, text=textSetting.textList["rsRail"]["ambLength"], font=textSetting.textList["font2"])
    lengthLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_length = tkinter.DoubleVar()
    ambValList.append(v_length)
    lengthEt = ttkCustomWidget.CustomTtkEntry(ambParentInfoLf, textvariable=v_length, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    lengthEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(lengthEt)

    railNoLb = ttkCustomWidget.CustomTtkLabel(ambParentInfoLf, text=textSetting.textList["rsRail"]["ambRailNo"], font=textSetting.textList["font2"])
    railNoLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambRailNo = tkinter.IntVar()
    ambValList.append(v_ambRailNo)
    ambRailNoEt = ttkCustomWidget.CustomTtkEntry(ambParentInfoLf, textvariable=v_ambRailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    ambRailNoEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(ambRailNoEt)

    railPosLb = ttkCustomWidget.CustomTtkLabel(ambParentInfoLf, text=textSetting.textList["rsRail"]["ambRailPos"], font=textSetting.textList["font2"])
    railPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambRailPos = tkinter.IntVar()
    ambValList.append(v_ambRailPos)
    ambRailPosEt = ttkCustomWidget.CustomTtkEntry(ambParentInfoLf, textvariable=v_ambRailPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    ambRailPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(ambRailPosEt)

    ambxyzFrameLf = ttkCustomWidget.CustomTtkLabelFrame(ambParentInfoFrame, text=textSetting.textList["rsRail"]["ambPosDirInfo"])
    ambxyzFrameLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, pady=10)

    xPosLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBasePosX"], font=textSetting.textList["font2"])
    xPosLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambxPos = tkinter.DoubleVar()
    ambValList.append(v_ambxPos)
    xPosEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=v_ambxPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    xPosEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(xPosEt)

    yPosLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBasePosY"], font=textSetting.textList["font2"])
    yPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambyPos = tkinter.DoubleVar()
    ambValList.append(v_ambyPos)
    yPosEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=v_ambyPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    yPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(yPosEt)

    zPosLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBasePosZ"], font=textSetting.textList["font2"])
    zPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambzPos = tkinter.DoubleVar()
    ambValList.append(v_ambzPos)
    zPosEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=v_ambzPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    zPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(zPosEt)

    xRotLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBaseDirX"], font=textSetting.textList["font2"])
    xRotLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambxRot = tkinter.DoubleVar()
    ambValList.append(v_ambxRot)
    xRotEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=v_ambxRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    xRotEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(xRotEt)

    yRotLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBaseDirY"], font=textSetting.textList["font2"])
    yRotLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambyRot = tkinter.DoubleVar()
    ambValList.append(v_ambyRot)
    yRotEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=v_ambyRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    yRotEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(yRotEt)

    zRotLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBaseDirZ"], font=textSetting.textList["font2"])
    zRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_ambzRot = tkinter.DoubleVar()
    ambValList.append(v_ambzRot)
    zRotEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=v_ambzRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    zRotEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    ambElementList.append(zRotEt)

    ambModelLf = ttkCustomWidget.CustomTtkLabelFrame(ambScrollFrame, text=textSetting.textList["rsRail"]["ambModelInfo"])
    ambModelLf.pack(anchor=tkinter.NW, padx=15, pady=15)
    setAmbModel(ambModelLf, True)

    ambChildModelLf = ttkCustomWidget.CustomTtkLabelFrame(ambScrollFrame, text=textSetting.textList["rsRail"]["ambChildModelInfo"])
    ambChildModelLf.pack(anchor=tkinter.NW, padx=15, pady=15)
    ambBlankLb = ttkCustomWidget.CustomTtkLabel(ambChildModelLf)
    ambBlankLb.pack()


def setAmbModel(ambModelLf, flag):
    global ambValList
    global ambElementList
    global ambChildValList
    global ambChildElementList

    xyzFrame = ttkCustomWidget.CustomTtkFrame(ambModelLf)
    xyzFrame.pack(anchor=tkinter.NW)
    xMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPosX"], font=textSetting.textList["font2"])
    xMdlPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_xMdlPos = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_xMdlPos)
    else:
        ambChildValList.append(v_xMdlPos)
    xMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_xMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    xMdlPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(xMdlPosEt)
    else:
        ambChildElementList.append(xMdlPosEt)

    yMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPosY"], font=textSetting.textList["font2"])
    yMdlPosLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_yMdlPos = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_yMdlPos)
    else:
        ambChildValList.append(v_yMdlPos)
    yMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_yMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    yMdlPosEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(yMdlPosEt)
    else:
        ambChildElementList.append(yMdlPosEt)

    zMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPosZ"], font=textSetting.textList["font2"])
    zMdlPosLb.grid(row=1, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_zMdlPos = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_zMdlPos)
    else:
        ambChildValList.append(v_zMdlPos)
    zMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_zMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    zMdlPosEt.grid(row=1, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(zMdlPosEt)
    else:
        ambChildElementList.append(zMdlPosEt)

    xMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelDirX"], font=textSetting.textList["font2"])
    xMdlRotLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_xMdlRot = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_xMdlRot)
    else:
        ambChildValList.append(v_xMdlRot)
    xMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_xMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    xMdlRotEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(xMdlRotEt)
    else:
        ambChildElementList.append(xMdlRotEt)

    yMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelDirY"], font=textSetting.textList["font2"])
    yMdlRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_yMdlRot = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_yMdlRot)
    else:
        ambChildValList.append(v_yMdlRot)
    yMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_yMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    yMdlRotEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(yMdlRotEt)
    else:
        ambChildElementList.append(yMdlRotEt)

    zMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelDirZ"], font=textSetting.textList["font2"])
    zMdlRotLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_zMdlRot = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_zMdlRot)
    else:
        ambChildValList.append(v_zMdlRot)
    zMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_zMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    zMdlRotEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(zMdlRotEt)
    else:
        ambChildElementList.append(zMdlRotEt)

    xMdlRot2Lb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelRotX"], font=textSetting.textList["font2"])
    xMdlRot2Lb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_xMdlRot2 = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_xMdlRot2)
    else:
        ambChildValList.append(v_xMdlRot2)
    xMdlRot2Et = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_xMdlRot2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    xMdlRot2Et.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(xMdlRot2Et)
    else:
        ambChildElementList.append(xMdlRot2Et)

    yMdlRot2Lb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelRotY"], font=textSetting.textList["font2"])
    yMdlRot2Lb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_yMdlRot2 = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_yMdlRot2)
    else:
        ambChildValList.append(v_yMdlRot2)
    yMdlRot2Et = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_yMdlRot2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    yMdlRot2Et.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(yMdlRot2Et)
    else:
        ambChildElementList.append(yMdlRot2Et)

    zMdlRot2Lb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelRotZ"], font=textSetting.textList["font2"])
    zMdlRot2Lb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_zMdlRot2 = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_zMdlRot2)
    else:
        ambChildValList.append(v_zMdlRot2)
    zMdlRot2Et = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_zMdlRot2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    zMdlRot2Et.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(zMdlRot2Et)
    else:
        ambChildElementList.append(zMdlRot2Et)

    perLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPer"], font=textSetting.textList["font2"])
    perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    v_per = tkinter.DoubleVar()
    if flag:
        ambValList.append(v_per)
    else:
        ambChildValList.append(v_per)
    perEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
    perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
    if flag:
        ambElementList.append(perEt)
    else:
        ambChildElementList.append(perEt)


def searchRailPos():
    global railPosSearchBtn

    railPosSearchBtn["text"] = textSetting.textList["rsRail"]["trainPosStopBtnLabel"]
    railPosSearchBtn["command"] = lambda: searchRailPosExit()
    railPosUpdate()


def railPosUpdate():
    global v_rail1PRail
    global v_rail1PPos
    global v_rail2PRail
    global v_rail2PPos
    global railPosSearchBtn
    global searchRailFuncId
    global memoryObj

    try:
        val1PList = memoryObj.getRailPos(0)
        if val1PList is not None:
            v_rail1PRail.set(val1PList[0])
            v_rail1PPos.set(val1PList[1])
        else:
            v_rail1PRail.set(-1)
            v_rail1PPos.set(-1)
    except Exception:
        v_rail1PRail.set(-1)
        v_rail1PPos.set(-1)

    try:
        val2PList = memoryObj.getRailPos(1)
        if val2PList is not None:
            v_rail2PRail.set(val2PList[0])
            v_rail2PPos.set(val2PList[1])
        else:
            v_rail2PRail.set(-1)
            v_rail2PPos.set(-1)
    except Exception:
        v_rail2PRail.set(-1)
        v_rail2PPos.set(-1)

    searchRailFuncId = railPosSearchBtn.after(1, railPosUpdate)


def searchRailPosExit():
    global searchRailFuncId
    global railPosSearchBtn

    railPosSearchBtn.after_cancel(searchRailFuncId)
    railPosSearchBtn["text"] = textSetting.textList["rsRail"]["trainPosSearchBtnLabel"]
    railPosSearchBtn["command"] = lambda: searchRailPos()


def searchRail():
    global v_railNo
    global memoryObj

    try:
        valList = memoryObj.getRailMemory(v_railNo.get())
    except Exception:
        errorMsg = textSetting.textList["errorList"]["E60"]
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        return

    if valList is None:
        errorMsg = textSetting.textList["errorList"]["E79"]
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
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
    modifyBtn["text"] = textSetting.textList["rsRail"]["saveBtnLabel"]
    modifyBtn["command"] = lambda: saveRail(v_railNo.get())

    for i in range(4):
        railElementList[3 + i]["state"] = "normal"


def saveRail(railNo):
    global railValList
    global railElementList
    global memoryObj

    message = textSetting.textList["infoList"]["I98"].format(railNo)
    result = mb.askyesnocancel(title=textSetting.textList["confirm"], message=message, icon="warning")
    if result is None:
        return

    railNoEt = railElementList[0]
    railNoEt["state"] = "normal"

    searchBtn = railElementList[1]
    searchBtn["state"] = "normal"

    modifyBtn = railElementList[2]
    modifyBtn["text"] = textSetting.textList["rsRail"]["modifyBtnLabel"]
    modifyBtn["command"] = lambda: modifyRail()

    for i in range(4):
        railElementList[3 + i]["state"] = "readonly"

    if result:
        valList = []
        try:
            for i in range(4):
                valList.append(railValList[i].get())
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E3"]
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        if not memoryObj.saveMemory(railNo, valList):
            memoryObj.printError()
            errorMsg = textSetting.textList["errorList"]["E80"]
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I99"].format(railNo))
    else:
        searchRail()


def searchAMB():
    global v_ambNo
    global memoryObj

    try:
        valList = memoryObj.getAMBMemory(v_ambNo.get())
    except Exception:
        errorMsg = textSetting.textList["errorList"]["E60"]
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        return

    if valList is None:
        errorMsg = textSetting.textList["errorList"]["E81"]
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
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
        separator = ttkCustomWidget.CustomTtkSeparator(ambChildModelLf, orient="horizontal")
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
    ambMmodifyBtn["text"] = textSetting.textList["rsRail"]["saveBtnLabel"]
    ambMmodifyBtn["command"] = lambda: saveAMB(v_ambNo.get())

    for i in range(len(ambElementList) - 3):
        ambElementList[3 + i]["state"] = "normal"

    for i in range(len(ambChildElementList)):
        ambChildElementList[i]["state"] = "normal"


def saveAMB(ambNo):
    global v_delay
    global ambValList
    global ambElementList
    global ambChildValList
    global memoryObj

    message = textSetting.textList["infoList"]["I100"].format(ambNo)
    result = mb.askyesnocancel(title=textSetting.textList["confirm"], message=message, icon="warning")
    if result is None:
        return

    ambRailNoEt = ambElementList[0]
    ambRailNoEt["state"] = "normal"

    ambSearchBtn = ambElementList[1]
    ambSearchBtn["state"] = "normal"

    ambModifyBtn = ambElementList[2]
    ambModifyBtn["text"] = textSetting.textList["rsRail"]["modifyBtnLabel"]
    ambModifyBtn["command"] = lambda: modifyAMB()

    for i in range(len(ambElementList) - 3):
        ambElementList[3 + i]["state"] = "readonly"

    for i in range(len(ambChildElementList)):
        ambChildElementList[i]["state"] = "readonly"

    if result:
        valList = []
        try:
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
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E3"]
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        delay = 0.3
        try:
            delay = v_delay.get()
        except Exception:
            v_delay.set(0.3)

        if not memoryObj.saveAMBMemory(ambNo, valList, delay):
            memoryObj.printError()
            errorMsg = textSetting.textList["errorList"]["E82"]
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I101"].format(ambNo))
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
            mb.showerror(title=textSetting.textList["error"], message=memoryObj.error)
            return
        deleteAllWidget()
        createWidget()


def call_rsRail(rootTk, appearance):
    global root
    global rootFrameAppearance
    global v_railNo
    global v_fileName
    global contentsLf

    root = rootTk
    rootFrameAppearance = appearance

    v_fileName = tkinter.StringVar()
    fileNameEt = ttkCustomWidget.CustomTtkEntry(root, textvariable=v_fileName, font=textSetting.textList["font2"], width=32, state="readonly", justify="center")
    fileNameEt.pack(padx=(50, 0), pady=(10, 0), anchor=tkinter.NW)

    contentsLf = ttkCustomWidget.CustomTtkLabelFrame(root, text=textSetting.textList["rsRail"]["contents"])
    contentsLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))
