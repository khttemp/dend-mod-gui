from functools import partial

import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomAskstring


class FixedListWidget:
    def __init__(self, frame, game, trainIdx, decryptFile, text, elseList, ver, rootFrameAppearance, reloadFunc):
        self.frame = frame
        self.game = game
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.ver = ver
        self.rootFrameAppearance = rootFrameAppearance
        self.reloadFunc = reloadFunc

        elseLf = ttkCustomWidget.CustomTtkLabelFrame(self.frame, text=text)
        elseLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10)

        txtFrame = ttkCustomWidget.CustomTtkFrame(elseLf)
        txtFrame.pack(anchor=tkinter.NW, padx=10)
        self.varList = []

        for i in range(len(self.elseList)):
            colNum = 0
            if self.game == 0 and ver == 1:
                varLb = ttkCustomWidget.CustomTtkLabel(txtFrame, text=textSetting.textList["orgInfoEditor"]["fixedListNumLabel"].format(i + 1), font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
                varLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
                colNum += 1
            self.varList.append(tkinter.StringVar(value=self.elseList[i]))
            tempTextLb = ttkCustomWidget.CustomTtkLabel(txtFrame, textvariable=self.varList[i], font=textSetting.textList["font6"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            tempTextLb.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E, ipadx=15)
            colNum += 1
            tempBtn = ttkCustomWidget.CustomTtkButton(txtFrame, text=textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], style="custom.update.TButton", command=partial(self.editVar, i, self.elseList[i]))
            tempBtn.grid(row=i, column=colNum, sticky=tkinter.W + tkinter.E)

    def editVar(self, i, elseInfo):
        resultObj = CustomAskstring(self.frame, title=textSetting.textList["orgInfoEditor"]["valueModify"], prompt=textSetting.textList["infoList"]["I44"], initialvalue=elseInfo, bgColor=self.rootFrameAppearance.bgColor)
        resultValue = resultObj.result

        if resultValue:
            self.elseList[i] = resultValue
            if not self.decryptFile.saveElseList(self.trainIdx, self.ver, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])
            self.reloadFunc()
