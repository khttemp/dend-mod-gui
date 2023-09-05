import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import program.textSetting as textSetting

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


class ElsePerfWidget():
    def __init__(self, root, trainIdx, game, frame, title, titleList, elsePerfList, isRequire, defaultData, decryptFile, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.title = title
        self.perfTitle = ""
        self.titleList = titleList
        self.elsePerfList = elsePerfList
        self.isRequire = isRequire
        self.defaultData = defaultData
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc

        if self.game == gameDefine.SS:
            self.editButton = tkinter.Button(self.frame, text=textSetting.textList["orgInfoEditor"]["SSElsePerfModifyBtn"], font=textSetting.textList["font7"], command=lambda: self.editElsePerf())
            self.editButton.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

            for i in range(len(self.titleList)):
                self.titleLb = tkinter.Label(self.frame, text=self.titleList[i], font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                self.titleLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
                if self.elsePerfList is not None:
                    self.perfValueLb = tkinter.Label(self.frame, text=self.elsePerfList[i], font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                    self.perfValueLb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E, ipadx=5)
                else:
                    self.perfValueLb = tkinter.Label(self.frame, text=textSetting.textList["orgInfoEditor"]["noPerf"], font=textSetting.textList["font6"], borderwidth=1, relief="solid")
                    self.perfValueLb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E, ipadx=5)

                if self.title == "rain":
                    defDataList = self.defaultData[self.trainIdx]["rain"]
                    self.perfTitle = textSetting.textList["orgInfoEditor"]["SSRainLfLabel"]
                elif self.title == "carb":
                    defDataList = self.defaultData[self.trainIdx]["carb"]
                    self.perfTitle = textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"]
                elif self.title == "other":
                    defDataList = self.defaultData[self.trainIdx]["other"]
                    self.perfTitle = textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"]
                elif self.title == "huriko":
                    defDataList = self.defaultData[self.trainIdx]["huriko"]
                    self.perfTitle = textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"]
                elif self.title == "oneWheel":
                    defDataList = self.defaultData[self.trainIdx]["oneWheel"]
                    self.perfTitle = textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"]

                if self.elsePerfList is not None and defDataList is not None:
                    if self.title == "other":
                        if i in [0, 1, 2, 3]:
                            if self.elsePerfList[i] < defDataList[i]:
                                self.titleLb["fg"] = "blue"
                                self.perfValueLb["fg"] = "blue"
                            elif self.elsePerfList[i] > defDataList[i]:
                                self.titleLb["fg"] = "red"
                                self.perfValueLb["fg"] = "red"
                    else:
                        if self.elsePerfList[i] < defDataList[i]:
                            self.titleLb["fg"] = "blue"
                            self.perfValueLb["fg"] = "blue"
                        elif self.elsePerfList[i] > defDataList[i]:
                            self.titleLb["fg"] = "red"
                            self.perfValueLb["fg"] = "red"
                elif self.elsePerfList is None and defDataList is not None:
                    self.titleLb["fg"] = "#CCCCCC"
                    self.perfValueLb["fg"] = "#CCCCCC"
                elif self.elsePerfList is not None and defDataList is None:
                    self.titleLb["fg"] = "green"
                    self.perfValueLb["fg"] = "green"

    def editElsePerf(self):
        result = EditElsePerfInfo(self.root, textSetting.textList["orgInfoEditor"]["SSElsePerfModifyLabel"].format(self.perfTitle), self.trainIdx, self.title, self.titleList, self.elsePerfList, self.isRequire, self.defaultData, self.decryptFile)
        if result.reloadFlag:
            if not self.decryptFile.saveElsePerfList(self.trainIdx, self.title, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
            self.reloadFunc()


class EditElsePerfInfo(sd.Dialog):
    def __init__(self, master, title, trainIdx, perfTitle, titleList, elsePerfList, isRequire, defaultData, decryptFile):
        self.trainIdx = trainIdx
        self.perfTitle = perfTitle
        self.titleList = titleList
        self.elsePerfList = elsePerfList
        self.isRequire = isRequire
        self.defaultData = defaultData
        self.decryptFile = decryptFile
        self.reloadFlag = False
        self.v_check = None
        super(EditElsePerfInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        if not self.isRequire:
            self.perfUseLb = tkinter.Label(frame, text=textSetting.textList["orgInfoEditor"]["useThisPerfLabel"], font=textSetting.textList["font2"])
            self.perfUseLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
            self.v_check = tkinter.IntVar()
            self.useCheck = tkinter.Checkbutton(frame, variable=self.v_check, command=self.enablePerfInput)
            self.useCheck.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, ipadx=5)
            if self.elsePerfList is None:
                self.v_check.set(0)
            else:
                self.v_check.set(1)
        self.varList = []
        self.varEtList = []
        for i in range(len(self.titleList)):
            self.titleLb = tkinter.Label(frame, text=self.titleList[i], font=textSetting.textList["font2"])
            self.titleLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
            if self.perfTitle == "other":
                if i in [0, 2, 3]:
                    self.v_perf = tkinter.IntVar()
                elif i == 1:
                    self.v_perf = tkinter.DoubleVar()
                else:
                    self.v_perf = tkinter.StringVar()
                self.v_perf.set(self.elsePerfList[i])
                self.varList.append(self.v_perf)
            else:
                self.v_perf = tkinter.DoubleVar()
                if self.elsePerfList is not None:
                    self.v_perf.set(self.elsePerfList[i])
                self.varList.append(self.v_perf)
            self.txtEt = ttk.Entry(frame, textvariable=self.v_perf, font=textSetting.textList["font2"])
            self.txtEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.varEtList.append(self.txtEt)

            if self.perfTitle == "rain":
                defDataList = self.defaultData[self.trainIdx]["rain"]
            elif self.perfTitle == "carb":
                defDataList = self.defaultData[self.trainIdx]["carb"]
            elif self.perfTitle == "other":
                defDataList = self.defaultData[self.trainIdx]["other"]
            elif self.perfTitle == "huriko":
                defDataList = self.defaultData[self.trainIdx]["huriko"]
            elif self.perfTitle == "oneWheel":
                defDataList = self.defaultData[self.trainIdx]["oneWheel"]

            if self.perfTitle == "other":
                if i in [0, 1, 2, 3]:
                    self.defLb = tkinter.Label(frame, text=defDataList[i], font=textSetting.textList["font2"])
                    self.defLb.grid(row=i + 1, column=2, sticky=tkinter.W + tkinter.E, ipadx=5)
            elif defDataList is not None:
                self.defLb = tkinter.Label(frame, text=defDataList[i], font=textSetting.textList["font2"])
                self.defLb.grid(row=i + 1, column=2, sticky=tkinter.W + tkinter.E, ipadx=5)
        self.enablePerfInput()

    def enablePerfInput(self):
        if not self.isRequire:
            usedFlag = (self.v_check.get() == 1)
            for i in range(len(self.varEtList)):
                if usedFlag:
                    self.varEtList[i]["state"] = "normal"
                else:
                    self.varEtList[i]["state"] = "disabled"

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I60"], parent=self)
        if result:
            try:
                if not self.isRequire and self.v_check.get() == 0:
                    self.resultValueList = None
                else:
                    for i in range(len(self.varList)):
                        self.resultValueList.append(self.varList[i].get())
                return True
            except Exception as e:
                print(e)
                errorMsg = textSetting.textList["errorList"]["E14"]
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
