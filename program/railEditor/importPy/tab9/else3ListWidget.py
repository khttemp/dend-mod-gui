from functools import partial

import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from program.tkinterScrollbarFrameClass import ScrollbarFrame


class Else3ListWidget:
    def __init__(self, frame, decryptFile, else3List, reloadFunc):
        self.text = "else3"
        self.frame = frame
        self.decryptFile = decryptFile
        self.else3List = else3List
        self.reloadFunc = reloadFunc

        if self.decryptFile.game == "LS":
            self.text = "Cam"
        self.elseLf = ttk.LabelFrame(self.frame, text=self.text)
        self.elseLf.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

        scrollbarFrame = ScrollbarFrame(self.elseLf)

        self.txtFrame = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.else3CntNameLb = tkinter.Label(self.txtFrame, text="{0}数".format(self.text), font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else3CntNameLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
        self.varElse3Cnt = tkinter.IntVar()
        self.varElse3Cnt.set(len(self.else3List))
        self.else3CntTextLb = tkinter.Label(self.txtFrame, textvariable=self.varElse3Cnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else3CntTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        if self.decryptFile.game in ["LS", "RS"]:
            self.else3CntBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editElse3Cnt(self.varElse3Cnt.get()))
            self.else3CntBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

        self.txtFrame2 = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame2.pack(anchor=tkinter.NW, pady=5)
        rowNum = 0

        for i in range(len(self.else3List)):
            else3Info = self.else3List[i]
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                if self.decryptFile.game == "RS":
                    self.tempBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse3ListCnt, i, else3Info[0:2]))
                    self.tempBtn.grid(row=rowNum, column=0, sticky=tkinter.W + tkinter.E)

                self.varRailNo = tkinter.IntVar()
                self.varRailNo.set(int(else3Info[0]))
                self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varRailNo, font=("", 20), width=7, borderwidth=1, relief="solid")
                self.tempfTextLb.grid(row=rowNum, column=1, sticky=tkinter.W + tkinter.E)

                self.varTemp = tkinter.IntVar()
                self.varTemp.set(len(else3Info[1]))
                self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                self.tempfTextLb.grid(row=rowNum, column=2, sticky=tkinter.W + tkinter.E)

                rowNum += 1

                for j in range(len(else3Info[1])):
                    tempList = else3Info[1][j]
                    for k in range(len(tempList)):
                        self.varTemp = tkinter.IntVar()
                        self.varTemp.set(int(tempList[k]))
                        self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                        self.tempfTextLb.grid(row=rowNum, column=k + 1, sticky=tkinter.W + tkinter.E)

                    self.tempBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse3List, i, j, tempList))
                    self.tempBtn.grid(row=rowNum, column=0, sticky=tkinter.W + tkinter.E)
                    rowNum += 1
            elif self.decryptFile.game == "LS":
                self.tempBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse3ListCnt, i, else3Info[0:4]))
                self.tempBtn.grid(row=rowNum, column=0, sticky=tkinter.W + tkinter.E)

                for j in range(3):
                    self.varfTemp = tkinter.DoubleVar()
                    self.varfTemp.set(else3Info[j])
                    self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varfTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=rowNum, column=1 + j, sticky=tkinter.W + tkinter.E)

                self.varTemp = tkinter.IntVar()
                self.varTemp.set(len(else3Info[3]))
                self.tempTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                self.tempTextLb.grid(row=rowNum, column=4, sticky=tkinter.W + tkinter.E)

                rowNum += 1

                for j in range(len(else3Info[3])):
                    tempList = else3Info[3][j]
                    for k in range(4):
                        self.varfTemp = tkinter.DoubleVar()
                        self.varfTemp.set(tempList[k])
                        self.tempfTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varfTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                        self.tempfTextLb.grid(row=rowNum, column=k + 1, sticky=tkinter.W + tkinter.E)
                    self.varTemp = tkinter.IntVar()
                    self.varTemp.set(tempList[4])
                    self.tempTextLb = tkinter.Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempTextLb.grid(row=rowNum, column=5, sticky=tkinter.W + tkinter.E)

                    self.tempBtn = tkinter.Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse3List, i, j, tempList))
                    self.tempBtn.grid(row=rowNum, column=0, sticky=tkinter.W + tkinter.E)
                    rowNum += 1

    def editElse3Cnt(self, val):
        result = EditElse3CntWidget(self.frame, "{0}数の変更".format(self.text), self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveElse3Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="{0}数を修正しました".format(self.text))
            self.reloadFunc()

    def editElse3ListCnt(self, i, valList):
        result = EditElse3ListCntWidget(self.frame, "{0}の変更".format(self.text), self.decryptFile, valList)
        if result.reloadFlag:
            if self.decryptFile.game == "RS":
                self.else3List[i][0] = result.resultValueList[0]

                val = result.resultValueList[1]
                if val < len(self.else3List[i][1]):
                    self.else3List[i][1] = self.else3List[i][1][:val]
                else:
                    cnt = val - len(self.else3List[i][1])
                    tempList = []
                    for j in range(8):
                        tempList.append(0)

                    for j in range(cnt):
                        self.else3List[i][1].append(tempList)
            elif self.decryptFile.game == "LS":
                for j in range(3):
                    self.else3List[i][j] = result.resultValueList[j]

                val = result.resultValueList[3]
                if val < len(self.else3List[i][3]):
                    self.else3List[i][3] = self.else3List[i][3][:val]
                else:
                    cnt = val - len(self.else3List[i][3])
                    for j in range(cnt):
                        self.else3List[i][3].append([0.0, 0.0, 0.0, 0.0, 0])
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="{0}情報を修正しました".format(self.text))
            self.reloadFunc()

    def editElse3List(self, i, j, valList):
        result = EditElse3ListWidget(self.frame, "{0}の変更".format(self.text), self.decryptFile, valList)
        if result.reloadFlag:
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                self.else3List[i][1][j] = result.resultValueList
            elif self.decryptFile.game == "LS":
                self.else3List[i][3][j] = result.resultValueList

            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="{0}情報を修正しました".format(self.text))
            self.reloadFunc()


class EditElse3CntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditElse3CntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varElse3Cnt = tkinter.IntVar()
        self.varElse3Cnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varElse3Cnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varElse3Cnt.get())
                    if res < 0:
                        errorMsg = "0以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValue = res
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return False
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

            if self.resultValue < self.val:
                msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True


class EditElse3ListCntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else3Info):
        self.decryptFile = decryptFile
        self.else3Info = else3Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse3ListCntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            else3InfoLbList = ["レールNo", "数"]
            for i in range(len(self.else3Info)):
                self.else3Lb = ttk.Label(master, text=else3InfoLbList[i], font=("", 14))
                self.else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varElse3 = tkinter.IntVar()
                if i == 0:
                    self.varElse3.set(self.else3Info[i])
                else:
                    self.varElse3.set(len(self.else3Info[i]))
                self.varList.append(self.varElse3)
                self.else3Et = ttk.Entry(master, textvariable=self.varElse3, font=("", 14))
                self.else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        elif self.decryptFile.game == "LS":
            else3InfoLbList = ["f1", "f2", "f3", "数"]
            for i in range(len(self.else3Info)):
                self.else3Lb = ttk.Label(master, text=else3InfoLbList[i], font=("", 14))
                self.else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 3:
                    self.varElse3 = tkinter.IntVar()
                    self.varElse3.set(len(self.else3Info[i]))
                else:
                    self.varElse3 = tkinter.DoubleVar()
                    self.varElse3.set(self.else3Info[i])
                self.varList.append(self.varElse3)
                self.else3Et = ttk.Entry(master, textvariable=self.varElse3, font=("", 14))
                self.else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    for i in range(len(self.varList)):
                        try:
                            res = int(self.varList[i].get())
                            if i == 0:
                                if res < 0:
                                    errorMsg = "0以上の数字で入力してください。"
                                    mb.showerror(title="数字エラー", message=errorMsg)
                                    return False
                            else:
                                if res <= 0:
                                    errorMsg = "1以上の数字で入力してください。"
                                    mb.showerror(title="数字エラー", message=errorMsg)
                                    return False
                            self.resultValueList.append(res)
                        except Exception:
                            errorMsg = "数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False

                    if self.resultValueList[1] < len(self.else3Info[1]):
                        msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                        result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                        if result:
                            return True
                    else:
                        return True
                elif self.decryptFile.game == "LS":
                    for i in range(len(self.varList)):
                        try:
                            if i == 3:
                                res = int(self.varList[i].get())
                                if res < 0:
                                    errorMsg = "0以上の数字で入力してください。"
                                    mb.showerror(title="数字エラー", message=errorMsg)
                                    return False
                                self.resultValueList.append(res)
                            else:
                                res = float(self.varList[i].get())
                                self.resultValueList.append(res)
                        except Exception:
                            errorMsg = "数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False

                    if self.resultValueList[3] < len(self.else3Info[3]):
                        msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                        result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                        if result:
                            return True
                    else:
                        return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True


class EditElse3ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else3Info):
        self.decryptFile = decryptFile
        self.else3Info = else3Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse3ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            else3InfoLbList = ["タイプ1", "タイプ2", "bin index", "anime1", "anime2"]
            for i in range(len(self.else3Info)):
                self.else3Lb = ttk.Label(master, text=else3InfoLbList[i], font=("", 14))
                self.else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                self.varElse3 = tkinter.IntVar()
                self.varElse3.set(self.else3Info[i])
                self.varList.append(self.varElse3)
                self.else3Et = ttk.Entry(master, textvariable=self.varElse3, font=("", 14))
                self.else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
        elif self.decryptFile.game == "LS":
            else3InfoLbList = ["f1", "f2", "f3", "f4", "b1"]
            for i in range(len(self.else3Info)):
                self.else3Lb = ttk.Label(master, text=else3InfoLbList[i], font=("", 14))
                self.else3Lb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
                if i == 4:
                    self.varElse3 = tkinter.IntVar()
                else:
                    self.varElse3 = tkinter.DoubleVar()
                self.varElse3.set(self.else3Info[i])
                self.varList.append(self.varElse3)
                self.else3Et = ttk.Entry(master, textvariable=self.varElse3, font=("", 14))
                self.else3Et.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    for i in range(len(self.varList)):
                        try:
                            res = int(self.varList[i].get())
                        except Exception:
                            errorMsg = "数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    return True
                elif self.decryptFile.game == "LS":
                    for i in range(len(self.varList)):
                        try:
                            if i == 4:
                                res = int(self.varList[i].get())
                            else:
                                res = float(self.varList[i].get())
                        except Exception:
                            errorMsg = "数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    return True
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

    def apply(self):
        self.reloadFlag = True
