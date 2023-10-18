import copy
import codecs
import UnityPy
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

notchCntLineName = "Cnt:"
perfLineName = "TlkData:"
rainLineName = "RainData:"
carbLineName = "CarbData:"
otherLineName = "OtherData:"
hurikoLineName = "HurikoData:"
oneWheelLineName = "OneWheelPow:"

perfName = [
    "None_Tlk",
    "Add_Best",
    "UpHill",
    "DownHill",
    "Weight",
    "CompPower",
    "First_break",
    "Second_Breake",
    "SpBreake",
    "D_Speed" + textSetting.textList["orgInfoEditor"]["noUsed"],
    "One_Speed" + textSetting.textList["orgInfoEditor"]["noUsed"],
    "OutParam",
    "D_Add",
    "D_Add2",
    "D_AddFrame" + textSetting.textList["orgInfoEditor"]["noUsed"],
    "Carbe",
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
    "LightningFullNotch_Frame",
    "D_Add_OneWheele",
    "D_Add_MaxOneWheele",
    "D_Add_OneWheeleTime",
]

rainName = [
    textSetting.textList["orgInfoEditor"]["rainAdd"],
    textSetting.textList["orgInfoEditor"]["rainBreake"],
    textSetting.textList["orgInfoEditor"]["rainHill"],
    textSetting.textList["orgInfoEditor"]["rainDown"],
]

carbName = [
    textSetting.textList["orgInfoEditor"]["trackOutPer"],
    textSetting.textList["orgInfoEditor"]["trackKntPer"],
    textSetting.textList["orgInfoEditor"]["breakeOutPow"],
    textSetting.textList["orgInfoEditor"]["maxOutParam"],
]

otherName = [
    textSetting.textList["orgInfoEditor"]["hurikoCntSS"],
    textSetting.textList["orgInfoEditor"]["hurikoAngleSS"],
    textSetting.textList["orgInfoEditor"]["trackCnt"],
    textSetting.textList["orgInfoEditor"]["readTrackNum"] + textSetting.textList["orgInfoEditor"]["noUsed"],
    textSetting.textList["orgInfoEditor"]["trackName"],
    textSetting.textList["orgInfoEditor"]["trackMdlName"],
    textSetting.textList["orgInfoEditor"]["lowTrackMdlName"],
]

hurikoName = [
    textSetting.textList["orgInfoEditor"]["hurikoPow"],
]

oneWheelName = [
    textSetting.textList["orgInfoEditor"]["oneWheelPow"],
    textSetting.textList["orgInfoEditor"]["oneWheelTime"],
    textSetting.textList["orgInfoEditor"]["oneWheelAfterTime"],
]


class SSdecrypt:
    def __init__(self, filePath):
        self.filePath = filePath
        self.trainNameList = SSTrainName
        self.trainPerfNameList = perfName
        self.trainRainNameList = rainName
        self.trainCarbNameList = carbName
        self.trainOtherNameList = otherName
        self.trainHurikoNameList = hurikoName
        self.trainOneWheelNameList = oneWheelName
        self.trainInfoList = []
        self.notchContentCnt = 4
        self.env = None
        self.allList = {}
        self.dataList = {}
        self.error = ""

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
            self.trainInfoList = []
            self.allList = {}
            self.dataList = {}
            for env in self.env.objects:
                if env.type.name != "AssetBundle":
                    data = env.read()
                    name = data.name
                    if name not in SSTrainName:
                        self.error = textSetting.textList["errorList"]["E51"].format(name)
                        return False
                    self.dataList[name] = data
                    self.allList[name] = data.script.tobytes().decode("utf-8").split("\n")
            for name in SSTrainName:
                lines = self.allList[name]
                resultList = self.decryptLines(lines)
                self.trainInfoList.append(resultList)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def decryptLines(self, lines):
        trainOrgInfo = []
        index = self.findLines(lines, notchCntLineName)
        if index == -1:
            self.error = textSetting.textList["errorList"]["E52"].format(notchCntLineName)
            return None
        try:
            trainSpeedInfo = []
            notchInfoList = [x.strip() for x in lines[index].strip().split("\t") if not x.strip() == ""]
            notchCnt = int(notchInfoList[1])
            index += 1
            for i in range(4):
                speedText = lines[index].strip()
                if speedText == "" or speedText.find("//") == 0:
                    self.error = textSetting.textList["errorList"]["E53"].format(index + 1)
                    return None
                speedList = [x.strip() for x in speedText.split("\t") if not x.strip() == ""]
                for j in range(notchCnt):
                    if i == 2:
                        trainSpeedInfo.append(int(speedList[j]))
                    else:
                        trainSpeedInfo.append(float(speedList[j]))
                index += 1
            trainOrgInfo.append(trainSpeedInfo)
        except Exception:
            self.error = traceback.format_exc()
            return None

        index = self.findLines(lines, perfLineName)
        if index == -1:
            self.error = textSetting.textList["errorList"]["E52"].format(perfLineName)
            return None
        index += 1
        try:
            trainPerfInfo = []
            perfText = lines[index].strip()
            if speedText == "" or speedText.find("//") == 0:
                self.error = textSetting.textList["errorList"]["E54"].format(index + 1)
                return None
            perfList = [x.strip() for x in perfText.split("\t") if not x.strip() == ""]
            for i in range(len(self.trainPerfNameList)):
                trainPerfInfo.append(float(perfList[i]))
            trainOrgInfo.append(trainPerfInfo)
        except Exception:
            self.error = traceback.format_exc()
            return None

        index = self.findLines(lines, rainLineName)
        if index == -1:
            self.error = textSetting.textList["errorList"]["E52"].format(rainLineName)
            return None
        index += 1
        try:
            trainRainInfo = []
            rainText = lines[index].strip()
            if rainText == "" or rainText.find("//") == 0:
                self.error = textSetting.textList["errorList"]["E55"].format(index + 1)
                return None
            rainList = [x.strip() for x in rainText.split("\t") if not x.strip() == ""]
            for i in range(len(self.trainRainNameList)):
                trainRainInfo.append(float(rainList[i]))
            trainOrgInfo.append(trainRainInfo)
        except Exception:
            self.error = traceback.format_exc()
            return None

        index = self.findLines(lines, carbLineName)
        if index == -1:
            self.error = textSetting.textList["errorList"]["E52"].format(carbLineName)
            return None
        index += 1
        try:
            trainCarbInfo = []
            carbText = lines[index].strip()
            if carbText == "" or carbText.find("//") == 0:
                self.error = textSetting.textList["errorList"]["E56"].format(index + 1)
                return None
            carbList = [x.strip() for x in carbText.split("\t") if not x.strip() == ""]
            for i in range(len(self.trainCarbNameList)):
                trainCarbInfo.append(float(carbList[i]))
            trainOrgInfo.append(trainCarbInfo)
        except Exception:
            self.error = traceback.format_exc()
            return None

        index = self.findLines(lines, otherLineName)
        if index == -1:
            self.error = textSetting.textList["errorList"]["E52"].format(otherLineName)
            return None
        index += 1
        try:
            trainOtherInfo = []
            otherText = lines[index].strip()
            if otherText == "" or otherText.find("//") == 0:
                self.error = textSetting.textList["errorList"]["E57"].format(index + 1)
                return None
            otherList = [x.strip() for x in otherText.split("\t") if not x.strip() == ""]
            for i in range(len(self.trainOtherNameList)):
                if i in [0, 2, 3]:
                    trainOtherInfo.append(int(otherList[i]))
                elif i == 1:
                    trainOtherInfo.append(float(otherList[i]))
                else:
                    trainOtherInfo.append(otherList[i])
            trainOrgInfo.append(trainOtherInfo)
        except Exception:
            self.error = traceback.format_exc()
            return None

        index = self.findLines(lines, hurikoLineName)
        if index != -1:
            index += 1
            trainHurikoInfo = []
            hurikoText = lines[index].strip()
            if hurikoText == "" or hurikoText.find("//") == 0:
                self.error = textSetting.textList["errorList"]["E58"].format(index + 1)
                return None
            hurikoList = [x.strip() for x in hurikoText.split("\t") if not x.strip() == ""]
            for i in range(len(self.trainHurikoNameList)):
                trainHurikoInfo.append(float(hurikoList[i]))
            trainOrgInfo.append(trainHurikoInfo)
        else:
            trainOrgInfo.append(None)

        index = self.findLines(lines, oneWheelLineName)
        if index != -1:
            index += 1
            trainOneWheelInfo = []
            oneWheelText = lines[index].strip()
            if oneWheelText == "" or oneWheelText.find("//") == 0:
                self.error = textSetting.textList["errorList"]["E59"].format(index + 1)
                return None
            oneWheelList = [x.strip() for x in oneWheelText.split("\t") if not x.strip() == ""]
            for i in range(len(self.trainOneWheelNameList)):
                trainOneWheelInfo.append(float(oneWheelList[i]))
            trainOrgInfo.append(trainOneWheelInfo)
        else:
            trainOrgInfo.append(None)
        return trainOrgInfo

    def findLines(self, lines, str):
        for index, line in enumerate(lines):
            if line.find("//") == 0:
                continue
            if line.find(str) == 0:
                return index
        return -1

    def saveNotchInfo(self, trainIdx, newNotchNum):
        trainOrgInfo = self.trainInfoList[trainIdx]
        speedList = trainOrgInfo[0]
        oldNotchNum = len(speedList) // self.notchContentCnt

        diff = newNotchNum - oldNotchNum
        newLines = ["{0}\t{1}\r".format(notchCntLineName, newNotchNum)]
        if diff <= 0:
            for i in range(self.notchContentCnt):
                newSpeed = []
                for j in range(newNotchNum):
                    newSpeed.append(speedList[oldNotchNum * i + j])
                newSpeedLine = "\t".join([str(x) for x in newSpeed])
                newSpeedLine += "\r"
                newLines.append(newSpeedLine)
        else:
            for i in range(self.notchContentCnt):
                newSpeed = []
                for j in range(oldNotchNum):
                    newSpeed.append(speedList[oldNotchNum * i + j])
                for j in range(diff):
                    newSpeed.append(0)
                newSpeedLine = "\t".join([str(x) for x in newSpeed])
                newSpeedLine += "\r"
                newLines.append(newSpeedLine)

        originLines = self.allList[SSTrainName[trainIdx]]
        originIndex = self.findLines(originLines, notchCntLineName)
        originIndex += 5
        newLines.extend(originLines[originIndex:])

        return self.saveTrain(trainIdx, newLines)

    def setDefaultTrainInfo(self, srcList, distData, checkStatusList):
        try:
            srcIdx = srcList[0]
            srcNotchNum = srcList[1]

            distNotchNum = len(distData["notch"])
            notchCheckStatus = checkStatusList[0]
            perfCheckStatus = checkStatusList[1]
            rainCheckStatus = checkStatusList[2]
            carbCheckStatus = checkStatusList[3]
            otherCheckStatus = checkStatusList[4]
            hurikoCheckStatus = checkStatusList[5]
            oneWheelCheckStatus = checkStatusList[6]

            originLines = self.allList[SSTrainName[srcIdx]]
            newLines = copy.deepcopy(originLines)

            index = self.findLines(newLines, notchCntLineName)
            index += 1
            if notchCheckStatus:
                loopCnt = 0
                if srcNotchNum > distNotchNum:
                    loopCnt = distNotchNum
                else:
                    loopCnt = srcNotchNum

                for i in range(self.notchContentCnt):
                    newSpeed = []
                    for j in range(loopCnt):
                        if i == 0:
                            newSpeed.append(distData["notch"][j])
                        elif i == 1:
                            newSpeed.append(distData["tlk"][j])
                        elif i == 2:
                            newSpeed.append(distData["soundNum"][j])
                        elif i == 3:
                            newSpeed.append(distData["add"][j])
                    newSpeedLine = "\t".join([str(x) for x in newSpeed])
                    newSpeedLine += "\r"
                    newLines[index] = newSpeedLine
                    index += 1

            index = self.findLines(newLines, perfLineName)
            index += 1
            if perfCheckStatus:
                newPerfLine = "\t".join([str(x) for x in distData["att"]])
                newPerfLine += "\r"
                newLines[index] = newPerfLine

            index = self.findLines(newLines, rainLineName)
            index += 1
            if rainCheckStatus:
                newRainLine = "\t".join([str(x) for x in distData["rain"]])
                newRainLine += "\r"
                newLines[index] = newRainLine

            index = self.findLines(newLines, carbLineName)
            index += 1
            if carbCheckStatus:
                newCarbLine = "\t".join([str(x) for x in distData["carb"]])
                newCarbLine += "\r"
                newLines[index] = newCarbLine

            index = self.findLines(newLines, otherLineName)
            index += 1
            if otherCheckStatus:
                newOtherLine = "\t".join([str(x) for x in distData["other"]])
                newOtherLine += "\r"
                newLines[index] = newOtherLine

            index = self.findLines(newLines, hurikoLineName)
            if index != -1:
                if hurikoCheckStatus:
                    if distData["huriko"] is not None:
                        index += 1
                        newHurikoLine = "\t".join([str(x) for x in distData["huriko"]])
                        newHurikoLine += "\r"
                        newLines[index] = newHurikoLine
                    else:
                        for i in range(3):
                            if i == 2:
                                if newLines[index].strip() != "":
                                    continue
                            newLines.pop(index)
            else:
                if hurikoCheckStatus:
                    index = self.findLines(newLines, otherLineName)
                    if distData["huriko"] is not None:
                        index += 3
                        newHurikoLines = ["\r"]
                        newHurikoLines.append("{0}\r".format(hurikoLineName))
                        newHurikoLine = "\t".join([str(x) for x in distData["huriko"]])
                        newHurikoLine += "\r"
                        newHurikoLines.append(newHurikoLine)
                        if newLines[index].strip() != "":
                            newHurikoLines.append("\r")
                        for line in reversed(newHurikoLines):
                            newLines.insert(index, line)

            index = self.findLines(newLines, oneWheelLineName)
            if index != -1:
                if oneWheelCheckStatus:
                    if distData["oneWheel"] is not None:
                        index += 1
                        newOneWheelLine = "\t".join([str(x) for x in distData["oneWheel"]])
                        newOneWheelLine += "\r"
                        newLines[index] = newOneWheelLine
                    else:
                        for i in range(3):
                            if i == 2:
                                if newLines[index].strip() != "":
                                    continue
                            newLines.pop(index)
            else:
                if oneWheelCheckStatus:
                    index = self.findLines(newLines, hurikoLineName)
                    if index != -1:
                        index += 2
                    else:
                        index = self.findLines(newLines, otherLineName)
                        index += 3
                    if distData["oneWheel"] is not None:
                        newOneWheelLines = ["\r"]
                        newOneWheelLines.append("{0}\r".format(oneWheelLineName))
                        newOneWheelLine = "\t".join([str(x) for x in distData["oneWheel"]])
                        newOneWheelLine += "\r"
                        newOneWheelLines.append(newOneWheelLine)
                        if newLines[index].strip() != "":
                            newOneWheelLines.append("\r")
                        for line in reversed(newOneWheelLines):
                            newLines.insert(index, line)

            return self.saveTrain(srcIdx, newLines)
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTrainInfo(self, trainIdx, varList):
        try:
            originLines = self.allList[SSTrainName[trainIdx]]
            newLines = copy.deepcopy(originLines)

            index = self.findLines(originLines, notchCntLineName)
            index += 1

            trainOrgInfo = self.trainInfoList[trainIdx]
            speedList = trainOrgInfo[0]
            notchCnt = len(speedList) // self.notchContentCnt

            for i in range(self.notchContentCnt):
                newSpeed = []
                for j in range(notchCnt):
                    if i == 0:
                        newSpeed.append(varList[self.notchContentCnt * j].get())
                    elif i == 1:
                        newSpeed.append(varList[self.notchContentCnt * j + 1].get())
                    elif i == 2:
                        newSpeed.append(varList[self.notchContentCnt * j + 2].get())
                    elif i == 3:
                        newSpeed.append(varList[self.notchContentCnt * j + 3].get())
                newSpeedLine = "\t".join([str(x) for x in newSpeed])
                newSpeedLine += "\r"
                newLines[index] = newSpeedLine
                index += 1

            index = self.findLines(originLines, perfLineName)
            index += 1
            newPerf = []
            for i in range(len(self.trainPerfNameList)):
                newPerf.append(varList[notchCnt * self.notchContentCnt + i].get())
            newPerfLine = "\t".join([str(x) for x in newPerf])
            newPerfLine += "\r"
            newLines[index] = newPerfLine

            return self.saveTrain(trainIdx, newLines)
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElsePerfList(self, trainIdx, title, resultValueList):
        try:
            originLines = self.allList[SSTrainName[trainIdx]]
            newLines = copy.deepcopy(originLines)

            if title == "rain":
                index = self.findLines(originLines, rainLineName)
                index += 1
                newRainLine = "\t".join([str(x) for x in resultValueList])
                newRainLine += "\r"
                newLines[index] = newRainLine
            elif title == "carb":
                index = self.findLines(originLines, carbLineName)
                index += 1
                newCarbLine = "\t".join([str(x) for x in resultValueList])
                newCarbLine += "\r"
                newLines[index] = newCarbLine
            elif title == "other":
                index = self.findLines(originLines, otherLineName)
                index += 1
                newOtherLine = "\t".join([str(x) for x in resultValueList])
                newOtherLine += "\r"
                newLines[index] = newOtherLine
            elif title == "huriko":
                index = self.findLines(originLines, hurikoLineName)
                if index != -1:
                    if resultValueList is not None:
                        index += 1
                        newHurikoLine = "\t".join([str(x) for x in resultValueList])
                        newHurikoLine += "\r"
                        newLines[index] = newHurikoLine
                    else:
                        for i in range(3):
                            if i == 2:
                                if newLines[index].strip() != "":
                                    continue
                            newLines.pop(index)
                else:
                    if resultValueList is not None:
                        index = self.findLines(originLines, otherLineName)
                        index += 3
                        newHurikoLines = ["\r"]
                        newHurikoLines.append("{0}\r".format(hurikoLineName))
                        newHurikoLine = "\t".join([str(x) for x in resultValueList])
                        newHurikoLine += "\r"
                        newHurikoLines.append(newHurikoLine)
                        if originLines[index].strip() != "":
                            newHurikoLines.append("\r")
                        for line in reversed(newHurikoLines):
                            newLines.insert(index, line)
            elif title == "oneWheel":
                index = self.findLines(originLines, oneWheelLineName)
                if index != -1:
                    if resultValueList is not None:
                        index += 1
                        newOneWheelLine = "\t".join([str(x) for x in resultValueList])
                        newOneWheelLine += "\r"
                        newLines[index] = newOneWheelLine
                    else:
                        for i in range(3):
                            if i == 2:
                                if newLines[index].strip() != "":
                                    continue
                            newLines.pop(index)
                else:
                    if resultValueList is not None:
                        index = self.findLines(originLines, hurikoLineName)
                        if index != -1:
                            index += 2
                        else:
                            index = self.findLines(originLines, otherLineName)
                            index += 3
                        newOneWheelLines = ["\r"]
                        newOneWheelLines.append("{0}\r".format(oneWheelLineName))
                        newOneWheelLine = "\t".join([str(x) for x in resultValueList])
                        newOneWheelLine += "\r"
                        newOneWheelLines.append(newOneWheelLine)
                        if originLines[index].strip() != "":
                            newOneWheelLines.append("\r")
                        for line in reversed(newOneWheelLines):
                            newLines.insert(index, line)
            return self.saveTrain(trainIdx, newLines)
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveAllEdit(self, perfIndex, num, calcIndex):
        try:
            for trainIdx in range(len(self.trainNameList)):
                originLines = self.allList[SSTrainName[trainIdx]]
                newLines = copy.deepcopy(originLines)

                index = self.findLines(originLines, perfLineName)
                index += 1

                trainOrgInfo = self.trainInfoList[trainIdx]
                newPerf = trainOrgInfo[1]

                if calcIndex == 0:
                    newPerf[perfIndex] *= num
                else:
                    newPerf[perfIndex] = num
                newPerfLine = "\t".join([str(x) for x in newPerf])
                newPerfLine += "\r"
                newLines[index] = newPerfLine

                data = self.dataList[SSTrainName[trainIdx]]
                data.script = bytearray("\n".join(newLines).encode("utf-8"))
                data.save()
            with open(self.filePath, "wb") as w:
                w.write(self.env.file.save())
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTrain(self, trainIdx, newLines):
        try:
            data = self.dataList[SSTrainName[trainIdx]]
            data.script = bytearray("\n".join(newLines).encode("utf-8"))
            data.save()
            with open(self.filePath, "wb") as w:
                w.write(self.env.file.save())
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False
