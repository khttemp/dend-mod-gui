import os
import codecs
import UnityPy
import struct
import traceback
import program.textSetting as textSetting

SSTrainName = [
    "H2000",
    "X200",
    "H4050",
    "H7011",
    "E233",
    "H8200",
    "TQ5050",
    "TQ5000",
    "TQ9001",
    "TQ300",
    "TQ8500",
    "Pano",
    "Mu2000",
    "T50000",
    "T200",
    "DRC",
    "H2800",
    "H9000",
    "KQ21XX",
    "JR2000",
    "Rapit",
    "K8000",
    "Arban21000R",
    "H8008",
    "KQ2199",
    "H2300",
    "JR223",
    "K800",
    "H7001",
    "K80",
    "Yuri",
    "AE86",
    "Deki",
    "MIZ1000",
    "KB1300",
]

SSBodyName = [
    "H2000Body",
    "H1000Body",
    "H4050Body",
    "H7011Body",
    "E233Body",
    "H8200Body",
    "TQ5050Body",
    "TQ5000Body",
    "TQ9001Body",
    "TQ300Body",
    "TQ8500Body",
    "PanoBody",
    "Mu2000Body",
    "TB50000Body",
    "TB200Body",
    "DRCBody",
    "H2800Body",
    "HS9000Body",
    "KQ21XXBody",
    "JR2000Body",
    "RapitBody",
    "K8000Body",
    "UVBody",
    "H8008Body",
    "H2300Body",
    "JR223Body",
    "K800Body",
    "H7001Body",
    "K80Body",
    "YuriBody",
    "AE86",
    # "DekiBody",
    "MIZ1000Body",
    "Kb_Body",
]

SSModelName = [
    "H2000Mdl00",
    "H2000Mdl01",
    "H1000Mdl00",
    "H1000Mdl01",
    "H4050Mdl",
    "H7000Mdl4050",
    "H920Mdl",
    "H7011Mdl00",
    "H7011Mdl01",
    "E233Mdl00",
    "E233Mdl01",
    "H8200Mdl00",
    "TQ5050Mdl00",
    "TQ5050Mdl01",
    "TQ5000Mdl00",
    "TQ5000Mdl01",
    "TQ9001Mdl00",
    "TQ9001Mdl01",
    "TQ300Mdl",
    "TQ8500Mdl00",
    "TQ8500Mdl01",
    "PanoMdl00",
    "PanoMdl01",
    "Mu2000Mdl00",
    "Mu2000Mdl01",
    "Mu2000Mdl02",
    "T50000Mdl00",
    "T50000Mdl01",
    "T200Mdl00",
    "T200Mdl01",
    "T200Mdl02",
    "T200Mdl03",
    "DRCMdl00",
    "DRCMdl01",
    "DRCMdl02",
    "DRCMdl03",
    "H2800Mdl00",
    "H2800Mdl01",
    "H9000Mdl00",
    "H9000Mdl01",
    "KQ21XXMdl00",
    "KQ21XXMdl01",
    "JR2000Mdl00",
    "JR2000Mdl01",
    "JR2000Mdl02",
    "RapitMdl00",
    "RapitMdl01",
    "K8000Mdl00",
    "K8000Mdl01",
    "K8000Mdl02",
    "UVMdl00",
    "UVMdl01",
    "UVMdl02",
    "H8008Mdl00",
    "H8008Mdl01",
    "H2300Mdl00",
    "H2300Mdl01",
    "KQ2199Mdl00",
    "JR223Mdl00",
    "JR223Mdl01",
    "K800Mdl00",
    "K800Mdl01",
    "H7001Mdl00",
    "H7001Mdl01",
    "K80Mdl",
    "YuMdl0",
    "YuMdl1",
    "AE86Mdl",
    # "DekiMdl",
    "MIZ1000Mdl",
    "KBMdl0",
]


class ResourcesDecrypt:
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileDir = os.path.dirname(filePath)
        self.filenameAndExt = os.path.splitext(os.path.basename(filePath))
        self.trainNameList = SSTrainName
        self.texNameList = SSBodyName
        self.trainModelNameList = SSModelName
        self.env = None
        self.keyNameList = [
            "TrainOrgInfo",
            "ChangeMeshTex",
        ]
        self.monoBehaviourList = []
        self.trainOrgInfoList = {}
        self.allChangeMeshTexList = []
        self.allModelToMeshTexList = {}
        self.changeMeshTexList = {}
        self.newTrainOrgInfo = []

    def open(self):
        try:
            self.env = UnityPy.load(self.filePath)
            return self.decrypt()
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(self.error)
        w.close()

    def decrypt(self):
        try:
            self.trainOrgInfoList = {}
            self.allChangeMeshTexList = []
            self.allModelToMeshTexList = {}
            self.changeMeshTexList = {}
            self.monoBehaviourList = [env for env in self.env.objects if env.type.name == "MonoBehaviour"]
            for mono in self.monoBehaviourList:
                data = mono.read()
                script = data.m_Script
                if script:
                    script = script.read()
                    if script.m_ClassName in self.keyNameList:
                        if script.m_ClassName == self.keyNameList[0]:
                            gameObject = data.m_GameObject.read()
                            if gameObject.name in self.trainNameList:
                                self.trainOrgInfoList[gameObject.name] = {
                                    "num": data.path_id,
                                    "data": {
                                        "className": script.m_ClassName,
                                        "monoData": data,
                                        "size": data.byte_size
                                    }
                                }
                        elif script.m_ClassName == self.keyNameList[1]:
                            self.allChangeMeshTexList.append({
                                "num": data.path_id,
                                "data": {
                                    "className": script.m_ClassName,
                                    "monoData": data,
                                    "size": data.byte_size
                                }
                            })
                    elif script.m_ClassName in self.texNameList:
                        gameObject = data.m_GameObject.read()
                        trainModelName = gameObject.name
                        if trainModelName in self.trainModelNameList:
                            meshTexInfoPathIdList = self.getMeshTexInfoPathIdList(data.raw_data)
                            self.allModelToMeshTexList[trainModelName] = meshTexInfoPathIdList

            for trainModelName in self.trainModelNameList:
                meshTexInfoPathIdList = self.allModelToMeshTexList[trainModelName]
                meshTexInfoList = []
                for meshTexInfoPathId in meshTexInfoPathIdList:
                    meshTexFilterList = [item for item in self.allChangeMeshTexList if item["num"] == meshTexInfoPathId]
                    meshTexFilterInfo = meshTexFilterList[0]
                    gameObject = meshTexFilterInfo["data"]["monoData"].m_GameObject.read()
                    meshTexFilterInfo["data"]["meshData"] = self.getChangeMeshTexInfo(meshTexFilterInfo["data"]["monoData"].raw_data)
                    meshTexInfoList.append(meshTexFilterInfo)
                self.changeMeshTexList[trainModelName] = meshTexInfoList
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def readStringPadding(self, nameLen):
        if nameLen % 4 != 0:
            return (4 - (nameLen % 4))
        return 0

    def getTrainOrgInfo(self, byteArr):
        try:
            trainOrgInfo = []
            index = 0
            trainNo = struct.unpack("<i", byteArr[index:index + 4])[0]
            trainOrgInfo.append(trainNo)
            index += 4

            notchNo = struct.unpack("<i", byteArr[index:index + 4])[0]
            trainOrgInfo.append(notchNo)
            index += 4

            for i in range(3):
                dummy = struct.unpack("<i", byteArr[index:index + 4])[0]
                trainOrgInfo.append(dummy)
                index += 4

            henseiNo = struct.unpack("<i", byteArr[index:index + 4])[0]
            trainOrgInfo.append(henseiNo)
            index += 4

            bodyClassCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            bodyClassList = []
            for i in range(bodyClassCnt):
                bodyClassNameCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
                index += 4
                bodyClassName = byteArr[index:index + bodyClassNameCnt].decode("shift-jis")
                bodyClassList.append(bodyClassName)
                index += bodyClassNameCnt
                index += self.readStringPadding(bodyClassNameCnt)
            trainOrgInfo.append(bodyClassList)

            bodyMdlCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            bodyMdlList = []
            for i in range(bodyMdlCnt):
                bodyMdlNameCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
                index += 4
                bodyMdlName = byteArr[index:index + bodyMdlNameCnt].decode("shift-jis")
                bodyMdlList.append(bodyMdlName)
                index += bodyMdlNameCnt
                index += self.readStringPadding(bodyMdlNameCnt)
            trainOrgInfo.append(bodyMdlList)

            pantaMdlCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            pantaMdlList = []
            for i in range(pantaMdlCnt):
                pantaMdlNameCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
                index += 4
                pantaMdlName = byteArr[index:index + pantaMdlNameCnt].decode("shift-jis")
                pantaMdlList.append(pantaMdlName)
                index += pantaMdlNameCnt
                index += self.readStringPadding(pantaMdlNameCnt)
            trainOrgInfo.append(pantaMdlList)

            bodyIndexCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            bodyIndexList = []
            for i in range(bodyIndexCnt):
                idx = struct.unpack("<i", byteArr[index:index + 4])[0]
                bodyIndexList.append(idx)
                index += 4
            trainOrgInfo.append(bodyIndexList)

            bodyMdlIndexCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            bodyMdlIndexList = []
            for i in range(bodyMdlIndexCnt):
                idx = struct.unpack("<i", byteArr[index:index + 4])[0]
                bodyMdlIndexList.append(idx)
                index += 4
            trainOrgInfo.append(bodyMdlIndexList)

            pantaMdlIndexCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            pantaMdlIndexList = []
            for i in range(pantaMdlIndexCnt):
                idx = struct.unpack("<i", byteArr[index:index + 4])[0]
                pantaMdlIndexList.append(idx)
                index += 4
            trainOrgInfo.append(pantaMdlIndexList)

            trackIndexCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            trackIndexList = []
            for i in range(trackIndexCnt):
                idx = struct.unpack("<i", byteArr[index:index + 4])[0]
                trackIndexList.append(idx)
                index += 4
            trainOrgInfo.append(trackIndexList)

            trackMdlIndexCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            trackMdlIndexList = []
            for i in range(trackMdlIndexCnt):
                idx = struct.unpack("<i", byteArr[index:index + 4])[0]
                trackMdlIndexList.append(idx)
                index += 4
            trainOrgInfo.append(trackMdlIndexList)
            return trainOrgInfo
        except Exception:
            self.error = traceback.format_exc()
            return None

    def checkCsv(self, csvLines):
        self.error = ""
        errorFlag = False
        self.newTrainOrgInfo = []
        bodyClassList = []
        bodyMdlList = []
        pantaMdlList = []
        bodyClassIndexList = []
        bodyMdlIndexList = []
        pantaMdlIndexList = []

        for index, csv in enumerate(csvLines):
            if index == 0:
                if textSetting.textList["ssUnity"]["csvNotchNum"] not in csv:
                    errorFlag = True
                    self.error = textSetting.textList["errorList"]["E22"]
                    break
                notchCnt = int(csv.split(",")[1])
                if notchCnt not in [4, 5, 12]:
                    errorFlag = True
                    self.error = textSetting.textList["errorList"]["E23"].format(notchCnt)
                    break
                self.newTrainOrgInfo.append(notchCnt)
            elif index == 1:
                if textSetting.textList["ssUnity"]["csvOrgNum"] not in csv:
                    errorFlag = True
                    self.error = textSetting.textList["errorList"]["E28"]
                    break
                henseiNo = int(csv.split(",")[1])
                if henseiNo <= 0:
                    errorFlag = True
                    self.error = textSetting.textList["errorList"]["E29"]
                    break
                self.newTrainOrgInfo.append(henseiNo)
            elif index in [3, 5, 7]:
                lineList = csv.split(",")
                for line in lineList:
                    line = line.strip()
                    if line == "":
                        continue
                    if index == 3:
                        bodyClassList.append(line)
                    elif index == 5:
                        bodyMdlList.append(line)
                    elif index == 7:
                        pantaMdlList.append(line)
            elif index in [9, 11, 13]:
                lineList = csv.split(",")
                for line in lineList:
                    line = line.strip()
                    if line == "":
                        continue
                    idx = int(line)
                    if index == 9:
                        if idx < -1 or idx >= len(bodyClassList):
                            errorFlag = True
                            self.error = textSetting.textList["errorList"]["E83"]
                            break
                        bodyClassIndexList.append(idx)
                    elif index == 11:
                        if idx < -1 or idx >= len(bodyMdlList):
                            errorFlag = True
                            self.error = textSetting.textList["errorList"]["E84"]
                            break
                        bodyMdlIndexList.append(idx)
                    elif index == 13:
                        if idx < -1 or idx >= len(pantaMdlList):
                            errorFlag = True
                            self.error = textSetting.textList["errorList"]["E85"]
                            break
                        pantaMdlIndexList.append(idx)
                if errorFlag:
                    break
                if index == 9:
                    if len(bodyClassIndexList) > 0 and len(bodyClassIndexList) != henseiNo:
                        errorFlag = True
                        self.error = textSetting.textList["errorList"]["E86"]
                        break
                elif index == 11:
                    if len(bodyMdlIndexList) > 0 and len(bodyMdlIndexList) != henseiNo:
                        errorFlag = True
                        self.error = textSetting.textList["errorList"]["E87"]
                        break
                elif index == 13:
                    if len(pantaMdlIndexList) > 0 and len(pantaMdlIndexList) != henseiNo:
                        errorFlag = True
                        self.error = textSetting.textList["errorList"]["E88"]
                        break
        if errorFlag:
            return False
        self.newTrainOrgInfo.append(bodyClassList)
        self.newTrainOrgInfo.append(bodyMdlList)
        self.newTrainOrgInfo.append(pantaMdlList)
        self.newTrainOrgInfo.append(bodyClassIndexList)
        self.newTrainOrgInfo.append(bodyMdlIndexList)
        self.newTrainOrgInfo.append(pantaMdlIndexList)
        return True

    def saveCsv(self, trainName):
        try:
            originData = self.trainOrgInfoList[trainName]["data"]["monoData"].raw_data
            newByteArr = bytearray()
            index = 0
            trainNo = struct.unpack("<i", originData[index:index + 4])[0]
            iTrainNo = struct.pack("<i", trainNo)
            newByteArr.extend(iTrainNo)

            notchCnt = self.newTrainOrgInfo[0]
            iNotchCnt = struct.pack("<i", notchCnt)
            newByteArr.extend(iNotchCnt)

            index = 8
            newByteArr.extend(originData[index:index + 4*3])

            henseiNo = self.newTrainOrgInfo[1]
            iHenseiNo = struct.pack("<i", henseiNo)
            newByteArr.extend(iHenseiNo)

            bodyClassCnt = len(self.newTrainOrgInfo[2])
            newByteArr.extend(struct.pack("<i", bodyClassCnt))
            for bodyClass in self.newTrainOrgInfo[2]:
                bodyClassNameCnt = len(bodyClass.encode("shift-jis"))
                newByteArr.extend(struct.pack("<i", bodyClassNameCnt))
                newByteArr.extend(bodyClass.encode("shift-jis"))

                for i in range(self.readStringPadding(bodyClassNameCnt)):
                    newByteArr.append(0)

            bodyMdlCnt = len(self.newTrainOrgInfo[3])
            newByteArr.extend(struct.pack("<i", bodyMdlCnt))
            for bodyMdl in self.newTrainOrgInfo[3]:
                bodyMdlNameCnt = len(bodyMdl.encode("shift-jis"))
                newByteArr.extend(struct.pack("<i", bodyMdlNameCnt))
                newByteArr.extend(bodyMdl.encode("shift-jis"))

                for i in range(self.readStringPadding(bodyMdlNameCnt)):
                    newByteArr.append(0)

            pantaMdlCnt = len(self.newTrainOrgInfo[4])
            newByteArr.extend(struct.pack("<i", pantaMdlCnt))
            for pantaMdl in self.newTrainOrgInfo[4]:
                pantaMdlNameCnt = len(pantaMdl.encode("shift-jis"))
                newByteArr.extend(struct.pack("<i", pantaMdlNameCnt))
                newByteArr.extend(pantaMdl.encode("shift-jis"))

                for i in range(self.readStringPadding(pantaMdlNameCnt)):
                    newByteArr.append(0)

            bodyClassIndexCnt = len(self.newTrainOrgInfo[5])
            newByteArr.extend(struct.pack("<i", bodyClassIndexCnt))
            for bodyClassIndex in self.newTrainOrgInfo[5]:
                newByteArr.extend(struct.pack("<i", bodyClassIndex))

            bodyMdlIndexCnt = len(self.newTrainOrgInfo[6])
            newByteArr.extend(struct.pack("<i", bodyMdlIndexCnt))
            for bodyMdlIndex in self.newTrainOrgInfo[6]:
                newByteArr.extend(struct.pack("<i", bodyMdlIndex))

            pantaMdlIndexCnt = len(self.newTrainOrgInfo[7])
            newByteArr.extend(struct.pack("<i", pantaMdlIndexCnt))
            for pantaIndex in self.newTrainOrgInfo[7]:
                newByteArr.extend(struct.pack("<i", pantaIndex))

            trackNum = 2
            # AE86, Deki
            if trainNo in [31, 32]:
                trackNum = 1

            for i in range(2):
                newByteArr.extend(struct.pack("<i", henseiNo * trackNum))
                for j in range(henseiNo * trackNum):
                    newByteArr.extend(struct.pack("<i", 0))

            data = self.trainOrgInfoList[trainName]["data"]["monoData"]
            data.save(raw_data=newByteArr)
            self.trainOrgInfoList[trainName]["data"]["size"] = len(newByteArr) + 32
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def getMeshTexInfoPathIdList(self, byteArr):
        try:
            meshTexInfoPathIdList = []
            index = 0
            # BodyOffset (fileId, pathId, padding)
            index += 12
            # fBodyOffset
            index += 4
            # FJOffset
            index += 4
            # BJOffset
            index += 4
            # PantaOffset
            index += 4
            # mBodyMat (fileId, pathId, padding)
            index += 12
            # MeshTexList
            meshTexListCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            for i in range(meshTexListCnt):
                # MeshTexInfo (fileId, pathId, padding)
                # fileId
                index += 4
                # pathId
                pathId = struct.unpack("<i", byteArr[index:index + 4])[0]
                meshTexInfoPathIdList.append(pathId)
                index += 4
                # padding
                index += 4
            return meshTexInfoPathIdList
        except Exception:
            self.error = traceback.format_exc()
            return None

    def getChangeMeshTexInfo(self, byteArr):
        try:
            changeMeshTexInfo = []
            index = 0
            # Target
            fileId = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            pathId = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            changeMeshTexInfo.append([fileId, pathId])
            index += 4
            # Target2
            fileId = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            pathId = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            changeMeshTexInfo.append([fileId, pathId])
            index += 4
            # MatIndex
            matIndex = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            changeMeshTexInfo.append(matIndex)
            # MatName
            matNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            matName = byteArr[index:index + matNameLen].decode("shift-jis")
            changeMeshTexInfo.append(matName)
            index += matNameLen
            index += self.readStringPadding(matNameLen)
            # shader_tex_name
            shaderTexNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            shaderTexName = byteArr[index:index + shaderTexNameLen].decode("shift-jis")
            changeMeshTexInfo.append(shaderTexName)
            index += shaderTexNameLen
            index += self.readStringPadding(shaderTexNameLen)
            # shader_emission_name
            shaderEmisNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            shaderEmisName = byteArr[index:index + shaderEmisNameLen].decode("shift-jis")
            changeMeshTexInfo.append(shaderEmisName)
            index += shaderEmisNameLen
            index += self.readStringPadding(shaderEmisNameLen)
            # asset_name
            assetNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            assetName = byteArr[index:index + assetNameLen].decode("shift-jis")
            changeMeshTexInfo.append(assetName)
            index += assetNameLen
            index += self.readStringPadding(assetNameLen)
            # TexName
            texNameListCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            texNameList = []
            for i in range(texNameListCnt):
                texNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
                index += 4
                texName = byteArr[index:index + texNameLen].decode("shift-jis")
                texNameList.append(texName)
                index += texNameLen
                index += self.readStringPadding(texNameLen)
            changeMeshTexInfo.append(texNameList)
            return changeMeshTexInfo
        except Exception:
            self.error = traceback.format_exc()
            return None

    def saveChangeMeshTex(self, csvLines, trainModelName, pathId):
        texNameList = [""] * 23
        for i in range(len(texNameList)):
            arr = csvLines[i].strip().split(",")
            texNameList[i] = arr[1]
        try:
            changeMeshTexInfoList = self.changeMeshTexList[trainModelName]
            changeMeshTexFilterInfo = [item for item in changeMeshTexInfoList if item["num"] == pathId][0]
            byteArr = changeMeshTexFilterInfo["data"]["monoData"].raw_data
            index = 0
            newByteArr = bytearray()
            # Target
            index += 12
            # Target2
            index += 12
            # MatIndex
            index += 4
            # MatName
            matNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            index += matNameLen
            index += self.readStringPadding(matNameLen)
            # shader_tex_name
            shaderTexNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            index += shaderTexNameLen
            index += self.readStringPadding(shaderTexNameLen)
            # shader_emission_name
            shaderEmisNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            index += shaderEmisNameLen
            index += self.readStringPadding(shaderEmisNameLen)
            # asset_name
            assetNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            index += assetNameLen
            index += self.readStringPadding(assetNameLen)
            # TexName
            newByteArr = bytearray(byteArr[0:index])

            texNameListCnt = struct.unpack("<i", byteArr[index:index + 4])[0]
            index += 4
            for i in range(texNameListCnt):
                texNameLen = struct.unpack("<i", byteArr[index:index + 4])[0]
                index += 4
                index += texNameLen
                index += self.readStringPadding(texNameLen)

            newTexNameListCnt = len(texNameList)
            iNewTexNameListCnt = struct.pack("<i", newTexNameListCnt)
            newByteArr.extend(iNewTexNameListCnt)
            for i in range(newTexNameListCnt):
                texNameLen = len(texNameList[i])
                iTexNameLen = struct.pack("<i", texNameLen)
                newByteArr.extend(iTexNameLen)
                newByteArr.extend(texNameList[i].encode("shift-jis"))
                for j in range(self.readStringPadding(texNameLen)):
                    newByteArr.append(0)
            newByteArr.extend(byteArr[index:])
            changeMeshTexFilterInfo["data"]["monoData"].save(raw_data=newByteArr)
            changeMeshTexFilterInfo["data"]["size"] = len(newByteArr) + 32
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveAssets(self):
        try:
            newFilename = self.filenameAndExt[0] + "_new" + self.filenameAndExt[1]
            newPath = os.path.join(self.fileDir, newFilename)
            with open(newPath, "wb") as f:
                f.write(self.env.file.save())
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False
