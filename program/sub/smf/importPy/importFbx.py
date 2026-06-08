import os
import traceback

from fbx import FbxManager
from fbx import FbxScene
from fbx import FbxImporter
from fbx import FbxNodeAttribute
from fbx import FbxLayerElement

import program.sub.textSetting as textSetting
from program.sub.errorLogClass import ErrorLogObj


class ImportFbxObject():
    def __init__(self, fbxFilePath):
        self.errObj = ErrorLogObj()
        self.fbxFilePath = fbxFilePath
        self.meshNameList = []
        self.meshNodeList = []
        self.meshPathList = []
        self.manager = None
        self.importer = None
        self.importFbx()

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

    def getNodePath(self, pNode):
        path = pNode.GetName()
        parent = pNode.GetParent()

        while parent and parent.GetParent():
            path = parent.GetName() + "/" + path
            parent = parent.GetParent()
        return path

    def getHierarchy(self, pNode):
        if self.isMeshType(pNode):
            self.meshNameList.append(pNode.GetName())
            self.meshNodeList.append(pNode.GetNodeAttribute())
            self.meshPathList.append(self.getNodePath(pNode))

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

    def makeMeshObj(self, swapMeshNode):
        try:
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
                    return (False, {"message": textSetting.textList["errorList"]["E123"]})

                if materialIndex not in materialIndexDict:
                    materialIndexDict[materialIndex] = []
                materialIndexDict[materialIndex].append(polygonIndex)

            swapMeshObj["coordIndexList"] = []
            vertexOverFlag = False
            materialKeyList = sorted(materialIndexDict.keys())
            for materialIndex in materialKeyList:
                for polygonIndex in materialIndexDict[materialIndex]:
                    indexList = []
                    for i in range(swapMeshNode.GetPolygonSize(polygonIndex)):
                        vertex = swapMeshNode.GetPolygonVertex(polygonIndex, i)
                        if vertex >= 0xFFFF:
                            vertexOverFlag = True
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

            return (True, {"data": swapMeshObj, "flag": vertexOverFlag})
        except Exception:
            self.printError(traceback.format_exc())
            return (False, {"message": textSetting.textList["errorList"]["E14"]})

    def destroyFbxObj(self):
        self.importer.Destroy()
        self.manager.Destroy()
