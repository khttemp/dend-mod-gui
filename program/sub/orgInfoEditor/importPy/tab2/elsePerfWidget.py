import tkinter
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog


class ElsePerfWidget(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, frame, trainIndex, decryptFile, elsePerfName, elsePerfTextNameList, elsePerfList, isRequire, defaultData, rootFrameAppearance, reloadWidget):
        super().__init__(frame)
        self.frame = frame
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elsePerfName = elsePerfName
        self.elsePerfTextNameList = elsePerfTextNameList
        self.elsePerfList = elsePerfList
        self.isRequire = isRequire
        self.defaultData = defaultData
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadWidget = reloadWidget

        mainFrame = ttkCustomWidget.CustomTtkFrame(self)
        mainFrame.pack()

        editButton = ttkCustomWidget.CustomTtkButton(mainFrame, text=textSetting.textList["orgInfoEditor"]["SSElsePerfModifyBtn"], style="custom.elsePerf.TButton", command=self.editElsePerf)
        editButton.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

        for i in range(len(self.elsePerfTextNameList)):
            titleLb = ttkCustomWidget.CustomTtkLabel(mainFrame, text=self.elsePerfTextNameList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            titleLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
            if self.elsePerfList is not None:
                perfValueLb = ttkCustomWidget.CustomTtkLabel(mainFrame, text=self.elsePerfList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            else:
                perfValueLb = ttkCustomWidget.CustomTtkLabel(mainFrame, text=textSetting.textList["orgInfoEditor"]["noPerf"], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            perfValueLb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E, ipadx=5)

            if self.elsePerfName == "rain":
                defDataList = self.defaultData["rain"]
                self.perfTitle = textSetting.textList["orgInfoEditor"]["SSRainLfLabel"]
            elif self.elsePerfName == "carb":
                defDataList = self.defaultData["carb"]
                self.perfTitle = textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"]
            elif self.elsePerfName == "other":
                defDataList = self.defaultData["other"]
                self.perfTitle = textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"]
            elif self.elsePerfName == "huriko":
                defDataList = self.defaultData["huriko"]
                self.perfTitle = textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"]
            elif self.elsePerfName == "oneWheel":
                defDataList = self.defaultData["oneWheel"]
                self.perfTitle = textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"]

            color = ""
            if self.elsePerfList is not None and defDataList is not None:
                if self.elsePerfName == "other":
                    if i in [0, 1, 2, 3]:
                        if self.elsePerfList[i] < defDataList[i]:
                            color = "blue"
                        elif self.elsePerfList[i] > defDataList[i]:
                            color = "red"
                else:
                    if self.elsePerfList[i] < defDataList[i]:
                        color = "blue"
                    elif self.elsePerfList[i] > defDataList[i]:
                        color = "red"
            elif self.elsePerfList is None and defDataList is not None:
                color = "#444444"
            elif self.elsePerfList is not None and defDataList is None:
                color = "green"
            self.setLabelColor(titleLb, perfValueLb, color)

    def setLabelColor(self, titleLb, perfValueLb, color):
        if color != "":
            titleLb.setFgColor(color)
            perfValueLb.setFgColor(color)

    def editElsePerf(self):
        result = EditElsePerfInfo(self.frame.winfo_toplevel(), textSetting.textList["orgInfoEditor"]["SSElsePerfModifyLabel"].format(self.perfTitle), self.trainIndex, self.decryptFile, self.elsePerfName, self.elsePerfTextNameList, self.elsePerfList, self.isRequire, self.defaultData, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveElsePerfList(self.trainIndex, self.elsePerfName, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
            self.reloadWidget()


class EditElsePerfInfo(CustomSimpleDialog):
    def __init__(self, master, title, trainIndex, decryptFile, elsePerfName, elsePerfTextNameList, elsePerfList, isRequire, defaultData, rootFrameAppearance):
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elsePerfName = elsePerfName
        self.elsePerfTextNameList = elsePerfTextNameList
        self.elsePerfList = elsePerfList
        self.isRequire = isRequire
        self.defaultData = defaultData
        self.reloadFlag = False
        self.v_check = None
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        if not self.isRequire:
            self.perfUseLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["useThisPerfLabel"], font=textSetting.textList["font2"])
            self.perfUseLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
            self.v_check = tkinter.IntVar()
            self.useCheck = ttkCustomWidget.CustomTtkCheckbutton(master, variable=self.v_check, command=self.enablePerfInput)
            self.useCheck.grid(row=0, column=1, sticky=tkinter.W + tkinter.E, ipadx=5)
            if self.elsePerfList is None:
                self.v_check.set(0)
            else:
                self.v_check.set(1)
        self.varList = []
        self.varEtList = []
        for i in range(len(self.elsePerfTextNameList)):
            self.elsePerfNameLb = ttkCustomWidget.CustomTtkLabel(master, text=self.elsePerfTextNameList[i], font=textSetting.textList["font2"])
            self.elsePerfNameLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
            if self.elsePerfName == "other":
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
            self.txtEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_perf, font=textSetting.textList["font2"])
            self.txtEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.varEtList.append(self.txtEt)

            if self.elsePerfName == "rain":
                defDataList = self.defaultData["rain"]
            elif self.elsePerfName == "carb":
                defDataList = self.defaultData["carb"]
            elif self.elsePerfName == "other":
                defDataList = self.defaultData["other"]
            elif self.elsePerfName == "huriko":
                defDataList = self.defaultData["huriko"]
            elif self.elsePerfName == "oneWheel":
                defDataList = self.defaultData["oneWheel"]

            if self.elsePerfName == "other":
                if i in [0, 1, 2, 3]:
                    self.defLb = ttkCustomWidget.CustomTtkLabel(master, text=defDataList[i], font=textSetting.textList["font2"])
                    self.defLb.grid(row=i + 1, column=2, sticky=tkinter.W + tkinter.E, ipadx=5)
            elif defDataList is not None:
                self.defLb = ttkCustomWidget.CustomTtkLabel(master, text=defDataList[i], font=textSetting.textList["font2"])
                self.defLb.grid(row=i + 1, column=2, sticky=tkinter.W + tkinter.E, ipadx=5)
        self.enablePerfInput()
        super().body(master)

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
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False

    def apply(self):
        self.reloadFlag = True
