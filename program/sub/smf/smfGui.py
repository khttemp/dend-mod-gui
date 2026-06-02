import os
import shutil
import copy
import traceback

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.sub.textSetting as textSetting
from program.sub.errorLogClass import ErrorLogObj
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.appearance.customSimpleDialog import CustomSimpleDialog

import program.sub.smf.smfProcess as smfProcess
from program.sub.smf.dendDecrypt.decrypt import SmfDecrypt
from program.sub.smf.importPy.tkinterScrollbarTreeviewSmf import ScrollbarTreeviewSmf
from program.sub.smf.importPy.importFbx import ImportFbxObject
from program.sub.smf.importPy.extractGlb import GlbObject
from program.sub.smf.importPy.extractFbx import FbxObject
from program.sub.smf.importPy.extractX import XObject

errObj = ErrorLogObj()


class SmfWindow(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, importDict, rootFrameAppearance):
        super().__init__(master)
        self.master = master
        self.importDict = importDict
        self.rootFrameAppearance = rootFrameAppearance
        self.decryptFile = None
        self.noTexList = []

        self.v_process = tkinter.IntVar()
        self.v_process.set(0)
        self.v_d_process = tkinter.DoubleVar()
        self.v_d_process.set(0)

        processScriptFrame = ttkCustomWidget.CustomTtkFrame(master)
        processScriptFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=25, pady=(25, 5))
        rightFrame = ttkCustomWidget.CustomTtkFrame(master)
        rightFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, padx=5, pady=5)
        buttonListFrame = ttkCustomWidget.CustomTtkFrame(rightFrame)
        buttonListFrame.pack(expand=True, fill=tkinter.BOTH)
        smfInfoLabelFrame = ttkCustomWidget.CustomTtkFrame(rightFrame)
        smfInfoLabelFrame.pack(expand=True, fill=tkinter.BOTH)
        smfImageSearchFrame = ttkCustomWidget.CustomTtkFrame(rightFrame)
        smfImageSearchFrame.pack(expand=True, fill=tkinter.BOTH)

        frameEditButtonFrame = ttkCustomWidget.CustomTtkFrame(buttonListFrame)
        frameEditButtonFrame.grid(row=0, column=0, pady=10)
        copyAndPasteFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["copyAndPasteFrameLabel"], width=25, command=self.copyAndPasteFrame, state="disabled")
        copyAndPasteFrameButton.grid(row=0, column=0, padx=30, pady=5)
        deleteFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["deleteFrameLabel"], width=25, command=self.deleteFrame, state="disabled")
        deleteFrameButton.grid(row=0, column=1, padx=30, pady=5)
        editInfoFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["editInfoFrameLabel"], width=25, command=self.editInfoFrame, state="disabled")
        editInfoFrameButton.grid(row=1, column=0, padx=30, pady=5)
        swapFrameButton = ttkCustomWidget.CustomTtkButton(frameEditButtonFrame, text=textSetting.textList["smf"]["swapFrameLabel"], width=25, command=self.swapFrame, state="disabled")
        swapFrameButton.grid(row=1, column=1, padx=30, pady=5)

        self.btnList = [
            copyAndPasteFrameButton,
            deleteFrameButton,
            editInfoFrameButton,
            swapFrameButton
        ]

        meshEditButtonFrame = ttkCustomWidget.CustomTtkFrame(buttonListFrame)
        meshEditButtonFrame.grid(row=1, column=0, pady=10)
        turnModelMeshButton = ttkCustomWidget.CustomTtkButton(meshEditButtonFrame, text=textSetting.textList["smf"]["turnModelMeshLabel"], width=25, command=self.turnModelMesh, state="disabled")
        turnModelMeshButton.grid(row=0, column=0, padx=30, pady=5)
        swapModelMeshButton = ttkCustomWidget.CustomTtkButton(meshEditButtonFrame, text=textSetting.textList["smf"]["swapModelMeshLabel"], width=25, command=self.swapModelMesh, state="disabled")
        swapModelMeshButton.grid(row=0, column=1, padx=30, pady=5)
        meshMaterialCsvSaveButton = ttkCustomWidget.CustomTtkButton(meshEditButtonFrame, text=textSetting.textList["smf"]["meshMaterialCsvSaveLabel"], width=25, command=self.meshMaterialCsvSave, state="disabled")
        meshMaterialCsvSaveButton.grid(row=1, column=0, padx=30, pady=5)
        meshMaterialCsvLoadButton = ttkCustomWidget.CustomTtkButton(meshEditButtonFrame, text=textSetting.textList["smf"]["meshMaterialCsvLoadLabel"], width=25, command=self.meshMaterialCsvLoad, state="disabled")
        meshMaterialCsvLoadButton.grid(row=1, column=1, padx=30, pady=5)

        self.meshBtnList = [
            turnModelMeshButton,
            swapModelMeshButton,
            meshMaterialCsvSaveButton,
            meshMaterialCsvLoadButton
        ]

        elseEditButtonFrame = ttkCustomWidget.CustomTtkFrame(buttonListFrame)
        elseEditButtonFrame.grid(row=2, column=0, pady=10)
        self.standardButton = ttkCustomWidget.CustomTtkButton(elseEditButtonFrame, text=textSetting.textList["smf"]["createStandardLabel"], width=25, command=self.createStandardGaugeButton, state="disabled")
        self.standardButton.grid(row=0, column=0, padx=30, pady=5)
        self.extract3dObjButton = ttkCustomWidget.CustomTtkButton(elseEditButtonFrame, text=textSetting.textList["smf"]["extract3dLabel"], width=25, command=self.extract3d, state="disabled")
        self.extract3dObjButton.grid(row=0, column=1, padx=30, pady=5)

        self.progressBar = ttk.Progressbar(processScriptFrame, orient=tkinter.HORIZONTAL, variable=self.v_process, maximum=100, length=400, mode="determinate")
        self.progressBar.pack(fill=tkinter.X)

        self.scriptLf = ttkCustomWidget.CustomTtkLabelFrame(processScriptFrame, text=textSetting.textList["smf"]["scriptLabel"])
        self.scriptLf.pack(expand=True, fill=tkinter.BOTH, pady=15)
        self.frame = ScrollbarTreeviewSmf(self.scriptLf, self.btnList, self.meshBtnList)

        framePosInfoLf = ttkCustomWidget.CustomTtkLabelFrame(smfInfoLabelFrame, text=textSetting.textList["smf"]["framePosInfoLabel"])
        framePosInfoLf.grid(row=0, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

        self.v_framePosX = tkinter.DoubleVar()
        framePosXEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=self.v_framePosX, width=12, state="readonly")
        framePosXEt.grid(row=0, column=0, padx=10, pady=5)

        self.v_framePosY = tkinter.DoubleVar()
        framePosYEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=self.v_framePosY, width=12, state="readonly")
        framePosYEt.grid(row=0, column=1, padx=10, pady=5)

        self.v_framePosZ = tkinter.DoubleVar()
        framePosZEt = ttkCustomWidget.CustomTtkEntry(framePosInfoLf, font=textSetting.textList["font2"], textvariable=self.v_framePosZ, width=12, state="readonly")
        framePosZEt.grid(row=0, column=2, padx=10, pady=5)

        frameRotInfoLf = ttkCustomWidget.CustomTtkLabelFrame(smfInfoLabelFrame, text=textSetting.textList["smf"]["frameRotInfoLabel"])
        frameRotInfoLf.grid(row=1, column=0, columnspan=4, sticky=tkinter.EW, padx=30, pady=5)

        self.v_frameRotX = tkinter.DoubleVar()
        frameRotXEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=self.v_frameRotX, width=12, state="readonly")
        frameRotXEt.grid(row=0, column=0, padx=10, pady=5)

        self.v_frameRotY = tkinter.DoubleVar()
        frameRotYEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=self.v_frameRotY, width=12, state="readonly")
        frameRotYEt.grid(row=0, column=1, padx=10, pady=5)

        self.v_frameRotZ = tkinter.DoubleVar()
        frameRotZEt = ttkCustomWidget.CustomTtkEntry(frameRotInfoLf, font=textSetting.textList["font2"], textvariable=self.v_frameRotZ, width=12, state="readonly")
        frameRotZEt.grid(row=0, column=2, padx=10, pady=5)

        self.scanSmfImageButton = ttkCustomWidget.CustomTtkButton(smfImageSearchFrame, text=textSetting.textList["smf"]["scanSmfImageLabel"], width=72, command=self.scanSmfImage)
        self.scanSmfImageButton.grid(row=0, column=0, sticky=tkinter.EW, padx=30, pady=5)

        self.v_modelCount = tkinter.StringVar()
        modelCountEntry = ttkCustomWidget.CustomTtkEntry(smfImageSearchFrame, textvariable=self.v_modelCount, font=textSetting.textList["defaultFont"], justify="center", state="readonly")
        modelCountEntry.grid(row=1, column=0, sticky=tkinter.EW, padx=30, pady=5)

        self.noImageListbox = tkinter.Listbox(smfImageSearchFrame, selectmode="single", height=8, font=textSetting.textList["font2"], bg=rootFrameAppearance.bgColor, fg=rootFrameAppearance.fgColor)
        self.noImageListbox.grid(row=2, column=0, sticky=tkinter.EW, padx=30, pady=5)

        self.v_modelPath = tkinter.StringVar()
        modelPathEntry = ttkCustomWidget.CustomTtkEntry(smfImageSearchFrame, textvariable=self.v_modelPath, font=textSetting.textList["defaultFont"], state="readonly")
        modelPathEntry.grid(row=3, column=0, sticky=tkinter.EW, padx=30, pady=5)

        self.copyImageButton = ttkCustomWidget.CustomTtkButton(smfImageSearchFrame, text=textSetting.textList["smf"]["copyImageLabel"], width=50, command=self.copyImage, state="disabled")
        self.copyImageButton.grid(row=4, column=0, sticky=tkinter.EW, padx=30, pady=5)

    def progressBarUpdate(self, value, flag=False):
        if flag:
            self.v_d_process.set(self.v_d_process.get() + value)
            self.v_process.set(round(self.v_d_process.get()))
        else:
            self.v_d_process.set(int(value))
            self.v_process.set(int(value))
        self.progressBar.update()

    def deleteWidget(self):
        children = self.scriptLf.winfo_children()
        for child in children:
            child.destroy()

        for btn in self.btnList:
            btn["state"] = "disabled"
        for btn in self.meshBtnList:
            btn["state"] = "disabled"
        self.standardButton["state"] = "disabled"
        self.extract3dObjButton["state"] = "disabled"

    def createWidget(self):
        self.createTreeWidget()

        self.v_framePosX.set(0)
        self.v_framePosY.set(0)
        self.v_framePosZ.set(0)
        self.v_frameRotX.set(0)
        self.v_frameRotY.set(0)
        self.v_frameRotZ.set(0)
        self.standardButton["state"] = "normal"
        self.extract3dObjButton["state"] = "normal"

    def createTreeWidget(self):
        self.frame = ScrollbarTreeviewSmf(self.scriptLf, self.btnList, self.meshBtnList, self.getFrameInfo)
        self.frame.tree.heading("#0", text=self.decryptFile.filename, anchor=tkinter.CENTER)

        for frameObj in self.decryptFile.frameList:
            frameIdx = frameObj["frameNo"]
            fName = frameObj["name"]
            meshNo = frameObj["meshNo"]
            tags = ""
            if meshNo != -1:
                fName += textSetting.textList["smf"]["treeMeshNumFormat"].format(meshNo)
                tags = "mesh"
            parentFrameNo = frameObj["parentFrameNo"]
            self.frame.tree.insert(parent="", index="end", iid=frameIdx, text=fName, tags=tags, open=True)
            if parentFrameNo != -1:
                self.frame.tree.move(frameIdx, parentFrameNo, "end")

    def getFrameInfo(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]

        matrix = frameObj["matrix"]
        pos = self.decryptFile.matrixToPosInfo(matrix)
        self.v_framePosX.set(round(pos[0], 5))
        self.v_framePosY.set(round(pos[1], 5))
        self.v_framePosZ.set(round(pos[2], 5))
        q = self.decryptFile.matrixToEulerAngleInfo(matrix)
        self.v_frameRotX.set(round(q[0], 5))
        self.v_frameRotY.set(round(q[1], 5))
        self.v_frameRotZ.set(round(q[2], 5))

    def openFile(self):
        file_path = fd.askopenfilename(filetypes=[(textSetting.textList["smf"]["fileType"], "*.SMF")])
        if not file_path:
            return

        flagList = smfProcess.getSmfFlagOption(self.importDict["configPath"])
        self.decryptFile = SmfDecrypt(file_path, flagList, self.progressBarUpdate)
        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])
            return
        self.deleteWidget()
        self.createWidget()

    def reloadWidget(self):
        try:
            self.decryptFile = self.decryptFile.reload()
            self.deleteWidget()
            self.createWidget()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])

    def copyAndPasteFrame(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]

        frameIdx = frameObj["frameNo"]
        parentIdx = frameObj["parentFrameNo"]
        frameName = frameObj["name"]
        warnMsg = textSetting.textList["infoList"]["I127"].format(frameName)

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.addFrame(frameIdx, parentIdx):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
            self.reloadWidget()

    def deleteFrame(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]

        frameIdx = frameObj["frameNo"]
        frameName = frameObj["name"]
        warnMsg = textSetting.textList["infoList"]["I109"].format(frameName)

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.deleteFrame(frameIdx, -1):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
            self.reloadWidget()

    def editInfoFrame(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]

        result = EditFrameInfoDialog(self.master.winfo_toplevel(), textSetting.textList["smf"]["editInfoFrame"], frameObj, self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            frameIdx = frameObj["frameNo"]
            if not self.decryptFile.updateFrameInfo(frameIdx, result.resultValueList, result.meshDeleteFlag):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I131"])
            self.reloadWidget()

    def swapFrame(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]

        result = SwapFrameDialog(self.master.winfo_toplevel(), textSetting.textList["smf"]["swapFrame"], frameObj, self.decryptFile, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveSwap(result.frameIdx, result.parentIdx):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
            self.reloadWidget()

    def turnModelMesh(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]
        meshNo = frameObj["meshNo"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I124"], icon="warning")
        if result:
            if not self.decryptFile.turnModelMesh(meshNo):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I125"])
            self.reloadWidget()

    def swapModelMesh(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]
        meshNo = frameObj["meshNo"]

        file_path = fd.askopenfilename(
            filetypes=[
                (textSetting.textList["smf"]["fileType"], "*.SMF"),
                (textSetting.textList["smf"]["fbxFile"], "*.fbx")
            ]
        )
        if not file_path:
            return

        ext = os.path.splitext(os.path.basename(file_path))[1].lower()
        if ext == ".smf":
            swapDecryptFile = SmfDecrypt(file_path)
            if not swapDecryptFile.open():
                swapDecryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E74"])
                return
            
            result = SwapMeshDialog(self.master.winfo_toplevel(), textSetting.textList["smf"]["swapFrame"], swapDecryptFile, self.rootFrameAppearance)
            if result.reloadFlag:
                processResult, obj = smfProcess.getSwapMeshByteArr(result.swapMeshNo, swapDecryptFile)
                if not processResult:
                    mb.showerror(title=textSetting.textList["error"], message=obj["message"])
                    return

                if not self.decryptFile.saveSwapMesh(meshNo, obj["data"]):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
                self.reloadWidget()
        elif ext == ".fbx":
            result = SwapFbxMeshDialog(self.master.winfo_toplevel(), textSetting.textList["smf"]["swapMesh"], file_path, self.rootFrameAppearance)
            if result.reloadFlag:
                importResult, obj = result.importFbxObj.makeMeshObj(result.swapMeshNode)
                result.importFbxObj.destroyFbxObj()
                if not importResult:
                    mb.showerror(title=textSetting.textList["error"], message=obj["message"])
                    return

                if not self.decryptFile.saveSwapFbxMesh(meshNo, obj["data"], obj["flag"]):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
                self.reloadWidget()

    def meshMaterialCsvSave(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]
        meshNo = frameObj["meshNo"]

        saveName = os.path.splitext(os.path.basename(self.decryptFile.filename))[0]
        saveName += "_mesh{0}".format(meshNo)
        file_path = fd.asksaveasfilename(
            initialfile=saveName,
            filetypes=[
                (textSetting.textList["smf"]["csvFile"], "*.csv")
            ],
            defaultextension=".csv"
        )
        if not file_path:
            return

        try:
            mtrlList = self.decryptFile.meshList[meshNo]["mtrlList"]
            smfProcess.writeMaterialCsv(file_path, mtrlList)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])

    def meshMaterialCsvLoad(self):
        idx = int(self.frame.tree.selection()[0])
        frameObj = self.decryptFile.frameList[idx]
        meshNo = frameObj["meshNo"]
        file_path = fd.askopenfilename(
            filetypes=[
                (textSetting.textList["smf"]["csvFile"], "*.csv")
            ],
            defaultextension=".csv"
        )
        if not file_path:
            return

        try:
            originMtrlList = self.decryptFile.meshList[meshNo]["mtrlList"]
            processResult, obj = smfProcess.loadCsvData(file_path, originMtrlList)
            if not processResult:
                mb.showerror(title=textSetting.textList["error"], message=obj["message"])
                return

            warnMsg = textSetting.textList["infoList"]["I136"]
            if obj["noTexcInputFlag"]:
                warnMsg = textSetting.textList["infoList"]["I138"] + warnMsg
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
            if result:
                if not self.decryptFile.modifyMaterial(meshNo, obj["data"]):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I137"])
                self.reloadWidget()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def createStandardGaugeButton(self):
        if not self.decryptFile.detectGauge():
            msg = textSetting.textList["infoList"]["I105"]
            for model in self.decryptFile.standardGuageList:
                msg += "\n" + model
            mb.showerror(title=textSetting.textList["error"], message=msg)
            return

        modelIndex = self.decryptFile.standardGuageList.index(self.decryptFile.filename)
        if self.decryptFile.detectMuTrack():
            if not self.decryptFile.createStandardGauge(None):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
        else:
            modelName = self.decryptFile.d4NarrowGuageList[modelIndex]
            msg = textSetting.textList["infoList"]["I106"].format(modelName)
            mb.showinfo(title=textSetting.textList["smf"]["smfFile"], message=msg)

            file_path = fd.askopenfilename(filetypes=[(textSetting.textList["smf"]["fileType"], "*.SMF")])
            if not file_path:
                return

            filename = os.path.basename(file_path)
            if filename.upper() != modelName:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["infoList"]["I107"])
                return

            d4DecryptFile = SmfDecrypt(file_path)
            if not d4DecryptFile.open():
                d4DecryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E74"])
                return

            if not self.decryptFile.createStandardGauge(d4DecryptFile):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I108"])
        self.reloadWidget()

    def extract3d(self):
        saveName = os.path.splitext(os.path.basename(self.decryptFile.filename))[0]
        file_path = fd.asksaveasfilename(
            initialfile=saveName,
            filetypes=[
                (textSetting.textList["smf"]["fbxFile"], "*.fbx"),
                (textSetting.textList["smf"]["glbFile"], "*.glb"),
                (textSetting.textList["smf"]["xFile"], "*.x")
            ],
            defaultextension=".fbx"
        )
        if not file_path:
            return

        ext = os.path.splitext(os.path.basename(file_path))[1].lower()
        if ext == ".fbx":
            fbxObj = FbxObject(file_path, self.decryptFile)
            if not fbxObj.makeFbxFile():
                fbxObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I123"])
        elif ext == ".glb":
            glbObj = GlbObject(file_path, self.decryptFile, self.importDict["configPath"])
            if not glbObj.makeGlbFile():
                glbObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I121"])
        elif ext == ".x":
            xObj = XObject(file_path, self.decryptFile)
            if not xObj.makeXFile():
                xObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I122"])

    def scanSmfImage(self):
        fileList = fd.askopenfilenames(filetypes=[(textSetting.textList["smf"]["fileListType"], "*.SMF")])
        if not fileList:
            return

        dirPath = os.path.dirname(fileList[0])
        self.v_modelPath.set(dirPath)
        allTexSet = set()
        modelCountFormat = "{0}/{1}"
        for idx, file in enumerate(fileList):
            self.v_modelCount.set(modelCountFormat.format(idx + 1, len(fileList)))
            self.master.update()

            decryptScanFile = SmfDecrypt(file)
            if not decryptScanFile.open():
                decryptScanFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E4"])
                return
            allTexSet |= decryptScanFile.texList
        allTexList = list(allTexSet)
        self.noTexList = []

        self.noImageListbox.delete(0, tkinter.END)
        for tex in allTexList:
            if not os.path.exists(os.path.join(dirPath, tex)):
                self.noTexList.append(tex)
                self.noImageListbox.insert(tkinter.END, "「{0}」がありません".format(tex))

        if len(self.noTexList) > 0:
            self.copyImageButton["state"] = "normal"
        else:
            self.copyImageButton["state"] = "disabled"

    def copyImage(self):
        folderPath = fd.askdirectory()
        if not folderPath:
            return

        newNoTexList = []
        self.noImageListbox.delete(0, tkinter.END)
        self.master.update()

        modelCountFormat = "{0}/{1}"
        for idx, tex in enumerate(self.noTexList):
            self.v_modelCount.set(modelCountFormat.format(idx + 1, len(self.noTexList)))
            imagePath = os.path.join(folderPath, tex)
            if os.path.exists(imagePath):
                shutil.copy(imagePath, self.v_modelPath.get())
                self.noImageListbox.insert(tkinter.END, "{0}をコピーしました".format(tex))
            else:
                newNoTexList.append(tex)
                self.noImageListbox.insert(0, "「{0}」が存在しません".format(tex))
            self.master.update()
        self.noTexList = copy.deepcopy(newNoTexList)
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I118"])
        if len(self.noTexList) > 0:
            self.copyImageButton["state"] = "normal"
        else:
            self.copyImageButton["state"] = "disabled"


class EditFrameInfoDialog(CustomSimpleDialog):
    def __init__(self, master, title, frameObj, decryptFile, rootFrameAppearance):
        self.frameObj = frameObj
        self.decryptFile = decryptFile
        self.meshDeleteFlag = False
        self.resultValueList = []
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        eleLabelList = ["Name", "pos", "rot", "meshNo"]
        self.varList = []
        self.varCnt = 0
        self.entryWidth = 20
        index = 0
        matrix = self.frameObj["matrix"]
        for label in eleLabelList:
            if label == "Name":
                eleLb = ttkCustomWidget.CustomTtkLabel(master, font=textSetting.textList["font2"], text=label)
                eleLb.grid(row=index, column=0, sticky=tkinter.W + tkinter.E)
                self.varList.append(tkinter.StringVar(value=self.frameObj["name"]))
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
                self.varList.append(tkinter.IntVar(value=self.frameObj["meshNo"]))
                eleEt = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"], textvariable=self.varList[self.varCnt], width=self.entryWidth)
                eleEt.grid(row=index, column=1, sticky=tkinter.W + tkinter.E)
                self.varCnt += 1
                index += 1
        super().body(master)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if not result:
            return

        self.meshDeleteFlag = False
        warnMsg = ""
        inputMeshNo = self.varList[-1].get()
        if inputMeshNo < -1:
            inputMeshNo = -1
        originMeshNo = self.frameObj["meshNo"]

        if inputMeshNo == -1:
            if originMeshNo != -1:
                self.meshDeleteFlag = True
                warnMsg = textSetting.textList["infoList"]["I133"].format(originMeshNo) + textSetting.textList["infoList"]["I130"]
        else:
            if originMeshNo == -1:
                inputMeshNo = self.decryptFile.meshCount
                warnMsg = textSetting.textList["infoList"]["I134"].format(inputMeshNo) + textSetting.textList["infoList"]["I130"]
            else:
                if originMeshNo != inputMeshNo:
                    if inputMeshNo < self.decryptFile.meshCount:
                        warnMsg = textSetting.textList["infoList"]["I132"].format(inputMeshNo) + textSetting.textList["infoList"]["I130"]
                    else:
                        warnMsg = textSetting.textList["infoList"]["I135"].format(originMeshNo, inputMeshNo) + textSetting.textList["infoList"]["I130"]

        if warnMsg:
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
            if not result:
                return

        self.resultValueList = []
        try:
            for i, var in enumerate(self.varList):
                if i == 0:
                    if not var.get():
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E138"])
                        return False

                self.resultValueList.append(var.get())
        except Exception:
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return False
        return True

    def apply(self):
        self.reloadFlag = True


class SwapFrameDialog(CustomSimpleDialog):
    def __init__(self, master, title, frameObj, decryptFile, rootFrameAppearance):
        self.frameObj = frameObj
        self.decryptFile = decryptFile
        self.swapFrameList = []
        self.frameIdx = -1
        self.parentIdx = -1
        self.reloadFlag = False
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)

        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["smf"]["locationParentFrame"], font=textSetting.textList["font2"])
        swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        swapFrameCbList = []
        for index, fObj in enumerate(self.decryptFile.frameList):
            if index == self.frameObj["frameNo"]:
                continue
            self.swapFrameList.append([index, fObj["name"]])
            swapFrameCbList.append("%02d(%s)" % (index, fObj["name"]))

        self.v_swap = tkinter.StringVar()
        self.v_swap.set(swapFrameCbList[0])
        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=20, state="readonly", font=textSetting.textList["font2"], value=swapFrameCbList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        super().body(master)

    def validate(self):
        swapCbIdx = self.swapCb.current()
        self.parentIdx = self.swapFrameList[swapCbIdx][0]
        parentName = self.swapFrameList[swapCbIdx][1]
        self.frameIdx = self.frameObj["frameNo"]
        frameName = self.frameObj["name"]
        warnMsg = textSetting.textList["infoList"]["I103"].format(frameName, parentName) + textSetting.textList["infoList"]["I102"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
        if result:
            return True

    def apply(self):
        self.reloadFlag = True


class SwapMeshDialog(CustomSimpleDialog):
    def __init__(self, master, title, swapDecryptFile, rootFrameAppearance):
        self.swapDecryptFile = swapDecryptFile
        self.reloadFlag = False
        self.swapMeshNo = -1
        self.swapMeshNoList = []
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        self.resizable(False, False)
        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["smf"]["swapToModelMeshNoLabel"], font=textSetting.textList["font2"])
        swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        swapMeshCbList = []
        for fObj in self.swapDecryptFile.frameList:
            if fObj["meshNo"] != -1:
                self.swapMeshNoList.append(fObj["meshNo"])
                swapMeshCbList.append("%s (Mesh No.%d)" % (fObj["name"], fObj["meshNo"]))

        self.v_swap = tkinter.StringVar()
        self.v_swap.set(swapMeshCbList[0])
        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=20, state="readonly", font=textSetting.textList["font2"], value=swapMeshCbList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        super().body(master)

    def validate(self):
        swapCbIdx = self.swapCb.current()
        self.swapMeshNo = self.swapMeshNoList[swapCbIdx]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I126"], icon="warning")
        if result:
            return True

    def apply(self):
        self.reloadFlag = True


class SwapFbxMeshDialog(CustomSimpleDialog):
    def __init__(self, master, title, fbxFilePath, rootFrameAppearance):
        self.fbxFilePath = fbxFilePath
        self.reloadFlag = False
        self.importFbxObj = ImportFbxObject(fbxFilePath)
        self.swapMeshNameList = self.importFbxObj.meshNameList
        self.swapMeshNodeList = self.importFbxObj.meshNodeList
        self.swapMeshPathList = self.importFbxObj.meshPathList
        self.swapMeshNode = None
        super().__init__(master, title, rootFrameAppearance.bgColor)

    def body(self, master):
        master.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["smf"]["swapToModelMeshNoLabel"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
        swapLb.grid(row=0, column=0, sticky=tkinter.EW)

        self.v_swap = tkinter.StringVar()
        self.v_swap.set(self.swapMeshNameList[0])
        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=20, state="readonly", font=textSetting.textList["font2"], value=self.swapMeshNameList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.EW, pady=10)
        self.swapCb.bind("<<ComboboxSelected>>", lambda e: self.showPath())

        self.v_path = tkinter.StringVar()
        pathEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_path)
        pathEt.grid(row=2, column=0, sticky=tkinter.EW)

        self.swapCb.current(0)
        self.showPath()
        master.columnconfigure(0, weight=1, uniform="aaa")

        super().body(master)

    def showPath(self):
        idx = self.swapCb.current()
        self.v_path.set("{0}".format(self.swapMeshPathList[idx]))

    def validate(self):
        swapCbIdx = self.swapCb.current()
        self.swapMeshNode = self.swapMeshNodeList[swapCbIdx]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I126"], icon="warning")
        if result:
            return True

    def apply(self):
        self.reloadFlag = True
