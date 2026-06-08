import struct
import traceback
from program.sub.encodingClass import SJISEncodingObject
from program.sub.errorLogClass import ErrorLogObj


class MdlBinDecrypt:
    def __init__(self, filePath, cmdList):
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
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
        self.errObj.write(self.error)

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
            imgName = self.encObj.convertString(self.byteArr[self.index:self.index + imgNameLen])
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
            smfName = self.encObj.convertString(self.byteArr[self.index:self.index + smfLen])
            self.smfList.append(smfName)
            self.index += smfLen

        wavCnt = self.byteArr[self.index]
        self.index += 1

        self.wavList = []
        for i in range(wavCnt):
            wavInfo = []
            wavLen = self.byteArr[self.index]
            self.index += 1
            wavName = self.encObj.convertString(self.byteArr[self.index:self.index + wavLen])
            wavInfo.append(wavName)
            self.index += wavLen
            wavInfo.append(self.byteArr[self.index])
            self.index += 1
            self.wavList.append(wavInfo)

        if self.ver != 1:
            lightTgaCnt = self.byteArr[self.index]
            self.index += 1

            self.tgaList = []
            for i in range(lightTgaCnt):
                tgaInfo = {}
                tgaInfo["tgaInfo"] = []
                for j in range(2):
                    lightTgaLen = self.byteArr[self.index]
                    self.index += 1
                    lightTgaName = self.encObj.convertString(self.byteArr[self.index:self.index + lightTgaLen])
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
                    temp = self.encObj.convertString(self.byteArr[self.index:self.index + txtLen])
                    self.index += txtLen
                    scriptData.append(temp)

            scriptDataInfo.append(scriptData)
        return scriptDataInfo

    def saveFile(self, itemIdArr, mode, scriptData=None):
        try:
            num = itemIdArr[0]
            listNum = itemIdArr[1]
            self.index = self.indexInfoList[num][listNum]

            startIdx = self.index
            cntIdx = self.index + 6
            if mode == "insert":
                cnt = self.byteArr[cntIdx]
                self.byteArr[cntIdx] = (cnt + 1)
            elif mode == "delete":
                cnt = self.byteArr[cntIdx]
                self.byteArr[cntIdx] = (cnt - 1)

            cmdDiff = itemIdArr[2]
            self.nextSection(cmdDiff - 1)
            newByteArr = self.byteArr[0:self.index]

            if mode == "modify" or mode == "insert":
                bIdx = struct.pack("<h", scriptData[0])
                newByteArr.extend(bIdx)

                bCmd = struct.pack("<h", scriptData[1])
                newByteArr.extend(bCmd)

                newByteArr.append(scriptData[2])
                strCount = 0
                if self.ver >= 2:
                    if scriptData[3] != 0xFF:
                        strCount = scriptData[3]
                    if self.ver >= 3:
                        newByteArr.append(scriptData[3])

                for i in range(scriptData[2]):
                    temp = scriptData[4 + i]
                    if i < scriptData[2] - strCount:
                        bTemp = struct.pack("<f", temp)
                        newByteArr.extend(bTemp)
                    else:
                        bTemp = self.encObj.convertByteArray(temp)
                        newByteArr.append(len(bTemp))
                        newByteArr.extend(bTemp)

            self.index = startIdx
            if mode == "modify" or mode == "delete":
                self.nextSection(cmdDiff)
            elif mode == "insert":
                self.nextSection(cmdDiff - 1)

            newByteArr.extend(self.byteArr[self.index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveListHeader(self, itemIdArr, headerList):
        try:
            num = itemIdArr[0]
            listNum = itemIdArr[1]
            index = self.indexInfoList[num][listNum]

            newByteArr = self.byteArr[0:index]
            for i in range(3):
                hVal = struct.pack("<h", headerList[i])
                newByteArr.extend(hVal)
                index += 2
            
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveListNum(self, itemIdArr, newListNum):
        try:
            num = itemIdArr[0]
            self.index = self.indexInfoList[num][0]

            listIdx = self.index - 1
            listCnt = self.byteArr[listIdx]
            self.byteArr[listIdx] = newListNum

            for i in range(listCnt):
                if i == newListNum:
                    break
                self.nextSection()

            newByteArr = self.byteArr[0:self.index]
            if newListNum < listCnt:
                for i in range(listCnt - newListNum):
                    self.nextSection()
            else:
                for i in range(newListNum - listCnt):
                    newHeaderInfo = [1, 0, 1]
                    cmdCnt = 0
                    for j in range(3):
                        hVal = struct.pack("<h", newHeaderInfo[j])
                        newByteArr.extend(hVal)
                    newByteArr.append(cmdCnt)

            newByteArr.extend(self.byteArr[self.index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveNumFile(self, num):
        try:
            self.index = self.allListIndex
            allListCnt = self.byteArr[self.index]
            newByteArr = bytearray(self.byteArr)
            newByteArr[self.index] = num
            if num > allListCnt:
                for i in range(num - allListCnt):
                    newByteArr.append(1)

                    newHeaderInfo = [1, 0, 1]
                    cmdCnt = 0
                    for j in range(3):
                        hVal = struct.pack("<h", newHeaderInfo[j])
                        newByteArr.extend(hVal)
                    newByteArr.append(cmdCnt)
            elif num < allListCnt:
                index = self.indexInfoList[num][0] - 1
                newByteArr = newByteArr[0:index]
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveHeader(self, imgList, imgSizeList, smfList, wavList, tgaList):
        try:
            index = 1
            newByteArr = bytearray(self.byteArr[0:index])

            newByteArr.append(len(imgList))
            for i in range(len(imgList)):
                newByteArr.append(len(imgList[i]["imgName"]))
                newByteArr.extend(self.encObj.convertByteArray(imgList[i]["imgName"]))
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
                newByteArr.extend(self.encObj.convertByteArray(smfList[i]))

            newByteArr.append(len(wavList))
            for i in range(len(wavList)):
                newByteArr.append(len(wavList[i][0]))
                newByteArr.extend(self.encObj.convertByteArray(wavList[i][0]))
                newByteArr.append(wavList[i][1])

            if self.ver != 1:
                newByteArr.append(len(tgaList))
                for i in range(len(tgaList)):
                    for j in range(4):
                        if j < 2:
                            newByteArr.append(len(tgaList[i]["tgaInfo"][j]))
                            newByteArr.extend(self.encObj.convertByteArray(tgaList[i]["tgaInfo"][j]))
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
            self.save(newByteArr)
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
                                    tempS = self.encObj.convertByteArray(csvScriptData[2 + i])
                                    paramByteList.append(struct.pack("<b", len(tempS)))
                                    paramByteList.append(tempS)
                            else:
                                tempS = self.encObj.convertByteArray(csvScriptData[2 + i])
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
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def reload(self):
        self.open()
        return self

    def save(self, newByteArr):
        self.byteArr = newByteArr
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
