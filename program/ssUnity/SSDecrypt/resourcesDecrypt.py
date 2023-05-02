import os
import UnityPy
import struct
import traceback


class ResourcesDecrypt:
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileDir = os.path.dirname(filePath)
        self.filenameAndExt = os.path.splitext(os.path.basename(filePath))
        self.env = None
        self.monoBehaviourList = []
        self.trainOrgInfoList = []

    def open(self):
        try:
            self.env = UnityPy.load(self.filePath)
            return self.decrypt()
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        f = open("error.log", "w")
        f.write(self.error)
        f.close()

    def decrypt(self):
        try:
            self.monoBehaviourList = []
            self.trainOrgInfoList = []

            self.monoBehaviourList = [env for env in self.env.objects if env.type.name == "MonoBehaviour"]
            for mono in self.monoBehaviourList:
                data = mono.read()
                script = data.m_Script
                if script:
                    script = script.read()
                    if script.m_ClassName == "TrainOrgInfo":
                        gameObject = data.m_GameObject.read()
                        self.trainOrgInfoList.append([gameObject.name, script.m_ClassName, data.byte_size, data, data.raw_data])
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

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
                if bodyClassNameCnt % 4 != 0:
                    index += 4 - bodyClassNameCnt % 4
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
                if bodyMdlNameCnt % 4 != 0:
                    index += 4 - bodyMdlNameCnt % 4
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
                if pantaMdlNameCnt % 4 != 0:
                    index += 4 - pantaMdlNameCnt % 4
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

    def saveCsv(self, num, newTrainOrgInfo):
        try:
            originData = self.trainOrgInfoList[num][-1]
            newByteArr = bytearray()
            index = 0
            trainNo = struct.unpack("<i", originData[index:index + 4])[0]
            iTrainNo = struct.pack("<i", trainNo)
            newByteArr.extend(iTrainNo)

            notchCnt = newTrainOrgInfo[0]
            iNotchCnt = struct.pack("<i", notchCnt)
            newByteArr.extend(iNotchCnt)

            index = 8
            newByteArr.extend(originData[index:index + 4*3])

            henseiNo = newTrainOrgInfo[1]
            iHenseiNo = struct.pack("<i", henseiNo)
            newByteArr.extend(iHenseiNo)

            bodyClassCnt = len(newTrainOrgInfo[2])
            newByteArr.extend(struct.pack("<i", bodyClassCnt))
            for bodyClass in newTrainOrgInfo[2]:
                bodyClassNameCnt = len(bodyClass.encode("shift-jis"))
                newByteArr.extend(struct.pack("<i", bodyClassNameCnt))
                newByteArr.extend(bodyClass.encode("shift-jis"))

                if bodyClassNameCnt % 4 != 0:
                    for i in range(4 - bodyClassNameCnt % 4):
                        newByteArr.append(0)

            bodyMdlCnt = len(newTrainOrgInfo[3])
            newByteArr.extend(struct.pack("<i", bodyMdlCnt))
            for bodyMdl in newTrainOrgInfo[3]:
                bodyMdlNameCnt = len(bodyMdl.encode("shift-jis"))
                newByteArr.extend(struct.pack("<i", bodyMdlNameCnt))
                newByteArr.extend(bodyMdl.encode("shift-jis"))

                if bodyMdlNameCnt % 4 != 0:
                    for i in range(4 - bodyMdlNameCnt % 4):
                        newByteArr.append(0)

            pantaMdlCnt = len(newTrainOrgInfo[4])
            newByteArr.extend(struct.pack("<i", pantaMdlCnt))
            for pantaMdl in newTrainOrgInfo[4]:
                pantaMdlNameCnt = len(pantaMdl.encode("shift-jis"))
                newByteArr.extend(struct.pack("<i", pantaMdlNameCnt))
                newByteArr.extend(pantaMdl.encode("shift-jis"))

                if pantaMdlNameCnt % 4 != 0:
                    for i in range(4 - pantaMdlNameCnt % 4):
                        newByteArr.append(0)

            bodyClassIndexCnt = len(newTrainOrgInfo[5])
            newByteArr.extend(struct.pack("<i", bodyClassIndexCnt))
            for bodyClassIndex in newTrainOrgInfo[5]:
                newByteArr.extend(struct.pack("<i", bodyClassIndex))

            bodyMdlIndexCnt = len(newTrainOrgInfo[6])
            newByteArr.extend(struct.pack("<i", bodyMdlIndexCnt))
            for bodyMdlIndex in newTrainOrgInfo[6]:
                newByteArr.extend(struct.pack("<i", bodyMdlIndex))

            pantaMdlIndexCnt = len(newTrainOrgInfo[7])
            newByteArr.extend(struct.pack("<i", pantaMdlIndexCnt))
            for pantaIndex in newTrainOrgInfo[7]:
                newByteArr.extend(struct.pack("<i", pantaIndex))

            trackNum = 2
            # AE86, Deki
            if trainNo in [31, 32]:
                trackNum = 1

            for i in range(2):
                newByteArr.extend(struct.pack("<i", henseiNo * trackNum))
                for j in range(henseiNo * trackNum):
                    newByteArr.extend(struct.pack("<i", 0))

            data = self.trainOrgInfoList[num][-2]
            data.save(raw_data=newByteArr)

            newFilename = self.filenameAndExt[0] + "_new" + self.filenameAndExt[1]
            newPath = os.path.join(self.fileDir, newFilename)
            with open(newPath, "wb") as f:
                f.write(self.env.file.save())
            return True

        except Exception:
            self.error = traceback.format_exc()
            return False
