import tkinter
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget


class AmbListWidget:
    def __init__(self, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.smfList.append("なし")
        self.ambList = decryptFile.ambList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.ambChildVarList = []
        self.ambChildVarCnt = 0

        self.setFirstHorizontalLayout()

        if self.decryptFile.game in ["CS", "RS"]:
            self.setDefaultSecondHorizontalLayout()
            self.setDefaultAmbModelInfoLayout()
            self.ambChildInfoFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
            self.ambChildInfoFrame.pack(anchor=tkinter.NW)
        elif self.decryptFile.game == "BS":
            self.setBsSecondHorizontalLayout()
            self.setBsAmbModelInfoLayout()
        elif self.decryptFile.game == "LS":
            self.setLsSecondHorizontalLayout()
        elif self.decryptFile.game == "LSTrial":
            if not self.decryptFile.oldFlag:
                self.setLsSecondHorizontalLayout()
            else:
                self.setLsTrialOldSecondHorizontalLayout()
                self.setLsTrialOldModelInfoLayout()

    def setFirstHorizontalLayout(self):
        ambNoFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        ambNoFrame.pack(anchor=tkinter.NW, padx=30, pady=30)
        ambNoLb = ttkCustomWidget.CustomTtkLabel(ambNoFrame, text=textSetting.textList["railEditor"]["ambAmbNo"], font=textSetting.textList["font2"])
        ambNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_ambNo = tkinter.IntVar()
        ambNoEt = ttkCustomWidget.CustomTtkEntry(ambNoFrame, textvariable=self.v_ambNo, font=textSetting.textList["font2"], width=7, justify="center")
        ambNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
        searchBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, text=textSetting.textList["railEditor"]["ambSearchBtnLabel"], command=self.searchAmb)
        searchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)

        csvExtractBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, width=25, text=textSetting.textList["railEditor"]["ambCsvExtractLabel"], command=self.extractCsv)
        csvExtractBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=5)
        csvSaveBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, width=25, text=textSetting.textList["railEditor"]["ambCsvSaveLabel"], command=self.saveCsv)
        csvSaveBtn.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=5)

    def setDefaultSecondHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW)

        ambInfoLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["ambInfoLabel"])
        ambInfoLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=30, pady=15)

        typeLb = ttkCustomWidget.CustomTtkLabel(ambInfoLf, text=textSetting.textList["railEditor"]["ambType"], font=textSetting.textList["font2"])
        typeLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_type = tkinter.IntVar()
        typeEt = ttkCustomWidget.CustomTtkEntry(ambInfoLf, textvariable=self.v_type, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        typeEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        lengthLb = ttkCustomWidget.CustomTtkLabel(ambInfoLf, text=textSetting.textList["railEditor"]["ambLength"], font=textSetting.textList["font2"])
        lengthLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_length = tkinter.IntVar()
        lengthEt = ttkCustomWidget.CustomTtkEntry(ambInfoLf, textvariable=self.v_length, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        lengthEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        railNoLb = ttkCustomWidget.CustomTtkLabel(ambInfoLf, text=textSetting.textList["railEditor"]["ambRailNo"], font=textSetting.textList["font2"])
        railNoLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railNo = tkinter.IntVar()
        railNoEt = ttkCustomWidget.CustomTtkEntry(ambInfoLf, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        railNoEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        railPosLb = ttkCustomWidget.CustomTtkLabel(ambInfoLf, text=textSetting.textList["railEditor"]["ambRailPos"], font=textSetting.textList["font2"])
        railPosLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railPos = tkinter.IntVar()
        railPosEt = ttkCustomWidget.CustomTtkEntry(ambInfoLf, textvariable=self.v_railPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        railPosEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        #
        xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["ambPosDirInfo"])
        xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, pady=15)
        xBasePosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBasePosX"], font=textSetting.textList["font2"])
        xBasePosLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_xBasePos = tkinter.DoubleVar()
        xBasePosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xBasePos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xBasePosEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yBasePosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBasePosY"], font=textSetting.textList["font2"])
        yBasePosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_yBasePos = tkinter.DoubleVar()
        yBasePosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yBasePos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yBasePosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zBasePosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBasePosZ"], font=textSetting.textList["font2"])
        zBasePosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_zBasePos = tkinter.DoubleVar()
        zBasePosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zBasePos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zBasePosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xBaseRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBaseDirX"], font=textSetting.textList["font2"])
        xBaseRotLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_xBaseRot = tkinter.DoubleVar()
        xBaseRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xBaseRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xBaseRotEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yBaseRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBaseDirY"], font=textSetting.textList["font2"])
        yBaseRotLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_yBaseRot = tkinter.DoubleVar()
        yBaseRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yBaseRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yBaseRotEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zBaseRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBaseDirZ"], font=textSetting.textList["font2"])
        zBaseRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_zBaseRot = tkinter.DoubleVar()
        zBaseRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zBaseRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zBaseRotEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        #
        ambInfo2Frame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["ambInfo2Label"])
        ambInfo2Frame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=30, pady=15)

        priorityLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambPriority"], font=textSetting.textList["font2"])
        priorityLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_priority = tkinter.IntVar()
        priorityEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_priority, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        priorityEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        fogLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambFog"], font=textSetting.textList["font2"])
        fogLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_fog = tkinter.IntVar()
        fogEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_fog, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        fogEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setDefaultAmbModelInfoLayout(self):
        ambModelLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["ambModelInfo"])
        ambModelLf.pack(anchor=tkinter.NW, padx=30, pady=15)
        mdlNoFrame = ttkCustomWidget.CustomTtkFrame(ambModelLf)
        mdlNoFrame.pack(anchor=tkinter.NW)

        mdlNoLb = ttkCustomWidget.CustomTtkLabel(mdlNoFrame, text=textSetting.textList["railEditor"]["ambModelSmf"], font=textSetting.textList["font2"])
        mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(mdlNoFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xyzFrame = ttkCustomWidget.CustomTtkFrame(ambModelLf)
        xyzFrame.pack(anchor=tkinter.NW)
        xMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosX"], font=textSetting.textList["font2"])
        xMdlPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_xMdlPos = tkinter.DoubleVar()
        xMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosY"], font=textSetting.textList["font2"])
        yMdlPosLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_yMdlPos = tkinter.DoubleVar()
        yMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlPosEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosZ"], font=textSetting.textList["font2"])
        zMdlPosLb.grid(row=1, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_zMdlPos = tkinter.DoubleVar()
        zMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlPosEt.grid(row=1, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirX"], font=textSetting.textList["font2"])
        xMdlDirLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_xMdlDir = tkinter.DoubleVar()
        xMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlDir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlDirEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirY"], font=textSetting.textList["font2"])
        yMdlDirLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_yMdlDir = tkinter.DoubleVar()
        yMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlDir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlDirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirZ"], font=textSetting.textList["font2"])
        zMdlDirLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_zMdlDir = tkinter.DoubleVar()
        zMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlDir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlDirEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotX"], font=textSetting.textList["font2"])
        xMdlRotLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_xMdlRot = tkinter.DoubleVar()
        xMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlRotEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotY"], font=textSetting.textList["font2"])
        yMdlRotLb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_yMdlRot = tkinter.DoubleVar()
        yMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlRotEt.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotZ"], font=textSetting.textList["font2"])
        zMdlRotLb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_zMdlRot = tkinter.DoubleVar()
        zMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlRotEt.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        perLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPer"], font=textSetting.textList["font2"])
        perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_per = tkinter.DoubleVar()
        perEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setDefaultAmbChildModelInfoLayout(self, childCount, ambChildInfo):
        children = self.ambChildInfoFrame.winfo_children()
        for child in children:
            child.destroy()

        if childCount == 0:
            ambChildFrame = ttkCustomWidget.CustomTtkFrame(self.ambChildInfoFrame)
            ambChildFrame.pack()
            return

        ambChildModelLf = ttkCustomWidget.CustomTtkLabelFrame(self.ambChildInfoFrame, text=textSetting.textList["railEditor"]["ambChildModelInfo"])
        ambChildModelLf.pack(anchor=tkinter.NW, padx=30, pady=15)

        ambSize = 11
        ambChunkList = [ambChildInfo[i:i + ambSize] for i in range(0, len(ambChildInfo), ambSize)]
        self.ambChildVarList = []
        self.ambChildVarCnt = 0
        for i, ambChunkInfo in enumerate(ambChunkList):
            ambChildFrame = ttkCustomWidget.CustomTtkFrame(ambChildModelLf)
            ambChildFrame.pack(anchor=tkinter.NW)
            self.setDefaultAmbChildModel(ambChildFrame, i, ambChunkInfo)
            if i != len(ambChunkList) - 1:
                separate = ttkCustomWidget.CustomTtkSeparator(ambChildModelLf, orient="horizontal")
                separate.pack(fill=tkinter.X)

    def setDefaultAmbChildModel(self, frame, index, ambInfo):
        mdlNoFrame = ttkCustomWidget.CustomTtkFrame(frame)
        mdlNoFrame.pack(anchor=tkinter.NW)

        mdlNoLb = ttkCustomWidget.CustomTtkLabel(mdlNoFrame, text=textSetting.textList["railEditor"]["ambChildModelSmf"].format(index), font=textSetting.textList["font2"])
        mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        mdlNoCb = ttkCustomWidget.CustomTtkCombobox(mdlNoFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        mdlNoCb.current(ambInfo[0])

        xyzFrame = ttkCustomWidget.CustomTtkFrame(frame)
        xyzFrame.pack(anchor=tkinter.NW)
        xMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosX"], font=textSetting.textList["font2"])
        xMdlPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[1]))
        xMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        yMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosY"], font=textSetting.textList["font2"])
        yMdlPosLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[2]))
        yMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlPosEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        zMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosZ"], font=textSetting.textList["font2"])
        zMdlPosLb.grid(row=1, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[3]))
        zMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlPosEt.grid(row=1, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        xMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirX"], font=textSetting.textList["font2"])
        xMdlDirLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[4]))
        xMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlDirEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        yMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirY"], font=textSetting.textList["font2"])
        yMdlDirLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[5]))
        yMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlDirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        zMdlDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirZ"], font=textSetting.textList["font2"])
        zMdlDirLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[6]))
        zMdlDirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlDirEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        xMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotX"], font=textSetting.textList["font2"])
        xMdlRotLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[7]))
        xMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlRotEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        yMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotY"], font=textSetting.textList["font2"])
        yMdlRotLb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[8]))
        yMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlRotEt.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        zMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotZ"], font=textSetting.textList["font2"])
        zMdlRotLb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[9]))
        zMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlRotEt.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

        perLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPer"], font=textSetting.textList["font2"])
        perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarList.append(tkinter.DoubleVar(value=ambInfo[10]))
        perEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.ambChildVarList[self.ambChildVarCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.ambChildVarCnt += 1

    def setBsSecondHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW)
        ambInfoFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["ambInfoLabel"])
        ambInfoFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=30, pady=15)

        railNoLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambRailNo"], font=textSetting.textList["font2"])
        railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railNo = tkinter.IntVar()
        railNoEt = ttkCustomWidget.CustomTtkEntry(ambInfoFrame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        priorityLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambPriority"], font=textSetting.textList["font2"])
        priorityLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_priority = tkinter.IntVar()
        priorityEt = ttkCustomWidget.CustomTtkEntry(ambInfoFrame, textvariable=self.v_priority, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        priorityEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        fogLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambFog"], font=textSetting.textList["font2"])
        fogLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_fog = tkinter.IntVar()
        fogEt = ttkCustomWidget.CustomTtkEntry(ambInfoFrame, textvariable=self.v_fog, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        fogEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setBsAmbModelInfoLayout(self):
        ambModelLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["ambModelInfo"])
        ambModelLf.pack(anchor=tkinter.NW, padx=30, pady=15)

        mdlNoFrame = ttkCustomWidget.CustomTtkFrame(ambModelLf)
        mdlNoFrame.pack(anchor=tkinter.NW)

        mdlNoLb = ttkCustomWidget.CustomTtkLabel(mdlNoFrame, text=textSetting.textList["railEditor"]["ambModelBsSmf"], font=textSetting.textList["font2"])
        mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(mdlNoFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        mdlDetailNoLb = ttkCustomWidget.CustomTtkLabel(mdlNoFrame, text=textSetting.textList["railEditor"]["ambModelBsDetail"], font=textSetting.textList["font2"])
        mdlDetailNoLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_mdlDetailNo = tkinter.IntVar()
        mdlDetailNoEt = ttkCustomWidget.CustomTtkEntry(mdlNoFrame, textvariable=self.v_mdlDetailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        mdlDetailNoEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xyzFrame = ttkCustomWidget.CustomTtkFrame(ambModelLf)
        xyzFrame.pack(anchor=tkinter.NW)
        xMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosX"], font=textSetting.textList["font2"])
        xMdlPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_xMdlPos = tkinter.DoubleVar()
        xMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosY"], font=textSetting.textList["font2"])
        yMdlPosLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_yMdlPos = tkinter.DoubleVar()
        yMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlPosEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosZ"], font=textSetting.textList["font2"])
        zMdlPosLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_zMdlPos = tkinter.DoubleVar()
        zMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlPosEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirX"], font=textSetting.textList["font2"])
        xMdlRotLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_xMdlRot = tkinter.DoubleVar()
        xMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xMdlRotEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirY"], font=textSetting.textList["font2"])
        yMdlRotLb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_yMdlRot = tkinter.DoubleVar()
        yMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yMdlRotEt.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirZ"], font=textSetting.textList["font2"])
        zMdlRotLb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_zMdlRot = tkinter.DoubleVar()
        zMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zMdlRotEt.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        perLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPer"], font=textSetting.textList["font2"])
        perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_per = tkinter.DoubleVar()
        perEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setLsSecondHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW)
        ambInfoFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["ambInfoLabel"])
        ambInfoFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=30, pady=15)

        railNoLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambRailNo"], font=textSetting.textList["font2"])
        railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railNo = tkinter.IntVar()
        railNoEt = ttkCustomWidget.CustomTtkEntry(ambInfoFrame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        posLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambLsPos"], font=textSetting.textList["font2"])
        posLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_pos = tkinter.IntVar()
        posEt = ttkCustomWidget.CustomTtkEntry(ambInfoFrame, textvariable=self.v_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        posEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        railPosLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambRailPos"], font=textSetting.textList["font2"])
        railPosLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railPos = tkinter.IntVar()
        railPosEt = ttkCustomWidget.CustomTtkEntry(ambInfoFrame, textvariable=self.v_railPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        railPosEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        mdlNoLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambLsModel"], font=textSetting.textList["font2"])
        mdlNoLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(ambInfoFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlNoCb.grid(row=2, column=1, columnspan=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        animeNoLb = ttkCustomWidget.CustomTtkLabel(ambInfoFrame, text=textSetting.textList["railEditor"]["ambLsAnime"], font=textSetting.textList["font2"])
        animeNoLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_animeNo = tkinter.IntVar()
        animeNoEt = ttkCustomWidget.CustomTtkEntry(ambInfoFrame, textvariable=self.v_animeNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        animeNoEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setLsTrialOldSecondHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW)
        xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railPosXyzInfo"])
        xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=25, pady=15)
        xLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosX"], font=textSetting.textList["font2"])
        xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_x_pos = tkinter.DoubleVar()
        x_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        x_posEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosY"], font=textSetting.textList["font2"])
        yLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_y_pos = tkinter.DoubleVar()
        y_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        y_posEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosZ"], font=textSetting.textList["font2"])
        zLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_z_pos = tkinter.DoubleVar()
        z_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        z_posEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        #
        xLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirX"], font=textSetting.textList["font2"])
        xLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_x_dir = tkinter.DoubleVar()
        x_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        x_dirEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        yLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirY"], font=textSetting.textList["font2"])
        yLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_y_dir = tkinter.DoubleVar()
        y_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        y_dirEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        zLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirZ"], font=textSetting.textList["font2"])
        zLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_z_dir = tkinter.DoubleVar()
        z_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        z_dirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        ###
        railFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railRailInfo"])
        railFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        nextLb = ttkCustomWidget.CustomTtkLabel(railFrame, text=textSetting.textList["railEditor"]["railNextRail"], font=textSetting.textList["font2"])
        nextLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_next = tkinter.StringVar()
        nextEt = ttkCustomWidget.CustomTtkEntry(railFrame, textvariable=self.v_next, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        nextEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        prevLb = ttkCustomWidget.CustomTtkLabel(railFrame, text=textSetting.textList["railEditor"]["railPrevRail"], font=textSetting.textList["font2"])
        prevLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_prev = tkinter.StringVar()
        prevEt = ttkCustomWidget.CustomTtkEntry(railFrame, textvariable=self.v_prev, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        prevEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setLsTrialOldModelInfoLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)

        kasenFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
        kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        leftMdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
        leftMdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.leftMdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.leftMdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        rightMdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
        rightMdlNoLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.rightMdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.rightMdlNoCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        mdlKasenchuLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
        mdlKasenchuLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.mdlKasenchuCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlKasenchuCb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        fixAmbLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railFixAmbLabel"], font=textSetting.textList["font2"])
        fixAmbLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.fixAmbCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.fixAmbCb.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def searchAmb(self):
        ambNo = self.v_ambNo.get()
        if len(self.ambList) == 0:
            return

        if ambNo < 0 or ambNo >= len(self.ambList):
            if ambNo < 0:
                ambNo = 0
            else:
                ambNo = len(self.ambList) - 1
            self.v_ambNo.set(ambNo)
        ambInfo = self.ambList[ambNo]

        if self.decryptFile.game in ["CS", "RS"]:
            self.v_type.set(ambInfo[0])
            self.v_length.set(ambInfo[1])
            self.v_railNo.set(ambInfo[2])
            self.v_railPos.set(ambInfo[3])
            self.v_xBasePos.set(ambInfo[4])
            self.v_yBasePos.set(ambInfo[5])
            self.v_zBasePos.set(ambInfo[6])
            self.v_xBaseRot.set(ambInfo[7])
            self.v_yBaseRot.set(ambInfo[8])
            self.v_zBaseRot.set(ambInfo[9])
            self.v_priority.set(ambInfo[10])
            self.v_fog.set(ambInfo[11])

            self.mdlNoCb.current(ambInfo[12])
            self.v_xMdlPos.set(ambInfo[13])
            self.v_yMdlPos.set(ambInfo[14])
            self.v_zMdlPos.set(ambInfo[15])
            self.v_xMdlDir.set(ambInfo[16])
            self.v_yMdlDir.set(ambInfo[17])
            self.v_zMdlDir.set(ambInfo[18])
            self.v_xMdlRot.set(ambInfo[19])
            self.v_yMdlRot.set(ambInfo[20])
            self.v_zMdlRot.set(ambInfo[21])
            self.v_per.set(ambInfo[22])

            childCount = ambInfo[23]
            self.setDefaultAmbChildModelInfoLayout(childCount, ambInfo[24:])
        elif self.decryptFile.game == "BS":
            self.v_railNo.set(ambInfo[0])
            self.v_priority.set(ambInfo[1])
            self.v_fog.set(ambInfo[2])
            self.mdlNoCb.current(ambInfo[3])
            self.v_mdlDetailNo.set(ambInfo[4])
            self.v_xMdlPos.set(ambInfo[5])
            self.v_yMdlPos.set(ambInfo[6])
            self.v_zMdlPos.set(ambInfo[7])
            self.v_xMdlRot.set(ambInfo[8])
            self.v_yMdlRot.set(ambInfo[9])
            self.v_zMdlRot.set(ambInfo[10])
            self.v_per.set(ambInfo[11])
        elif self.decryptFile.game == "LS":
            blankIndex = len(self.smfList) - 1
            self.v_railNo.set(ambInfo[0])
            self.v_pos.set(ambInfo[1])
            self.v_railPos.set(ambInfo[2])
            if ambInfo[3] == 0:
                self.mdlNoCb.current(blankIndex)
            else:
                self.mdlNoCb.current(ambInfo[3])
            self.v_animeNo.set(ambInfo[4])
        elif self.decryptFile.game == "LSTrial" and not self.decryptFile.oldFlag:
            blankIndex = len(self.smfList) - 1
            self.v_railNo.set(ambInfo[0])
            self.v_pos.set(ambInfo[1])
            self.v_railPos.set(ambInfo[2])
            if ambInfo[3] == 0:
                self.mdlNoCb.current(blankIndex)
            else:
                self.mdlNoCb.current(ambInfo[3])
            self.v_animeNo.set(ambInfo[4])
        elif self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag:
            blankIndex = len(self.smfList) - 1
            self.v_x_pos.set(ambInfo[0])
            self.v_y_pos.set(ambInfo[1])
            self.v_z_pos.set(ambInfo[2])
            self.v_next.set(ambInfo[3])
            self.v_prev.set(ambInfo[4])
            self.v_x_dir.set(ambInfo[5])
            self.v_y_dir.set(ambInfo[6])
            self.v_z_dir.set(ambInfo[7])
            if ambInfo[8] == -1:
                self.leftMdlNoCb.current(blankIndex)
            else:
                self.leftMdlNoCb.current(ambInfo[8])

            if ambInfo[9] == -1:
                self.rightMdlNoCb.current(blankIndex)
            else:
                self.rightMdlNoCb.current(ambInfo[9])

            if ambInfo[10] == -1:
                self.mdlKasenchuCb.current(blankIndex)
            else:
                self.mdlKasenchuCb.current(ambInfo[10])

            if ambInfo[11] == -1:
                self.fixAmbCb.current(blankIndex)
            else:
                self.fixAmbCb.current(ambInfo[11])

    def extractCsv(self):
        filename = self.decryptFile.filename + "_amb.csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["ambCsvFileType"], "*.csv")])
        if not file_path:
            return

        try:
            self.decryptFile.extractAmbCsv(file_path)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except PermissionError:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def saveCsv(self):
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["ambCsvFileType"], "*.csv")])
        if not file_path:
            return

        ambObj, message = self.decryptFile.loadAmbCsv(file_path)
        if message:
            mb.showerror(title=textSetting.textList["error"], message=message)
            return

        msg = textSetting.textList["infoList"]["I15"].format(ambObj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            ambList = ambObj["data"]
            if not self.decryptFile.saveAmbCsv(ambList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I95"])
            self.reloadFunc()
