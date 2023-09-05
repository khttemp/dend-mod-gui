import struct
import traceback
import codecs
import program.textSetting as textSetting

BSTrainName = [
    "H2000",
    "K8000",
    "H8200",
    "UV21000",
    "H8008",
    "K2199",
    "K21XX",
    "H7001",
    "K800",
    "JR223",
]

perfName = [
    "None_Tlk",
    "add",
    "UpHill",
    "DownHill",
    "Weight",
    "First_break",
    "Second_Breake" + textSetting.textList["orgInfoEditor"]["noUsed"],
    "SpBreake",
    "CompPower",
    "D_Speed" + textSetting.textList["orgInfoEditor"]["noUsed"],
    "One_Speed",
    "OutParam",
    "D_Add",
    "D_Add2",
    "D_AddFrame" + textSetting.textList["orgInfoEditor"]["noUsed"],
    "Carbe" + textSetting.textList["orgInfoEditor"]["noUsed"],
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


class BSdecrypt():
    def __init__(self, filePath):
        self.filePath = filePath
        self.trainNameList = BSTrainName
        self.trainPerfNameList = perfName
        self.trainHurikoNameList = hurikoName
        self.trainInfoList = []
        self.indexList = []
        self.mdlIndexList = []
        self.henseiIndexList = []
        self.henseiModelEndIndexList = []
        self.henseiStartIndexList = []
        self.henseiEndIndexList = []
        self.else2IndexList = []
        self.lensIndexList = []
        self.tailIndexList = []
        self.tailEndIndexList = []
        self.colorMapEndIndexList = []
        self.csvReadInfo = {}
        self.byteArr = []
        self.error = ""
        self.trainModelList = []
        self.colorIdx = -1
        self.stageIdx = -1
        self.stageList = []
        self.stageEditIdx = 0
        self.stageCnt = 6
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
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(self.error)
        w.close()

    def decrypt(self, line):
        self.trainInfoList = []
        self.indexList = []
        self.mdlIndexList = []
        self.henseiIndexList = []
        self.henseiModelEndIndexList = []
        self.henseiStartIndexList = []
        self.henseiEndIndexList = []
        self.else2IndexList = []
        self.lensIndexList = []
        self.tailIndexList = []
        self.tailEndIndexList = []
        self.colorMapEndIndexList = []
        self.csvReadInfo = {}
        self.error = ""
        self.trainModelList = []
        self.stageList = []

        index = 0
        trainCnt = line[index]
        index += 1

        for i in range(trainCnt):
            trainNameCnt = line[index]
            index += 1
            # trainName
            line[index:index + trainNameCnt].decode("shift-jis")
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
                "colorMapList": []
            }

            daishaCnt = line[index]
            train["daishaCnt"] = daishaCnt
            index += 1

            daishaModelNameCnt = line[index]
            index += 1
            daishaModelName = line[index:index + daishaModelNameCnt].decode("shift-jis")
            train["trackNames"].append(daishaModelName)
            index += daishaModelNameCnt

            self.henseiIndexList.append(index)

            henseiCnt = line[index]
            train["mdlCnt"] = henseiCnt
            index += 1

            modelCnt = line[index]
            index += 1
            for j in range(modelCnt):
                modelNameCnt = line[index]
                index += 1
                modelName = line[index:index + modelNameCnt].decode("shift-jis")
                train["mdlNames"].append(modelName)
                index += modelNameCnt

            train["mdlNames"].append(textSetting.textList["orgInfoEditor"]["noList"])

            for j in range(modelCnt):
                colNameCnt = line[index]
                index += 1
                colName = line[index:index + colNameCnt].decode("shift-jis")
                train["colNames"].append(colName)
                index += colNameCnt

            train["colNames"].append(textSetting.textList["orgInfoEditor"]["noList"])

            pantaModelCnt = line[index]
            index += 1

            if pantaModelCnt > 0:
                for j in range(pantaModelCnt):
                    pantaModelNameCnt = line[index]
                    index += 1
                    pantaModelName = line[index:index + pantaModelNameCnt].decode("shift-jis")
                    train["pantaNames"].append(pantaModelName)
                    index += pantaModelNameCnt

                train["pantaNames"].append(textSetting.textList["orgInfoEditor"]["noList"])

            self.henseiModelEndIndexList.append(index)

            self.henseiStartIndexList.append(index)
            # mdlList
            for j in range(henseiCnt):
                idx = line[index]
                if idx == 0xFF:
                    train["mdlList"].append(-1)
                else:
                    train["mdlList"].append(idx)
                index += 1

            if pantaModelCnt > 0:
                for j in range(henseiCnt):
                    idx = line[index]
                    if idx == 0xFF:
                        train["pantaList"].append(-1)
                    else:
                        train["pantaList"].append(idx)
                    index += 1

            self.henseiEndIndexList.append(index)

            for j in range(5):
                b = line[index]
                index += 1
                train["else2Model"].append(line[index:index + b].decode("shift-jis"))
                index += b

            self.else2IndexList.append(index)
            elseList2 = []
            for j in range(2):
                seFileCnt = line[index]
                index += 1
                seLen = line[index]
                index += 1
                seFileName = line[index:index + seLen].decode("shift-jis")
                index += seLen
                elseList2.append([seFileCnt, seFileName])

            train["elseList2"] = elseList2

            self.lensIndexList.append(index)

            lensCnt = line[index]
            index += 1
            for j in range(lensCnt):
                lensList = []
                b = line[index]
                index += 1
                lensName = line[index:index + b].decode("shift-jis")
                lensList.append(lensName)
                index += b

                b = line[index]
                index += 1
                lensName = line[index:index + b].decode("shift-jis")
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
                tailSmfName = line[index:index + b].decode("shift-jis")
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
                lensName = line[index:index + b].decode("shift-jis")
                lensList.append(lensName)
                index += b

                b = line[index]
                index += 1
                lensName = line[index:index + b].decode("shift-jis")
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

            for j in range(modelCnt):
                index += 1

            # カラー設定は設定しているモデルに依存
            colorCnt = line[index]
            train["colorCnt"] = colorCnt
            index += 1
            for color in range(colorCnt):
                modelList = []
                for model in range(modelCnt):
                    colorList = []
                    cnt = line[index]
                    index += 1
                    for j in range(cnt):
                        mapList = []
                        mapList.append(line[index])
                        index += 1
                        mapList.append(line[index])
                        index += 1
                        txtLen = line[index]
                        index += 1
                        txt = line[index:index + txtLen].decode("shift-jis")
                        mapList.append(txt)
                        index += txtLen
                        colorList.append(mapList)
                    modelList.append(colorList)
                train["colorMapList"].append(modelList)

            self.trainModelList.append(train)
            self.colorMapEndIndexList.append(index)
        self.stageIdx = index

        stageCnt = line[index]
        index += 1
        for i in range(stageCnt):
            stageNum = line[index]
            index += 1
            train_1pIdx = line[index]
            if train_1pIdx == 0xFF:
                train_1pIdx = -1
            index += 1
            train_2pIdx = line[index]
            if train_2pIdx == 0xFF:
                train_2pIdx = -1
            index += 1
            train_3pIdx = line[index]
            if train_3pIdx == 0xFF:
                train_3pIdx = -1
            index += 1
            self.stageList.append([stageNum, train_1pIdx, train_2pIdx, train_3pIdx])

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

            # mdlList
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

            # pantaList
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

            for i in range(cnt):
                idx = trainWidget.comboList[2 * i].current()
                if idx == len(trainWidget.comboList[2 * i]["values"]) - 1:
                    idx = 255
                newByteArr.append(idx)
                index += 1

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

    def saveModelInfo(self, trainIdx, modelInfo):
        try:
            index = self.mdlIndexList[trainIdx]
            newByteArr = self.byteArr[0:index]

            newTrackList = modelInfo["trackNames"]

            newByteArr.append(len(newTrackList))
            for newTrack in newTrackList:
                newByteArr.append(len(newTrack))
                newByteArr.extend(newTrack.encode("shift-jis"))

            newCnt = modelInfo["mdlCnt"]
            newByteArr.append(newCnt)

            newMdlList = modelInfo["mdlNames"]
            newByteArr.append(len(newMdlList) - 1)
            for newMdl in newMdlList:
                if newMdl == textSetting.textList["orgInfoEditor"]["noList"]:
                    continue
                newByteArr.append(len(newMdl))
                newByteArr.extend(newMdl.encode("shift-jis"))

            for i in range(len(newMdlList) - 1):
                strHex = "H2000_COL_0.smf"
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex.encode("shift-jis"))

            newPantaList = modelInfo["pantaNames"]
            newByteArr.append(len(newPantaList) - 1)
            for newPanta in newPantaList:
                if newPanta == textSetting.textList["orgInfoEditor"]["noList"]:
                    continue
                newByteArr.append(len(newPanta))
                newByteArr.extend(newPanta.encode("shift-jis"))

            index = self.henseiModelEndIndexList[trainIdx]
            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElseList(self, trainIdx, ver, elseList):
        try:
            if ver == 2:
                index = self.henseiEndIndexList[trainIdx]
                newByteArr = self.byteArr[0:index]

                for i in range(5):
                    strHex = elseList[i].encode("shift-jis")
                    newByteArr.append(len(strHex))
                    newByteArr.extend(strHex)
                index = self.else2IndexList[trainIdx]

                newByteArr.extend(self.byteArr[index:])
                self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse2List(self, trainIdx, elseList):
        try:
            index = self.else2IndexList[trainIdx]

            newByteArr = self.byteArr[0:index]

            for i in range(len(elseList)):
                elseInfo = elseList[i]
                num = elseInfo[0]
                newByteArr.append(num)

                strHex = elseInfo[1].encode("shift-jis")
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
                    strHex = "lensflear00.tga".encode("shift-jis")
                    newByteArr.append(len(strHex))
                    newByteArr.extend(strHex)
                    strHex = "lensflear01.tga".encode("shift-jis")
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
                        strHex = valInfo[j].encode("shift-jis")
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
                    strHex = ".smf".encode("shift-jis")
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
                    strHex = "lensflear00.tga".encode("shift-jis")
                    newByteArr.insert(index, len(strHex))
                    index += 1
                    for s in strHex:
                        newByteArr.insert(index, s)
                        index += 1

                    strHex = "lensflear01.tga".encode("shift-jis")
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
                strHex = valInfo.encode("shift-jis")
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
                        strHex = valInfo[j].encode("shift-jis")
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

    def saveStageInfo(self, stageList):
        try:
            index = self.stageIdx
            stageAllCnt = self.byteArr[index]
            index += 1

            for i in range(stageAllCnt):
                index += 1

                if stageList[i][1] == -1:
                    self.byteArr[index] = 0xFF
                else:
                    self.byteArr[index] = stageList[i][1]
                index += 1

                if stageList[i][2] == -1:
                    self.byteArr[index] = 0xFF
                else:
                    self.byteArr[index] = stageList[i][2]
                index += 1

                if stageList[i][3] == -1:
                    self.byteArr[index] = 0xFF
                else:
                    self.byteArr[index] = stageList[i][3]
                index += 1

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
            w = codecs.open(filePath, "w", "utf-8-sig", "ignore")
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
            w.write("{0}\n".format(textSetting.textList["orgInfoEditor"]["csvDaishaTitle"]))
            w.write(",".join(train["trackNames"]))
            w.write("\n")

            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvOrgNumTitle"], train["mdlCnt"]))

            mdlCnt = len(train["mdlNames"][:-1])
            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvMdlTitle"], mdlCnt))
            w.write(",".join(train["mdlNames"][:-1]))
            w.write("\n")

            w.write("{0},".format(textSetting.textList["orgInfoEditor"]["csvMdlIdxTitle"]))
            w.write(",".join([str(x) for x in train["mdlList"]]))
            w.write("\n")

            w.write("{0}:{1}\n".format(textSetting.textList["orgInfoEditor"]["csvPantaTitle"], len(train["pantaNames"][:-1])))
            w.write(",".join(train["pantaNames"][:-1]))
            w.write("\n")

            w.write("{0},".format(textSetting.textList["orgInfoEditor"]["csvPantaIdxTitle"]))
            w.write(",".join([str(x) for x in train["pantaList"]]))
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

            index = self.tailEndIndexList[trainIdx]
            w.write("{0},".format(textSetting.textList["orgInfoEditor"]["csvModelIdx2Title"]))
            for i in range(mdlCnt):
                w.write("{0},".format(self.byteArr[index]))
                index += 1
            w.write("\n")

            w.write("{0},{1}\n".format(textSetting.textList["orgInfoEditor"]["colorCnt"], train["colorCnt"]))

            colorMapList = train["colorMapList"]
            cIdx = 1
            for colorMap in colorMapList:

                mIdx = 1
                for modelList in colorMap:
                    w.write(textSetting.textList["orgInfoEditor"]["csvColorIdx"].format(cIdx))
                    w.write(textSetting.textList["orgInfoEditor"]["csvModelIdx"].format(mIdx, len(modelList)))
                    for model in modelList:
                        w.write(",".join([str(x) for x in model]))
                        w.write("\n")
                    mIdx += 1
                cIdx += 1
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
            if notchCnt not in [4, 5]:
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

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["csvDaishaTitle"]:
                self.error = textSetting.textList["errorList"]["E27"]
                return False
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
            if orgCnt < 2:
                self.error = textSetting.textList["errorList"]["E40"]
                return False
            cnt += 1
            self.csvReadInfo["orgCnt"] = orgCnt

            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["csvMdlTitle"]:
                self.error = textSetting.textList["errorList"]["E30"]
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            mdlCnt = int(arr.split(",")[0])
            cnt += 1

            mdlNameList = []
            arr = csvLines[cnt].strip().split(",")
            for i in range(mdlCnt):
                mdlNameList.append(arr[i])
            cnt += 1
            self.csvReadInfo["mdlNameList"] = mdlNameList

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["csvMdlIdxTitle"]:
                self.error = textSetting.textList["errorList"]["E41"]
                return False

            mdlList = []
            arr = csvLines[cnt].strip().split(",")[1:]
            for i in range(orgCnt):
                try:
                    idx = int(arr[i])
                    if idx < -1 or idx >= mdlCnt:
                        self.error = textSetting.textList["errorList"]["E42"]
                        return False
                except Exception:
                    self.error = textSetting.textList["errorList"]["E43"]
                    return False
                mdlList.append(idx)
            cnt += 1
            self.csvReadInfo["mdlList"] = mdlList

            if csvLines[cnt].strip().split(":")[0] != textSetting.textList["orgInfoEditor"]["csvPantaTitle"]:
                self.error = textSetting.textList["errorList"]["E32"]
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            pantaCnt = int(arr.split(",")[0])
            cnt += 1

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
            arr = csvLines[cnt].strip().split(",")
            for i in range(tailCnt):
                tailSmfNameList.append(arr[i])
            cnt += 1
            tailList.append(tailSmfNameList)

            tailElseList = []
            arr = csvLines[cnt].strip().split(",")
            for i in range(tailCnt):
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

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["csvModelIdx2Title"]:
                self.error = textSetting.textList["errorList"]["E44"]
                return False

            mdlIdxList2 = []
            arr = csvLines[cnt].strip().split(",")[1:]
            for i in range(mdlCnt):
                mdlIdxList2.append(int(arr[i]))

            self.csvReadInfo["mdlIdxList2"] = mdlIdxList2
            cnt += 1

            if csvLines[cnt].strip().split(",")[0] != textSetting.textList["orgInfoEditor"]["colorCnt"]:
                self.error = textSetting.textList["errorList"]["E45"]
                return False

            arr = csvLines[cnt].strip().split(",")[1:]
            colorCnt = int(arr[0])
            self.csvReadInfo["colorCnt"] = colorCnt
            cnt += 1

            self.csvReadInfo["colorMapList"] = []
            for color in range(colorCnt):
                modelMap = []
                for model in range(mdlCnt):
                    arr = csvLines[cnt].strip().split(",")
                    strArr = ",".join(arr[0:2])
                    if strArr != textSetting.textList["orgInfoEditor"]["csvColorModelIdx"].format(color + 1, model + 1):
                        self.error = textSetting.textList["errorList"]["E46"]
                        return False

                    readCnt = int(arr[2])
                    cnt += 1

                    modelList = []
                    for i in range(readCnt):
                        modelInfo = []
                        arr = csvLines[cnt].strip().split(",")
                        modelInfo.append(int(arr[0]))
                        modelInfo.append(int(arr[1]))
                        modelInfo.append(arr[2])
                        modelList.append(modelInfo)
                        cnt += 1
                    modelMap.append(modelList)
                self.csvReadInfo["colorMapList"].append(modelMap)

            return True
        except Exception:
            self.error = textSetting.textList["errorList"]["E39"].format(cnt + 1)
            return False

    def saveCsvTrainInfo(self, trainIdx):
        try:
            index = self.indexList[trainIdx]
            newByteArr = self.byteArr[0:index]
            train = self.trainModelList[trainIdx]

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

            daishaCnt = train["daishaCnt"]
            newByteArr.append(daishaCnt)

            trackInfo = self.csvReadInfo["trackInfo"]
            for i in range(len(trackInfo)):
                strHex = trackInfo[i].encode("shift-jis")
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            orgCnt = self.csvReadInfo["orgCnt"]
            newByteArr.append(orgCnt)

            mdlNameList = self.csvReadInfo["mdlNameList"]
            newByteArr.append(len(mdlNameList))
            for i in range(len(mdlNameList)):
                strHex = mdlNameList[i].encode("shift-jis")
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            for i in range(len(mdlNameList)):
                strHex = "H2000_COL_0.smf".encode("shift-jis")
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            pantaNameList = self.csvReadInfo["pantaNameList"]
            newByteArr.append(len(pantaNameList))
            for i in range(len(pantaNameList)):
                strHex = pantaNameList[i].encode("shift-jis")
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            mdlList = self.csvReadInfo["mdlList"]
            for i in range(len(mdlList)):
                if mdlList[i] == -1:
                    newByteArr.append(0xFF)
                else:
                    newByteArr.append(mdlList[i])

            pantaList = self.csvReadInfo["pantaList"]
            for i in range(len(mdlList)):
                if pantaList[i] == -1:
                    newByteArr.append(0xFF)
                else:
                    newByteArr.append(pantaList[i])

            startIdx = self.henseiEndIndexList[trainIdx]
            index = self.lensIndexList[trainIdx]
            newByteArr.extend(self.byteArr[startIdx:index])

            lensList = self.csvReadInfo["lensList"]
            newByteArr.append(len(lensList))
            for i in range(len(lensList)):
                lensInfo = lensList[i]
                for j in range(len(lensInfo)):
                    if j in [0, 1]:
                        strHex = lensInfo[j].encode("shift-jis")
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
                strHex = tailList[0][i].encode("shift-jis")
                newByteArr.append(len(strHex))
                newByteArr.extend(strHex)

            for i in range(tailCnt):
                newByteArr.append(tailList[1][i])

            for i in range(tailCnt):
                lensInfo = tailList[2][i]
                for j in range(len(lensInfo)):
                    if j in [0, 1]:
                        strHex = lensInfo[j].encode("shift-jis")
                        newByteArr.append(len(strHex))
                        newByteArr.extend(strHex)
                    elif j in [2, 3]:
                        tempF = struct.pack("<f", lensInfo[j])
                        newByteArr.extend(tempF)
                    elif j == 4:
                        bList = lensInfo[j]
                        for k in range(len(bList)):
                            newByteArr.append(bList[k])

            mdlIdxList2 = self.csvReadInfo["mdlIdxList2"]
            for i in range(len(mdlIdxList2)):
                newByteArr.append(mdlIdxList2[i])

            colorCnt = self.csvReadInfo["colorCnt"]
            newByteArr.append(colorCnt)

            colorMapList = self.csvReadInfo["colorMapList"]
            for colorList in colorMapList:
                for modelList in colorList:
                    newByteArr.append(len(modelList))
                    for modelInfo in modelList:
                        newByteArr.append(modelInfo[0])
                        newByteArr.append(modelInfo[1])
                        strHex = modelInfo[2].encode("shift-jis")
                        newByteArr.append(len(strHex))
                        newByteArr.extend(strHex)

            index = self.colorMapEndIndexList[trainIdx]
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
