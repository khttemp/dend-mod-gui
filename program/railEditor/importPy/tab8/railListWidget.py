import os
import copy

import tkinter
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget


class RailListWidget:
    def __init__(self, frame, decryptFile, railList, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.railList = railList
        self.varRailList = []
        self.varRevRailList = []
        self.reloadFunc = reloadFunc

        if self.decryptFile.game in ["CS", "RS"]:
            self.smfList.extend(textSetting.textList["railEditor"]["smfListAddList1"])
        elif self.decryptFile.game in ["LS", "BS"]:
            self.smfList.extend(textSetting.textList["railEditor"]["smfListAddList2"])

        railNoFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        railNoFrame.pack(anchor=tkinter.NW, padx=30, pady=30, fill=tkinter.X)
        railNoLb = ttkCustomWidget.CustomTtkLabel(railNoFrame, text=textSetting.textList["railEditor"]["railRailNo"], font=textSetting.textList["font2"])
        railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_railNo = tkinter.IntVar()
        railNoEt = ttkCustomWidget.CustomTtkEntry(railNoFrame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center")
        railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
        searchBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["railEditor"]["railSearchBtnLabel"], command=lambda: self.searchRail(self.v_railNo.get()))
        searchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)

        csvExtractBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, width=25, text=textSetting.textList["railEditor"]["railCsvExtractLabel"], command=self.extractCsv)
        csvExtractBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=5)
        csvSaveBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, width=25, text=textSetting.textList["railEditor"]["railCsvSaveLabel"], command=self.saveCsv)
        csvSaveBtn.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=5)

        if self.decryptFile.game == "CS":
            csToRsBtn = ttkCustomWidget.CustomTtkButton(railNoFrame, text=textSetting.textList["railEditor"]["railCsToRs"], command=self.csToRs)
            csToRsBtn.grid(row=0, column=5, sticky=tkinter.W + tkinter.E, padx=10)

        ###
        sidePackFrame = ttkCustomWidget.CustomTtkFrame(self.frame)
        sidePackFrame.pack(anchor=tkinter.NW, padx=20)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            #
            blockFrameLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railBlockInfo"])
            blockFrameLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            prevRailLb = ttkCustomWidget.CustomTtkLabel(blockFrameLf, text=textSetting.textList["railEditor"]["railPrevRailNo"], font=textSetting.textList["font2"])
            prevRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_prevRail = tkinter.IntVar()
            prevRailEt = ttkCustomWidget.CustomTtkEntry(blockFrameLf, textvariable=self.v_prevRail, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            prevRailEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            blockLb = ttkCustomWidget.CustomTtkLabel(blockFrameLf, text=textSetting.textList["railEditor"]["railBlockNo"], font=textSetting.textList["font2"])
            blockLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_block = tkinter.IntVar()
            blockEt = ttkCustomWidget.CustomTtkEntry(blockFrameLf, textvariable=self.v_block, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            blockEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            #
            xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railXyzInfo"])
            xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            xLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirX"], font=textSetting.textList["font2"])
            xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_x = tkinter.DoubleVar()
            xEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_x, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            xEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirY"], font=textSetting.textList["font2"])
            yLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_y = tkinter.DoubleVar()
            yEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_y, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            yEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zLb = ttkCustomWidget.CustomTtkLabel(xyzFrame, text=textSetting.textList["railEditor"]["railDirZ"], font=textSetting.textList["font2"])
            zLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_z = tkinter.DoubleVar()
            zEt = ttkCustomWidget.CustomTtkEntry(xyzFrame, textvariable=self.v_z, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            zEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            kasenFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
            kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            mdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
            mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            mdlKasenLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
            mdlKasenLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlKasenCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            mdlKasenchuLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
            mdlKasenchuLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlKasenchuCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenchuCb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            perLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPer"], font=textSetting.textList["font2"])
            perLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_per = tkinter.DoubleVar()
            perEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            perEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        elif self.decryptFile.game == "LS":
            if self.decryptFile.ver == "DEND_MAP_VER0101":
                verLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railLsVer0101"])
                verLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
                prevRailLb = ttkCustomWidget.CustomTtkLabel(verLf, text=textSetting.textList["railEditor"]["railPrevRail2No"], font=textSetting.textList["font2"])
                prevRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                self.v_prevRail2 = tkinter.IntVar()
                prevRailEt = ttkCustomWidget.CustomTtkEntry(verLf, textvariable=self.v_prevRail2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
                prevRailEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            #
            xyzFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railPosXyzInfo"])
            xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
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

            #
            self.xyzRotFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["railEditor"]["railRotXyzInfo"])
            self.xyzRotFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            xLb = ttkCustomWidget.CustomTtkLabel(self.xyzRotFrame, text=textSetting.textList["railEditor"]["railRotX"], font=textSetting.textList["font2"])
            xLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_x_rot = tkinter.StringVar()
            x_dirEt = ttkCustomWidget.CustomTtkEntry(self.xyzRotFrame, textvariable=self.v_x_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            x_dirEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            yLb = ttkCustomWidget.CustomTtkLabel(self.xyzRotFrame, text=textSetting.textList["railEditor"]["railRotY"], font=textSetting.textList["font2"])
            yLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_y_rot = tkinter.StringVar()
            y_dirEt = ttkCustomWidget.CustomTtkEntry(self.xyzRotFrame, textvariable=self.v_y_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            y_dirEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            zLb = ttkCustomWidget.CustomTtkLabel(self.xyzRotFrame, text=textSetting.textList["railEditor"]["railRotZ"], font=textSetting.textList["font2"])
            zLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_z_rot = tkinter.StringVar()
            z_dirEt = ttkCustomWidget.CustomTtkEntry(self.xyzRotFrame, textvariable=self.v_z_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            z_dirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            ###
            sidePackFrame2 = ttkCustomWidget.CustomTtkFrame(self.frame)
            sidePackFrame2.pack(anchor=tkinter.NW, padx=20)

            kasenFrame = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
            kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            mdlNoLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
            mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlNoCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            prevRailLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPrevRailNo"], font=textSetting.textList["font2"])
            prevRailLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_prevRail = tkinter.IntVar()
            prevRailEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_prevRail, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            prevRailEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            mdlKasenchuLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
            mdlKasenchuLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlKasenchuCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenchuCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            mdlKasenLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
            mdlKasenLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlKasenCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenCb.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            fixAmbLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railFixAmbLabel"], font=textSetting.textList["font2"])
            fixAmbLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.fixAmbCb = ttkCustomWidget.CustomTtkCombobox(kasenFrame, width=25, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.fixAmbCb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            perLb = ttkCustomWidget.CustomTtkLabel(kasenFrame, text=textSetting.textList["railEditor"]["railPer"], font=textSetting.textList["font2"])
            perLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_per = tkinter.DoubleVar()
            perEt = ttkCustomWidget.CustomTtkEntry(kasenFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            perEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        ###
        flagFrameLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["railFlagInfo"])
        flagFrameLf.pack(padx=25, pady=15, fill=tkinter.X)

        flagInfoList = copy.deepcopy(textSetting.textList["railEditor"]["railFlagInfoList"])

        if self.decryptFile.game != "RS":
            flagInfoList[1][4] = textSetting.textList["railEditor"]["railOldFlag1"]
            flagInfoList[1][5] = textSetting.textList["railEditor"]["railOldFlag2"]
            flagInfoList[1][6] = textSetting.textList["railEditor"]["railOldFlag3"]
            flagInfoList[1][7] = textSetting.textList["railEditor"]["railOldFlag4"]

        self.v_flagHexList = []
        self.v_flagInfoList = []
        self.chkInfoList = []

        for i in range(len(flagInfoList)):
            v_flagInfo = []
            chkInfo = []
            flagFrame = ttkCustomWidget.CustomTtkFrame(flagFrameLf)
            flagFrame.pack(anchor=tkinter.NW, pady=3)

            self.v_flagHex = tkinter.StringVar()
            self.v_flagHex.set("0x00")
            self.v_flagHexList.append(self.v_flagHex)
            flagHexLb = ttkCustomWidget.CustomTtkLabel(flagFrame, textvariable=self.v_flagHex, font=textSetting.textList["font2"])
            flagHexLb.grid(row=0, column=0, columnspan=8, sticky=tkinter.W + tkinter.E, padx=3, pady=3)
            for j in range(len(flagInfoList[i])):
                self.v_flag = tkinter.IntVar()
                self.v_flag.set(0)
                v_flagInfo.append(self.v_flag)
                flagChk = ttkCustomWidget.CustomTtkCheckbutton(flagFrame, text=flagInfoList[i][j], style="custom.railFlag.TCheckbutton", width=12, variable=self.v_flag, command=self.changeFlag)
                flagChk.grid(row=1, column=j, sticky=tkinter.W + tkinter.E, padx=6, ipadx=6, pady=3)
                chkInfo.append(flagChk)
            self.v_flagInfoList.append(v_flagInfo)
            self.chkInfoList.append(chkInfo)

        ###
        railFrameLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=textSetting.textList["railEditor"]["railRailInfo"])
        railFrameLf.pack(anchor=tkinter.NW, padx=25, pady=15)

        railFrameCntFrame = ttkCustomWidget.CustomTtkFrame(railFrameLf)
        railFrameCntFrame.pack(anchor=tkinter.NW, padx=10, pady=10)
        railDataCntLb = ttkCustomWidget.CustomTtkLabel(railFrameCntFrame, text=textSetting.textList["railEditor"]["railRailDataCnt"], font=textSetting.textList["font2"])
        railDataCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railDataCnt = tkinter.IntVar()
        railDataCntEt = ttkCustomWidget.CustomTtkEntry(railFrameCntFrame, textvariable=self.v_railDataCnt, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        railDataCntEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        if self.decryptFile.ver == "DEND_MAP_VER0300":
            csvRevRailSaveBtn = ttkCustomWidget.CustomTtkButton(railFrameCntFrame, text=textSetting.textList["railEditor"]["railCreateRevRail"], command=self.saveRevRailCsv)
            csvRevRailSaveBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)

        self.railFrame = ttkCustomWidget.CustomTtkFrame(railFrameLf)
        self.railFrame.pack(anchor=tkinter.NW, padx=10, pady=10)

        self.revRailFrame = ttkCustomWidget.CustomTtkFrame(railFrameLf)
        self.revRailFrame.pack(anchor=tkinter.NW, padx=10, pady=10)

        self.searchRail(self.v_railNo.get())

    def changeFlag(self):
        for i in range(len(self.v_flagInfoList)):
            res = 0
            v_flagInfo = self.v_flagInfoList[i]
            for j in range(len(v_flagInfo)):
                if v_flagInfo[j].get() == 1:
                    res += 2**(7 - j)
            strFlagHex = "0x{0:02x}".format(res)
            self.v_flagHexList[i].set(strFlagHex)

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

    def searchRail(self, railNo):
        if railNo < 0 or railNo >= len(self.railList):
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E70"])
            return
        railInfo = self.railList[railNo]

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.v_prevRail.set(railInfo[1])
            self.v_block.set(railInfo[2])
            self.v_x.set(railInfo[3])
            self.v_y.set(railInfo[4])
            self.v_z.set(railInfo[5])
            self.mdlNoCb.current(railInfo[6])
            kasenNo = railInfo[7]
            if kasenNo == -1:
                kasenNo = len(self.smfList) + kasenNo
            self.mdlKasenCb.current(kasenNo)

            kasenchuNo = railInfo[8]
            if kasenchuNo == -1 or kasenchuNo == -2:
                kasenchuNo = len(self.smfList) + kasenchuNo
            self.mdlKasenchuCb.current(kasenchuNo)
            self.v_per.set(railInfo[9])

            for i in range(4):
                strFlagHex = "0x{0:02x}".format(railInfo[10 + i])
                self.v_flagHexList[i].set(strFlagHex)
                for j in range(8):
                    if railInfo[10 + i] & (2**(7 - j)) == 0:
                        self.v_flagInfoList[i][j].set(0)
                    else:
                        self.v_flagInfoList[i][j].set(1)

            self.v_railDataCnt.set(railInfo[14])
            self.setRailInfo(railInfo[14])
            for i in range(len(self.varRailList)):
                self.varRailList[i].set(railInfo[15 + i])

            if self.decryptFile.ver == "DEND_MAP_VER0400":
                railCount = railInfo[14]
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

            for i in range(4):
                strFlagHex = "0x{0:02x}".format(railInfo[railIdx])
                self.v_flagHexList[i].set(strFlagHex)
                for j in range(8):
                    if railInfo[railIdx] & (2**(7 - j)) == 0:
                        self.v_flagInfoList[i][j].set(0)
                    else:
                        self.v_flagInfoList[i][j].set(1)
                railIdx += 1

            self.v_railDataCnt.set(railInfo[railIdx])
            self.setRailInfo(railInfo[railIdx])
            railIdx += 1
            for i in range(len(self.varRailList)):
                self.varRailList[i].set(railInfo[railIdx])
                railIdx += 1

    def extractCsv(self):
        filename = self.decryptFile.filename + ".csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["railCsvFileType"], "*.csv")])
        errorMsg = textSetting.textList["errorList"]["E7"]
        if file_path:
            if not self.decryptFile.extractRailCsv(file_path):
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])

    def saveCsv(self):
        errorMsg = textSetting.textList["errorList"]["E71"]
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["railCsvFileType"], "*.csv")])
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
            railList = []
            count = 0
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                for csv in csvLines:
                    railInfo = []
                    csv = csv.strip()
                    arr = csv.split(",")
                    if len(arr) < 15:
                        raise Exception

                    prev_rail = int(arr[1])
                    railInfo.append(prev_rail)

                    block = int(arr[2])
                    railInfo.append(block)

                    for i in range(3):
                        dirF = float(arr[3 + i])
                        railInfo.append(dirF)

                    mdl_no = int(arr[6])
                    railInfo.append(mdl_no)

                    kasen = int(arr[7])
                    railInfo.append(kasen)

                    kasenchu = int(arr[8])
                    railInfo.append(kasenchu)

                    per = float(arr[9])
                    railInfo.append(per)

                    for i in range(4):
                        flag = int(arr[10 + i], 16)
                        railInfo.append(flag)

                    rail_data = int(arr[14])
                    railInfo.append(rail_data)

                    readCount = 4
                    if self.decryptFile.ver == "DEND_MAP_VER0400":
                        readCount = 8

                    for i in range(rail_data * readCount):
                        rail = int(arr[15 + i])
                        railInfo.append(rail)

                    if self.decryptFile.game in ["BS", "CS"]:
                        copyElse3List = []
                        if int(arr[0]) < len(self.decryptFile.railList):
                            originRailInfo = self.decryptFile.railList[int(arr[0])]
                            originRailData = originRailInfo[14]
                            originEndcntIndex = 15 + originRailData * readCount
                            originElse3List = originRailInfo[originEndcntIndex]
                            copyElse3List = copy.deepcopy(originElse3List)
                        railInfo.append(copyElse3List)

                        else4Info = []
                        if prev_rail == -1:
                            originRailInfo = self.decryptFile.railList[int(arr[0])]
                            originPrevRail = originRailInfo[1]
                            if originPrevRail == -1:
                                originRailData = originRailInfo[14]
                                originElse4Index = 16 + originRailData * readCount
                                else4Info = originRailInfo[originElse4Index]
                            else:
                                else4Info.append(-1)
                                for i in range(6):
                                    else4Info.append(0)
                        railInfo.append(else4Info)

                        if self.decryptFile.game == "BS":
                            originRailInfo = self.decryptFile.railList[int(arr[0])]
                            originRailData = originRailInfo[14]
                            ambListIndex = 17 + originRailData * readCount
                            ambList = originRailInfo[ambListIndex]
                            railInfo.append(ambList)
                    railList.append(railInfo)
                    count += 1
            elif self.decryptFile.game == "LS":
                for csv in csvLines:
                    railInfo = []
                    csv = csv.strip()
                    arr = csv.split(",")
                    if len(arr) < 21:
                        raise Exception

                    if self.decryptFile.ver == "DEND_MAP_VER0101":
                        originRailInfo = self.decryptFile.railList[int(arr[0])]
                        prev_rail2 = originRailInfo[1]
                        railInfo.append(prev_rail2)

                        if prev_rail2 != -1:
                            if int(arr[0]) < len(self.decryptFile.railList):
                                originElse4Info = originRailInfo[2]
                                if len(originElse4Info) > 0:
                                    railInfo.append(originRailInfo[2])
                                else:
                                    else4Info = []
                                    for i in range(6):
                                        else4Info.append(0.0)
                                    railInfo.append(else4Info)
                            else:
                                else4Info = []
                                for i in range(6):
                                    else4Info.append(0.0)
                                railInfo.append(else4Info)
                        else:
                            railInfo.append([])

                    csvIdx = 2
                    for i in range(6):
                        tempF = float(arr[csvIdx])
                        railInfo.append(tempF)
                        csvIdx += 1

                    mdl_no = int(arr[csvIdx])
                    railInfo.append(mdl_no)
                    csvIdx += 1

                    kasen = int(arr[csvIdx])
                    csvIdx += 1

                    kasenchu = int(arr[csvIdx])
                    csvIdx += 1

                    prev_rail = int(arr[1])
                    railInfo.append(prev_rail)

                    for i in range(3):
                        if prev_rail == -1:
                            tempF = float(arr[csvIdx])
                            railInfo.append(tempF)
                        csvIdx += 1

                    railInfo.append(kasenchu)
                    railInfo.append(kasen)

                    fixAmbNo = int(arr[csvIdx])
                    railInfo.append(fixAmbNo)
                    csvIdx += 1

                    per = float(arr[csvIdx])
                    railInfo.append(per)
                    csvIdx += 1

                    for i in range(4):
                        flag = int(arr[csvIdx], 16)
                        railInfo.append(flag)
                        csvIdx += 1

                    rail_data = int(arr[csvIdx])
                    railInfo.append(rail_data)
                    csvIdx += 1

                    for i in range(rail_data * 4):
                        rail = int(arr[csvIdx])
                        railInfo.append(rail)
                        csvIdx += 1

                    if int(arr[0]) < len(self.decryptFile.railList):
                        originRailInfo = self.decryptFile.railList[int(arr[0])]
                        originAmbList = originRailInfo[-1]
                        railInfo.append(originAmbList)
                    else:
                        railInfo.append([])

                    railList.append(railInfo)
                    count += 1

            msg = textSetting.textList["infoList"]["I15"].format(count)
            result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")

            if result:
                if not self.decryptFile.saveRailCsv(railList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I88"])
                self.reloadFunc()

        except Exception:
            errorMsg = textSetting.textList["errorList"]["E15"].format(count + 1)
            mb.showerror(title=textSetting.textList["readError"], message=errorMsg)
            return

    def saveRevRailCsv(self):
        allRailOriginNextList = {}
        allRailOriginPrevList = {}
        for railInfo in self.railList:
            nextRailInfo = []
            prevRailInfo = []
            rail_data = railInfo[14]
            for i in range(rail_data):
                for j in range(4):
                    if j % 4 == 0:
                        nextRail = railInfo[15 + 4 * i + j]
                        nextRailNo = railInfo[15 + 4 * i + j + 1]
                        if nextRailNo == -1:
                            nextRail = -1
                        nextRailInfo.append([nextRail, nextRailNo])
                    elif j % 4 == 2:
                        prevRail = railInfo[15 + 4 * i + j]
                        prevRailNo = railInfo[15 + 4 * i + j + 1]
                        if prevRailNo == -1:
                            prevRail = -1
                        prevRailInfo.append([prevRail, prevRailNo])
            allRailOriginNextList[railInfo[0]] = nextRailInfo
            allRailOriginPrevList[railInfo[0]] = prevRailInfo

        allModelRailCount = {railInfo[0]: railInfo[14] for railInfo in self.railList}
        allModelRailLen = {i: self.decryptFile.smfList[i][3] for i in range(len(self.decryptFile.smfList))}

        filename = self.decryptFile.filename + "_rev.csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[(textSetting.textList["railEditor"]["railCsvFileType"], "*.csv")])
        newRailList = []
        errorMsg = textSetting.textList["errorList"]["E7"]
        if file_path:
            try:
                directory = os.path.dirname(file_path)
                name = os.path.splitext(os.path.basename(file_path))[0]
                path = os.path.join(directory, name + ".csv")
                w = open(path, "w")
                w.write("index,prev_rail,block,")
                w.write("dir_x,dir_y,dir_z,")
                w.write("mdl_no,mdl_kasen,mdl_kasenchu,per,")
                w.write("flg,flg,flg,flg,")
                w.write("rail_data,")
                w.write("next_rail,next_no,prev_rail,prev_no,\n")
                for railInfo in self.railList:
                    newRailInfo = railInfo[1:]
                    w.write("{0},{1},{2},".format(railInfo[0], railInfo[1], railInfo[2]))
                    for i in range(3):
                        w.write("{0},".format(railInfo[3 + i]))
                    w.write("{0},".format(railInfo[6]))
                    w.write("{0},".format(railInfo[7]))
                    w.write("{0},".format(railInfo[8]))
                    w.write("{0},".format(railInfo[9]))
                    for i in range(4):
                        w.write("0x{:02x},".format(railInfo[10 + i]))
                    rail_data = railInfo[14]
                    w.write("{0},".format(rail_data))
                    originRailList = []
                    for i in range(rail_data):
                        originRailInfo = []
                        for j in range(4):
                            if j % 2 == 0:
                                if railInfo[15 + 4 * i + j + 1] == -1:
                                    originRailInfo.append(-1)
                                else:
                                    originRailInfo.append(railInfo[15 + 4 * i + j])
                            w.write("{0},".format(railInfo[15 + 4 * i + j]))
                        originRailList.append(originRailInfo)

                    revRailList = []
                    originRailList.reverse()
                    for railIndex, originRailInfo in enumerate(originRailList):
                        originRailInfo.reverse()
                        for i in range(len(originRailInfo)):
                            w.write("{0},".format(originRailInfo[i]))
                            revRailList.append(originRailInfo[i])
                            newRailInfo.append(originRailInfo[i])

                            if i == 0:
                                if originRailInfo[i] == -1:
                                    w.write("{0},".format(-1))
                                    newRailInfo.append(-1)
                                    continue

                                if allModelRailCount[railInfo[0]] < allModelRailCount[originRailInfo[i]]:
                                    originNextRailList = allRailOriginNextList[originRailInfo[i]]
                                    revNextNo = 0
                                    for index, originNextRailInfo in enumerate(originNextRailList):
                                        if originNextRailInfo[0] == railInfo[0]:
                                            railCount = allModelRailCount[originRailInfo[i]]
                                            revNextNo = (railCount - 1 - index)

                                    if allModelRailCount[originRailInfo[i]] > 1:
                                        revNextNo += (revRailList.count(originRailInfo[i]) - 1)
                                    revNextNo *= 100
                                    w.write("{0},".format(revNextNo))
                                    newRailInfo.append(revNextNo)
                                else:
                                    revNextNo = (revRailList.count(originRailInfo[i]) - 1) * 100
                                    w.write("{0},".format(revNextNo))
                                    newRailInfo.append(revNextNo)
                            else:
                                if originRailInfo[i] == -1:
                                    w.write("{0},".format(-1))
                                    revRailList.append(-1)
                                    newRailInfo.append(-1)
                                    continue

                                mdlNo = self.railList[originRailInfo[i]][6]
                                railLen = allModelRailLen[mdlNo]
                                if allModelRailCount[railInfo[0]] < allModelRailCount[originRailInfo[i]]:
                                    originPrevRailList = allRailOriginPrevList[originRailInfo[i]]
                                    revPrevNo = 0
                                    for index, originPrevRailInfo in enumerate(originPrevRailList):
                                        if originPrevRailInfo[0] == railInfo[0]:
                                            railCount = allModelRailCount[originRailInfo[i]]
                                            revPrevNo = (railCount - 1 - index)

                                    if allModelRailCount[originRailInfo[i]] > 1:
                                        revPrevNo += (revRailList.count(originRailInfo[i]) - 1)
                                    revPrevNo *= 100
                                    revPrevNo += (railLen - 1)
                                    w.write("{0},".format(revPrevNo))
                                    newRailInfo.append(revPrevNo)
                                else:
                                    revPrevNo = (revRailList.count(originRailInfo[i]) - 1) * 100 + railLen - 1
                                    w.write("{0},".format(revPrevNo))
                                    newRailInfo.append(revPrevNo)
                    newRailList.append(newRailInfo)
                    w.write("\n")
                w.close()

                self.decryptFile.ver = "DEND_MAP_VER0400"
                self.decryptFile.byteArr[13] = 0x34
                path = os.path.join(directory, name + ".BIN")
                self.decryptFile.filePath = path
                if not self.decryptFile.saveRailCsv(newRailList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I89"])
                self.reloadFunc()

            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)

    def csToRs(self):
        filename = self.decryptFile.filename + "_RS.bin"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="bin", filetypes=[(textSetting.textList["railEditor"]["railCsToRsBinType"], "*.bin")])
        if file_path:
            newByteArr = self.decryptFile.csToRs()
            if newByteArr is None:
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E72"])
                return

            w = open(file_path, "wb")
            w.write(newByteArr)
            w.close()

            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I90"])
