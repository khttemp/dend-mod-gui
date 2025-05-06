import os
import tkinter
import codecs
import traceback
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from fbx import FbxManager
from fbx import FbxScene
from fbx import FbxImporter
from fbx import FbxNodeAttribute


class SwapFbxMeshDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, fbxFilePath, rootFrameAppearance, meshNo):
        self.decryptFile = decryptFile
        self.fbxFilePath = fbxFilePath
        self.meshNo = meshNo
        self.reloadFlag = False
        self.swapMeshNameList = []
        self.swapMeshNodeList = []
        self.manager = None
        self.importer = None
        self.infoMsg = textSetting.textList["infoList"]["I126"]
        self.importFbx()
        super().__init__(master, title, rootFrameAppearance.bgColor)
    
    def printError(self, error):
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(error)
        w.close()

    def importFbx(self):
        self.manager = FbxManager.Create()
        scene = FbxScene.Create(self.manager, "MyScene")
        self.importer = FbxImporter.Create(self.manager, "")
        self.importer.Initialize(self.fbxFilePath)
        self.importer.Import(scene)
        rootNode = scene.GetRootNode()
        self.getHierarchy(rootNode)

    def isMeshType(self, pNode):
        if pNode.GetNodeAttribute() is None:
            return False
        attributeType = pNode.GetNodeAttribute().GetAttributeType()
        if attributeType == FbxNodeAttribute.EType.eMesh:
            return True
        return False

    def getHierarchy(self, pNode):
        if self.isMeshType(pNode):
            name = pNode.GetName()
            self.swapMeshNameList.append(name)
            mesh = pNode.GetNodeAttribute()
            self.swapMeshNodeList.append(mesh)

        for i in range(pNode.GetChildCount()):
            self.getHierarchy(pNode.GetChild(i))

    def body(self, master):
        self.resizable(False, False)

        swapLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["smf"]["swapToModelMeshNoLabel"], font=textSetting.textList["font2"])
        swapLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        self.v_swap = tkinter.StringVar()
        self.v_swap.set(self.swapMeshNameList[0])
        self.swapCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_swap, width=20, state="readonly", font=textSetting.textList["font2"], value=self.swapMeshNameList)
        self.swapCb.grid(row=1, column=0, sticky=tkinter.N + tkinter.S, pady=10)
        self.swapCb.set(self.swapMeshNameList[0])
        super().body(master)

    def validate(self):
        try:
            swapCbIdx = self.swapCb.current()
            swapMeshNode = self.swapMeshNodeList[swapCbIdx]
            swapMeshObj = {}
            swapMeshObj["coordList"] = []
            for i in range(swapMeshNode.GetControlPointsCount()):
                coord = swapMeshNode.GetControlPointAt(i)
                swapMeshObj["coordList"].append([-coord[0], coord[1], coord[2]])

            swapMeshObj["coordIndexList"] = []
            for i in range(swapMeshNode.GetPolygonCount()):
                indexList = []
                for j in range(swapMeshNode.GetPolygonSize(i)):
                    vertex = swapMeshNode.GetPolygonVertex(i, j)
                    indexList.append(vertex)
                swapMeshObj["coordIndexList"].append(reversed(indexList))

            swapMeshObj["normalList"] = []
            normals = swapMeshNode.GetElementNormal(0)
            for normal in normals.GetDirectArray():
                swapMeshObj["normalList"].append([-normal[0], normal[1], normal[2]])

            swapMeshObj["uvList"] = []
            uvs = swapMeshNode.GetElementUV(0)
            for uv in uvs.GetDirectArray():
                swapMeshObj["uvList"].append([uv[0], 1.0 - uv[1]])

            material = swapMeshNode.GetElementMaterial(0)
            materialIndexList = []
            materialGroupList = []
            mIdx = -1
            for idx, materialIndex in enumerate(material.GetIndexArray()):
                if mIdx != materialIndex:
                    materialIndexList.append(idx)
                    mIdx = materialIndex
            for i in range(len(materialIndexList) - 1):
                materialGroupList.append([materialIndexList[i], materialIndexList[i+1]-materialIndexList[i]])
            materialGroupList.append([materialIndexList[-1], material.GetIndexArray().GetCount() - materialIndexList[-1]])

            swapMeshObj["mtrlList"] = []
            for mIdx, material in enumerate(material.GetDirectArray()):
                mtrlObj = {}
                mtrlObj["polyIndexStart"] = materialGroupList[mIdx][0]
                mtrlObj["polyCount"] = materialGroupList[mIdx][1]
                diff = material.Diffuse.Get()
                mtrlObj["diff"] = [diff[0], diff[1], diff[2]]
                emis = material.Emissive.Get()
                mtrlObj["emis"] = [emis[0], emis[1], emis[2]]
                spec = material.Specular.Get()
                mtrlObj["spec"] = [spec[0], spec[1], spec[2]]
                texc = os.path.basename(material.Diffuse.GetSrcObject().GetFileName())
                mtrlObj["texc"] = texc
                swapMeshObj["mtrlList"].append(mtrlObj)

            result = mb.askokcancel(title=textSetting.textList["confirm"], message=self.infoMsg, icon="warning", parent=self)
            if result:
                errorMsg = textSetting.textList["errorList"]["E4"]
                if not self.decryptFile.saveSwapFbxMesh(self.meshNo, swapMeshObj):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                    return False
                return True
        except Exception:
            self.printError(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            self.importer.Destroy()
            self.manager.Destroy()
            return False

    def apply(self):
        self.importer.Destroy()
        self.manager.Destroy()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
        self.reloadFlag = True