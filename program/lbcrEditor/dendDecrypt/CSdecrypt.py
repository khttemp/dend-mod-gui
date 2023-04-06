import struct
import traceback
import codecs

CSTrainName = [
    "H2000",
    "H2800",
    "H8200",
    "HS9000",
    "KQ21XX",
    "JR2000",
    "Rapit",

    "Old_H2000",
    "Old_H8200",

    "Arban21000R",
    "K800",
    "H7001",
    "K8000",
    "H8000",
    "KQ2199",
    "JR223",
    "H2300",
    "AE86",
    "Deki3",
    "K80"
]

perfName = [
    "None_Tlk",
    "Add_Best",
    "UpHill",
    "DownHill",
    "Weight",
    "First_break",
    "Second_Breake(未使用)",
    "SpBreake",
    "CompPower",
    "D_Speed(未使用)",
    "One_Speed(未使用)",
    "OutParam",
    "D_Add",
    "D_Add2",
    "D_AddFrame(未使用)",
    "Carbe(未使用)",
    "Jump",
    "ChangeFrame",
    "OutRun_Top",
    "OutRun_Other",
    "OutRun_Frame",
    "OutRun_Speed",
    "OutRun_JumpFrame",
    "OutRun_JumpHeight",
    "LightningFullNotch_per",
    "LightningFullNotch_Speed",
    "LightningFullNotch_Frame"
]

hurikoName = [
    "振り子の曲げる段階",
    "振り子の曲げる角度(°)"
]


class CSdecrypt():
    def __init__(self, filePath):
        self.filePath = filePath
        self.trainNameList = CSTrainName
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
        self.csvReadInfo = {}
        self.byteArr = []
        self.error = ""
        self.trainModelList = []
        self.colorIdx = 0
        self.stageIdx = -1
        self.stageList = []
        self.stageEditIdx = 11
        self.stageCnt = 5
        self.notchContentCnt = 4

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
        f = open("error.log", "w")
        f.write(self.error)
        f.close()

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
        self.csvReadInfo = {}
        self.error = ""
        self.trainModelList = []
        self.stageList = []

        index = 0
        trainCnt = line[index]
        index += 1

        for i in range(trainCnt):
            self.indexList.append(index)
            train_speed = []
            notchCnt = line[index]
            index += 1
            for j in range(4):
                if j == 2:
                    for k in range(notchCnt):
                        signedB = struct.unpack("<b", line[index].to_bytes(1, 'big'))[0]
                        train_speed.append(signedB)
                        index += 1
                else:
                    for k in range(notchCnt):
                        speed = struct.unpack("<f", line[index:index + 4])[0]
                        speed = round(speed, 4)
                        train_speed.append(speed)
                        index += 4
            self.trainInfoList.append(train_speed)

            train_perf = []
            for j in range(len(perfName)):
                perf = struct.unpack("<f", line[index:index + 4])[0]
                perf = round(perf, 5)
                train_perf.append(perf)
                index += 4
            self.trainInfoList.append(train_perf)

            train_huriko = []
            for j in range(2):
                signedB = struct.unpack("<b", line[index].to_bytes(1, 'big'))[0]
                train_huriko.append(signedB)
                index += 1
            self.trainInfoList.append(train_huriko)

            self.mdlIndexList.append(index)

            train = {
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
                "tailList": []
            }

            smfTrackCnt = line[index]
            index += 1
            for j in range(smfTrackCnt):
                b = line[index]
                index += 1
                train["trackNames"].append(line[index:index + b].decode("shift-jis"))
                index += b

            self.henseiIndexList.append(index)

            mdlCnt = line[index]
            train["mdlCnt"] = mdlCnt
            index += 1

            mdlSmfCnt = line[index]
            index += 1
            for j in range(mdlSmfCnt):
                b = line[index]
                index += 1
                train["mdlNames"].append(line[index:index + b].decode("shift-jis"))
                index += b

            train["mdlNames"].append("なし")

            for j in range(mdlSmfCnt):
                b = line[index]
                index += 1
                train["colNames"].append(line[index:index + b].decode("shift-jis"))
                index += b

            train["colNames"].append("なし")

            pantaCnt = line[index]
            index += 1
            for j in range(pantaCnt):
                b = line[index]
                index += 1
                train["pantaNames"].append(line[index:index + b].decode("shift-jis"))
                index += b

            train["pantaNames"].append("なし")

            self.henseiModelEndIndexList.append(index)

            for j in range(4):
                b = line[index]
                index += 1
                train["elseModel"].append(line[index:index + b].decode("shift-jis"))
                index += b

            self.henseiStartIndexList.append(index)
            # mdlList
            for j in range(mdlCnt):
                if line[index] == 0xFF:
                    train["mdlList"].append(-1)
                else:
                    train["mdlList"].append(line[index])
                index += 1
            # pantaList
            for j in range(mdlCnt):
                if line[index] == 0xFF:
                    train["pantaList"].append(-1)
                else:
                    train["pantaList"].append(line[index])
                index += 1

            self.henseiEndIndexList.append(index)

            for j in range(5):
                b = line[index]
                index += 1
                train["else2Model"].append(line[index:index + b].decode("shift-jis"))
                index += b

            self.else2IndexList.append(index)
            elseList2 = []
            cnta = line[index]
            index += 1
            b = line[index]
            index += 1
            name = line[index:index + b].decode("shift-jis")
            index += b
            elseList2.append([cnta, name])

            cntb = line[index]
            index += 1
            b = line[index]
            index += 1
            name = line[index:index + b].decode("shift-jis")
            index += b
            elseList2.append([cntb, name])

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

            self.trainModelList.append(train)

        self.colorIdx = index
        for i in range(trainCnt):
            if i == len(CSTrainName):
                # trainName = "S300"
                pass
            elif i == len(CSTrainName) + 1:
                # trainName = "Yokohama"
                pass
            elif i == len(CSTrainName) + 2:
                # trainName = "S500"
                pass
            else:
                # trainName = CSTrainName[i]
                self.trainModelList[i]["colorCnt"] = line[index]
            index += 1
        self.stageIdx = index

        stageCnt = line[index]
        index += 1
        for i in range(stageCnt):
            stageNum = struct.unpack("<h", line[index:index + 2])[0]
            index += 2
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
            daishaIdx = line[index]
            index += 1
            self.stageList.append([stageNum, train_1pIdx, train_2pIdx, train_3pIdx, daishaIdx])

    def saveNotchInfo(self, trainIdx, newNotchNum):
        try:
            newByteArr = bytearray()
            index = self.indexList[trainIdx]
            speed = self.trainInfoList[3 * trainIdx]
            notchContentCnt = 4
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
                if i >= 2 * newNotchNum and i < 3 * newNotchNum:
                    byteB = struct.pack("<b", newSpeed[i])
                    newByteArr.extend(byteB)
                else:
                    byteF = struct.pack("<f", newSpeed[i])
                    newByteArr.extend(byteF)

            for i in range(len(speed)):
                if i >= 2 * oldNotchNum and i < 3 * oldNotchNum:
                    index += 1
                else:
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
            newByteArr = bytearray()

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

            for i in range(notchCnt):
                sound = struct.pack("<b", varList[self.notchContentCnt * i + 2].get())
                newByteArr.extend(sound)

            for i in range(notchCnt):
                add = struct.pack("<f", varList[self.notchContentCnt * i + 3].get())
                newByteArr.extend(add)

            perfCnt = len(self.trainPerfNameList)
            for i in range(perfCnt):
                perf = struct.pack("<f", varList[notchCnt * self.notchContentCnt + i].get())
                newByteArr.extend(perf)

            for i in range(2):
                huriko = struct.pack("<b", varList[notchCnt * self.notchContentCnt + perfCnt + i].get())
                newByteArr.extend(huriko)

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

    def saveColor(self, trainIdx, num):
        try:
            index = self.colorIdx + trainIdx
            self.byteArr[index] = num

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
                if newMdl == "なし":
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
                if newPanta == "なし":
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
            if ver == 1:
                index = self.henseiModelEndIndexList[trainIdx]
                newByteArr = self.byteArr[0:index]

                for i in range(4):
                    strHex = elseList[i].encode("shift-jis")
                    newByteArr.append(len(strHex))
                    newByteArr.extend(strHex)
                index = self.henseiStartIndexList[trainIdx]

                newByteArr.extend(self.byteArr[index:])
                self.byteArr = newByteArr
            elif ver == 2:
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
                index += 2

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

                self.byteArr[index] = stageList[i][4]
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
                # sound
                for i in range(notchCnt):
                    idx += 1
                # add
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
        srcHuriko = srcList[4]
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
            for i in range(len(srcHuriko)):
                srcHuriko[i] = distData["huriko"][i]

            for i in range(4):
                if i == 0:
                    data = distData["notch"]
                elif i == 1:
                    data = distData["tlk"]
                elif i == 2:
                    data = distData["soundNum"]
                elif i == 3:
                    data = distData["add"]

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

            for i in range(srcNotchNum):
                if notchCheckStatus:
                    sound = struct.pack("<b", srcSpeed[2 * srcNotchNum + i])
                    for n in sound:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 1

            for i in range(srcNotchNum):
                if notchCheckStatus:
                    add = struct.pack("<f", srcSpeed[3 * srcNotchNum + i])
                    for n in add:
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

            for i in range(2):
                if perfCheckStatus:
                    huriko = struct.pack("<b", srcHuriko[i])
                    for n in huriko:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 1
            self.saveTrain()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def extractCsvTrainInfo(self, trainIdx, filePath):
        try:
            w = codecs.open(filePath, "w", "utf-8-sig", "ignore")
            speedList = self.trainInfoList[3 * trainIdx]
            index = self.indexList[trainIdx]
            notchCnt = self.byteArr[index]

            w.write("ノッチ:{0}\n".format(notchCnt))
            w.write("speed,tlk,sound,add\n")

            for i in range(notchCnt):
                for j in range(self.notchContentCnt):
                    w.write("{0}".format(speedList[i + notchCnt * j]))
                    if j == self.notchContentCnt - 1:
                        w.write("\n")
                    else:
                        w.write(",")
            w.write("性能\n")

            perfList = self.trainInfoList[3 * trainIdx + 1]
            perfNameList = self.trainPerfNameList
            for i in range(len(perfList)):
                w.write("{0},{1}\n".format(perfNameList[i], perfList[i]))

            hurikoList = self.trainInfoList[3 * trainIdx + 2]
            hurikoNameList = self.trainHurikoNameList

            for i in range(len(hurikoList)):
                w.write("{0},{1}\n".format(hurikoNameList[i], hurikoList[i]))

            train = self.trainModelList[trainIdx]
            w.write("台車モデル:{0}\n".format(len(train["trackNames"])))
            w.write(",".join(train["trackNames"]))
            w.write("\n")

            w.write("編成数:{0}\n".format(train["mdlCnt"]))

            w.write("車両モデル:{0}\n".format(len(train["mdlNames"][:-1])))
            w.write(",".join(train["mdlNames"][:-1]))
            w.write("\n")

            w.write("車両index,")
            w.write(",".join([str(x) for x in train["mdlList"]]))
            w.write("\n")

            w.write("パンタモデル:{0}\n".format(len(train["pantaNames"][:-1])))
            w.write(",".join(train["pantaNames"][:-1]))
            w.write("\n")

            w.write("パンタindex,")
            w.write(",".join([str(x) for x in train["pantaList"]]))
            w.write("\n")

            w.write("レンズフレア:{0}\n".format(len(train["lensList"])))
            for i in range(len(train["lensList"])):
                lensInfo = train["lensList"][i]
                w.write("{0},{1}\n".format(lensInfo[0], lensInfo[1]))
                w.write("{0},{1}\n".format(lensInfo[2], lensInfo[3]))
                w.write(",".join([str(x) for x in lensInfo[4]]))
                w.write("\n")

            tailCnt = len(train["tailList"][0])
            w.write("テールランプ:{0}\n".format(tailCnt))
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
            if csvLines[cnt].strip().split(":")[0] != "ノッチ":
                self.error = "ノッチ情報を探せません"
                return False

            arr = csvLines[cnt].strip().split(":")[1]

            notchCnt = int(arr.split(",")[0])
            if notchCnt not in [4, 5, 12]:
                self.error = "{0}ノッチは非対応です".format(notchCnt)
                return False
            self.csvReadInfo["notchCnt"] = notchCnt
            cnt += 1

            arr = csvLines[cnt].strip().split(",")[0:4]
            header = ",".join(arr)
            if header != "speed,tlk,sound,add":
                self.error = "ノッチのヘッダーがありません"
                return False
            cnt += 1

            speed = []
            tlk = []
            sound = []
            add = []
            try:
                for i in range(notchCnt):
                    arr = csvLines[cnt].strip().split(",")
                    speed.append(float(arr[0]))
                    tlk.append(float(arr[1]))
                    sound.append(int(arr[2]))
                    add.append(float(arr[3]))
                    cnt += 1
            except Exception:
                self.error = "{0}ノッチ読み込み中\n{1}ノッチ情報読み込み失敗".format(notchCnt, i + 1)
                return False
            speed.extend(tlk)
            speed.extend(sound)
            speed.extend(add)
            self.csvReadInfo["speed"] = speed

            if csvLines[cnt].strip().split(",")[0] != "性能":
                self.error = "性能情報を探せません"
                return False
            cnt += 1

            perf = []
            for i in range(len(self.trainPerfNameList)):
                arr = csvLines[cnt].strip().split(",")
                perf.append(float(arr[1]))
                cnt += 1
            self.csvReadInfo["perf"] = perf

            huriko = []
            for i in range(len(self.trainHurikoNameList)):
                arr = csvLines[cnt].strip().split(",")
                huriko.append(int(arr[1]))
                cnt += 1
            self.csvReadInfo["huriko"] = huriko

            if csvLines[cnt].strip().split(":")[0] != "台車モデル":
                self.error = "台車モデル情報を探せません"
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            trackCnt = int(arr.split(",")[0])
            if trackCnt < 2:
                self.error = "台車モデルの数が2個より少ないです"
                return False
            cnt += 1

            trackInfo = []
            arr = csvLines[cnt].strip().split(",")
            for i in range(trackCnt):
                trackInfo.append(arr[i])
            cnt += 1
            self.csvReadInfo["trackInfo"] = trackInfo

            if csvLines[cnt].strip().split(":")[0] != "編成数":
                self.error = "編成数情報を探せません"
                return False

            arr = csvLines[cnt].strip().split(":")[1]
            orgCnt = int(arr.split(",")[0])
            if orgCnt < 2:
                self.error = "編成数が2個より少ないです"
                return False
            cnt += 1
            self.csvReadInfo["orgCnt"] = orgCnt

            if csvLines[cnt].strip().split(":")[0] != "車両モデル":
                self.error = "車両モデル情報を探せません"
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

            if csvLines[cnt].strip().split(",")[0] != "車両index":
                self.error = "車両index情報を探せません"
                return False

            mdlList = []
            arr = csvLines[cnt].strip().split(",")[1:]
            for i in range(orgCnt):
                try:
                    idx = int(arr[i])
                    if idx < -1 or idx >= mdlCnt:
                        self.error = "車両index情報が不正です"
                        return False
                except Exception:
                    self.error = "車両index情報 読み込み失敗"
                    return False
                mdlList.append(idx)
            cnt += 1
            self.csvReadInfo["mdlList"] = mdlList

            if csvLines[cnt].strip().split(":")[0] != "パンタモデル":
                self.error = "パンタモデル情報を探せません"
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

            if csvLines[cnt].strip().split(",")[0] != "パンタindex":
                self.error = "パンタindex情報を探せません"
                return False

            pantaList = []
            arr = csvLines[cnt].strip().split(",")[1:]
            for i in range(orgCnt):
                try:
                    idx = int(arr[i])
                    if idx < -1 or idx >= pantaCnt:
                        self.error = "パンタindex情報が不正です"
                        return False
                except Exception:
                    self.error = "パンタindex情報 読み込み失敗"
                    return False
                pantaList.append(idx)
            cnt += 1
            self.csvReadInfo["pantaList"] = pantaList

            if csvLines[cnt].strip().split(":")[0] != "レンズフレア":
                self.error = "レンズフレア情報を探せません"
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

            if csvLines[cnt].strip().split(":")[0] != "テールランプ":
                self.error = "テールランプ情報を探せません"
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

            return True
        except Exception:
            self.error = "{0}行目の読み込み失敗".format(cnt + 1)
            return False

    def saveCsvTrainInfo(self, trainIdx):
        try:
            index = self.indexList[trainIdx]
            newByteArr = self.byteArr[0:index]

            notchCnt = self.csvReadInfo["notchCnt"]
            newByteArr.append(notchCnt)

            speed = self.csvReadInfo["speed"]
            for i in range(4):
                for j in range(notchCnt):
                    if i == 2:
                        b = struct.pack("<b", speed[i * notchCnt + j])
                        newByteArr.extend(b)
                    else:
                        f = struct.pack("<f", speed[i * notchCnt + j])
                        newByteArr.extend(f)

            perf = self.csvReadInfo["perf"]
            for i in range(len(perf)):
                f = struct.pack("<f", perf[i])
                newByteArr.extend(f)

            huriko = self.csvReadInfo["huriko"]
            for i in range(len(huriko)):
                b = struct.pack("<b", huriko[i])
                newByteArr.extend(b)

            trackInfo = self.csvReadInfo["trackInfo"]
            newByteArr.append(len(trackInfo))
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

            train = self.trainModelList[trainIdx]
            elseModel = train["elseModel"]

            for i in range(4):
                strHex = elseModel[i].encode("shift-jis")
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
