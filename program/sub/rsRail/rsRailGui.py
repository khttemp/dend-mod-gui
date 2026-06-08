import os
import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.rsRail.getMemory.getMemory import GetMemory
from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame


class RsRailWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict):
        super().__init__(master)
        self.master = master
        self.importDict = importDict
        self.memoryObj = None
        self.searchRailFuncId = None

        self.v_fileName = tkinter.StringVar()
        fileNameEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_fileName, font=textSetting.textList["font2"], width=32, state="readonly", justify="center")
        fileNameEt.pack(padx=(50, 0), pady=(10, 0), anchor=tkinter.NW)

        self.contentsLf = ttkCustomWidget.CustomTtkLabelFrame(master, text=textSetting.textList["rsRail"]["contents"])
        self.contentsLf.pack(expand=True, fill=tkinter.BOTH, padx=25, pady=(0, 25))
    
    def delelteWidget(self):
        for children in self.contentsLf.winfo_children():
            children.destroy()

    def createWidget(self):
        self.createRailPosWidget()
        self.createRailNoWidget()
        self.createAmbNoWidget()
        self.createAmbModelWidget()

    def createRailPosWidget(self):
        railPosFrame = ttkCustomWidget.CustomTtkFrame(self.contentsLf)
        railPosFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

        rail1PLf = ttkCustomWidget.CustomTtkLabelFrame(railPosFrame, text=textSetting.textList["rsRail"]["1pRailPos"])
        rail1PLf.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        self.v_rail1PRail = tkinter.IntVar()
        self.v_rail1PRail.set(-1)
        rail1PRailLb = ttkCustomWidget.CustomTtkLabel(rail1PLf, textvariable=self.v_rail1PRail, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
        rail1PRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        self.v_rail1PPos = tkinter.IntVar()
        self.v_rail1PPos.set(-1)
        rail1PPosLb = ttkCustomWidget.CustomTtkLabel(rail1PLf, textvariable=self.v_rail1PPos, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
        rail1PPosLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        rail2PLf = ttkCustomWidget.CustomTtkLabelFrame(railPosFrame, text=textSetting.textList["rsRail"]["2pRailPos"])
        rail2PLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=10)

        self.v_rail2PRail = tkinter.IntVar()
        self.v_rail2PRail.set(-1)
        rail2PRailLb = ttkCustomWidget.CustomTtkLabel(rail2PLf, textvariable=self.v_rail2PRail, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
        rail2PRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        self.v_rail2PPos = tkinter.IntVar()
        self.v_rail2PPos.set(-1)
        rail2PPosLb = ttkCustomWidget.CustomTtkLabel(rail2PLf, textvariable=self.v_rail2PPos, font=textSetting.textList["font2"], width=7, justify="center", anchor="center")
        rail2PPosLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        self.railPosSearchBtn = ttkCustomWidget.CustomTtkButton(railPosFrame, text=textSetting.textList["rsRail"]["trainPosSearchBtnLabel"], command=self.searchRailPos)
        self.railPosSearchBtn.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=10, pady=20)

        self.railPosSearchStopBtn = ttkCustomWidget.CustomTtkButton(railPosFrame, text=textSetting.textList["rsRail"]["trainPosStopBtnLabel"], command=self.searchRailPosStop)

    def createRailNoWidget(self):
        railNoFrame = ttkCustomWidget.CustomTtkFrame(self.contentsLf)
        railNoFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

        railNoLb = ttkCustomWidget.CustomTtkLabel(railNoFrame, text=textSetting.textList["rsRail"]["railNo"], font=textSetting.textList["font2"])
        railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_railNo = tkinter.IntVar()
        self.railNoEt = ttkCustomWidget.CustomTtkEntry(railNoFrame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center")
        self.railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
        self.railSearchBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["rsRail"]["railSearchBtnLabel"], command=self.searchRail)
        self.railSearchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)
        self.railModifyBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["rsRail"]["railChangeBtnLabel"], command=self.modifyRail, state="disabled")
        self.railModifyBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=30)
        self.railSaveBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["rsRail"]["saveBtnLabel"], command=self.saveRail)
        self.railSaveBtn.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=30)
        self.railSaveBtn.grid_remove()

        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.contentsLf)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)

        xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["rsRail"]["railXyzInfo"])
        xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)

        xLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["railDirX"], font=textSetting.textList["font2"])
        xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railDirX = tkinter.DoubleVar()
        self.railDirXEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_railDirX, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.railDirXEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["railDirY"], font=textSetting.textList["font2"])
        yLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railDirY = tkinter.DoubleVar()
        self.railDirYEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_railDirY, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.railDirYEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["railDirZ"], font=textSetting.textList["font2"])
        zLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railDirZ = tkinter.DoubleVar()
        self.railDirZEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_railDirZ, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.railDirZEt.grid(row=0, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        perFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["rsRail"]["railModelPer"])
        perFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)

        perLb = ttkCustomWidget.CustomTtkLabel(perFrame, text=textSetting.textList["rsRail"]["railPer"], font=textSetting.textList["font2"])
        perLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railPer = tkinter.DoubleVar()
        self.railPerEt = ttkCustomWidget.CustomTtkEntry(perFrame, textvariable=self.v_railPer, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.railPerEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def createAmbNoWidget(self):
        ambNoFrame = ttkCustomWidget.CustomTtkFrame(self.contentsLf)
        ambNoFrame.pack(anchor=tkinter.NW, padx=30, pady=10, fill=tkinter.X)

        ambNoLb = ttkCustomWidget.CustomTtkLabel(ambNoFrame, text=textSetting.textList["rsRail"]["ambNo"], font=textSetting.textList["font2"])
        ambNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_ambNo = tkinter.IntVar()
        self.ambNoEt = ttkCustomWidget.CustomTtkEntry(ambNoFrame, textvariable=self.v_ambNo, font=textSetting.textList["font2"], width=7, justify="center")
        self.ambNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
        self.ambSearchBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, text=textSetting.textList["rsRail"]["ambSearchBtnLabel"], command=self.searchAMB)
        self.ambSearchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)
        self.ambModifyBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, text=textSetting.textList["rsRail"]["ambChangeBtnLabel"], command=self.modifyAMB, state="disabled")
        self.ambModifyBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=30)
        self.ambSaveBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, text=textSetting.textList["rsRail"]["saveBtnLabel"], command=self.saveAMB)
        self.ambSaveBtn.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=30)
        self.ambSaveBtn.grid_remove()

        delayLb = ttkCustomWidget.CustomTtkLabel(ambNoFrame, text=textSetting.textList["rsRail"]["ambRecreateTime"], font=textSetting.textList["font2"])
        delayLb.grid(row=0, column=5, sticky=tkinter.W + tkinter.E)
        self.v_delay = tkinter.DoubleVar()
        self.v_delay.set(0.3)
        delayEt = ttkCustomWidget.CustomTtkEntry(ambNoFrame, textvariable=self.v_delay, font=textSetting.textList["font2"], width=7, justify="center")
        delayEt.grid(row=0, column=6, sticky=tkinter.W + tkinter.E, padx=10)

    def createAmbModelWidget(self):
        self.ambParentValList = []
        self.ambParentWidgetList = []
        self.ambChildVarList = []
        self.ambChildWidgetList = []

        ambContentsFrame = ttkCustomWidget.CustomTtkFrame(self.contentsLf)
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
        self.v_length = tkinter.DoubleVar()
        self.ambParentValList.append(self.v_length)
        self.lengthEt = ttkCustomWidget.CustomTtkEntry(ambParentInfoLf, textvariable=self.v_length, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.lengthEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.lengthEt)

        railNoLb = ttkCustomWidget.CustomTtkLabel(ambParentInfoLf, text=textSetting.textList["rsRail"]["ambRailNo"], font=textSetting.textList["font2"])
        railNoLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambRailNo = tkinter.IntVar()
        self.ambParentValList.append(self.v_ambRailNo)
        self.ambRailNoEt = ttkCustomWidget.CustomTtkEntry(ambParentInfoLf, textvariable=self.v_ambRailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambRailNoEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambRailNoEt)

        railPosLb = ttkCustomWidget.CustomTtkLabel(ambParentInfoLf, text=textSetting.textList["rsRail"]["ambRailPos"], font=textSetting.textList["font2"])
        railPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambRailPos = tkinter.IntVar()
        self.ambParentValList.append(self.v_ambRailPos)
        self.ambRailPosEt = ttkCustomWidget.CustomTtkEntry(ambParentInfoLf, textvariable=self.v_ambRailPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambRailPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambRailPosEt)

        ambxyzFrameLf = ttkCustomWidget.CustomTtkLabelFrame(ambParentInfoFrame, text=textSetting.textList["rsRail"]["ambPosDirInfo"])
        ambxyzFrameLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, pady=10)

        xPosLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBasePosX"], font=textSetting.textList["font2"])
        xPosLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambBasePosX = tkinter.DoubleVar()
        self.ambParentValList.append(self.v_ambBasePosX)
        self.ambBasePosXEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=self.v_ambBasePosX, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambBasePosXEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambBasePosXEt)

        yPosLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBasePosY"], font=textSetting.textList["font2"])
        yPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambBasePosY = tkinter.DoubleVar()
        self.ambParentValList.append(self.v_ambBasePosY)
        self.ambBasePosYEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=self.v_ambBasePosY, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambBasePosYEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambBasePosYEt)

        zPosLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBasePosZ"], font=textSetting.textList["font2"])
        zPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambBasePosZ = tkinter.DoubleVar()
        self.ambParentValList.append(self.v_ambBasePosZ)
        self.ambBasePosZEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=self.v_ambBasePosZ, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambBasePosZEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambBasePosZEt)

        xRotLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBaseRotX"], font=textSetting.textList["font2"])
        xRotLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambBaseRotX = tkinter.DoubleVar()
        self.ambParentValList.append(self.v_ambBaseRotX)
        self.ambBaseRotXEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=self.v_ambBaseRotX, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambBaseRotXEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambBaseRotXEt)

        yRotLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBaseRotY"], font=textSetting.textList["font2"])
        yRotLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambBaseRotY = tkinter.DoubleVar()
        self.ambParentValList.append(self.v_ambBaseRotY)
        self.ambBaseRotYEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=self.v_ambBaseRotY, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambBaseRotYEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambBaseRotYEt)

        zRotLb = ttkCustomWidget.CustomTtkLabel(ambxyzFrameLf, text=textSetting.textList["rsRail"]["ambBaseRotZ"], font=textSetting.textList["font2"])
        zRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_ambBaseRotZ = tkinter.DoubleVar()
        self.ambParentValList.append(self.v_ambBaseRotZ)
        self.ambBaseRotZEt = ttkCustomWidget.CustomTtkEntry(ambxyzFrameLf, textvariable=self.v_ambBaseRotZ, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.ambBaseRotZEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambParentWidgetList.append(self.ambBaseRotZEt)

        ambModelLf = ttkCustomWidget.CustomTtkLabelFrame(ambScrollFrame, text=textSetting.textList["rsRail"]["ambModelInfo"])
        ambModelLf.pack(anchor=tkinter.NW, padx=15, pady=15)
        self.setAmbModelInfo(ambModelLf, self.ambParentValList, self.ambParentWidgetList)

        self.ambChildModelLf = ttkCustomWidget.CustomTtkLabelFrame(ambScrollFrame, text=textSetting.textList["rsRail"]["ambChildModelInfo"])
        self.ambChildModelLf.pack(anchor=tkinter.NW, padx=15, pady=15)
        ambBlankLb = ttkCustomWidget.CustomTtkLabel(self.ambChildModelLf)
        ambBlankLb.pack()

    def setAmbModelInfo(self, parent, varList, widgetList, childFlag=False, childNo=None):
        if childFlag:
            ambModelNameLb = ttkCustomWidget.CustomTtkLabel(parent, text=textSetting.textList["rsRail"]["ambChildModelSmf"].format(childNo), font=textSetting.textList["font2"])
        else:
            ambModelNameLb = ttkCustomWidget.CustomTtkLabel(parent, text=textSetting.textList["rsRail"]["ambModelSmf"], font=textSetting.textList["font2"])
        ambModelNameLb.pack(anchor=tkinter.NW, padx=10)

        xyzFrame = ttkCustomWidget.CustomTtkFrame(parent)
        xyzFrame.pack()
        xMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPosX"], font=textSetting.textList["font2"])
        xMdlPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_xMdlPos = tkinter.DoubleVar()
        varList.append(v_xMdlPos)
        xMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_xMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(xMdlPosEt)

        yMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPosY"], font=textSetting.textList["font2"])
        yMdlPosLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_yMdlPos = tkinter.DoubleVar()
        varList.append(v_yMdlPos)
        yMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_yMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlPosEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(yMdlPosEt)

        zMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPosZ"], font=textSetting.textList["font2"])
        zMdlPosLb.grid(row=1, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_zMdlPos = tkinter.DoubleVar()
        varList.append(v_zMdlPos)
        zMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_zMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlPosEt.grid(row=1, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(zMdlPosEt)

        xMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelDirX"], font=textSetting.textList["font2"])
        xMdlDirLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_xMdlDir = tkinter.DoubleVar()
        varList.append(v_xMdlDir)
        xMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_xMdlDir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlDirEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(xMdlDirEt)

        yMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelDirY"], font=textSetting.textList["font2"])
        yMdlDirLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_yMdlDir = tkinter.DoubleVar()
        varList.append(v_yMdlDir)
        yMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_yMdlDir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlDirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(yMdlDirEt)

        zMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelDirZ"], font=textSetting.textList["font2"])
        zMdlDirLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_zMdlDir = tkinter.DoubleVar()
        varList.append(v_zMdlDir)
        zMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_zMdlDir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlDirEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(zMdlDirEt)

        xMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelRotX"], font=textSetting.textList["font2"])
        xMdlRotLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_xMdlRot = tkinter.DoubleVar()
        varList.append(v_xMdlRot)
        xMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_xMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlRotEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(xMdlRotEt)

        yMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelRotY"], font=textSetting.textList["font2"])
        yMdlRotLb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_yMdlRot = tkinter.DoubleVar()
        varList.append(v_yMdlRot)
        yMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_yMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlRotEt.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(yMdlRotEt)

        zMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelRotZ"], font=textSetting.textList["font2"])
        zMdlRotLb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_zMdlRot = tkinter.DoubleVar()
        varList.append(v_zMdlRot)
        zMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_zMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlRotEt.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(zMdlRotEt)

        perLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["rsRail"]["ambModelPer"], font=textSetting.textList["font2"])
        perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        v_per = tkinter.DoubleVar()
        varList.append(v_per)
        perEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        widgetList.append(perEt)

    def setAmbChildModel(self, childValList):
        children = self.ambChildModelLf.winfo_children()
        for child in children:
            child.destroy()

        if len(childValList) == 0:
            ambBlankLb = ttkCustomWidget.CustomTtkLabel(self.ambChildModelLf)
            ambBlankLb.pack()
            return

        self.ambChildVarList = []
        self.ambChildWidgetList = []
        for idx, childValInfo in enumerate(childValList):
            childVarList = []
            childWidgetList = []
            self.setAmbModelInfo(self.ambChildModelLf, childVarList, childWidgetList, True, idx + 1)
            for i, var in enumerate(childVarList):
                var.set(round(childValInfo[i], 5))
            self.ambChildVarList.extend(childVarList)
            self.ambChildWidgetList.extend(childWidgetList)

            if idx < len(childValList) - 1:
                separator = ttkCustomWidget.CustomTtkSeparator(self.ambChildModelLf, orient="horizontal")
                separator.pack(fill=tkinter.X)

    def searchRailPos(self):
        self.railPosSearchBtn.pack_forget()
        self.railPosSearchStopBtn.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=10, pady=20)
        self.railPosUpdateFunc()

    def searchRailPosStop(self):
        self.railPosSearchBtn.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=10, pady=20)
        self.railPosSearchStopBtn.pack_forget()
        self.after_cancel(self.searchRailFuncId)

    def railPosUpdateFunc(self):
        try:
            val1PList = self.memoryObj.getRailPos(0)
            if val1PList is not None:
                self.v_rail1PRail.set(val1PList[0])
                self.v_rail1PPos.set(val1PList[1])
            else:
                self.v_rail1PRail.set(-1)
                self.v_rail1PPos.set(-1)
        except Exception:
            self.v_rail1PRail.set(-1)
            self.v_rail1PPos.set(-1)

        try:
            val2PList = self.memoryObj.getRailPos(1)
            if val2PList is not None:
                self.v_rail2PRail.set(val2PList[0])
                self.v_rail2PPos.set(val2PList[1])
            else:
                self.v_rail2PRail.set(-1)
                self.v_rail2PPos.set(-1)
        except Exception:
            self.v_rail2PRail.set(-1)
            self.v_rail2PPos.set(-1)
        self.searchRailFuncId = self.after(1, self.railPosUpdateFunc)

    def searchRail(self):
        self.railModifyBtn["state"] = "disabled"
        self.v_railDirX.set(float(0))
        self.v_railDirY.set(float(0))
        self.v_railDirZ.set(float(0))
        self.v_railPer.set(float(0))

        try:
            valList = self.memoryObj.getRailMemory(self.v_railNo.get())
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E60"])
            return

        if valList is None:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E79"])
            return

        self.railModifyBtn["state"] = "normal"
        self.v_railDirX.set(valList[0])
        self.v_railDirY.set(valList[1])
        self.v_railDirZ.set(valList[2])
        self.v_railPer.set(valList[3])

    def modifyRail(self):
        self.railSearchBtn["state"] = "disabled"
        self.railNoEt["state"] = "disabled"
        self.railModifyBtn.grid_remove()
        self.railSaveBtn.grid()
        self.railDirXEt["state"] = "normal"
        self.railDirYEt["state"] = "normal"
        self.railDirZEt["state"] = "normal"
        self.railPerEt["state"] = "normal"

    def saveRail(self):
        try:
            railNo = self.v_railNo.get()
        except Exception:
            return

        message = textSetting.textList["infoList"]["I98"].format(railNo)
        result = mb.askyesnocancel(title=textSetting.textList["confirm"], message=message, icon="warning")
        if result is None:
            return

        self.railSearchBtn["state"] = "normal"
        self.railNoEt["state"] = "normal"
        self.railModifyBtn.grid()
        self.railSaveBtn.grid_remove()

        self.railDirXEt["state"] = "readonly"
        self.railDirYEt["state"] = "readonly"
        self.railDirZEt["state"] = "readonly"
        self.railPerEt["state"] = "readonly"

        if result:
            valList = []
            try:
                valList.append(self.v_railDirX.get())
                valList.append(self.v_railDirY.get())
                valList.append(self.v_railDirZ.get())
                valList.append(self.v_railPer.get())
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E3"])
                return

            if not self.memoryObj.saveMemory(railNo, valList):
                self.memoryObj.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E80"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I99"].format(railNo))
        else:
            self.searchRail()

    def searchAMB(self):
        try:
            valList = self.memoryObj.getAMBMemory(self.v_ambNo.get())
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E60"])
            return

        if valList is None:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E81"])
            return

        self.ambModifyBtn["state"] = "normal"
        for i, var in enumerate(self.ambParentValList):
            if i in [1, 2]:
                var.set(valList[i])
            else:
                var.set(round(valList[i], 5))
        self.setAmbChildModel(valList[-1])

    def modifyAMB(self):
        self.ambNoEt["state"] = "disabled"
        self.ambSearchBtn["state"] = "disabled"

        self.ambModifyBtn.grid_remove()
        self.ambSaveBtn.grid()

        for widget in self.ambParentWidgetList:
            widget["state"] = "normal"
        for widget in self.ambChildWidgetList:
            widget["state"] = "normal"

    def saveAMB(self):
        try:
            ambNo = self.v_ambNo.get()
        except Exception:
            return

        message = textSetting.textList["infoList"]["I100"].format(ambNo)
        result = mb.askyesnocancel(title=textSetting.textList["confirm"], message=message, icon="warning")
        if result is None:
            return

        self.ambNoEt["state"] = "normal"
        self.ambSearchBtn["state"] = "normal"

        self.ambModifyBtn.grid()
        self.ambSaveBtn.grid_remove()

        for widget in self.ambParentWidgetList:
            widget["state"] = "readonly"
        for widget in self.ambChildWidgetList:
            widget["state"] = "readonly"

        if result:
            valList = []
            try:
                for i, var in enumerate(self.ambParentValList):
                    if i in [1, 2]:
                        valList.append(var.get())
                    else:
                        valList.append(float(var.get()))

                childList = []
                childInfo = []
                for i, var in enumerate(self.ambChildVarList):
                    childInfo.append(float(var.get()))
                    if i % 10 == 9:
                        childList.append(childInfo)
                        childInfo = []
                valList.append(childList)
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E3"])
                return

            delay = 0.3
            try:
                delay = self.v_delay.get()
            except Exception:
                delay = 0.3

            if not self.memoryObj.saveAMBMemory(ambNo, valList, delay):
                self.memoryObj.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E82"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I101"].format(ambNo))
        else:
            self.searchAMB()

    def openFile(self):
        file_path = fd.askopenfilename(filetypes=[("DEND_RS_EXE", "*.exe")])
        if not file_path:
            return

        filename = os.path.basename(file_path)
        self.v_fileName.set(filename)
        del self.memoryObj
        self.memoryObj = GetMemory(file_path)
        if not self.memoryObj.open():
            self.memoryObj.printError()
            mb.showerror(title=textSetting.textList["error"], message=self.memoryObj.error)
            return
        self.delelteWidget()
        self.createWidget()
