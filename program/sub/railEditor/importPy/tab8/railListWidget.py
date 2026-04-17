import copy
from functools import partial

import tkinter
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.errorLogClass import ErrorLogObj


class RailListWidget:
    def __init__(self, frame, decryptFile, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.railList = decryptFile.railList
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc
        self.varRailList = []
        self.varRevRailList = []
        self.errObj = ErrorLogObj()

        if self.decryptFile.game in ["CS", "RS"]:
            self.smfList.extend(textSetting.textList["railEditor"]["smfListAddList1"])
        else:
            self.smfList.extend(textSetting.textList["railEditor"]["smfListAddList2"])

        self.setFirstHorizontalLayout()

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.setDefaultSecondHorizontalLayout()
        elif self.decryptFile.game == "LS":
            self.setLsSecondHorizontalLayout()
            self.setLsModelInfoHorizontalLayout()
        elif self.decryptFile.game == "LSTrial":
            self.setLsTrialSecondHorizontalLayout()
            self.setLsTrialModelInfoHorizontalLayout()

        self.setFlagInfoLayout()
        self.setRailDataInfoLayout()

    def setFirstHorizontalLayout(self):
        railNoFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        railNoFrame.pack(anchor=tkinter.NW, padx=30, pady=30, fill=tkinter.X)
        # railNoName
        railNoLb = ttkCustomWidget.CustomTtkLabel(railNoFrame, text=textSetting.textList["railEditor"]["railRailNo"], font=textSetting.textList["font2"])
        railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        # railNo
        self.v_railNo = tkinter.IntVar()
        railNoEt = ttkCustomWidget.CustomTtkEntry(railNoFrame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center")
        railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
        # searchRailButton
        searchBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["railEditor"]["railSearchBtnLabel"], command=self.searchRail)
        searchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)
        # csvExtractButton
        csvExtractBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, width=25, text=textSetting.textList["railEditor"]["railCsvExtractLabel"], command=self.extractCsv)
        csvExtractBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=5)
        # csvSaveButton
        csvSaveBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, width=25, text=textSetting.textList["railEditor"]["railCsvSaveLabel"], command=self.saveCsv)
        csvSaveBtn.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=5)
        if self.decryptFile.game == "CS":
            # csToRsButton
            csToRsBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["railEditor"]["railCsToRs"], command=self.csToRs)
            csToRsBtn.grid(row=0, column=5, sticky=tkinter.W + tkinter.E, padx=10)

    def setDefaultSecondHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)

        blockFrameLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railBlockInfo"])
        blockFrameLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        # prevRailName
        prevRailLb = ttkCustomWidget.CustomTtkLabel(blockFrameLf, text=textSetting.textList["railEditor"]["railPrevRailNo"], font=textSetting.textList["font2"])
        prevRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # prevRail
        self.v_prevRail = tkinter.IntVar()
        prevRailEt = ttkCustomWidget.CustomTtkEntry(blockFrameLf, textvariable=self.v_prevRail, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        prevRailEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # blockName
        blockLb = ttkCustomWidget.CustomTtkLabel(blockFrameLf, text=textSetting.textList["railEditor"]["railBlockNo"], font=textSetting.textList["font2"])
        blockLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # block
        self.v_block = tkinter.IntVar()
        blockEt = ttkCustomWidget.CustomTtkEntry(blockFrameLf, textvariable=self.v_block, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        blockEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railXyzInfo"])
        xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        # railDirXName
        xLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirX"], font=textSetting.textList["font2"])
        xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirX
        self.v_x = tkinter.DoubleVar()
        xEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        xEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirYName
        yLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirY"], font=textSetting.textList["font2"])
        yLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirY
        self.v_y = tkinter.DoubleVar()
        yEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        yEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirZName
        zLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirZ"], font=textSetting.textList["font2"])
        zLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirZ
        self.v_z = tkinter.DoubleVar()
        zEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        zEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        kasenFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
        kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        # modelName
        mdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
        mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # modelNameCombo
        self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenName
        mdlKasenLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
        mdlKasenLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenNameCombo
        self.mdlKasenCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlKasenCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenchuName
        mdlKasenchuLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
        mdlKasenchuLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenchuNameCombo
        self.mdlKasenchuCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlKasenchuCb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # perName
        perLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPer"], font=textSetting.textList["font2"])
        perLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # per
        self.v_per = tkinter.DoubleVar()
        perEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        perEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setLsSecondHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)

        if self.decryptFile.ver == "DEND_MAP_VER0101":
            verLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railLsVer0101"])
            verLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            # prevRail2Name
            prevRail2Lb = ttkCustomWidget.CustomTtkLabel(verLf, text=textSetting.textList["railEditor"]["railPrevRail2No"], font=textSetting.textList["font2"])
            prevRail2Lb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # prevRail2
            self.v_prevRail2 = tkinter.IntVar()
            prevRail2Et = ttkCustomWidget.CustomTtkEntry(verLf, textvariable=self.v_prevRail2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            prevRail2Et.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railPosXyzInfo"])
        xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        # railPosXName
        xPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosX"], font=textSetting.textList["font2"])
        xPosLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosX
        self.v_x_pos = tkinter.DoubleVar()
        x_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        x_posEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosYName
        yPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosY"], font=textSetting.textList["font2"])
        yPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosY
        self.v_y_pos = tkinter.DoubleVar()
        y_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        y_posEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosZName
        zPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosZ"], font=textSetting.textList["font2"])
        zPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosZ
        self.v_z_pos = tkinter.DoubleVar()
        z_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        z_posEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirXName
        xDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirX"], font=textSetting.textList["font2"])
        xDirLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirX
        self.v_x_dir = tkinter.DoubleVar()
        x_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        x_dirEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirYName
        yDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirY"], font=textSetting.textList["font2"])
        yDirLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirY
        self.v_y_dir = tkinter.DoubleVar()
        y_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        y_dirEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirZName
        zDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirZ"], font=textSetting.textList["font2"])
        zDirLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirZ
        self.v_z_dir = tkinter.DoubleVar()
        z_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        z_dirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        xyzRotFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railRotXyzInfo"])
        xyzRotFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        # railRotXName
        xRotLb = ttkCustomWidget.CustomTtkLabel(xyzRotFrame, text=textSetting.textList["railEditor"]["railRotX"], font=textSetting.textList["font2"])
        xRotLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railRotX
        self.v_x_rot = tkinter.StringVar()
        x_dirEt = ttkCustomWidget.CustomTtkEntry(xyzRotFrame, textvariable=self.v_x_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        x_dirEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railRotYName
        yRotLb = ttkCustomWidget.CustomTtkLabel(xyzRotFrame, text=textSetting.textList["railEditor"]["railRotY"], font=textSetting.textList["font2"])
        yRotLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railRotY
        self.v_y_rot = tkinter.StringVar()
        y_dirEt = ttkCustomWidget.CustomTtkEntry(xyzRotFrame, textvariable=self.v_y_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        y_dirEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railRotZName
        zRotLb = ttkCustomWidget.CustomTtkLabel(xyzRotFrame, text=textSetting.textList["railEditor"]["railRotZ"], font=textSetting.textList["font2"])
        zRotLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railRotZ
        self.v_z_rot = tkinter.StringVar()
        z_dirEt = ttkCustomWidget.CustomTtkEntry(xyzRotFrame, textvariable=self.v_z_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        z_dirEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setLsModelInfoHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)
        kasenFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
        kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        # modelName
        mdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
        mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # modelNameCombo
        self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # prevRailName
        prevRailLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPrevRailNo"], font=textSetting.textList["font2"])
        prevRailLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # prevRail
        self.v_prevRail = tkinter.IntVar()
        prevRailEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_prevRail, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        prevRailEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenchuName
        mdlKasenchuLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
        mdlKasenchuLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenchuNameCombo
        self.mdlKasenchuCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlKasenchuCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenName
        mdlKasenLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
        mdlKasenLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # kasenNameCombo
        self.mdlKasenCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.mdlKasenCb.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # fixAmbName
        fixAmbLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railFixAmbLabel"], font=textSetting.textList["font2"])
        fixAmbLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # fixAmbNamecombo
        self.fixAmbCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
        self.fixAmbCb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # perName
        perLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPer"], font=textSetting.textList["font2"])
        perLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # per
        self.v_per = tkinter.DoubleVar()
        perEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        perEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setLsTrialSecondHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)
        xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railPosXyzInfo"])
        xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        # railPosXName
        xPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosX"], font=textSetting.textList["font2"])
        xPosLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosX
        self.v_x_pos = tkinter.DoubleVar()
        x_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        x_posEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosYName
        yPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosY"], font=textSetting.textList["font2"])
        yPosLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosY
        self.v_y_pos = tkinter.DoubleVar()
        y_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        y_posEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosZName
        zPosLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railPosZ"], font=textSetting.textList["font2"])
        zPosLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railPosZ
        self.v_z_pos = tkinter.DoubleVar()
        z_posEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        z_posEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirXName
        xDirLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirX"], font=textSetting.textList["font2"])
        xDirLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirX
        self.v_x_dir = tkinter.DoubleVar()
        x_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        x_dirEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirYName
        yLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirY"], font=textSetting.textList["font2"])
        yLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirY
        self.v_y_dir = tkinter.DoubleVar()
        y_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        y_dirEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirZName
        zLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirZ"], font=textSetting.textList["font2"])
        zLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDirZ
        self.v_z_dir = tkinter.DoubleVar()
        z_dirEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        z_dirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        if self.decryptFile.oldFlag:
            railFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railRailInfo"])
            railFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            # nextRailName
            nextLb = ttkCustomWidget.CustomTtkLabel(railFrame, text=textSetting.textList["railEditor"]["railNextRail"], font=textSetting.textList["font2"])
            nextLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # nextRail
            self.v_next = tkinter.StringVar()
            nextEt = ttkCustomWidget.CustomTtkEntry(railFrame, textvariable=self.v_next, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            nextEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # prevRailName
            prevLb = ttkCustomWidget.CustomTtkLabel(railFrame, text=textSetting.textList["railEditor"]["railPrevRail"], font=textSetting.textList["font2"])
            prevLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # prevRail
            self.v_prev = tkinter.StringVar()
            prevEt = ttkCustomWidget.CustomTtkEntry(railFrame, textvariable=self.v_prev, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            prevEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        else:
            if self.decryptFile.readFlag or self.decryptFile.filenameNum == 7:
                xyzRotFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railRotXyzInfo"])
                xyzRotFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
                # railRotXName
                xRotLb = ttkCustomWidget.CustomTtkLabel(xyzRotFrame, text=textSetting.textList["railEditor"]["railRotX"], font=textSetting.textList["font2"])
                xRotLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                # railRotX
                self.v_x_rot = tkinter.StringVar()
                x_dirEt = ttkCustomWidget.CustomTtkEntry(xyzRotFrame, textvariable=self.v_x_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
                x_dirEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                # railRotYName
                yRotLb = ttkCustomWidget.CustomTtkLabel(xyzRotFrame, text=textSetting.textList["railEditor"]["railRotY"], font=textSetting.textList["font2"])
                yRotLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                # railRotY
                self.v_y_rot = tkinter.StringVar()
                y_dirEt = ttkCustomWidget.CustomTtkEntry(xyzRotFrame, textvariable=self.v_y_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
                y_dirEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                # railRotZName
                zRotLb = ttkCustomWidget.CustomTtkLabel(xyzRotFrame, text=textSetting.textList["railEditor"]["railRotZ"], font=textSetting.textList["font2"])
                zRotLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                # railRotZ
                self.v_z_rot = tkinter.StringVar()
                z_dirEt = ttkCustomWidget.CustomTtkEntry(xyzRotFrame, textvariable=self.v_z_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
                z_dirEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setLsTrialModelInfoHorizontalLayout(self):
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)
        kasenFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
        kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
        if self.decryptFile.oldFlag:
            # modelName
            mdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
            mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # modelNameCombo
            self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # kasenName
            mdlKasenLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
            mdlKasenLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # kasenNameCombo
            self.mdlKasenCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenCb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        else:
            # modelName
            mdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
            mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # modelNameCombo
            self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # prevRailName
            prevRailLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPrevRailNo"], font=textSetting.textList["font2"])
            prevRailLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # prevRail
            self.v_prevRail = tkinter.IntVar()
            prevRailEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_prevRail, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            prevRailEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # kasenchuName
            mdlKasenchuLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
            mdlKasenchuLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # kasenchuNameCombo
            self.mdlKasenchuCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenchuCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # kasenName
            mdlKasenLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
            mdlKasenLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # kasenNameCombo
            self.mdlKasenCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenCb.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # fixAmbName
            fixAmbLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railFixAmbLabel"], font=textSetting.textList["font2"])
            fixAmbLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # fixAmbNameCombo
            self.fixAmbCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.fixAmbCb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # perName
            perLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPer"], font=textSetting.textList["font2"])
            perLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            # per
            self.v_per = tkinter.DoubleVar()
            perEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            perEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

    def setFlagInfoLayout(self):
        flagInfoList = copy.deepcopy(textSetting.textList["railEditor"]["railFlagInfoList"])
        if self.decryptFile.game == "LSTrial":
            if self.decryptFile.oldFlag:
                return
            flagInfoList = [flagInfoList.pop(0)]
        else:
            if self.decryptFile.game != "RS":
                flagInfoList[1][4] = textSetting.textList["railEditor"]["railOldFlag1"]
                flagInfoList[1][5] = textSetting.textList["railEditor"]["railOldFlag2"]
                flagInfoList[1][6] = textSetting.textList["railEditor"]["railOldFlag3"]
                flagInfoList[1][7] = textSetting.textList["railEditor"]["railOldFlag4"]

        flagFrameLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["railFlagInfo"])
        flagFrameLf.pack(padx=25, pady=15, fill=tkinter.X)

        self.v_flagInfoList = []
        self.chkInfoList = []

        for i in range(len(flagInfoList)):
            v_flagInfo = []
            chkInfo = []
            flagFrame = ttkCustomWidget.CustomTtkFrame(flagFrameLf)
            flagFrame.pack(anchor=tkinter.NW, pady=3)
            # flagHexLabel
            v_flagHex = tkinter.StringVar()
            v_flagHex.set("0x00 (= 0)")
            flagHexLb = ttkCustomWidget.CustomTtkLabel(flagFrame, textvariable=v_flagHex, font=textSetting.textList["font2"])
            flagHexLb.grid(row=0, column=0, columnspan=8, sticky=tkinter.W + tkinter.E, padx=3, pady=3)
            for j in range(len(flagInfoList[i])):
                v_flag = tkinter.IntVar()
                v_flag.set(0)
                v_flagInfo.append(v_flag)
                flagChk = ttkCustomWidget.CustomTtkCheckbutton(flagFrame, text=flagInfoList[i][j], style="custom.railFlag.TCheckbutton", width=12, variable=v_flag, command=partial(self.changeFlag, v_flagInfo, v_flagHex))
                flagChk.grid(row=1, column=j, sticky=tkinter.W + tkinter.E, padx=6, ipadx=6, pady=3)
                chkInfo.append(flagChk)
            self.v_flagInfoList.append(v_flagInfo)
            self.chkInfoList.append(chkInfo)

    def setRailDataInfoLayout(self):
        if self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag:
            return

        railFrameLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["railRailInfo"])
        railFrameLf.pack(anchor=tkinter.NW, padx=25, pady=15)

        railFrameCntFrame = ttkCustomWidget.CustomTtkFrame(railFrameLf)
        railFrameCntFrame.pack(anchor=tkinter.NW, padx=10, pady=10)
        # railDataCountName
        railDataCntLb = ttkCustomWidget.CustomTtkLabel(railFrameCntFrame, text=textSetting.textList["railEditor"]["railRailDataCnt"], font=textSetting.textList["font2"])
        railDataCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        # railDataCount
        self.v_railDataCnt = tkinter.IntVar()
        railDataCntEt = ttkCustomWidget.CustomTtkEntry(railFrameCntFrame, textvariable=self.v_railDataCnt, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        railDataCntEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        if self.decryptFile.ver == "DEND_MAP_VER0300":
            # csvRevRailSaveButton
            csvRevRailSaveBtn = ttkCustomWidget.CustomTtkButton(railFrameCntFrame, text=textSetting.textList["railEditor"]["railCreateRevRail"], command=self.saveRevRailCsv)
            csvRevRailSaveBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)

        self.railFrame = ttkCustomWidget.CustomTtkFrame(railFrameLf)
        self.railFrame.pack(anchor=tkinter.NW, padx=10, pady=10)

        self.revRailFrame = ttkCustomWidget.CustomTtkFrame(railFrameLf)
        self.revRailFrame.pack(anchor=tkinter.NW, padx=10, pady=10)

    def changeFlag(self, v_flagInfo, v_flagHex):
        res = 0
        for i, v_flag in enumerate(v_flagInfo):
            if v_flag.get() == 1:
                res += 2**(7 - i)
        strFlagHex = "0x{0:02x} (= {1})".format(res, res)
        v_flagHex.set(strFlagHex)

    def setRailInfo(self, cnt):
        self.varRailList = []
        self.varRailCnt = 0
        children = self.railFrame.winfo_children()
        for child in children:
            child.destroy()

        for i in range(cnt):
            nextRailLb = ttkCustomWidget.CustomTtkLabel(self.railFrame, text=textSetting.textList["railEditor"]["railNextRail"], width=10, font=textSetting.textList["font2"])
            nextRailLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.varRailList.append(tkinter.IntVar())
            nextRailNoEt = ttkCustomWidget.CustomTtkEntry(self.railFrame, textvariable=self.varRailList[self.varRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            nextRailNoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRailCnt += 1
            self.varRailList.append(tkinter.IntVar())
            nextRailPosEt = ttkCustomWidget.CustomTtkEntry(self.railFrame, textvariable=self.varRailList[self.varRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            nextRailPosEt.grid(row=i, column=2, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRailCnt += 1

            prevRailLb = ttkCustomWidget.CustomTtkLabel(self.railFrame, text=textSetting.textList["railEditor"]["railPrevRail"], width=10, font=textSetting.textList["font2"])
            prevRailLb.grid(row=i, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.varRailList.append(tkinter.IntVar())
            prevRailNoEt = ttkCustomWidget.CustomTtkEntry(self.railFrame, textvariable=self.varRailList[self.varRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            prevRailNoEt.grid(row=i, column=4, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRailCnt += 1
            self.varRailList.append(tkinter.IntVar())
            prevRailPosEt = ttkCustomWidget.CustomTtkEntry(self.railFrame, textvariable=self.varRailList[self.varRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            prevRailPosEt.grid(row=i, column=5, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRailCnt += 1

    def setRevRailInfo(self, cnt):
        self.varRevRailList = []
        self.varRevRailCnt = 0
        children = self.revRailFrame.winfo_children()
        for child in children:
            child.destroy()

        for i in range(cnt):
            revNextRailLb = ttkCustomWidget.CustomTtkLabel(self.revRailFrame, text=textSetting.textList["railEditor"]["railRevNextRail"], font=textSetting.textList["font2"])
            revNextRailLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.varRevRailList.append(tkinter.IntVar())
            revNextRailNoEt = ttkCustomWidget.CustomTtkEntry(self.revRailFrame, textvariable=self.varRevRailList[self.varRevRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            revNextRailNoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRevRailCnt += 1
            self.varRevRailList.append(tkinter.IntVar())
            revNextRailPosEt = ttkCustomWidget.CustomTtkEntry(self.revRailFrame, textvariable=self.varRevRailList[self.varRevRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            revNextRailPosEt.grid(row=i, column=2, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRevRailCnt += 1

            revPrevRailLb = ttkCustomWidget.CustomTtkLabel(self.revRailFrame, text=textSetting.textList["railEditor"]["railRevPrevRail"], font=textSetting.textList["font2"])
            revPrevRailLb.grid(row=i, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.varRevRailList.append(tkinter.IntVar())
            revPrevRailNoEt = ttkCustomWidget.CustomTtkEntry(self.revRailFrame, textvariable=self.varRevRailList[self.varRevRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            revPrevRailNoEt.grid(row=i, column=4, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRevRailCnt += 1
            self.varRevRailList.append(tkinter.IntVar())
            revPrevRailPosEt = ttkCustomWidget.CustomTtkEntry(self.revRailFrame, textvariable=self.varRevRailList[self.varRevRailCnt], font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            revPrevRailPosEt.grid(row=i, column=5, sticky=tkinter.W + tkinter.E, pady=5)
            self.varRevRailCnt += 1

    def searchRail(self):
        railNo = self.v_railNo.get()
        if len(self.railList) == 0:
            return

        if railNo < 0 or railNo >= len(self.railList):
            if railNo < 0:
                railNo = 0
            else:
                railNo = len(self.railList) - 1
            self.v_railNo.set(railNo)

        railInfo = self.railList[railNo]

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.v_prevRail.set(railInfo[1])
            self.v_block.set(railInfo[2])
            self.v_x.set(railInfo[3])
            self.v_y.set(railInfo[4])
            self.v_z.set(railInfo[5])

            self.mdlNoCb.current(railInfo[6])
            kasenNo = railInfo[7]
            if kasenNo == -1 or kasenNo == -2:
                kasenNo = len(self.smfList) + kasenNo
            self.mdlKasenCb.current(kasenNo)

            kasenchuNo = railInfo[8]
            if kasenchuNo == -1 or kasenchuNo == -2:
                kasenchuNo = len(self.smfList) + kasenchuNo
            self.mdlKasenchuCb.current(kasenchuNo)
            self.v_per.set(railInfo[9])

            for i, v_flagInfo in enumerate(self.v_flagInfoList):
                railFlag = railInfo[10 + i]
                for j, v_flag in enumerate(v_flagInfo):
                    chk = self.chkInfoList[i][j]
                    if railFlag & (2**(7 - j)) == 0:
                        v_flag.set(1)
                        chk.invoke()
                    else:
                        v_flag.set(0)
                        chk.invoke()

            railCount = railInfo[14]
            self.v_railDataCnt.set(railCount)
            self.setRailInfo(railCount)
            for i in range(len(self.varRailList)):
                self.varRailList[i].set(railInfo[15 + i])

            if self.decryptFile.ver == "DEND_MAP_VER0400":
                self.setRevRailInfo(railCount)
                for i in range(len(self.varRevRailList)):
                    self.varRevRailList[i].set(railInfo[15 + railCount * 4 + i])
        elif self.decryptFile.game == "LS":
            railIdx = 1
            if self.decryptFile.ver == "DEND_MAP_VER0101":
                self.v_prevRail2.set(railInfo[railIdx])
                railIdx += 2
            #
            self.v_x_pos.set(railInfo[railIdx])
            railIdx += 1
            self.v_y_pos.set(railInfo[railIdx])
            railIdx += 1
            self.v_z_pos.set(railInfo[railIdx])
            railIdx += 1
            self.v_x_dir.set(railInfo[railIdx])
            railIdx += 1
            self.v_y_dir.set(railInfo[railIdx])
            railIdx += 1
            self.v_z_dir.set(railInfo[railIdx])
            railIdx += 1

            self.mdlNoCb.current(railInfo[railIdx])
            railIdx += 1
            self.v_prevRail.set(railInfo[railIdx])
            railIdx += 1

            if railInfo[railIdx - 1] == -1:
                self.v_x_rot.set(str(railInfo[railIdx]))
                railIdx += 1
                self.v_y_rot.set(str(railInfo[railIdx]))
                railIdx += 1
                self.v_z_rot.set(str(railInfo[railIdx]))
                railIdx += 1
            else:
                self.v_x_rot.set("-")
                self.v_y_rot.set("-")
                self.v_z_rot.set("-")

            kasenchuNo = railInfo[railIdx]
            if kasenchuNo == -1:
                kasenchuNo = len(self.smfList) + kasenchuNo
            self.mdlKasenchuCb.current(kasenchuNo)
            railIdx += 1

            kasenNo = railInfo[railIdx]
            if kasenNo == -1:
                kasenNo = len(self.smfList) + kasenNo
            self.mdlKasenCb.current(kasenNo)
            railIdx += 1

            fixAmbNo = railInfo[railIdx]
            if fixAmbNo == -1:
                fixAmbNo = len(self.smfList) + fixAmbNo
            self.fixAmbCb.current(fixAmbNo)
            railIdx += 1

            self.v_per.set(railInfo[railIdx])
            railIdx += 1

            for i, v_flagInfo in enumerate(self.v_flagInfoList):
                railFlag = railInfo[railIdx]
                for j, v_flag in enumerate(v_flagInfo):
                    chk = self.chkInfoList[i][j]
                    if railFlag & (2**(7 - j)) == 0:
                        v_flag.set(1)
                        chk.invoke()
                    else:
                        v_flag.set(0)
                        chk.invoke()
                railIdx += 1

            railData = railInfo[railIdx]
            self.v_railDataCnt.set(railData)
            self.setRailInfo(railData)
            railIdx += 1
            for i in range(len(self.varRailList)):
                self.varRailList[i].set(railInfo[railIdx])
                railIdx += 1
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.oldFlag:
                railIdx = 1
                #
                self.v_x_pos.set(railInfo[railIdx])
                railIdx += 1
                self.v_y_pos.set(railInfo[railIdx])
                railIdx += 1
                self.v_z_pos.set(railInfo[railIdx])
                railIdx += 1

                self.v_next.set(railInfo[railIdx])
                railIdx += 1
                self.v_prev.set(railInfo[railIdx])
                railIdx += 1

                self.v_x_dir.set(railInfo[railIdx])
                railIdx += 1
                self.v_y_dir.set(railInfo[railIdx])
                railIdx += 1
                self.v_z_dir.set(railInfo[railIdx])
                railIdx += 1

                self.mdlNoCb.current(railInfo[railIdx])
                railIdx += 1

                kasenNo = railInfo[railIdx]
                if kasenNo == -1:
                    kasenNo = len(self.smfList) + kasenNo
                self.mdlKasenCb.current(kasenNo)
                railIdx += 1
            else:
                railIdx = 1
                #
                self.v_x_pos.set(railInfo[railIdx])
                railIdx += 1
                self.v_y_pos.set(railInfo[railIdx])
                railIdx += 1
                self.v_z_pos.set(railInfo[railIdx])
                railIdx += 1
                self.v_x_dir.set(railInfo[railIdx])
                railIdx += 1
                self.v_y_dir.set(railInfo[railIdx])
                railIdx += 1
                self.v_z_dir.set(railInfo[railIdx])
                railIdx += 1

                self.mdlNoCb.current(railInfo[railIdx])
                railIdx += 1
                self.v_prevRail.set(railInfo[railIdx])
                railIdx += 1

                if self.decryptFile.readFlag or self.decryptFile.filenameNum == 7:
                    if railInfo[railIdx - 1] == -1:
                        self.v_x_rot.set(str(railInfo[railIdx]))
                        railIdx += 1
                        self.v_y_rot.set(str(railInfo[railIdx]))
                        railIdx += 1
                        self.v_z_rot.set(str(railInfo[railIdx]))
                        railIdx += 1
                    else:
                        self.v_x_rot.set("-")
                        self.v_y_rot.set("-")
                        self.v_z_rot.set("-")

                kasenchuNo = railInfo[railIdx]
                if kasenchuNo == -1:
                    kasenchuNo = len(self.smfList) + kasenchuNo
                self.mdlKasenchuCb.current(kasenchuNo)
                railIdx += 1

                kasenNo = railInfo[railIdx]
                if kasenNo == -1:
                    kasenNo = len(self.smfList) + kasenNo
                self.mdlKasenCb.current(kasenNo)
                railIdx += 1

                fixAmbNo = railInfo[railIdx]
                if fixAmbNo == -1:
                    fixAmbNo = len(self.smfList) + fixAmbNo
                self.fixAmbCb.current(fixAmbNo)
                railIdx += 1

                self.v_per.set(railInfo[railIdx])
                railIdx += 1

                for i, v_flagInfo in enumerate(self.v_flagInfoList):
                    railFlag = railInfo[railIdx]
                    for j, v_flag in enumerate(v_flagInfo):
                        chk = self.chkInfoList[i][j]
                        if railFlag & (2**(7 - j)) == 0:
                            v_flag.set(1)
                            chk.invoke()
                        else:
                            v_flag.set(0)
                            chk.invoke()
                    railIdx += 1

                railData = railInfo[railIdx]
                self.v_railDataCnt.set(railData)
                self.setRailInfo(railData)
                railIdx += 1
                for i in range(len(self.varRailList)):
                    self.varRailList[i].set(railInfo[railIdx])
                    railIdx += 1

    def extractCsv(self):
        filename = self.decryptFile.filename + ".csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["railCsvFileType"], "*.csv")])
        if not file_path:
            return

        try:
            self.decryptFile.extractRailCsv(file_path)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except PermissionError:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def saveCsv(self):
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["railCsvFileType"], "*.csv")])
        if not file_path:
            return

        railObj, message = self.decryptFile.loadRailCsv(file_path)
        if message:
            mb.showerror(title=textSetting.textList["error"], message=message)
            return

        msg = textSetting.textList["infoList"]["I15"].format(railObj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result:
            railList = railObj["data"]
            if not self.decryptFile.saveRailCsv(railList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I88"])
            self.reloadFunc()

    def saveRevRailCsv(self):
        filename = self.decryptFile.filename + "_rev.BIN"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="bin", filetypes=[(textSetting.textList["railEditor"]["fileType"], "*.bin")])
        if not file_path:
            return

        revRailList = self.decryptFile.createRevRailList()
        if revRailList is None:
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        if not self.decryptFile.createRevRailFile(revRailList, file_path):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E134"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I89"])
        self.reloadFunc()

    def csToRs(self):
        filename = self.decryptFile.filename + "_RS.BIN"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="bin", filetypes=[(textSetting.textList["railEditor"]["railCsToRsBinType"], "*.bin")])
        if not file_path:
            return

        newByteArr = self.decryptFile.csToRs()
        if newByteArr is None:
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E72"])
            return
        self.decryptFile.createCsToRsRailFile(newByteArr, file_path)
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I90"])
