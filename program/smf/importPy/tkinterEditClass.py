import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog


class SwapDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, rootFrameAppearance, selectId):
        self.decryptFile = decryptFile
        self.selectId = selectId
        self.itemList = []
        self.v_itemList = []
        self.entryList = []
        self.swapFrameList = []
        self.reloadFlag = False
        self.infoMsg = textSetting.textList["infoList"]["I102"]

        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["smf"]["locationParentFrame"], font=textSetting.textList["font2"])
        swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        frameIdx = int(self.selectId[4:])
        self.swapFrameList = []
        swapFrameCbList = []
        for index, frameInfo in enumerate(self.decryptFile.frameList):
            if index == frameIdx:
                continue
            self.swapFrameList.append([index, frameInfo["name"]])
            swapFrameCbList.append("%02d(%s)" % (index, frameInfo["name"]))

        self.v_swap = tkinter.StringVar()
        self.v_swap.set(swapFrameCbList[0])
        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=20, state="readonly", font=textSetting.textList["font2"], value=swapFrameCbList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        self.swapCb.set(swapFrameCbList[0])
        super().body(master)

    def validate(self):
        swapCbIdx = self.swapCb.current()
        parentIdx = self.swapFrameList[swapCbIdx][0]
        parentName = self.swapFrameList[swapCbIdx][1]
        frameIdx = int(self.selectId[4:])
        frameName = self.decryptFile.frameList[frameIdx]["name"]
        self.warnMsg = textSetting.textList["infoList"]["I103"].format(frameName, parentName) + self.infoMsg

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=self.warnMsg, icon="warning", parent=self)
        if result:
            errorMsg = textSetting.textList["errorList"]["E4"]
            if not self.decryptFile.saveSwap(frameIdx, parentIdx):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
        self.reloadFlag = True


class SwapMeshDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, swapDecryptFile, rootFrameAppearance, meshNo):
        self.decryptFile = decryptFile
        self.swapDecryptFile = swapDecryptFile
        self.meshNo = meshNo
        self.reloadFlag = False
        self.swapMeshList = []
        self.infoMsg = textSetting.textList["infoList"]["I126"]
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["smf"]["swapToModelMeshNoLabel"], font=textSetting.textList["font2"])
        swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        self.swapMeshList = []
        swapMeshCbList = []
        for frameInfo in self.swapDecryptFile.frameList:
            if frameInfo["meshNo"] != -1:
                self.swapMeshList.append(frameInfo["meshNo"])
                swapMeshCbList.append("%s (Mesh No.%d)" % (frameInfo["name"], frameInfo["meshNo"]))

        self.v_swap = tkinter.StringVar()
        self.v_swap.set(swapMeshCbList[0])
        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=20, state="readonly", font=textSetting.textList["font2"], value=swapMeshCbList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        self.swapCb.set(swapMeshCbList[0])
        super().body(master)

    def validate(self):
        swapCbIdx = self.swapCb.current()
        swapMeshNo = self.swapMeshList[swapCbIdx]
        swapMeshStartIdx = -1
        swapMeshEndIdx = -1
        self.swapDecryptFile.index = self.swapDecryptFile.meshStartIdx
        for mesh in range(self.swapDecryptFile.meshCount):
            if mesh == swapMeshNo:
                swapMeshStartIdx = self.swapDecryptFile.index
            nameAndLength = self.swapDecryptFile.getStructNameAndLength()
            if not self.swapDecryptFile.readMESH(mesh, nameAndLength[1], int(50 / self.swapDecryptFile.meshCount)):
                return False
            if mesh == swapMeshNo:
                swapMeshEndIdx = self.swapDecryptFile.index
                break
        if swapMeshStartIdx == -1 or swapMeshEndIdx == -1:
            return False
        swapMeshByteArr = self.swapDecryptFile.byteArr[swapMeshStartIdx:swapMeshEndIdx]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=self.infoMsg, icon="warning", parent=self)
        if result:
            errorMsg = textSetting.textList["errorList"]["E4"]
            if not self.decryptFile.saveSwapMesh(self.meshNo, swapMeshByteArr):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
        self.reloadFlag = True


class FrameInfoDialog(CustomSimpleDialog):
    def __init__(self, master, title, frameIdx, decryptFile, rootFrameAppearance):
        self.frameIdx = frameIdx
        self.decryptFile = decryptFile
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        eleLabelList = ["Name", "pos", "rot", "meshNo"]
        self.varList = []
        self.varCnt = 0
        self.entryWidth = 20
        index = 0
        frameInfo = self.decryptFile.frameList[self.frameIdx]
        matrix = frameInfo["matrix"]
        for label in eleLabelList:
            if label == "Name":
                eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=label)
                eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.StringVar(value=frameInfo["name"]))
                eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
                index += 1
            elif label == "pos":
                posLabel = ["pos_x", "pos_y", "pos_z"]
                posInfo = self.decryptFile.matrixToPosInfo(matrix)
                for i in range(3):
                    eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=posLabel[i])
                    eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.varList.append(tkinter.DoubleVar(value=round(posInfo[i], 5)))
                    eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                    eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varCnt += 1
                    index += 1
            elif label == "rot":
                rotLabel = ["rot_x", "rot_y", "rot_z"]
                rotInfo = self.decryptFile.matrixToEulerAngleInfo(matrix)
                for i in range(3):
                    eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=rotLabel[i])
                    eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                    self.varList.append(tkinter.DoubleVar(value=round(rotInfo[i], 5)))
                    eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                    eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                    self.varCnt += 1
                    index += 1
            else:
                eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=label)
                eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.IntVar(value=frameInfo["meshNo"]))
                eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
                index += 1
        super().body(master)

    def validate(self):
        warnMsg = textSetting.textList["infoList"]["I130"]
        meshNo = self.varList[-1].get()
        if meshNo < -1:
            meshNo = -1
        frameInfo = self.decryptFile.frameList[self.frameIdx]
        originMeshNo = frameInfo["meshNo"]
        deleteFlag = False
        if originMeshNo != meshNo and meshNo != -1:
            if meshNo < self.decryptFile.meshCount:
                warnMsg = textSetting.textList["infoList"]["I132"].format(meshNo) + warnMsg
            elif originMeshNo != -1:
                warnMsg = textSetting.textList["infoList"]["I135"].format(originMeshNo) + warnMsg
            else:
                meshNo = self.decryptFile.meshCount
                warnMsg = textSetting.textList["infoList"]["I134"].format(meshNo) + warnMsg
        if originMeshNo != -1 and meshNo == -1:
            deleteFlag = True
            warnMsg = textSetting.textList["infoList"]["I133"].format(originMeshNo) + warnMsg
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            varList = []
            for var in self.varList:
                varList.append(var.get())
            if not self.decryptFile.updateFrameInfo(self.frameIdx, varList, deleteFlag):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            return True

    def apply(self):
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I131"])
        self.reloadFlag = True