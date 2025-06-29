import os
import shutil
import json
import struct
import traceback
from program.encodingClass import SJISEncodingObject
from program.errorLogClass import ErrorLogObj


class GlbObject:
    def __init__(self, filePath, decryptFile):
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.headerName = "glTF"
        self.headerVersion = 2
        self.jsonName = "JSON"
        self.binName = "BIN"
        self.uByteType = 5121
        self.uShortType = 5123
        self.floatType = 5126
        self.arrayBufferType = 34962
        self.elementArrayBufferType = 34963
        self.filePath = filePath
        self.decryptFile = decryptFile
        self.imageFileList = []
        self.byteArr = bytearray()
        self.binFileLenAddr = -1
        self.jsonLenAddr = -1
        self.bufferByteArr = bytearray()

    def makeGlbFile(self):
        try:
            self.imageFileList = []
            self.makeHeader()
            self.makeJson()
            self.makeBin()
            byteArrLen = len(self.byteArr)
            iByteArrLen = struct.pack("<I", byteArrLen)
            for addr, val in enumerate(iByteArrLen):
                self.byteArr[self.binFileLenAddr + addr] = val
            self.exportGlb()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        self.errObj.write(self.error)

    def makeHeader(self):
        self.byteArr = bytearray()
        self.byteArr.extend(self.encObj.convertByteArray(self.headerName))
        self.byteArr.extend(struct.pack("<I", self.headerVersion))
        self.binFileLenAddr = len(self.byteArr)
        self.byteArr.extend(struct.pack("<I", 0))

    def getMaxAndMin(self, coordList):
        if len(coordList) == 0:
            return [[0, 0, 0], [0, 0, 0]]
        firstCoord = coordList[0]
        minX = firstCoord[0]
        minY = firstCoord[1]
        minZ = firstCoord[2]
        maxX = firstCoord[0]
        maxY = firstCoord[1]
        maxZ = firstCoord[2]
        for coord in coordList:
            minX = min(minX, coord[0])
            minY = min(minY, coord[1])
            minZ = min(minZ, coord[2])
            maxX = max(maxX, coord[0])
            maxY = max(maxY, coord[1])
            maxZ = max(maxZ, coord[2])
        return ([maxX, maxY, maxZ], [minX, minY, minZ])

    def makeJson(self):
        self.jsonLenAddr = len(self.byteArr)
        self.byteArr.extend(struct.pack("<I", 0))
        self.byteArr.extend(self.encObj.convertByteArray(self.jsonName))
        jsonDict = {}
        jsonDict["asset"] = {}
        jsonDict["asset"]["generator"] = "convertSMFtoGLB"
        jsonDict["asset"]["version"] = "2.0"

        sceneObj = {}
        sceneObj["name"] = "Scene"
        sceneObj["nodes"] = [0]
        jsonDict["scene"] = 0
        jsonDict["scenes"] = [sceneObj]

        frameObjList = []
        for frameIdx, trans in enumerate(self.decryptFile.frameList):
            newMatrix = []
            pos = [
                -trans["matrix"][3][0],
                trans["matrix"][3][1],
                trans["matrix"][3][2]
            ]
            q = self.decryptFile.getQuaternion(trans["matrix"])
            newMatrix.extend(pos)
            frameObj = {
                "name": trans["name"],
                "children": [],
                "translation":pos,
                "rotation":q
            }

            if trans["parentFrameNo"] != -1:
                frameObjList[trans["parentFrameNo"]]["children"].append(frameIdx)
            if trans["meshNo"] != -1:
                frameObj["mesh"] = trans["meshNo"]
            frameObjList.append(frameObj)
        jsonDict["nodes"] = frameObjList

        meshObjList = []
        accessorsList = []
        bufferViewsList = []
        self.bufferByteArr = bytearray()
        bufferViewIndex = 0
        materialIndex = 0
        materialsList = []
        texturesList = []
        imagesList = []
        for mesh in self.decryptFile.meshList:
            meshObj = {}
            meshObj["name"] = mesh["name"]
            primitivesList = []
            for mtrl in mesh["mtrlList"]:
                primitiveObj = {}
                primitiveObj["attributes"] = {}

                coordIndexStart = mtrl["coordIndexStart"]
                coordIndexEnd = coordIndexStart + mtrl["coordCount"]
                splitCoordList = mesh["coordList"][coordIndexStart:coordIndexEnd]
                # coord
                primitiveObj["attributes"]["POSITION"] = bufferViewIndex
                posAccObj = {}
                posAccObj["bufferView"] = bufferViewIndex
                posAccObj["componentType"] = self.floatType
                posAccObj["count"] = len(splitCoordList)
                maxAndMinList = self.getMaxAndMin(splitCoordList)
                posAccObj["max"] = maxAndMinList[0]
                posAccObj["min"] = maxAndMinList[1]
                posAccObj["type"] = "VEC3"
                accessorsList.append(posAccObj)
                bufferViewObj = {}
                bufferViewObj["buffer"] = 0
                bufferViewObj["byteOffset"] = len(self.bufferByteArr)
                for coordList in splitCoordList:
                    for cidx, coord in enumerate(coordList):
                        if cidx == 0:
                            self.bufferByteArr.extend(struct.pack("<f", -coord))
                        else:
                            self.bufferByteArr.extend(struct.pack("<f", coord))
                bufferViewObj["byteLength"] = len(self.bufferByteArr) - bufferViewObj["byteOffset"]
                bufferViewObj["target"] = self.arrayBufferType
                bufferViewsList.append(bufferViewObj)
                bufferViewIndex += 1

                # normal
                splitNormalList = mesh["normalList"][coordIndexStart:coordIndexEnd]
                primitiveObj["attributes"]["NORMAL"] = bufferViewIndex
                normalAccObj = {}
                normalAccObj["bufferView"] = bufferViewIndex
                normalAccObj["componentType"] = self.floatType
                normalAccObj["count"] = len(splitNormalList)
                normalAccObj["type"] = "VEC3"
                accessorsList.append(normalAccObj)
                bufferViewObj = {}
                bufferViewObj["buffer"] = 0
                bufferViewObj["byteOffset"] = len(self.bufferByteArr)
                for normalList in splitNormalList:
                    for nidx, normal in enumerate(normalList):
                        if nidx == 0:
                            self.bufferByteArr.extend(struct.pack("<f", -normal))
                        else:
                            self.bufferByteArr.extend(struct.pack("<f", normal))
                bufferViewObj["byteLength"] = len(self.bufferByteArr) - bufferViewObj["byteOffset"]
                bufferViewObj["target"] = self.arrayBufferType
                bufferViewsList.append(bufferViewObj)
                bufferViewIndex += 1

                # uv
                splitUvList = mesh["uvList"][coordIndexStart:coordIndexEnd]
                primitiveObj["attributes"]["TEXCOORD_0"] = bufferViewIndex
                texAccObj = {}
                texAccObj["bufferView"] = bufferViewIndex
                texAccObj["componentType"] = self.floatType
                texAccObj["count"] = len(splitUvList)
                texAccObj["type"] = "VEC2"
                accessorsList.append(texAccObj)
                bufferViewObj = {}
                bufferViewObj["buffer"] = 0
                bufferViewObj["byteOffset"] = len(self.bufferByteArr)
                for uvList in splitUvList:
                    self.bufferByteArr.extend(struct.pack("<f", uvList[0]))
                    self.bufferByteArr.extend(struct.pack("<f", uvList[1]))
                bufferViewObj["byteLength"] = len(self.bufferByteArr) - bufferViewObj["byteOffset"]
                bufferViewObj["target"] = self.arrayBufferType
                bufferViewsList.append(bufferViewObj)
                bufferViewIndex += 1

                # color
                splitColorInfoList = mesh["colorInfoList"][coordIndexStart:coordIndexEnd]
                primitiveObj["attributes"]["COLOR_0"] = bufferViewIndex
                colorAccObj = {}
                colorAccObj["bufferView"] = bufferViewIndex
                colorAccObj["componentType"] = self.uByteType
                colorAccObj["count"] = len(splitColorInfoList)
                colorAccObj["type"] = "VEC4"
                accessorsList.append(colorAccObj)
                bufferViewObj = {}
                bufferViewObj["buffer"] = 0
                bufferViewObj["byteOffset"] = len(self.bufferByteArr)
                for colorList in splitColorInfoList:
                    self.bufferByteArr.append(colorList[2])
                    self.bufferByteArr.append(colorList[1])
                    self.bufferByteArr.append(colorList[0])
                    self.bufferByteArr.append(colorList[3])
                bufferViewObj["byteLength"] = len(self.bufferByteArr) - bufferViewObj["byteOffset"]
                bufferViewObj["target"] = self.arrayBufferType
                bufferViewsList.append(bufferViewObj)
                bufferViewIndex += 1

                # polygon
                indicesIndexStart = mtrl["polyIndexStart"] * 3
                polyCount = mtrl["polyCount"]
                indicesIndexEnd = indicesIndexStart + polyCount * 3
                splitPolyList = mesh["coordIndexList"][indicesIndexStart:indicesIndexEnd]
                primitiveObj["indices"] = bufferViewIndex
                coordIndexAccObj = {}
                coordIndexAccObj["bufferView"] = bufferViewIndex
                coordIndexAccObj["componentType"] = self.uShortType
                coordIndexAccObj["count"] = len(splitPolyList)
                coordIndexAccObj["type"] = "SCALAR"
                accessorsList.append(coordIndexAccObj)
                bufferViewObj = {}
                bufferViewObj["buffer"] = 0
                bufferViewObj["byteOffset"] = len(self.bufferByteArr)

                polygonInfoList = []
                polygonInfo = []
                for polyIdx, coordIndex in enumerate(splitPolyList):
                    polygonInfo.append(coordIndex - coordIndexStart)
                    if polyIdx % 3 == 2:
                        polygonInfoList.append(polygonInfo)
                        polygonInfo = []
                for polygonInfo in polygonInfoList:
                    for coordIndex in reversed(polygonInfo):
                        self.bufferByteArr.extend(struct.pack("<H", coordIndex))
                bufferViewObj["byteLength"] = len(self.bufferByteArr) - bufferViewObj["byteOffset"]
                bufferViewObj["target"] = self.elementArrayBufferType
                bufferViewsList.append(bufferViewObj)
                bufferViewIndex += 1

                # material
                primitiveObj["material"] = materialIndex
                materialObj = {
                    "pbrMetallicRoughness": {
                        "baseColorFactor": mtrl["diff"]
                    }
                }
                materialIndex += 1

                # texture
                if "texc" in mtrl:
                    file = mtrl["texc"]
                    dirname = os.path.dirname(self.filePath)
                    self.imageFileList.append(os.path.join(dirname, file))
                    imageObj = {
                        "uri": file
                    }
                    textureObj = {
                        "source": len(imagesList)
                    }
                    materialObj["pbrMetallicRoughness"]["baseColorTexture"] = {
                        "index":len(texturesList)
                    }
                    imagesList.append(imageObj)
                    texturesList.append(textureObj)
                primitivesList.append(primitiveObj)
                materialsList.append(materialObj)
            meshObj["primitives"] = primitivesList
            meshObjList.append(meshObj)
        jsonDict["meshes"] = meshObjList
        jsonDict["materials"] = materialsList
        jsonDict["textures"] = texturesList
        jsonDict["images"] = imagesList
        jsonDict["accessors"] = accessorsList
        jsonDict["bufferViews"] = bufferViewsList

        jsonDict["buffers"] = [
            {
                "byteLength":len(self.bufferByteArr)
            }
        ]
        if len(self.bufferByteArr) % 4 != 0:
            cnt = 4 - len(self.bufferByteArr) % 4
            for i in range(cnt):
                self.bufferByteArr.append(0)

        jsonDump = json.dumps(jsonDict, separators=(',', ':'))
        jsonByteArr = bytearray(self.encObj.convertByteArray(jsonDump))
        if len(jsonByteArr) % 4 != 0:
            cnt = 4 - len(jsonByteArr) % 4
            for i in range(cnt):
                jsonByteArr.extend(self.encObj.convertByteArray(" "))
        self.byteArr.extend(jsonByteArr)
        byteJsonLen = len(jsonByteArr)
        iByteJsonLen = struct.pack("<I", byteJsonLen)
        for addr, val in enumerate(iByteJsonLen):
            self.byteArr[self.jsonLenAddr + addr] = val

    def makeBin(self):
        self.byteArr.extend(struct.pack("<I", len(self.bufferByteArr)))
        self.byteArr.extend(self.encObj.convertByteArray(self.binName))
        self.byteArr.append(0)
        self.byteArr.extend(self.bufferByteArr)

    def exportGlb(self):
        dirname = os.path.splitext(self.filePath)[0]
        filename = os.path.basename(self.filePath)
        newFilePath = os.path.join(dirname, filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

        for imageFile in self.imageFileList:
            if os.path.exists(imageFile):
                newPath = os.path.join(dirname, os.path.basename(imageFile))
                shutil.copy(imageFile, newPath)
        w = open(newFilePath, "wb")
        w.write(self.byteArr)
        w.close()
