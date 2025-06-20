import struct
import traceback
import program.textSetting as textSetting
from program.encodingClass import SJISEncodingObject
from program.errorLogClass import ErrorLogObj


LSTrainName = [
    "H2000",
    "H8200",
    "H2300",
    "JR223",
    "21000R",
    "K800",
    "H7000",
    "DEKI",
    "TAKUMI",
    "K80",
    "S300"
]

perfName = [
    "None_Tlk",
    "add1",
    "add2",
    "add3",
    "UpHill",
    "DownHill",
    "Weight",
    "CompPower",
    "First_break",
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    "Second_Breake",
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    "SpBreake",
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    "D_Speed" + textSetting.textList["orgInfoEditor"]["noUsed"],
    "One_Speed",
    "OutParam",
    "D_Add",
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    textSetting.textList["orgInfoEditor"]["unknown"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    "Carbe",
    "Jump",
    "ChangeFrame",
    "OutRun_Top",
    "OutRun_Other",
    "OutRun_Frame",
    "OutRun_Speed",
    "OutRun_JumpFrame",
    "OutRun_JumpHeight",
]

hurikoName = ""


class LSdecrypt():
    def __init__(self, filePath):
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.trainNameList = LSTrainName
        self.trainPerfNameList = perfName
        self.trainHurikoNameList = hurikoName
        self.trainInfoList = []
        self.indexList = []
        self.mdlIndexList = []
        self.henseiIndexList = []
        self.henseiStartIndexList = []
        self.henseiEndIndexList = []
        self.else2IndexList = []
        self.elseList2IndexList = []
        self.lensIndexList = []
        self.tailIndexList = []
        self.tailEndIndexList = []
        self.byteArr = []
        self.error = ""
        self.trainModelList = []
        self.colorIdx = -1
        self.stageIdx = -1
        self.notchContentCnt = 2

    def open(self):
        try:
            f = open(self.filePath, "rb")
            line = f.read()
            f.close()
            self.decrypt(line)
            self.byteArr = bytearray(line)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        self.errObj.write(self.error)

    def decrypt(self, line):
        self.trainInfoList = []
        self.indexList = []
        self.mdlIndexList = []
        self.henseiIndexList = []
        self.henseiStartIndexList = []
        self.henseiEndIndexList = []
        self.else2IndexList = []
        self.elseList2IndexList = []
        self.lensIndexList = []
        self.tailIndexList = []
        self.tailEndIndexList = []
        self.error = ""
        self.trainModelList = []

        index = 0
        trainCnt = line[index]
        index += 1

        for i in range(trainCnt):
            trainNameCnt = line[index]
            index += 1
            # trainName
            self.encObj.convertString(line[index:index + trainNameCnt])
            index += trainNameCnt

            trainOrgInfo = []
            self.indexList.append(index)
            trainSpeedInfo = []
            notchCnt = int(line[index])
            index += 1
            for j in range(2):
                for k in range(notchCnt):
                    speed = struct.unpack("<f", line[index:index + 4])[0]
                    speed = round(speed, 4)
                    trainSpeedInfo.append(speed)
                    index += 4
            trainOrgInfo.append(trainSpeedInfo)

            trainPerfInfo = []
            for j in range(len(perfName)):
                perf = struct.unpack("<f", line[index:index + 4])[0]
                perf = round(perf, 5)
                trainPerfInfo.append(perf)
                index += 4
            trainOrgInfo.append(trainPerfInfo)
            self.trainInfoList.append(trainOrgInfo)

            self.mdlIndexList.append(index)

            train = {
                "daishaCnt": 0,
                "trackNames": [],
                "mdlCnt": 0,
                "mdlNames": [],
                "colNames": [],
                "pantaNames": [],
                "mdlList": [],
                "pantaList": [],
                "colList": [],
                "colorCnt": 0,
                "elseModel": [],
                "else2Model": [],
                "elseList2": [],
                "lensList": [],
                "tailList": [],
            }

            daishaCnt = line[index]
            train["daishaCnt"] = daishaCnt
            index += 1

            daishaModelNameCnt = line[index]
            index += 1
            daishaModelName = self.encObj.convertString(line[index:index + daishaModelNameCnt])
            train["trackNames"].append(daishaModelName)
            index += daishaModelNameCnt

            self.henseiIndexList.append(index)

            henseiCnt = line[index]
            train["mdlCnt"] = henseiCnt
            index += 1

            # LSはモデル3つ固定
            for j in range(3):
                modelNameCnt = line[index]
                index += 1
                modelName = self.encObj.convertString(line[index:index + modelNameCnt])
                train["mdlNames"].append(modelName)
                index += modelNameCnt

            # LSはCOLも3つ固定
            for j in range(3):
                colNameCnt = line[index]
                index += 1
                colName = self.encObj.convertString(line[index:index + colNameCnt])
                train["colNames"].append(colName)
                index += colNameCnt

            # LSは固定で自動編成
            for i in range(henseiCnt):
                train["mdlList"].append(1)
            train["mdlList"][0] = 0
            train["mdlList"][-1] = len(train["mdlNames"]) - 1

            self.henseiStartIndexList.append(index)

            pantaModelCnt = line[index]
            index += 1

            # 86、新幹線はパンタなし
            if pantaModelCnt > 0:
                for j in range(pantaModelCnt):
                    pantaModelNameCnt = line[index]
                    index += 1
                    pantaModelName = self.encObj.convertString(line[index:index + pantaModelNameCnt])
                    train["pantaNames"].append(pantaModelName)
                    index += pantaModelNameCnt

                train["pantaNames"].append(textSetting.textList["orgInfoEditor"]["noList"])

                for j in range(henseiCnt):
                    idx = line[index]
                    if idx == 0xFF:
                        train["pantaList"].append(-1)
                    else:
                        train["pantaList"].append(idx)
                    index += 1

            self.henseiEndIndexList.append(index)

            for j in range(9):
                idx = line[index]
                if idx == 0xFF:
                    idx = -1
                train["elseModel"].append(idx)
                index += 1

            self.else2IndexList.append(index)

            for j in range(4):
                seLen = line[index]
                index += 1
                seFileName = self.encObj.convertString(line[index:index + seLen])
                train["else2Model"].append(seFileName)
                index += seLen

            seLen = line[index]
            index += 1
            seFileName = self.encObj.convertString(line[index:index + seLen])
            train["else2Model"].append(seFileName)
            index += seLen
            tempF = struct.unpack("<f", line[index:index + 4])[0]
            tempF = "{0}".format(round(tempF, 4))
            train["else2Model"].append(tempF)
            index += 4

            sstLen = line[index]
            index += 1
            sstFileName = self.encObj.convertString(line[index:index + sstLen])
            train["else2Model"].append(sstFileName)
            index += sstLen

            seLen = line[index]
            index += 1
            seFileName = self.encObj.convertString(line[index:index + seLen])
            train["else2Model"].append(seFileName)
            index += seLen

            self.elseList2IndexList.append(index)

            for j in range(2):
                seFileCnt = line[index]
                index += 1
                seLen = line[index]
                index += 1
                seFileName = self.encObj.convertString(line[index:index + seLen])
                index += seLen
                train["elseList2"].append([seFileCnt, seFileName])

            self.lensIndexList.append(index)

            lensCnt = line[index]
            index += 1
            for j in range(lensCnt):
                lensList = []
                b = line[index]
                index += 1
                lensName = self.encObj.convertString(line[index:index + b])
                lensList.append(lensName)
                index += b

                b = line[index]
                index += 1
                lensName = self.encObj.convertString(line[index:index + b])
                lensList.append(lensName)
                index += b

                f1 = struct.unpack("<f", line[index:index + 4])[0]
                lensList.append(f1)
                index += 4
                f2 = struct.unpack("<f", line[index:index + 4])[0]
                lensList.append(f2)
                index += 4

                tempList = []
                for k in range(4):
                    tempList.append(line[index])
                    index += 1
                lensList.append(tempList)
                train["lensList"].append(lensList)

            self.tailIndexList.append(index)

            tailCnt = line[index]
            index += 1

            tailList = []
            tailSmfList = []
            for j in range(tailCnt):
                b = line[index]
                index += 1
                tailSmfName = self.encObj.convertString(line[index:index + b])
                tailSmfList.append(tailSmfName)
                index += b
            tailList.append(tailSmfList)

            tailElseList = []
            for j in range(tailCnt):
                tailElseList.append(line[index])
                index += 1
            tailList.append(tailElseList)

            tailLensList = []
            for j in range(tailCnt):
                lensList = []
                b = line[index]
                index += 1
                lensName = self.encObj.convertString(line[index:index + b])
                lensList.append(lensName)
                index += b

                b = line[index]
                index += 1
                lensName = self.encObj.convertString(line[index:index + b])
                lensList.append(lensName)
                index += b

                f1 = struct.unpack("<f", line[index:index + 4])[0]
                lensList.append(f1)
                index += 4
                f2 = struct.unpack("<f", line[index:index + 4])[0]
                lensList.append(f2)
                index += 4

                tempList = []
                for k in range(4):
                    tempList.append(line[index])
                    index += 1
                lensList.append(tempList)
                tailLensList.append(lensList)

            self.tailEndIndexList.append(index)
            train["tailList"] = [tailSmfList, tailElseList, tailLensList]

            self.trainModelList.append(train)

    def saveNotchInfo(self, trainIdx, newNotchNum):
        try:
            newByteArr = bytearray()
            index = self.indexList[trainIdx]
            trainOrgInfo = self.trainInfoList[trainIdx]
            speed = trainOrgInfo[0]
            notchContentCnt = 2
            oldNotchNum = len(speed) // notchContentCnt

            diff = newNotchNum - oldNotchNum
            newSpeed = []
            if diff <= 0:
                for i in range(notchContentCnt):
                    for j in range(newNotchNum):
                        newSpeed.append(speed[oldNotchNum * i + j])
            else:
                for i in range(notchContentCnt):
                    for j in range(oldNotchNum):
                        newSpeed.append(speed[oldNotchNum * i + j])
                    for j in range(diff):
                        newSpeed.append(0)

            newByteArr.extend(self.byteArr[0:index])
            newByteArr.append(newNotchNum)
            index += 1

            for i in range(len(newSpeed)):
                byteF = struct.pack("<f", newSpeed[i])
                newByteArr.extend(byteF)

            for i in range(len(speed)):
                index += 4

            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTrainInfo(self, trainIdx, varList):
        try:
            index = self.indexList[trainIdx]
            notchCnt = self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]

            for i in range(notchCnt):
                speed = struct.pack("<f", varList[self.notchContentCnt * i].get())
                newByteArr.extend(speed)

            for i in range(notchCnt):
                tlk = struct.pack("<f", varList[self.notchContentCnt * i + 1].get())
                newByteArr.extend(tlk)

            perfCnt = len(self.trainPerfNameList)
            for i in range(perfCnt):
                perf = struct.pack("<f", varList[notchCnt * self.notchContentCnt + i].get())
                newByteArr.extend(perf)

            index = self.mdlIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveHenseiNum(self, trainIdx, num):
        try:
            newByteArr = bytearray()

            index = self.henseiStartIndexList[trainIdx]
            newByteArr = self.byteArr[0:index]

            henseiIndex = self.henseiIndexList[trainIdx]

            newByteArr[henseiIndex] = num
            oldCnt = self.byteArr[henseiIndex]

            pantaModelCnt = self.byteArr[index]
            newByteArr.append(pantaModelCnt)
            index += 1

            # pantaList
            if pantaModelCnt > 0:
                startIdx = index
                for j in range(pantaModelCnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b

                newByteArr.extend(self.byteArr[startIdx:index])

                if num < oldCnt:
                    for j in range(num):
                        newByteArr.append(self.byteArr[index])
                        index += 1

                    for j in range(oldCnt - num):
                        index += 1
                else:
                    for j in range(oldCnt):
                        newByteArr.append(self.byteArr[index])
                        index += 1

                    for j in range(num - oldCnt):
                        newByteArr.append(0)

            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveHensei(self, trainIdx, trainWidget):
        try:
            index = self.henseiStartIndexList[trainIdx]
            newByteArr = self.byteArr[0:index]

            henseiIndex = self.henseiIndexList[trainIdx]
            cnt = self.byteArr[henseiIndex]

            pantaModelCnt = self.byteArr[index]
            newByteArr.append(pantaModelCnt)
            index += 1

            if pantaModelCnt > 0:
                startIdx = index
                for j in range(pantaModelCnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b
                newByteArr.extend(self.byteArr[startIdx:index])

                for i in range(cnt):
                    idx = trainWidget.comboList[2 * i + 1].current()
                    if idx == len(trainWidget.comboList[2 * i + 1]["values"]) - 1:
                        idx = 255
                    newByteArr.append(idx)
                    index += 1

            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElseList(self, trainIdx, ver, elseList):
        try:
            if ver == 1:
                index = self.henseiEndIndexList[trainIdx]
                newByteArr = self.byteArr[0:index]

                for i in range(len(elseList)):
                    idx = int(elseList[i])
                    if idx == -1:
                        idx = 0xFF
                    newByteArr.append(idx)
                    index += 1
                newByteArr.extend(self.byteArr[index:])
                self.byteArr = newByteArr

            elif ver == 2:
                index = self.else2IndexList[trainIdx]
                newByteArr = self.byteArr[0:index]

                for i in range(len(elseList)):
                    if i == 5:
                        f = struct.pack("<f", float(elseList[i]))
                        newByteArr.extend(f)
                    else:
                        strHex = self.encObj.convertByteArray(elseList[i])
                        newByteArr.append(len(strHex))
                        newByteArr.extend(strHex)
                index = self.elseList2IndexList[trainIdx]

                newByteArr.extend(self.byteArr[index:])
                self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse2List(self, trainIdx, elseList):
        try:
            index = self.elseList2IndexList[trainIdx]

            newByteArr = self.byteArr[0:index]

            for i in range(len(elseList)):
                elseInfo = elseList[i]
                num = elseInfo[0]
                newByteArr.append(num)

                strHex = self.encObj.convertByteArray(elseInfo[1])
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            index = self.lensIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveLensCnt(self, trainIdx, cnt):
        try:
            index = self.lensIndexList[trainIdx]
            lensCnt = self.byteArr[index]
            index += 1

            if cnt > lensCnt:
                index = self.tailIndexList[trainIdx]
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - lensCnt):
                    strHex = self.encObj.convertByteArray("lensflear00.tga")
                    newByteArr.append(len(strHex))
                    newByteArr.extend(strHex)
                    strHex = self.encObj.convertByteArray("lensflear01.tga")
                    newByteArr.append(len(strHex))
                    newByteArr.extend(strHex)

                    tempF0 = struct.pack("<f", 0)
                    for j in range(2):
                        newByteArr.extend(tempF0)
                    for j in range(4):
                        newByteArr.append(0)
            else:
                for i in range(cnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    b = self.byteArr[index]
                    index += 1
                    index += b

                    for j in range(2):
                        index += 4
                    for j in range(4):
                        index += 1
                newByteArr = self.byteArr[0:index]

            index = self.tailIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])
            index = self.lensIndexList[trainIdx]
            newByteArr[index] = cnt

            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveLensList(self, trainIdx, valList):
        try:
            index = self.lensIndexList[trainIdx]
            index += 1
            newByteArr = self.byteArr[0:index]

            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j in [0, 1]:
                        strHex = self.encObj.convertByteArray(valInfo[j])
                        newByteArr.append(len(strHex))
                        newByteArr.extend(strHex)
                    elif j in [2, 3]:
                        tempF = struct.pack("<f", valInfo[j])
                        newByteArr.extend(tempF)
                    elif j == 4:
                        bList = valInfo[j]
                        for k in range(len(bList)):
                            newByteArr.append(bList[k])

            index = self.tailIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTailCnt(self, trainIdx, cnt):
        try:
            index = self.tailIndexList[trainIdx]
            tailCnt = self.byteArr[index]
            index += 1

            if cnt > tailCnt:
                index = self.tailEndIndexList[trainIdx]
                newByteArr = self.byteArr[0:index]

                index = self.tailIndexList[trainIdx]
                index += 1

                for i in range(tailCnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b

                for i in range(cnt - tailCnt):
                    strHex = self.encObj.convertByteArray(".smf")
                    newByteArr.insert(index, len(strHex))
                    index += 1
                    for s in strHex:
                        newByteArr.insert(index, s)
                        index += 1

                for i in range(tailCnt):
                    index += 1

                for i in range(cnt - tailCnt):
                    newByteArr.insert(index, 0)

                for i in range(tailCnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b

                    b = self.byteArr[index]
                    index += 1
                    index += b

                    for j in range(2):
                        index += 4
                    for j in range(4):
                        index += 1

                for i in range(cnt - tailCnt):
                    strHex = self.encObj.convertByteArray("lensflear00.tga")
                    newByteArr.insert(index, len(strHex))
                    index += 1
                    for s in strHex:
                        newByteArr.insert(index, s)
                        index += 1

                    strHex = self.encObj.convertByteArray("lensflear01.tga")
                    newByteArr.insert(index, len(strHex))
                    index += 1
                    for s in strHex:
                        newByteArr.insert(index, s)
                        index += 1

                    tempF0 = struct.pack("<f", 0)
                    for j in range(2):
                        for s in tempF0:
                            newByteArr.insert(index, s)
                            index += 1
                    for j in range(4):
                        newByteArr.insert(index, 0)
                        index += 1
            else:
                for i in range(cnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b
                newByteArr = self.byteArr[0:index]

                for i in range(tailCnt - cnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b

                startIdx = index
                for i in range(cnt):
                    index += 1
                newByteArr.extend(self.byteArr[startIdx:index])

                for i in range(tailCnt - cnt):
                    index += 1

                startIdx = index
                for i in range(cnt):
                    b = self.byteArr[index]
                    index += 1
                    index += b

                    b = self.byteArr[index]
                    index += 1
                    index += b

                    for j in range(2):
                        index += 4
                    for j in range(4):
                        index += 1
                newByteArr.extend(self.byteArr[startIdx:index])

            index = self.tailEndIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])
            index = self.tailIndexList[trainIdx]
            newByteArr[index] = cnt

            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTailSmfElse(self, trainIdx, valList):
        try:
            index = self.tailIndexList[trainIdx]
            # tailCnt
            self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]
            cnt = len(valList) // 2
            for i in range(cnt):
                valInfo = valList[i]
                strHex = self.encObj.convertByteArray(valInfo)
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

                b = self.byteArr[index]
                index += 1
                index += b

            for i in range(cnt):
                valInfo = valList[cnt + i]
                newByteArr.append(valInfo)

                index += 1

            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTailLensList(self, trainIdx, valList):
        try:
            index = self.tailIndexList[trainIdx]
            tailCnt = self.byteArr[index]
            index += 1

            for i in range(tailCnt):
                b = self.byteArr[index]
                index += 1
                index += b

            for i in range(tailCnt):
                index += 1

            newByteArr = self.byteArr[0:index]

            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j in [0, 1]:
                        strHex = self.encObj.convertByteArray(valInfo[j])
                        newByteArr.append(len(strHex))
                        newByteArr.extend(strHex)
                    elif j in [2, 3]:
                        tempF = struct.pack("<f", valInfo[j])
                        newByteArr.extend(tempF)
                    elif j == 4:
                        bList = valInfo[j]
                        for k in range(len(bList)):
                            newByteArr.append(bList[k])

            index = self.tailEndIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveAllEdit(self, perfIndex, num, calcIndex):
        try:
            for index in self.indexList:
                idx = index
                notchCnt = self.byteArr[index]
                idx += 1
                # speed
                for i in range(notchCnt):
                    idx += 4
                # tlk
                for i in range(notchCnt):
                    idx += 4

                idx = idx + 4 * perfIndex

                originPerf = struct.unpack("<f", self.byteArr[idx:idx + 4])[0]
                if calcIndex == 0:
                    originPerf *= num
                else:
                    originPerf = num

                perf = struct.pack("<f", originPerf)
                for n in perf:
                    self.byteArr[idx] = n
                    idx += 1
            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def setDefaultTrainInfo(self, srcList, distData, checkStatusList):
        srcIndex = srcList[0]
        srcNotchNum = srcList[1]
        srcSpeed = srcList[2]
        srcPerf = srcList[3]
        distNotchNum = len(distData["notch"])
        notchCheckStatus = checkStatusList[0]
        perfCheckStatus = checkStatusList[1]

        try:
            loopCnt = 0
            if srcNotchNum > distNotchNum:
                loopCnt = distNotchNum
            else:
                loopCnt = srcNotchNum

            index = srcIndex
            index += 1

            for i in range(len(srcPerf)):
                srcPerf[i] = distData["att"][i]

            for i in range(2):
                if i == 0:
                    data = distData["notch"]
                elif i == 1:
                    data = distData["tlk"]

                for j in range(loopCnt):
                    srcSpeed[i * srcNotchNum + j] = data[j]

            for i in range(srcNotchNum):
                if notchCheckStatus:
                    speed = struct.pack("<f", srcSpeed[0 * srcNotchNum + i])
                    for n in speed:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4
            for i in range(srcNotchNum):
                if notchCheckStatus:
                    tlk = struct.pack("<f", srcSpeed[1 * srcNotchNum + i])
                    for n in tlk:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4

            for i in range(len(distData["att"])):
                if perfCheckStatus:
                    perf = struct.pack("<f", srcPerf[i])
                    for n in perf:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def extractCsvTrainInfo(self, trainIdx, filePath):
        try:
            w = open(filePath, "w", encoding="utf-8-sig")
            trainOrgInfo = self.trainInfoList[trainIdx]
            speedList = trainOrgInfo[0]
            index = self.indexList[trainIdx]
            notchCnt = self.byteArr[index]

            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["notchLabel"], notchCnt))
            w.write("{0},{1}\n".format(
                textSetting.textList["orgInfoEditor"]["csvNotchSpeed"],
                textSetting.textList["orgInfoEditor"]["csvNotchTlk"])
            )

            for i in range(notchCnt):
                for j in range(self.notchContentCnt):
                    w.write("{0}".format(speedList[i + notchCnt * j]))
                    if j == self.notchContentCnt - 1:
                        w.write("\n")
                    else:
                        w.write(",")
            w.write("{0}\n".format(textSetting.textList["orgInfoEditor"]["perfLabel"]))

            perfList = trainOrgInfo[1]
            perfNameList = self.trainPerfNameList
            for i in range(len(perfList)):
                w.write("{0},{1}\n".format(perfNameList[i], perfList[i]))

            train = self.trainModelList[trainIdx]
            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvDaishaTitle"], train["daishaCnt"]))
            w.write(",".join(train["trackNames"]))
            w.write("\n")

            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvOrgNumTitle"], train["mdlCnt"]))

            # mdlCnt = len(train["mdlNames"])
            w.write("{0}\n".format(textSetting.textList["orgInfoEditor"]["csvMdlTitle"]))
            w.write(",".join(train["mdlNames"]))
            w.write("\n")

            # colCnt = len(train["colNames"])
            w.write("{0}\n".format(textSetting.textList["orgInfoEditor"]["csvColTitle"]))
            w.write(",".join(train["colNames"]))
            w.write("\n")

            if len(train["pantaNames"]) > 0:
                w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvPantaTitle"], len(train["pantaNames"][:-1])))
                w.write(",".join(train["pantaNames"][:-1]))
                w.write("\n")

                w.write("{0},".format(textSetting.textList["orgInfoEditor"]["csvPantaIdxTitle"]))
                w.write(",".join([str(x) for x in train["pantaList"]]))
                w.write("\n")
            else:
                w.write("{0}:0\n".format(textSetting.textList["orgInfoEditor"]["csvPantaTitle"]))

            w.write("{0},".format(textSetting.textList["orgInfoEditor"]["csvElseTitle"]))
            w.write(",".join([str(x) for x in train["elseModel"]]))
            w.write("\n")

            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvLensTitle"], len(train["lensList"])))
            for i in range(len(train["lensList"])):
                lensInfo = train["lensList"][i]
                w.write("{0},{1}\n".format(lensInfo[0], lensInfo[1]))
                w.write("{0},{1}\n".format(lensInfo[2], lensInfo[3]))
                w.write(",".join([str(x) for x in lensInfo[4]]))
                w.write("\n")

            tailCnt = len(train["tailList"][0])
            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvTailTitle"], tailCnt))
            w.write(",".join(train["tailList"][0]))
            w.write("\n")
            w.write(",".join([str(x) for x in train["tailList"][1]]))
            w.write("\n")
            for i in range(len(train["tailList"][2])):
                lensInfo = train["tailList"][2][i]
                w.write("{0},{1}\n".format(lensInfo[0], lensInfo[1]))
                w.write("{0},{1}\n".format(lensInfo[2], lensInfo[3]))
                w.write(",".join([str(x) for x in lensInfo[4]]))
                w.write("\n")

            w.close()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def checkCsvResult(self, csvLines):
        cnt = 0
        self.csvReadInfo = {}
        try:
            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["notchLabel"]:
                self.error = textSetting.textList["errorList"]["E22"]
                return False

            arr = csvLines[cnt].strip().split(":")[1]

            notchCnt = int(arr.split(",")[0])
            if notchCnt not in [3, 4, 5]:
                self.error = textSetting.textList["errorList"]["E23"].format(notchCnt)
                return False
            self.csvReadInfo["notchCnt"] = notchCnt
            cnt += 1

            arr = csvLines[cnt].strip().split(",")[0:2]
            header = ",".join(arr)
            inspHeader = "{0},{1}".format(
                textSetting.textList["orgInfoEditor"]["csvNotchSpeed"],
                textSetting.textList["orgInfoEditor"]["csvNotchTlk"]
            )
            if header != inspHeader:
                self.error = textSetting.textList["errorList"]["E24"]
                return False
            cnt += 1

            speed = []
            tlk = []
            try:
                for i in range(notchCnt):
                    arr = csvLines[cnt].strip().split(",")
                    speed.append(float(arr[0]))
                    tlk.append(float(arr[1]))
                    cnt += 1
            except Exception:
                self.error = textSetting.textList["errorList"]["E25"].format(notchCnt, i + 1)
                return False
            speed.extend(tlk)
            self.csvReadInfo["speed"] = speed

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["perfLabel"]:
                self.error = textSetting.textList["errorList"]["E26"]
                return False
            cnt += 1

            perf = []
            for i in range(len(self.trainPerfNameList)):
                arr = csvLines[cnt].strip().split(",")
                perf.append(float(arr[1]))
                cnt += 1
            self.csvReadInfo["perf"] = perf

            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["csvDaishaTitle"]:
                self.error = textSetting.textList["errorList"]["E27"]
                return False
            arr = csvLines[cnt].strip().split(":")[1]
            daishaCnt = int(arr.split(",")[0])
            self.csvReadInfo["daishaCnt"] = daishaCnt
            cnt += 1

            trackInfo = []
            arr = csvLines[cnt].strip().split(",")
            trackInfo.append(arr[0])
            cnt += 1
            self.csvReadInfo["trackInfo"] = trackInfo

            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["csvOrgNumTitle"]:
                self.error = textSetting.textList["errorList"]["E28"]
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            orgCnt = int(arr.split(",")[0])
            if orgCnt < 1:
                self.error = textSetting.textList["errorList"]["E29"]
                return False
            cnt += 1
            self.csvReadInfo["orgCnt"] = orgCnt

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["csvMdlTitle"]:
                self.error = textSetting.textList["errorList"]["E30"]
                return False

            mdlCnt = 3
            cnt += 1

            mdlNameList = []
            arr = csvLines[cnt].strip().split(",")
            for i in range(mdlCnt):
                mdlNameList.append(arr[i])
            cnt += 1
            self.csvReadInfo["mdlNameList"] = mdlNameList

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["csvColTitle"]:
                self.error = textSetting.textList["errorList"]["E31"]
                return False

            colCnt = 3
            cnt += 1

            colNameList = []
            arr = csvLines[cnt].strip().split(",")
            for i in range(colCnt):
                colNameList.append(arr[i])
            cnt += 1
            self.csvReadInfo["colNameList"] = colNameList

            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["csvPantaTitle"]:
                self.error = textSetting.textList["errorList"]["E32"]
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            pantaCnt = int(arr.split(",")[0])
            cnt += 1
            self.csvReadInfo["pantaCnt"] = pantaCnt

            if pantaCnt > 0:
                pantaNameList = []
                arr = csvLines[cnt].strip().split(",")
                for i in range(pantaCnt):
                    pantaNameList.append(arr[i])
                cnt += 1
                self.csvReadInfo["pantaNameList"] = pantaNameList

                if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["csvPantaIdxTitle"]:
                    self.error = textSetting.textList["errorList"]["E33"]
                    return False

                pantaList = []
                arr = csvLines[cnt].strip().split(",")[1:]
                for i in range(orgCnt):
                    try:
                        idx = int(arr[i])
                        if idx < -1 or idx >= pantaCnt:
                            self.error = textSetting.textList["errorList"]["E34"]
                            return False
                    except Exception:
                        self.error = textSetting.textList["errorList"]["E35"]
                        return False
                    pantaList.append(idx)
                cnt += 1
                self.csvReadInfo["pantaList"] = pantaList

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["csvElseTitle"]:
                self.error = textSetting.textList["errorList"]["E36"]
                return False

            arr = csvLines[cnt].strip().split(",")[1:]
            elseModel = []
            for i in range(9):
                elseModel.append(int(arr[i]))
            self.csvReadInfo["elseModel"] = elseModel
            cnt += 1

            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["csvLensTitle"]:
                self.error = textSetting.textList["errorList"]["E37"]
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            lensCnt = int(arr.split(",")[0])
            cnt += 1

            lensList = []
            for i in range(lensCnt):
                lensInfo = []

                arr = csvLines[cnt].strip().split(",")
                lensInfo.append(arr[0])
                lensInfo.append(arr[1])
                cnt += 1

                arr = csvLines[cnt].strip().split(",")
                lensInfo.append(float(arr[0]))
                lensInfo.append(float(arr[1]))
                cnt += 1

                arr = csvLines[cnt].strip().split(",")
                tempList = []
                tempList.append(int(arr[0]))
                tempList.append(int(arr[1]))
                tempList.append(int(arr[2]))
                tempList.append(int(arr[3]))
                lensInfo.append(tempList)
                cnt += 1

                lensList.append(lensInfo)
            self.csvReadInfo["lensList"] = lensList

            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["csvTailTitle"]:
                self.error = textSetting.textList["errorList"]["E38"]
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            tailCnt = int(arr.split(",")[0])
            cnt += 1

            tailList = []
            tailSmfNameList = []
            for i in range(tailCnt):
                arr = csvLines[cnt].strip().split(",")
                tailSmfNameList.append(arr[i])
            cnt += 1
            tailList.append(tailSmfNameList)

            tailElseList = []
            for i in range(tailCnt):
                arr = csvLines[cnt].strip().split(",")
                tailElseList.append(int(arr[i]))
            cnt += 1
            tailList.append(tailElseList)

            tailLensList = []
            for i in range(tailCnt):
                lensInfo = []

                arr = csvLines[cnt].strip().split(",")
                lensInfo.append(arr[0])
                lensInfo.append(arr[1])
                cnt += 1

                arr = csvLines[cnt].strip().split(",")
                lensInfo.append(float(arr[0]))
                lensInfo.append(float(arr[1]))
                cnt += 1

                arr = csvLines[cnt].strip().split(",")
                tempList = []
                tempList.append(int(arr[0]))
                tempList.append(int(arr[1]))
                tempList.append(int(arr[2]))
                tempList.append(int(arr[3]))
                lensInfo.append(tempList)
                cnt += 1

                tailLensList.append(lensInfo)
            tailList.append(tailLensList)
            self.csvReadInfo["tailList"] = tailList

            return True
        except Exception:
            self.error = textSetting.textList["errorList"]["E39"].format(cnt + 1)
            return False

    def saveCsvTrainInfo(self, trainIdx):
        try:
            index = self.indexList[trainIdx]
            newByteArr = self.byteArr[0:index]

            notchCnt = self.csvReadInfo["notchCnt"]
            newByteArr.append(notchCnt)

            speed = self.csvReadInfo["speed"]
            for i in range(2):
                for j in range(notchCnt):
                    f = struct.pack("<f", speed[i * notchCnt + j])
                    newByteArr.extend(f)

            perf = self.csvReadInfo["perf"]
            for i in range(len(perf)):
                f = struct.pack("<f", perf[i])
                newByteArr.extend(f)

            daishaCnt = self.csvReadInfo["daishaCnt"]
            newByteArr.append(daishaCnt)

            trackInfo = self.csvReadInfo["trackInfo"]
            for i in range(len(trackInfo)):
                strHex = self.encObj.convertByteArray(trackInfo[i])
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            orgCnt = self.csvReadInfo["orgCnt"]
            newByteArr.append(orgCnt)

            mdlNameList = self.csvReadInfo["mdlNameList"]
            for i in range(len(mdlNameList)):
                strHex = self.encObj.convertByteArray(mdlNameList[i])
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            colNameList = self.csvReadInfo["colNameList"]
            for i in range(len(colNameList)):
                strHex = self.encObj.convertByteArray(colNameList[i])
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            pantaCnt = self.csvReadInfo["pantaCnt"]
            newByteArr.append(pantaCnt)

            if pantaCnt > 0:
                pantaNameList = self.csvReadInfo["pantaNameList"]
                for i in range(len(pantaNameList)):
                    strHex = self.encObj.convertByteArray(pantaNameList[i])
                    newByteArr.append(len(strHex))
                    newByteArr.extend(strHex)

                pantaList = self.csvReadInfo["pantaList"]
                for i in range(orgCnt):
                    if pantaList[i] == -1:
                        newByteArr.append(0xFF)
                    else:
                        newByteArr.append(pantaList[i])

            elseModel = self.csvReadInfo["elseModel"]
            for i in range(len(elseModel)):
                idx = elseModel[i]
                if idx == -1:
                    idx = 0xFF
                newByteArr.append(idx)

            startIdx = self.else2IndexList[trainIdx]
            index = self.lensIndexList[trainIdx]
            newByteArr.extend(self.byteArr[startIdx:index])

            lensList = self.csvReadInfo["lensList"]
            newByteArr.append(len(lensList))
            for i in range(len(lensList)):
                lensInfo = lensList[i]
                for j in range(len(lensInfo)):
                    if j in [0, 1]:
                        strHex = self.encObj.convertByteArray(lensInfo[j])
                        newByteArr.append(len(strHex))
                        newByteArr.extend(strHex)
                    elif j in [2, 3]:
                        tempF = struct.pack("<f", lensInfo[j])
                        newByteArr.extend(tempF)
                    elif j == 4:
                        bList = lensInfo[j]
                        for k in range(len(bList)):
                            newByteArr.append(bList[k])

            tailList = self.csvReadInfo["tailList"]
            tailCnt = len(tailList[0])
            newByteArr.append(tailCnt)

            for i in range(tailCnt):
                strHex = self.encObj.convertByteArray(tailList[0][i])
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            for i in range(tailCnt):
                newByteArr.append(tailList[1][i])

            for i in range(tailCnt):
                lensInfo = tailList[2][i]
                for j in range(len(lensInfo)):
                    if j in [0, 1]:
                        strHex = self.encObj.convertByteArray(lensInfo[j])
                        newByteArr.append(len(strHex))
                        newByteArr.extend(strHex)
                    elif j in [2, 3]:
                        tempF = struct.pack("<f", lensInfo[j])
                        newByteArr.extend(tempF)
                    elif j == 4:
                        bList = lensInfo[j]
                        for k in range(len(bList)):
                            newByteArr.append(bList[k])

            index = self.tailEndIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])

            self.byteArr = newByteArr
            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTrain(self):
        w = open(self.filePath, "wb")
        w.write(self.byteArr)
        w.close()
