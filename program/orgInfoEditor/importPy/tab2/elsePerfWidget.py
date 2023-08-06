import tkinter
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

import program.orgInfoEditor.importPy.gameDefine as gameDefine
gameDefine.load()


class ElsePerfWidget():
    def __init__(self, root, trainIdx, game, frame, title, titleList, elsePerfList, isRequire, defaultData, decryptFile, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.title = title
        self.titleList = titleList
        self.elsePerfList = elsePerfList
        self.isRequire = isRequire
        self.defaultData = defaultData
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc
        
        if self.game == gameDefine.SS:
            self.editButton = tkinter.Button(self.frame, text="修正する", font=("", 14), command=lambda: self.editElsePerf())
            self.editButton.grid(columnspan=2, row=0, column=0, sticky=tkinter.W + tkinter.E)

            for i in range(len(self.titleList)):
                self.titleLb = tkinter.Label(self.frame, text=self.titleList[i], font=("", 20), borderwidth=1, relief="solid")
                self.titleLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
                if self.elsePerfList is not None:
                    self.perfValueLb = tkinter.Label(self.frame, text=self.elsePerfList[i], font=("", 20), borderwidth=1, relief="solid")
                    self.perfValueLb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E, ipadx=5)
                else:
                    self.perfValueLb = tkinter.Label(self.frame, text="ー", font=("", 20), borderwidth=1, relief="solid")
                    self.perfValueLb.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E, ipadx=5)
                
                if self.title == "雨":
                    defDataList = self.defaultData[self.trainIdx]["rain"]
                elif self.title == "カーブ":
                    defDataList = self.defaultData[self.trainIdx]["carb"]
                elif self.title == "Other":
                    defDataList = self.defaultData[self.trainIdx]["other"]
                elif self.title == "振り子":
                    defDataList = self.defaultData[self.trainIdx]["huriko"]
                elif self.title == "片輪走行":
                    defDataList = self.defaultData[self.trainIdx]["oneWheel"]
                
                if self.elsePerfList is not None and defDataList is not None:
                    if self.title == "Other":
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
        result = EditElsePerfInfo(self.root, "{0}情報修正".format(self.title), self.trainIdx, self.title, self.titleList, self.elsePerfList, self.isRequire, self.defaultData, self.decryptFile)
        if result.reloadFlag:
            if not self.decryptFile.saveElsePerfList(self.trainIdx, self.title, result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="情報を修正しました")
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
            self.perfUseLb = tkinter.Label(frame, text="この性能を使う", font=("", 14))
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
            self.titleLb = tkinter.Label(frame, text=self.titleList[i], font=("", 14))
            self.titleLb.grid(row=i + 1, column=0, sticky=tkinter.W + tkinter.E, ipadx=5)
            if self.perfTitle == "Other":
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
            self.txtEt = ttk.Entry(frame, textvariable=self.v_perf, font=("", 14))
            self.txtEt.grid(row=i + 1, column=1, sticky=tkinter.W + tkinter.E)
            self.varEtList.append(self.txtEt)

            if self.perfTitle == "雨":
                defDataList = self.defaultData[self.trainIdx]["rain"]
            elif self.perfTitle == "カーブ":
                defDataList = self.defaultData[self.trainIdx]["carb"]
            elif self.perfTitle == "Other":
                defDataList = self.defaultData[self.trainIdx]["other"]
            elif self.perfTitle == "振り子":
                defDataList = self.defaultData[self.trainIdx]["huriko"]
            elif self.perfTitle == "片輪走行":
                defDataList = self.defaultData[self.trainIdx]["oneWheel"]
            
            if self.perfTitle == "Other":
                if i in [0, 1, 2, 3]:
                    self.defLb = tkinter.Label(frame, text=defDataList[i], font=("", 14))
                    self.defLb.grid(row=i + 1, column=2, sticky=tkinter.W + tkinter.E, ipadx=5)
            elif defDataList is not None:
                self.defLb = tkinter.Label(frame, text=defDataList[i], font=("", 14))
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
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
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
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True     
