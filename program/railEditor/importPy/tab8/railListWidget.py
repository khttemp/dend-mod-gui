import os
import copy

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import program.textSetting as textSetting


class RailListWidget:
    def __init__(self, frame, decryptFile, railList, reloadFunc):
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

        self.railNoFrame = ttk.Frame(self.frame)
        self.railNoFrame.pack(anchor=tkinter.NW, padx=30, pady=30, fill=tkinter.X)
        self.railNoLb = ttk.Label(self.railNoFrame, text=textSetting.textList["railEditor"]["railRailNo"], font=textSetting.textList["font2"])
        self.railNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.v_railNo = tkinter.IntVar()
        self.railNoEt = ttk.Entry(self.railNoFrame, textvariable=self.v_railNo, font=textSetting.textList["font2"], width=7, justify="center")
        self.railNoEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10)
        self.searchBtn = ttk.Button(self.railNoFrame, text=textSetting.textList["railEditor"]["railSearchBtnLabel"], command=lambda: self.searchRail(self.v_railNo.get()))
        self.searchBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)

        self.csvSaveBtn = ttk.Button(self.railNoFrame, text=textSetting.textList["railEditor"]["railCsvSaveLabel"], command=self.saveCsv)
        self.csvSaveBtn.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=30)

        if self.decryptFile.game == "CS":
            self.csToRsBtn = ttk.Button(self.railNoFrame, text=textSetting.textList["railEditor"]["railCsToRs"], command=self.csToRs)
            self.csToRsBtn.grid(row=0, column=4, sticky=tkinter.W + tkinter.E, padx=30)

        ###
        self.sidePackFrame = ttk.Frame(self.frame)
        self.sidePackFrame.pack(anchor=tkinter.NW, padx=20)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            #
            self.blockFrameLf = ttk.LabelFrame(self.sidePackFrame, text=textSetting.textList["railEditor"]["railBlockInfo"])
            self.blockFrameLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            self.prevRailLb = ttk.Label(self.blockFrameLf, text=textSetting.textList["railEditor"]["railPrevRailNo"], font=textSetting.textList["font2"])
            self.prevRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_prevRail = tkinter.IntVar()
            self.prevRailEt = ttk.Entry(self.blockFrameLf, textvariable=self.v_prevRail, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.prevRailEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.blockLb = ttk.Label(self.blockFrameLf, text=textSetting.textList["railEditor"]["railBlockNo"], font=textSetting.textList["font2"])
            self.blockLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_block = tkinter.IntVar()
            self.blockEt = ttk.Entry(self.blockFrameLf, textvariable=self.v_block, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.blockEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            #
            self.xyzFrame = ttk.LabelFrame(self.sidePackFrame, text=textSetting.textList["railEditor"]["railXyzInfo"])
            self.xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            self.xLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railDirX"], font=textSetting.textList["font2"])
            self.xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_x = tkinter.DoubleVar()
            self.xEt = ttk.Entry(self.xyzFrame, textvariable=self.v_x, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.xEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.yLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railDirY"], font=textSetting.textList["font2"])
            self.yLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_y = tkinter.DoubleVar()
            self.yEt = ttk.Entry(self.xyzFrame, textvariable=self.v_y, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.yEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.zLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railDirZ"], font=textSetting.textList["font2"])
            self.zLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_z = tkinter.DoubleVar()
            self.zEt = ttk.Entry(self.xyzFrame, textvariable=self.v_z, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.zEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.kasenFrame = ttk.LabelFrame(self.sidePackFrame, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
            self.kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            self.mdlNoLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
            self.mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlNoCb = ttk.Combobox(self.kasenFrame, width=30, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            if self.decryptFile.game in ["CS", "RS"]:
                self.mdlKasenLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railKasenNoLabel"], font=textSetting.textList["font2"])
                self.mdlKasenLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                self.v_mdlKasen = tkinter.IntVar()
                self.mdlKasenEt = ttk.Entry(self.kasenFrame, textvariable=self.v_mdlKasen, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
                self.mdlKasenEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            elif self.decryptFile.game == "BS":
                self.mdlKasenLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
                self.mdlKasenLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                self.mdlKasenCb = ttk.Combobox(self.kasenFrame, width=30, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
                self.mdlKasenCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.mdlKasenchuLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
            self.mdlKasenchuLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlKasenchuCb = ttk.Combobox(self.kasenFrame, width=30, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenchuCb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.perLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railPer"], font=textSetting.textList["font2"])
            self.perLb.grid(row=3, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_per = tkinter.DoubleVar()
            self.perEt = ttk.Entry(self.kasenFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.perEt.grid(row=3, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        elif self.decryptFile.game == "LS":
            if self.decryptFile.ver == "DEND_MAP_VER0101":
                self.verLf = ttk.LabelFrame(self.sidePackFrame, text=textSetting.textList["railEditor"]["railLsVer0101"])
                self.verLf.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
                self.prevRailLb = ttk.Label(self.verLf, text=textSetting.textList["railEditor"]["railPrevRail2No"], font=textSetting.textList["font2"])
                self.prevRailLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
                self.v_prevRail2 = tkinter.IntVar()
                self.prevRailEt = ttk.Entry(self.verLf, textvariable=self.v_prevRail2, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
                self.prevRailEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            #
            self.xyzFrame = ttk.LabelFrame(self.sidePackFrame, text=textSetting.textList["railEditor"]["railPosXyzInfo"])
            self.xyzFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            self.xLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railPosX"], font=textSetting.textList["font2"])
            self.xLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_x_pos = tkinter.DoubleVar()
            self.x_posEt = ttk.Entry(self.xyzFrame, textvariable=self.v_x_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.x_posEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.yLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railPosY"], font=textSetting.textList["font2"])
            self.yLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_y_pos = tkinter.DoubleVar()
            self.y_posEt = ttk.Entry(self.xyzFrame, textvariable=self.v_y_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.y_posEt.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.zLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railPosZ"], font=textSetting.textList["font2"])
            self.zLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_z_pos = tkinter.DoubleVar()
            self.z_posEt = ttk.Entry(self.xyzFrame, textvariable=self.v_z_pos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.z_posEt.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            #
            self.xLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railDirX"], font=textSetting.textList["font2"])
            self.xLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_x_dir = tkinter.DoubleVar()
            self.x_dirEt = ttk.Entry(self.xyzFrame, textvariable=self.v_x_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.x_dirEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.yLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railDirY"], font=textSetting.textList["font2"])
            self.yLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_y_dir = tkinter.DoubleVar()
            self.y_dirEt = ttk.Entry(self.xyzFrame, textvariable=self.v_y_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.y_dirEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.zLb = ttk.Label(self.xyzFrame, text=textSetting.textList["railEditor"]["railDirZ"], font=textSetting.textList["font2"])
            self.zLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_z_dir = tkinter.DoubleVar()
            self.z_dirEt = ttk.Entry(self.xyzFrame, textvariable=self.v_z_dir, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.z_dirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            #
            self.xyzRotFrame = ttk.LabelFrame(self.sidePackFrame, text=textSetting.textList["railEditor"]["railRotXyzInfo"])
            self.xyzRotFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            self.xLb = ttk.Label(self.xyzRotFrame, text=textSetting.textList["railEditor"]["railRotX"], font=textSetting.textList["font2"])
            self.xLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_x_rot = tkinter.StringVar()
            self.x_dirEt = ttk.Entry(self.xyzRotFrame, textvariable=self.v_x_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.x_dirEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.yLb = ttk.Label(self.xyzRotFrame, text=textSetting.textList["railEditor"]["railRotY"], font=textSetting.textList["font2"])
            self.yLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_y_rot = tkinter.StringVar()
            self.y_dirEt = ttk.Entry(self.xyzRotFrame, textvariable=self.v_y_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.y_dirEt.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.zLb = ttk.Label(self.xyzRotFrame, text=textSetting.textList["railEditor"]["railRotZ"], font=textSetting.textList["font2"])
            self.zLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_z_rot = tkinter.StringVar()
            self.z_dirEt = ttk.Entry(self.xyzRotFrame, textvariable=self.v_z_rot, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.z_dirEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            ###
            self.sidePackFrame2 = ttk.Frame(self.frame)
            self.sidePackFrame2.pack(anchor=tkinter.NW, padx=20)

            self.kasenFrame = ttk.LabelFrame(self.sidePackFrame2, text=textSetting.textList["railEditor"]["railModelKasenInfo"])
            self.kasenFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=15)
            self.mdlNoLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railModelLabel"], font=textSetting.textList["font2"])
            self.mdlNoLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlNoCb = ttk.Combobox(self.kasenFrame, width=30, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlNoCb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.prevRailLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railPrevRailNo"], font=textSetting.textList["font2"])
            self.prevRailLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_prevRail = tkinter.IntVar()
            self.prevRailEt = ttk.Entry(self.kasenFrame, textvariable=self.v_prevRail, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.prevRailEt.grid(row=0, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.mdlKasenchuLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railKasenchuLabel"], font=textSetting.textList["font2"])
            self.mdlKasenchuLb.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlKasenchuCb = ttk.Combobox(self.kasenFrame, width=30, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenchuCb.grid(row=1, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.mdlKasenLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railKasenLabel"], font=textSetting.textList["font2"])
            self.mdlKasenLb.grid(row=1, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.mdlKasenCb = ttk.Combobox(self.kasenFrame, width=30, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.mdlKasenCb.grid(row=1, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.fixAmbLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railFixAmbLabel"], font=textSetting.textList["font2"])
            self.fixAmbLb.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.fixAmbCb = ttk.Combobox(self.kasenFrame, width=30, font=textSetting.textList["font2"], values=self.smfList, state="disabled")
            self.fixAmbCb.grid(row=2, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

            self.perLb = ttk.Label(self.kasenFrame, text=textSetting.textList["railEditor"]["railPer"], font=textSetting.textList["font2"])
            self.perLb.grid(row=2, column=2, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
            self.v_per = tkinter.DoubleVar()
            self.perEt = ttk.Entry(self.kasenFrame, textvariable=self.v_per, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.perEt.grid(row=2, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        ###
        self.flagFrameLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["railFlagInfo"])
        self.flagFrameLf.pack(padx=30, pady=15, fill=tkinter.X)

        flagInfoList = textSetting.textList["railEditor"]["railFlagInfoList"]

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
            self.flagFrame = tkinter.Frame(self.flagFrameLf)
            self.flagFrame.pack(anchor=tkinter.NW, pady=3)

            self.v_flagHex = tkinter.StringVar()
            self.v_flagHex.set("0x00")
            self.v_flagHexList.append(self.v_flagHex)
            self.flagHexLb = ttk.Label(self.flagFrame, textvariable=self.v_flagHex, font=textSetting.textList["font2"])
            self.flagHexLb.grid(row=0, column=0, columnspan=8, sticky=tkinter.W + tkinter.E, padx=3, pady=3)
            for j in range(len(flagInfoList[i])):
                self.v_flag = tkinter.IntVar()
                self.v_flag.set(0)
                v_flagInfo.append(self.v_flag)
                self.flagChk = tkinter.Checkbutton(self.flagFrame, text=flagInfoList[i][j], width=10, variable=self.v_flag, command=self.changeFlag)
                self.flagChk.grid(row=1, column=j, sticky=tkinter.W + tkinter.E, padx=6, ipadx=6, pady=3)
                chkInfo.append(self.flagChk)
            self.v_flagInfoList.append(v_flagInfo)
            self.chkInfoList.append(chkInfo)

        ###
        self.railFrameLf = ttk.LabelFrame(self.frame, text=textSetting.textList["railEditor"]["railRailInfo"])
        self.railFrameLf.pack(anchor=tkinter.NW, padx=30, pady=15)

        self.railFrameCntFrame = ttk.Frame(self.railFrameLf)
        self.railFrameCntFrame.pack(anchor=tkinter.NW, padx=10, pady=10)
        self.railDataCntLb = ttk.Label(self.railFrameCntFrame, text=textSetting.textList["railEditor"]["railRailDataCnt"], font=textSetting.textList["font2"])
        self.railDataCntLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=10)
        self.v_railDataCnt = tkinter.IntVar()
        self.railDataCntEt = ttk.Entry(self.railFrameCntFrame, textvariable=self.v_railDataCnt, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
        self.railDataCntEt.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, padx=10, pady=10)

        if self.decryptFile.ver == "DEND_MAP_VER0300":
            self.csvRevRailSaveBtn = ttk.Button(self.railFrameCntFrame, text=textSetting.textList["railEditor"]["railCreateRevRail"], command=self.saveRevRailCsv)
            self.csvRevRailSaveBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E, padx=30)

        self.railFrame = ttk.Frame(self.railFrameLf)
        self.railFrame.pack(anchor=tkinter.NW, padx=10, pady=10)

        self.revRailFrame = ttk.Frame(self.railFrameLf)
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
        children = self.railFrame.winfo_children()
        for child in children:
            child.destroy()

        for i in range(cnt):
            self.nextRailLb = ttk.Label(self.railFrame, text=textSetting.textList["railEditor"]["railNextRail"], width=11, font=textSetting.textList["font2"])
            self.nextRailLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.v_nextRailNo = tkinter.IntVar()
            self.varRailList.append(self.v_nextRailNo)
            self.nextRailNoEt = ttk.Entry(self.railFrame, textvariable=self.v_nextRailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.nextRailNoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E, pady=5)
            self.v_nextRailPos = tkinter.IntVar()
            self.varRailList.append(self.v_nextRailPos)
            self.nextRailPosEt = ttk.Entry(self.railFrame, textvariable=self.v_nextRailPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.nextRailPosEt.grid(row=i, column=2, sticky=tkinter.W + tkinter.E, pady=5)

            self.prevRailLb = ttk.Label(self.railFrame, text=textSetting.textList["railEditor"]["railPrevRail"], width=11, font=textSetting.textList["font2"])
            self.prevRailLb.grid(row=i, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.v_prevRailNo = tkinter.IntVar()
            self.varRailList.append(self.v_prevRailNo)
            self.prevRailNoEt = ttk.Entry(self.railFrame, textvariable=self.v_prevRailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.prevRailNoEt.grid(row=i, column=4, sticky=tkinter.W + tkinter.E, pady=5)
            self.v_prevRailPos = tkinter.IntVar()
            self.varRailList.append(self.v_prevRailPos)
            self.prevRailPosEt = ttk.Entry(self.railFrame, textvariable=self.v_prevRailPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.prevRailPosEt.grid(row=i, column=5, sticky=tkinter.W + tkinter.E, pady=5)

    def setRevRailInfo(self, cnt):
        self.varRevRailList = []
        children = self.revRailFrame.winfo_children()
        for child in children:
            child.destroy()

        for i in range(cnt):
            self.revNextRailLb = ttk.Label(self.revRailFrame, text=textSetting.textList["railEditor"]["railRevNextRail"], font=textSetting.textList["font2"])
            self.revNextRailLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.v_revNextRailNo = tkinter.IntVar()
            self.varRevRailList.append(self.v_revNextRailNo)
            self.revNextRailNoEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revNextRailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.revNextRailNoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E, pady=5)
            self.v_revNextRailPos = tkinter.IntVar()
            self.varRevRailList.append(self.v_revNextRailPos)
            self.revNextRailPosEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revNextRailPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.revNextRailPosEt.grid(row=i, column=2, sticky=tkinter.W + tkinter.E, pady=5)

            self.revPrevRailLb = ttk.Label(self.revRailFrame, text=textSetting.textList["railEditor"]["railRevPrevRail"], font=textSetting.textList["font2"])
            self.revPrevRailLb.grid(row=i, column=3, sticky=tkinter.W + tkinter.E, padx=10, pady=5)
            self.v_revPrevRailNo = tkinter.IntVar()
            self.varRevRailList.append(self.v_revPrevRailNo)
            self.revPrevRailNoEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revPrevRailNo, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.revPrevRailNoEt.grid(row=i, column=4, sticky=tkinter.W + tkinter.E, pady=5)
            self.v_revPrevRailPos = tkinter.IntVar()
            self.varRevRailList.append(self.v_revPrevRailPos)
            self.revPrevRailPosEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revPrevRailPos, font=textSetting.textList["font2"], width=7, justify="center", state="readonly")
            self.revPrevRailPosEt.grid(row=i, column=5, sticky=tkinter.W + tkinter.E, pady=5)

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
            if self.decryptFile.game in ["CS", "RS"]:
                self.v_mdlKasen.set(railInfo[7])
            elif self.decryptFile.game == "BS":
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
                        endcnt = int(arr[15 + rail_data * readCount])
                        copyElse3List = []
                        if endcnt > 0:
                            if int(arr[0]) < len(self.decryptFile.railList):
                                originRailInfo = self.decryptFile.railList[int(arr[0])]
                                originRailData = originRailInfo[14]
                                originEndcntIndex = 15 + originRailData * readCount
                                originElse3List = originRailInfo[originEndcntIndex]
                                copyElse3List = copy.deepcopy(originElse3List)

                                for i in range(endcnt):
                                    if i >= len(originElse3List):
                                        tempInfo = []
                                        for j in range(8):
                                            tempInfo.append(0)
                                        copyElse3List.append(tempInfo)
                            else:
                                for i in range(endcnt):
                                    tempInfo = []
                                    for j in range(8):
                                        tempInfo.append(0)
                                    copyElse3List.append(tempInfo)
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

                    csvIdx = 1
                    if self.decryptFile.ver == "DEND_MAP_VER0101":
                        prev_rail2 = int(arr[csvIdx])
                        railInfo.append(prev_rail2)
                        csvIdx += 1

                        if prev_rail2 != -1:
                            if int(arr[0]) < len(self.decryptFile.railList):
                                originRailInfo = self.decryptFile.railList[int(arr[0])]
                                originElse4Info = originRailInfo[2]
                                if len(originElse4Info) > 0:
                                    railInfo.append(originRailInfo[2][2:])
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

                    for i in range(6):
                        tempF = float(arr[csvIdx])
                        railInfo.append(tempF)
                        csvIdx += 1

                    mdl_no = int(arr[csvIdx])
                    railInfo.append(mdl_no)
                    csvIdx += 1

                    prev_rail = int(arr[csvIdx])
                    railInfo.append(prev_rail)
                    csvIdx += 1

                    for i in range(3):
                        if prev_rail == -1:
                            tempF = float(arr[csvIdx])
                            railInfo.append(tempF)
                        csvIdx += 1

                    kasenchu = int(arr[csvIdx])
                    railInfo.append(kasenchu)
                    csvIdx += 1

                    kasen = int(arr[csvIdx])
                    railInfo.append(kasen)
                    csvIdx += 1

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
