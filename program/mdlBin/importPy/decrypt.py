import struct
import traceback


class MdlBinDecrypt:
    def __init__(self, filePath, cmdList):
        self.filePath = filePath
        self.byteArr = []
        self.error = ""
        self.cmdList = cmdList
        self.max_param = 1
        self.ver = 0
        self.index = 0
        self.allListIndex = 0
        self.imgList = []
        self.imgSizeList = []
        self.smfList = []
        self.wavList = []
        self.tgaList = []

        self.indexInfoList = []
        self.scriptDataAllInfoList = []

    def open(self):
        try:
            f = open(self.filePath, "rb")
            self.byteArr = bytearray(f.read())
            f.close()
            self.decrypt()
            self.readScript()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        w = open("error.log", "w")
        w.write(self.error)
        w.close()

    def decrypt(self):
        self.ver = self.byteArr[0]
        self.index = 1
        imgCnt = self.byteArr[self.index]
        self.index += 1

        self.imgList = []
        for img in range(imgCnt):
            imgInfo = {}
            imgNameLen = self.byteArr[self.index]
            self.index += 1
            imgName = self.byteArr[self.index:self.index + imgNameLen].decode("shift-jis")
            imgInfo["imgName"] = imgName
            self.index += imgNameLen
            imgInfo["imgElse"] = []
            if self.ver == 4:
                tmp = self.byteArr[self.index]
                imgInfo["imgElse"].append(tmp)
                self.index += 1
                if tmp != 0:
                    h = struct.unpack("<h", self.byteArr[self.index:self.index + 2])[0]
                    imgInfo["imgElse"].append(h)
                    self.index += 2
            self.imgList.append(imgInfo)

        imgSizeCnt = self.byteArr[self.index]
        self.index += 1

        self.imgSizeList = []
        for imgSize in range(imgSizeCnt):
            imgSizeInfo = []
            imgIdx = self.byteArr[self.index]
            imgSizeInfo.append(imgIdx)
            self.index += 1

            imgSize = []
            for i in range(4):
                size = struct.unpack("<f", self.byteArr[self.index:self.index + 4])[0]
                imgSize.append(size)
                self.index += 4
            imgSizeInfo.append(imgSize)
            self.imgSizeList.append(imgSizeInfo)

        smfCnt = self.byteArr[self.index]
        self.index += 1

        self.smfList = []
        for i in range(smfCnt):
            smfLen = self.byteArr[self.index]
            self.index += 1
            smfName = self.byteArr[self.index:self.index + smfLen].decode("shift-jis")
            self.smfList.append(smfName)
            self.index += smfLen

        wavCnt = self.byteArr[self.index]
        self.index += 1
        for i in range(wavCnt):
            wavInfo = []
            wavLen = self.byteArr[self.index]
            self.index += 1
            wavName = self.byteArr[self.index:self.index + wavLen].decode("shift-jis")
            wavInfo.append(wavName)
            self.index += wavLen
            wavInfo.append(self.byteArr[self.index])
            self.index += 1
            self.wavList.append(wavInfo)

        if self.ver != 1:
            lightTgaCnt = self.byteArr[self.index]
            self.index += 1
            for i in range(lightTgaCnt):
                tgaInfo = {}
                tgaInfo["tgaInfo"] = []
                for j in range(2):
                    lightTgaLen = self.byteArr[self.index]
                    self.index += 1
                    lightTgaName = self.byteArr[self.index:self.index + lightTgaLen].decode("shift-jis")
                    tgaInfo["tgaInfo"].append(lightTgaName)
                    self.index += lightTgaLen

                for i in range(2):
                    tempF = struct.unpack("<f", self.byteArr[self.index:self.index + 4])[0]
                    tgaInfo["tgaInfo"].append(tempF)
                    self.index += 4

                tgaInfo["tgaElse"] = []
                for i in range(4):
                    tgaInfo["tgaElse"].append(self.byteArr[self.index])
                    self.index += 1

                h = struct.unpack("<h", self.byteArr[self.index:self.index + 2])[0]
                tgaInfo["tgaElse"].append(h)
                self.index += 2

                self.tgaList.append(tgaInfo)

    def readScript(self):
        self.indexInfoList = []
        self.scriptDataAllInfoList = []

        self.allListIndex = self.index
        allListCnt = self.byteArr[self.index]
        self.index += 1

        for section in range(allListCnt):
            indexInfo = []
            cnt = self.byteArr[self.index]
            self.index += 1

            scriptDataInfoList = []
            for c in range(cnt):
                indexInfo.append(self.index)
                scriptDataInfo = self.nextSection()
                scriptDataInfoList.append(scriptDataInfo)

            self.indexInfoList.append(indexInfo)
            self.scriptDataAllInfoList.append(scriptDataInfoList)

    def nextSection(self, cmdDiff=None):
        scriptDataInfo = []
        headerInfo = []
        for i in range(3):
            h = struct.unpack("<h", self.byteArr[self.index:self.index + 2])[0]
            headerInfo.append(h)
            self.index += 2
        scriptDataInfo.append(headerInfo)

        cmdcnt = self.byteArr[self.index]
        self.index += 1
        if cmdDiff is not None:
            cmdcnt = cmdDiff

        for i in range(cmdcnt):
            scriptData = []
            idx = struct.unpack("<h", self.byteArr[self.index:self.index + 2])[0]
            self.index += 2
            scriptData.append(idx)

            cmdNum = struct.unpack("<h", self.byteArr[self.index:self.index + 2])[0]
            self.index += 2
            scriptData.append(cmdNum)

            paraCnt = self.byteArr[self.index]
            if self.max_param < paraCnt:
                self.max_param = paraCnt
            self.index += 1
            scriptData.append(paraCnt)

            if self.ver >= 3:
                fileCnt = self.byteArr[self.index]
                self.index += 1
            elif self.ver == 2 and self.cmdList[cmdNum] in ["MDL_GETINDEX", "SET_LENSFLEAR_MT"]:
                fileCnt = 1
            else:
                fileCnt = 0xFF
            scriptData.append(fileCnt)

            if fileCnt != 0xFF:
                paraCnt -= fileCnt

            for j in range(paraCnt):
                temp = struct.unpack("<f", self.byteArr[self.index:self.index + 4])[0]
                temp = round(temp, 5)
                self.index += 4
                scriptData.append(temp)

            if fileCnt != 0xFF:
                for j in range(fileCnt):
                    txtLen = self.byteArr[self.index]
                    self.index += 1
                    temp = self.byteArr[self.index:self.index + txtLen].decode("shift-jis")
                    self.index += txtLen
                    scriptData.append(temp)

            scriptDataInfo.append(scriptData)
        return scriptDataInfo

    def saveHeader(self, imgList, imgSizeList, smfList, wavList, tgaList):
        try:
            index = 1
            newByteArr = bytearray(self.byteArr[0:index])

            newByteArr.append(len(imgList))
            for i in range(len(imgList)):
                newByteArr.append(len(imgList[i]["imgName"]))
                newByteArr.extend(imgList[i]["imgName"].encode("shift-jis"))
                if self.ver == 4:
                    newByteArr.append(imgList[i]["imgElse"][0])
                    if imgList[i]["imgElse"][0] != 0:
                        h = struct.pack("<h", imgList[i]["imgElse"][1])
                        newByteArr.extend(h)

            newByteArr.append(len(imgSizeList))
            for i in range(len(imgSizeList)):
                newByteArr.append(imgSizeList[i][0])
                for j in range(4):
                    f = struct.pack("<f", imgSizeList[i][1][j])
                    newByteArr.extend(f)

            newByteArr.append(len(smfList))
            for i in range(len(smfList)):
                newByteArr.append(len(smfList[i]))
                newByteArr.extend(smfList[i].encode("shift-jis"))

            newByteArr.append(len(wavList))
            for i in range(len(wavList)):
                newByteArr.append(len(wavList[i][0]))
                newByteArr.extend(wavList[i][0].encode("shift-jis"))
                newByteArr.append(wavList[i][1])

            if self.ver != 1:
                newByteArr.append(len(tgaList))
                for i in range(len(tgaList)):
                    for j in range(4):
                        if j < 2:
                            newByteArr.append(len(tgaList[i]["tgaInfo"][j]))
                            newByteArr.extend(tgaList[i]["tgaInfo"][j].encode("shift-jis"))
                        else:
                            f = struct.pack("<f", tgaList[i]["tgaInfo"][j])
                            newByteArr.extend(f)

                    for j in range(5):
                        if j == 4:
                            h = struct.pack("<h", tgaList[i]["tgaElse"][j])
                            newByteArr.extend(h)
                        else:
                            newByteArr.append(tgaList[i]["tgaElse"][j])

            index = self.allListIndex
            newByteArr.extend(self.byteArr[index:])

            self.byteArr = newByteArr
            self.save()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveFile(self, num, listNum, cmdDiff, mode, scriptData=None):
        try:
            self.index = self.indexInfoList[num][listNum]

            if mode == "list":
                listIdx = self.index - 1
                listcnt = self.byteArr[listIdx]
                self.byteArr[listIdx] = scriptData

                for i in range(listcnt):
                    if i == scriptData:
                        break

                    self.nextSection()

                newByteArr = self.byteArr[0:self.index]
                if scriptData < listcnt:
                    for i in range(listcnt - scriptData):
                        self.nextSection()
                else:
                    for i in range(scriptData - listcnt):
                        newByteArr.extend([1, 0, 0, 0, 1, 0])
                        newByteArr.append(0)

                newByteArr.extend(self.byteArr[self.index:])
            else:
                cntIdx = self.index
                if self.ver != 1:
                    if self.byteArr[cntIdx] != 0:
                        cntIdx += 6
                    else:
                        cntIdx += 1
                else:
                    cntIdx += 6

                startIdx = self.index
                if mode == "insert":
                    cnt = self.byteArr[cntIdx]
                    self.byteArr[cntIdx] = (cnt + 1)
                elif mode == "delete":
                    cnt = self.byteArr[cntIdx]
                    self.byteArr[cntIdx] = (cnt - 1)

                self.nextSection(cmdDiff - 1)
                newByteArr = self.byteArr[0:self.index]

                if mode == "edit" or mode == "insert":
                    bIdx = struct.pack("<h", scriptData[0])
                    newByteArr.extend(bIdx)

                    bCmd = struct.pack("<h", scriptData[1])
                    newByteArr.extend(bCmd)

                    newByteArr.append(scriptData[2])
                    if self.ver >= 3:
                        newByteArr.append(scriptData[3])

                    floatFlag = True
                    for i in range(scriptData[2]):
                        temp = 0
                        if floatFlag:
                            try:
                                temp = float(scriptData[4 + i])
                            except Exception:
                                floatFlag = False

                        if self.ver == 2:
                            if self.cmdList[scriptData[1]] in ["MDL_GETINDEX", "SET_LENSFLEAR_MT"] and i == 1:
                                floatFlag = False

                        if floatFlag:
                            bTemp = struct.pack("<f", temp)
                            newByteArr.extend(bTemp)
                        else:
                            temp = scriptData[4 + i].encode("shift-jis")
                            newByteArr.append(len(temp))
                            newByteArr.extend(temp)

                self.index = startIdx
                if mode == "edit" or mode == "delete":
                    self.nextSection(cmdDiff)
                elif mode == "insert":
                    self.nextSection(cmdDiff - 1)

                newByteArr.extend(self.byteArr[self.index:])

            self.byteArr = newByteArr
            self.save()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveListHeader(self, num, listNum, headerList):
        try:
            index = self.indexInfoList[num][listNum]
            for i in range(3):
                hVal = struct.pack("<h", headerList[i])
                for h in hVal:
                    self.byteArr[index] = h
                    index += 1
            self.save()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveNumFile(self, num):
        try:
            self.index = self.allListIndex
            curNum = len(self.indexInfoList)
            self.byteArr[self.index] = num
            if num > curNum:
                for i in range(num - curNum):
                    self.byteArr.append(1)

                    self.byteArr.extend([1, 0, 0, 0, 1, 0])
                    self.byteArr.append(0)
            elif num < curNum:
                index = self.indexInfoList[num][0] - 1
                self.byteArr = self.byteArr[0:index]
            self.save()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveCsv(self, csvScriptDataAllInfoList):
        try:
            index = self.allListIndex
            newByteArr = self.byteArr[0:index]

            allListCnt = len(csvScriptDataAllInfoList)
            newByteArr.append(allListCnt)

            for csvScriptDataInfoList in csvScriptDataAllInfoList:
                listCnt = len(csvScriptDataInfoList)
                newByteArr.append(listCnt)

                for csvScriptDataInfo in csvScriptDataInfoList:
                    headerInfo = csvScriptDataInfo[0]
                    for header in headerInfo:
                        if header == "":
                            continue
                        h = struct.pack("<h", int(header))
                        newByteArr.extend(h)

                    cmdCnt = len(csvScriptDataInfo[1])
                    newByteArr.append(cmdCnt)
                    for csvScriptData in csvScriptDataInfo[1]:
                        delay = int(csvScriptData[0])
                        delayH = struct.pack("<h", delay)
                        newByteArr.extend(delayH)

                        cmdName = csvScriptData[1]
                        cmdIdx = self.cmdList.index(cmdName)
                        cmdIdxH = struct.pack("<h", cmdIdx)
                        newByteArr.extend(cmdIdxH)

                        csvAllParamList = csvScriptData[2:]
                        allParamList = []
                        for param in csvAllParamList:
                            if param == "":
                                continue
                            allParamList.append(param)

                        allParamCnt = len(allParamList)
                        floatCnt = 0
                        paramByteList = []
                        floatFlag = True
                        for i in range(allParamCnt):
                            if floatFlag:
                                try:
                                    tempF = struct.pack("<f", float(csvScriptData[2 + i]))
                                    floatCnt += 1
                                    paramByteList.append(tempF)
                                except Exception:
                                    floatFlag = False
                                    tempS = csvScriptData[2 + i].encode("shift-jis")
                                    paramByteList.append(struct.pack("<b", len(tempS)))
                                    paramByteList.append(tempS)
                            else:
                                tempS = csvScriptData[2 + i].encode("shift-jis")
                                paramByteList.append(struct.pack("<b", len(tempS)))
                                paramByteList.append(tempS)

                        stringCnt = allParamCnt - floatCnt
                        if stringCnt == 0:
                            stringCnt = 0xFF

                        newByteArr.append(allParamCnt)
                        if self.ver >= 3:
                            newByteArr.append(stringCnt)

                        for paramByte in paramByteList:
                            newByteArr.extend(paramByte)
            self.byteArr = newByteArr
            self.save()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def save(self):
        w = open(self.filePath, "wb")
        w.write(self.byteArr)
        w.close()
