import tkinter
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class AmbListWidget:
    def __init__(self, frame, decryptFile, ambList, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.ambList = ambList
        self.varList = []
        self.varChildList = []
        self.reloadFunc = reloadFunc

        #
        ambNoFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        ambNoFrame.pack(anchor=tkinter.NW, padx=30, pady=30)
        ambNoLb = ttkCustomWidget.CustomTtkLabel(ambNoFrame, text=textSetting.textList["railEditor"]["ambAmbNo"], font=textSetting.textList["font2"])
        ambNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_ambNo = tkinter.IntVar()
        ambNoEt = ttkCustomWidget.CustomTtkEntry(ambNoFrame, textvariable=self.v_ambNo, font=textSetting.textList["font2"], width=7, justify="center")
        ambNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
        searchBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, text=textSetting.textList["railEditor"]["ambSearchBtnLabel"], command=lambda: self.searchAmb(self.v_ambNo.get()))
        searchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)

        csvExtractBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, width=25, text=textSetting.textList["railEditor"]["ambCsvExtractLabel"], command=self.extractCsv)
        csvExtractBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=5)
        csvSaveBtn = ttkCustomWidget.CustomTtkButton(ambNoFrame, width=25, text=textSetting.textList["railEditor"]["ambCsvSaveLabel"], command=self.saveCsv)
        csvSaveBtn.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=5)

        ###
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW)

        #
        if self.decryptFile.game in ["CS", "RS"]:
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
            xPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBasePosX"], font=textSetting.textList["font2"])
            xPosLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_xPos = tkinter.DoubleVar()
            xPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xPosEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBasePosY"], font=textSetting.textList["font2"])
            yPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_yPos = tkinter.DoubleVar()
            yPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBasePosZ"], font=textSetting.textList["font2"])
            zPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_zPos = tkinter.DoubleVar()
            zPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            xRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBaseDirX"], font=textSetting.textList["font2"])
            xRotLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_xRot = tkinter.DoubleVar()
            xRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xRotEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBaseDirY"], font=textSetting.textList["font2"])
            yRotLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_yRot = tkinter.DoubleVar()
            yRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yRotEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambBaseDirZ"], font=textSetting.textList["font2"])
            zRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_zRot = tkinter.DoubleVar()
            zRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zRotEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

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
        elif self.decryptFile.game == "BS":
            ambInfo2Frame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["ambInfoLabel"])
            ambInfo2Frame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=30, pady=15)

            railNoLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambRailNo"], font=textSetting.textList["font2"])
            railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_railNo = tkinter.IntVar()
            railNoEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            priorityLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambPriority"], font=textSetting.textList["font2"])
            priorityLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_priority = tkinter.IntVar()
            priorityEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_priority, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            priorityEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            fogLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambFog"], font=textSetting.textList["font2"])
            fogLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_fog = tkinter.IntVar()
            fogEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_fog, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            fogEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        elif self.decryptFile.game == "LS":
            ambInfo2Frame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["ambInfoLabel"])
            ambInfo2Frame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=30, pady=15)

            railNoLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambRailNo"], font=textSetting.textList["font2"])
            railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_railNo = tkinter.IntVar()
            railNoEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            posLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambLsPos"], font=textSetting.textList["font2"])
            posLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_pos = tkinter.IntVar()
            posEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            posEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            railPosLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambRailPos"], font=textSetting.textList["font2"])
            railPosLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_railPos = tkinter.IntVar()
            railPosEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_railPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            railPosEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            mdlNoLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambLsModel"], font=textSetting.textList["font2"])
            mdlNoLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(ambInfo2Frame, width=40, values=self.smfList, state="disabled")
            self.mdlNoCb.grid(row=2, column=1, columnspan=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            animeNoLb = ttkCustomWidget.CustomTtkLabel(ambInfo2Frame, text=textSetting.textList["railEditor"]["ambLsAnime"], font=textSetting.textList["font2"])
            animeNoLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_animeNo = tkinter.IntVar()
            animeNoEt = ttkCustomWidget.CustomTtkEntry(ambInfo2Frame, textvariable=self.v_animeNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            animeNoEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        #
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            ambModelLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["ambModelInfo"])
            ambModelLf.pack(anchor=tkinter.NW, padx=30, pady=15)
            self.setAmbInfo(ambModelLf, True)

        #
        if self.decryptFile.game in ["CS", "RS"]:
            self.ambChildModelLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["ambChildModelInfo"])
            self.ambChildModelLf.pack(anchor=tkinter.NW, padx=30, pady=15)

        self.searchAmb(self.v_ambNo.get())

    def setAmbInfo(self, frame, flag):
        mdlNoFrame = ttkCustomWidget.CustomTtkFrame(frame)
        mdlNoFrame.pack(anchor=tkinter.NW)
        if self.decryptFile.game in ["CS", "RS"]:
            mdlNoLb = ttkCustomWidget.CustomTtkLabel(mdlNoFrame, text=textSetting.textList["railEditor"]["ambModelSmf"], font=textSetting.textList["font2"])
            mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            mdlNoCb = ttkCustomWidget.CustomTtkCombobox(mdlNoFrame, width=40, values=self.smfList, state="disabled")
            mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            if flag:
                self.varList.append(mdlNoCb)
            else:
                self.varChildList.append(mdlNoCb)

            xyzFrame = ttkCustomWidget.CustomTtkFrame(frame)
            xyzFrame.pack(anchor=tkinter.NW)
            xMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosX"], font=textSetting.textList["font2"])
            xMdlPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_xMdlPos = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_xMdlPos)
            else:
                self.varChildList.append(self.v_xMdlPos)
            xMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xMdlPosEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosY"], font=textSetting.textList["font2"])
            yMdlPosLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_yMdlPos = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_yMdlPos)
            else:
                self.varChildList.append(self.v_yMdlPos)
            yMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yMdlPosEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosZ"], font=textSetting.textList["font2"])
            zMdlPosLb.grid(row=1, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_zMdlPos = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_zMdlPos)
            else:
                self.varChildList.append(self.v_zMdlPos)
            zMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zMdlPosEt.grid(row=1, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            xMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirX"], font=textSetting.textList["font2"])
            xMdlRotLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_xMdlRot = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_xMdlRot)
            else:
                self.varChildList.append(self.v_xMdlRot)
            xMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xMdlRotEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirY"], font=textSetting.textList["font2"])
            yMdlRotLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_yMdlRot = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_yMdlRot)
            else:
                self.varChildList.append(self.v_yMdlRot)
            yMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yMdlRotEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirZ"], font=textSetting.textList["font2"])
            zMdlRotLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_zMdlRot = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_zMdlRot)
            else:
                self.varChildList.append(self.v_zMdlRot)
            zMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zMdlRotEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            xMdlRot2Lb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotX"], font=textSetting.textList["font2"])
            xMdlRot2Lb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_xMdlRot2 = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_xMdlRot2)
            else:
                self.varChildList.append(self.v_xMdlRot2)
            xMdlRot2Et = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlRot2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xMdlRot2Et.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yMdlRot2Lb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotY"], font=textSetting.textList["font2"])
            yMdlRot2Lb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_yMdlRot2 = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_yMdlRot2)
            else:
                self.varChildList.append(self.v_yMdlRot2)
            yMdlRot2Et = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlRot2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yMdlRot2Et.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zMdlRot2Lb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelRotZ"], font=textSetting.textList["font2"])
            zMdlRot2Lb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_zMdlRot2 = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_zMdlRot2)
            else:
                self.varChildList.append(self.v_zMdlRot2)
            zMdlRot2Et = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlRot2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zMdlRot2Et.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            perLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPer"], font=textSetting.textList["font2"])
            perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_per = tkinter.DoubleVar()
            if flag:
                self.varList.append(self.v_per)
            else:
                self.varChildList.append(self.v_per)
            perEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        elif self.decryptFile.game == "BS":
            mdlNoLb = ttkCustomWidget.CustomTtkLabel(mdlNoFrame, text=textSetting.textList["railEditor"]["ambModelBsSmf"], font=textSetting.textList["font2"])
            mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            mdlNoCb = ttkCustomWidget.CustomTtkCombobox(mdlNoFrame, width=40, values=self.smfList, state="disabled")
            mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.varList.append(mdlNoCb)

            mdlDetailNoLb = ttkCustomWidget.CustomTtkLabel(mdlNoFrame, text=textSetting.textList["railEditor"]["ambModelBsDetail"], font=textSetting.textList["font2"])
            mdlDetailNoLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_mdlDetailNo = tkinter.IntVar()
            self.varList.append(self.v_mdlDetailNo)
            mdlDetailNoEt = ttkCustomWidget.CustomTtkEntry(mdlNoFrame, textvariable=self.v_mdlDetailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            mdlDetailNoEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            xyzFrame = ttkCustomWidget.CustomTtkFrame(frame)
            xyzFrame.pack(anchor=tkinter.NW)
            xMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosX"], font=textSetting.textList["font2"])
            xMdlPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_xMdlPos = tkinter.DoubleVar()
            self.varList.append(self.v_xMdlPos)
            xMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xMdlPosEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosY"], font=textSetting.textList["font2"])
            yMdlPosLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_yMdlPos = tkinter.DoubleVar()
            self.varList.append(self.v_yMdlPos)
            yMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yMdlPosEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zMdlPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPosZ"], font=textSetting.textList["font2"])
            zMdlPosLb.grid(row=2, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_zMdlPos = tkinter.DoubleVar()
            self.varList.append(self.v_zMdlPos)
            zMdlPosEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zMdlPosEt.grid(row=2, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            xMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirX"], font=textSetting.textList["font2"])
            xMdlRotLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_xMdlRot = tkinter.DoubleVar()
            self.varList.append(self.v_xMdlRot)
            xMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_xMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xMdlRotEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirY"], font=textSetting.textList["font2"])
            yMdlRotLb.grid(row=3, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_yMdlRot = tkinter.DoubleVar()
            self.varList.append(self.v_yMdlRot)
            yMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_yMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yMdlRotEt.grid(row=3, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zMdlRotLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelDirZ"], font=textSetting.textList["font2"])
            zMdlRotLb.grid(row=3, column=4, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_zMdlRot = tkinter.DoubleVar()
            self.varList.append(self.v_zMdlRot)
            zMdlRotEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_zMdlRot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zMdlRotEt.grid(row=3, column=5, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            perLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["ambModelPer"], font=textSetting.textList["font2"])
            perLb.grid(row=4, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_per = tkinter.DoubleVar()
            self.varList.append(self.v_per)
            perEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            perEt.grid(row=4, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setAmbChildInfo(self, ambInfo):
        children = self.ambChildModelLf.winfo_children()
        for child in children:
            child.destroy()

        self.varChildList = []
        childCount = ambInfo[23]
        for i in range(childCount):
            ambChildFrame = ttkCustomWidget.CustomTtkFrame(self.ambChildModelLf)
            ambChildFrame.pack(anchor=tkinter.NW)
            self.setAmbInfo(ambChildFrame, False)
            separate = ttkCustomWidget.CustomTtkSeparator(self.ambChildModelLf, orient="horizontal")
            separate.pack(fill=tkinter.X)

    def searchAmb(self, ambNo):
        if ambNo < 0 or ambNo >= len(self.ambList):
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E73"])
            return
        ambInfo = self.ambList[ambNo]

        if self.decryptFile.game in ["CS", "RS"]:
            self.v_type.set(ambInfo[0])
            self.v_length.set(ambInfo[1])
            self.v_railNo.set(ambInfo[2])
            self.v_railPos.set(ambInfo[3])
            self.v_xPos.set(ambInfo[4])
            self.v_yPos.set(ambInfo[5])
            self.v_zPos.set(ambInfo[6])
            self.v_xRot.set(ambInfo[7])
            self.v_yRot.set(ambInfo[8])
            self.v_zRot.set(ambInfo[9])
            self.v_priority.set(ambInfo[10])
            self.v_fog.set(ambInfo[11])

            self.varList[0].current(ambInfo[12])
            self.varList[1].set(ambInfo[13])
            self.varList[2].set(ambInfo[14])
            self.varList[3].set(ambInfo[15])
            self.varList[4].set(ambInfo[16])
            self.varList[5].set(ambInfo[17])
            self.varList[6].set(ambInfo[18])
            self.varList[7].set(ambInfo[19])
            self.varList[8].set(ambInfo[20])
            self.varList[9].set(ambInfo[21])
            self.varList[10].set(ambInfo[22])

            self.setAmbChildInfo(ambInfo)
            childCount = ambInfo[23]
            for i in range(childCount):
                self.varChildList[11 * i + 0].current(ambInfo[11 * i + 24])
                self.varChildList[11 * i + 1].set(ambInfo[11 * i + 25])
                self.varChildList[11 * i + 2].set(ambInfo[11 * i + 26])
                self.varChildList[11 * i + 3].set(ambInfo[11 * i + 27])
                self.varChildList[11 * i + 4].set(ambInfo[11 * i + 28])
                self.varChildList[11 * i + 5].set(ambInfo[11 * i + 29])
                self.varChildList[11 * i + 6].set(ambInfo[11 * i + 30])
                self.varChildList[11 * i + 7].set(ambInfo[11 * i + 31])
                self.varChildList[11 * i + 8].set(ambInfo[11 * i + 32])
                self.varChildList[11 * i + 9].set(ambInfo[11 * i + 33])
                self.varChildList[11 * i + 10].set(ambInfo[11 * i + 34])
        elif self.decryptFile.game == "BS":
            self.v_railNo.set(ambInfo[0])
            self.v_priority.set(ambInfo[1])
            self.v_fog.set(ambInfo[2])
            self.varList[0].current(ambInfo[3])
            self.varList[1].set(ambInfo[4])
            self.varList[2].set(ambInfo[5])
            self.varList[3].set(ambInfo[6])
            self.varList[4].set(ambInfo[7])
            self.varList[5].set(ambInfo[8])
            self.varList[6].set(ambInfo[9])
            self.varList[7].set(ambInfo[10])
            self.varList[8].set(ambInfo[11])
        elif self.decryptFile.game == "LS":
            self.v_railNo.set(ambInfo[0])
            self.v_pos.set(ambInfo[1])
            self.v_railPos.set(ambInfo[2])
            if ambInfo[3] == 0:
                self.mdlNoCb.set("なし")
            else:
                self.mdlNoCb.current(ambInfo[3])
            self.v_animeNo.set(ambInfo[4])

    def extractCsv(self):
        filename = self.decryptFile.filename + "_amb.csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["ambCsvFileType"], "*.csv")])
        errorMsg = textSetting.textList["errorList"]["E7"]
        if file_path:
            if not self.decryptFile.extractAmbCsv(file_path):
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])

    def saveCsv(self):
        errorMsg = textSetting.textList["errorList"]["E71"]
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["ambCsvFileType"], "*.csv")])
        if not file_path:
            return
        try:
            f = open(file_path)
            csvLines = f.readlines()
            f.close()
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E74"]
            mb.showerror(title=textSetting.textList["readError"], message=errorMsg)
            return

        try:
            csvLines.pop(0)
            ambList = []
            ambInfo = []
            count = 0
            childCount = 0
            childAllCount = 0
            childFlag = False
            for csv in csvLines:
                csv = csv.strip()
                arr = csv.split(",")

                if self.decryptFile.game in ["CS", "RS"]:
                    if not childFlag:
                        ambInfo = []

                        if len(arr) < 24:
                            raise Exception

                        type0 = int(float(arr[1]))
                        ambInfo.append(type0)

                        length = int(float(arr[2]))
                        ambInfo.append(length)

                        railNo = int(arr[3])
                        ambInfo.append(railNo)

                        railPos = int(arr[4])
                        ambInfo.append(railPos)

                        for i in range(6):
                            tempF = float(arr[5 + i])
                            ambInfo.append(tempF)

                        priority = int(arr[11])
                        ambInfo.append(priority)

                        fog = int(arr[12])
                        ambInfo.append(fog)

                        #
                        mdl_no = int(arr[13])
                        ambInfo.append(mdl_no)

                        for i in range(10):
                            tempF = float(arr[14 + i])
                            ambInfo.append(tempF)

                        childFlag = True
                        count += 1
                        continue

                    if childCount == 0:
                        childAllCount = int(arr[12])
                        ambInfo.append(childAllCount)

                    if childAllCount > 0:
                        mdl_no = int(arr[13])
                        ambInfo.append(mdl_no)

                        for i in range(10):
                            tempF = float(arr[14 + i])
                            ambInfo.append(tempF)

                        childCount += 1

                    if childCount == childAllCount:
                        childFlag = False
                        childCount = 0
                        ambList.append(ambInfo)
                    count += 1
                elif self.decryptFile.game == "BS":
                    ambInfo = []
                    if len(arr) < 12:
                        raise Exception

                    for i in range(5):
                        temp = int(arr[i])
                        ambInfo.append(temp)

                    for i in range(7):
                        tempF = float(arr[5 + i])
                        ambInfo.append(tempF)
                    ambList.append(ambInfo)
                    count += 1
                elif self.decryptFile.game == "LS":
                    ambInfo = []
                    if len(arr) < 5:
                        raise Exception

                    for i in range(5):
                        temp = int(arr[i])
                        ambInfo.append(temp)
                    ambList.append(ambInfo)
                    count += 1

            if childCount != 0 and childCount != childAllCount:
                msg = textSetting.textList["errorList"]["E74"]
                mb.showerror(title=textSetting.textList["error"], message=msg)
                return

            if childFlag:
                msg = textSetting.textList["errorList"]["E74"]
                mb.showerror(title=textSetting.textList["error"], message=msg)
                return

            msg = textSetting.textList["infoList"]["I15"].format(count)
            result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")

            if result:
                if not self.decryptFile.saveAmbCsv(ambList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I95"])
                self.reloadFunc()

        except Exception:
            errorMsg = textSetting.textList["errorList"]["E15"].format(count + 1)
            mb.showerror(title=textSetting.textList["readError"], message=errorMsg)
            return
