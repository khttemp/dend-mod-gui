import os
import tkinter
import traceback
from tkinter import messagebox as mb
import program.textSetting as textSetting
from program.errorLogClass import ErrorLogObj
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog

from fbx import FbxManager
from fbx import FbxScene
from fbx import FbxImporter
from fbx import FbxNodeAttribute
from fbx import FbxLayerElement


class SwapFbxMeshDialog(CustomSimpleDialog):
    def __init__(self, master, title, decryptFile, fbxFilePath, rootFrameAppearance, meshNo):
        self.errObj = ErrorLogObj()
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
        self.errObj.write(error)

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

    def getData(self, node, element):
        dataList = []
        mappingMode = element.GetMappingMode()
        referenceMode = element.GetReferenceMode()
        if mappingMode == FbxLayerElement.EMappingMode.eByControlPoint:
            for i in range(node.GetControlPointsCount()):
                if referenceMode == FbxLayerElement.EReferenceMode.eDirect:
                    dataList.append(element.GetDirectArray().GetAt(i))
                # eIndexToDirect
                else:
                    index = element.GetIndexArray().GetAt(i)
                    dataList.append(element.GetDirectArray().GetAt(index))
        elif mappingMode == FbxLayerElement.EMappingMode.eByPolygonVertex:
            if referenceMode == FbxLayerElement.EReferenceMode.eIndexToDirect:
                tempDataList = []
                for data in element.GetDirectArray():
                    tempDataList.append(data)
                for index in element.GetIndexArray():
                    dataList.append(tempDataList[index])
            # eDirect
            else:
                for data in element.GetDirectArray():
                    dataList.append(data)

        return dataList

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

            material = swapMeshNode.GetElementMaterial(0)
            materialIndexDict = {}
            # マテリアルリストから、ポリゴン情報を抽出
            for polygonIndex, materialIndex in enumerate(material.GetIndexArray()):
                polygonSize = swapMeshNode.GetPolygonSize(polygonIndex)
                if polygonSize != 3:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E123"])
                    return False

                if materialIndex not in materialIndexDict:
                    materialIndexDict[materialIndex] = []
                materialIndexDict[materialIndex].append(polygonIndex)

            swapMeshObj["coordIndexList"] = []
            vertexFlag = False
            materialKeyList = sorted(materialIndexDict.keys())
            for materialIndex in materialKeyList:
                for polygonIndex in materialIndexDict[materialIndex]:
                    indexList = []
                    for i in range(swapMeshNode.GetPolygonSize(polygonIndex)):
                        vertex = swapMeshNode.GetPolygonVertex(polygonIndex, i)
                        if vertex >= 0xFFFF:
                            vertexFlag = True
                        indexList.append(vertex)
                    swapMeshObj["coordIndexList"].append(list(reversed(indexList)))

            colorElement = swapMeshNode.GetLayer(0).GetVertexColors()
            swapMeshObj["colorInfoList"] = []
            if colorElement:
                colorList = self.getData(swapMeshNode, colorElement)
                for color in colorList:
                    red = int(color.mRed * 255.0)
                    green = int(color.mGreen * 255.0)
                    blue = int(color.mBlue * 255.0)
                    alpha = int(color.mAlpha * 255.0)
                    swapMeshObj["colorInfoList"].append([red, green, blue, alpha])

            swapMeshObj["normalList"] = []
            normals = swapMeshNode.GetElementNormal(0)
            if normals:
                normalList = self.getData(swapMeshNode, normals)
                for normal in normalList:
                    swapMeshObj["normalList"].append([-normal[0], normal[1], normal[2]])

            swapMeshObj["uvList"] = []
            uvs = swapMeshNode.GetElementUV(0)
            if uvs:
                uvList = self.getData(swapMeshNode, uvs)
                for uv in uvList:
                    swapMeshObj["uvList"].append([uv[0], 1.0 - uv[1]])

            swapMeshObj["mtrlList"] = []
            polyIndexStart = 0
            for mIdx, material in enumerate(material.GetDirectArray()):
                mtrlObj = {}
                mtrlObj["polyIndexStart"] = polyIndexStart
                mtrlObj["polyCount"] = len(materialIndexDict[mIdx])
                polyIndexStart += len(materialIndexDict[mIdx])
                diff = material.Diffuse.Get()
                mtrlObj["diff"] = [diff[0], diff[1], diff[2]]
                emis = material.Emissive.Get()
                mtrlObj["emis"] = [emis[0], emis[1], emis[2]]
                try:
                    spec = material.Specular.Get()
                    mtrlObj["spec"] = [spec[0], spec[1], spec[2]]
                except Exception:
                    pass
                obj = material.Diffuse.GetSrcObject()
                if obj is not None:
                    texc = os.path.basename(material.Diffuse.GetSrcObject().GetFileName())
                else:
                    texc = ""
                mtrlObj["texc"] = texc
                swapMeshObj["mtrlList"].append(mtrlObj)

            result = mb.askokcancel(title=textSetting.textList["confirm"], message=self.infoMsg, icon="warning", parent=self)
            if result:
                errorMsg = textSetting.textList["errorList"]["E4"]
                if not self.decryptFile.saveSwapFbxMesh(self.meshNo, swapMeshObj, vertexFlag):
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