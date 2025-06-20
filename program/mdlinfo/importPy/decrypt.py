import os
import struct
import traceback
import program.textSetting as textSetting
from program.encodingClass import SJISEncodingObject
from program.errorLogClass import ErrorLogObj


class MdlDecrypt:
    def __init__(self, filePath):
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.allInfoList = []
        self.error = ""
        self.byteArr = []

    def open(self):
        try:
            f = open(self.filePath, "rb")
            line = f.read()
            f.close()
            if not self.decrypt(line):
                return False
            self.byteArr = bytearray(line)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        self.errObj.write(self.error)

    def decrypt(self, line):
        self.allInfoList = []
        self.error = ""

        index = 16
        header = self.encObj.convertString(line[0:index])
        if header != "MDL_INFO_VER_100":
            self.error = textSetting.textList["errorList"]["E16"]
            raise False

        allcnt = struct.unpack("<h", line[index:index + 2])[0]
        index += 2

        for i in range(allcnt):
            mdlInfo = {}
            mdlInfo["smfIndex"] = index
            smfLen = line[index]
            index += 1
            smfName = self.encObj.convertString(line[index:index + smfLen])
            index += smfLen
            mdlInfo["smfName"] = smfName

            mdlInfo["meshMtrlCntIndex"] = index
            meshMtrlCnt = line[index]
            index += 1
            smfType = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
            mdlInfo["smfType"] = smfType
            index += 1
            mdlInfo["detailMdlList"] = []
            for j in range(meshMtrlCnt):
                detailMdlInfo = {}
                detailMdlInfo["detailMtrlIndex"] = index

                detailMdlInfo["materialList"] = []
                meshNum = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                detailMdlInfo["materialList"].append(meshNum)
                index += 1
                mtrlNum = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                detailMdlInfo["materialList"].append(mtrlNum)
                index += 1

                for k in range(4):
                    b = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                    detailMdlInfo["materialList"].append(b)
                    index += 1

                for k in range(4):
                    diff = struct.unpack("<f", line[index:index + 4])[0]
                    diff = round(diff, 5)
                    detailMdlInfo["materialList"].append(diff)
                    index += 4

                detailMdlInfo["materialList"].append(line[index])
                index += 1

                for k in range(3):
                    emis = struct.unpack("<f", line[index:index + 4])[0]
                    emis = round(emis, 5)
                    detailMdlInfo["materialList"].append(emis)
                    index += 4

                b = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                detailMdlInfo["materialList"].append(b)
                index += 1

                h = struct.unpack("<h", line[index:index + 2])[0]
                detailMdlInfo["materialList"].append(h)
                index += 2

                detailMdlInfo["detailImgIndex"] = index
                b = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                detailMdlInfo["colorCnt"] = b
                index += 1
                detailMdlInfo["textureImgList"] = []
                for k in range(b):
                    imgLen = line[index]
                    index += 1
                    imgName = self.encObj.convertString(line[index:index + imgLen])
                    index += imgLen
                    detailMdlInfo["textureImgList"].append(imgName)

                mdlInfo["detailMdlList"].append(detailMdlInfo)

            mdlInfo["smfDetailList"] = []
            mdlInfo["smfDetailListIndex"] = index
            detailCnt = line[index]
            index += 1
            for j in range(detailCnt):
                smfDetailInfo = {}
                smfDetailInfo["smfDetailIndex"] = index
                smfDetailInfo["smfDetail"] = []

                mdlLen = line[index]
                index += 1
                mdlName = self.encObj.convertString(line[index:index + mdlLen])
                index += mdlLen
                smfDetailInfo["smfDetail"].append(mdlName)

                for k in range(6):
                    f = struct.unpack("<f", line[index:index + 4])[0]
                    f = round(f, 5)
                    smfDetailInfo["smfDetail"].append(f)
                    index += 4
                mdlInfo["smfDetailList"].append(smfDetailInfo)

            mdlInfo["binInfo"] = []
            mdlInfo["binInfoIndex"] = index
            binFileLen = line[index]
            index += 1
            binFileName = self.encObj.convertString(line[index:index + binFileLen])
            mdlInfo["binInfo"].append(binFileName)
            index += binFileLen

            h = struct.unpack("<h", line[index:index + 2])[0]
            index += 2
            mdlInfo["binInfo"].append(h)

            self.allInfoList.append(mdlInfo)
        return True

    def updateTexImage(self, smfNum, detailInfoNum, imgList):
        try:
            index = self.allInfoList[smfNum]["detailMdlList"][detailInfoNum]["detailImgIndex"]
            newByteArr = self.byteArr[0:index]

            newByteArr.append(len(imgList))
            for img in imgList:
                newByteArr.append(len(img))
                newByteArr.extend(self.encObj.convertByteArray(img))

            oldImgCnt = self.byteArr[index]
            index += 1
            for i in range(oldImgCnt):
                imgLen = self.byteArr[index]
                index += 1
                index += imgLen

            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def updateTex(self, smfNum, detailInfoNum, varList, mode):
        try:
            meshMtrlCntIndex = self.allInfoList[smfNum]["meshMtrlCntIndex"]
            meshMtrlCnt = self.byteArr[meshMtrlCntIndex]
            if mode == "insert":
                meshMtrlCnt += 1
            elif mode == "delete":
                meshMtrlCnt -= 1
            self.byteArr[meshMtrlCntIndex] = meshMtrlCnt

            if mode == "edit" or mode == "delete":
                index = self.allInfoList[smfNum]["detailMdlList"][detailInfoNum]["detailMtrlIndex"]
                newByteArr = self.byteArr[0:index]
            elif mode == "insert":
                if detailInfoNum >= len(self.allInfoList[smfNum]["detailMdlList"]) - 1:
                    index = self.allInfoList[smfNum]["smfDetailListIndex"]
                else:
                    index = self.allInfoList[smfNum]["detailMdlList"][detailInfoNum + 1]["detailMtrlIndex"]
                newByteArr = self.byteArr[0:index]

            if mode == "edit" or mode == "insert":
                varIdx = 0
                for i in range(6):
                    b = struct.pack("<b", varList[varIdx])
                    newByteArr.extend(b)
                    varIdx += 1
                    if mode == "edit":
                        index += 1

                for i in range(4):
                    f = struct.pack("<f", varList[varIdx])
                    newByteArr.extend(f)
                    varIdx += 1
                    if mode == "edit":
                        index += 4

                b = struct.pack("<b", varList[varIdx])
                newByteArr.extend(b)
                varIdx += 1
                if mode == "edit":
                    index += 1

                for i in range(3):
                    f = struct.pack("<f", varList[varIdx])
                    newByteArr.extend(f)
                    varIdx += 1
                    if mode == "edit":
                        index += 4

                b = struct.pack("<b", varList[varIdx])
                newByteArr.extend(b)
                varIdx += 1
                if mode == "edit":
                    index += 1

                h = struct.pack("<h", varList[varIdx])
                newByteArr.extend(h)
                varIdx += 1
                if mode == "edit":
                    index += 2

                if mode == "insert":
                    newByteArr.append(0)
            elif mode == "delete":
                if detailInfoNum >= len(self.allInfoList[smfNum]["detailMdlList"]) - 1:
                    index = self.allInfoList[smfNum]["smfDetailListIndex"]
                else:
                    index = self.allInfoList[smfNum]["detailMdlList"][detailInfoNum + 1]["detailMtrlIndex"]

            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def updateTexList(self, smfNum, firstDetailInfoNum, materialList):
        try:
            newByteArr = bytearray(self.byteArr)
            for mIdx, materialInfo in enumerate(materialList):
                index = self.allInfoList[smfNum]["detailMdlList"][firstDetailInfoNum + mIdx]["detailMtrlIndex"]
                varIdx = 0
                for i in range(6):
                    bValue = struct.pack("<b", materialInfo[varIdx])
                    for b in bValue:
                        newByteArr[index] = b
                        index += 1
                    varIdx += 1

                for i in range(4):
                    fValue = struct.pack("<f", materialInfo[varIdx])
                    for f in fValue:
                        newByteArr[index] = f
                        index += 1
                    varIdx += 1

                bValue = struct.pack("<b", materialInfo[varIdx])
                for b in bValue:
                    newByteArr[index] = b
                    index += 1
                varIdx += 1

                for i in range(3):
                    fValue = struct.pack("<f", materialInfo[varIdx])
                    for f in fValue:
                        newByteArr[index] = f
                        index += 1
                    varIdx += 1

                bValue = struct.pack("<b", materialInfo[varIdx])
                for b in bValue:
                    newByteArr[index] = b
                    index += 1
                varIdx += 1

                hValue = struct.pack("<h", materialInfo[varIdx])
                for h in hValue:
                    newByteArr[index] = h
                    index += 1

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def updateType(self, smfNum, smfType):
        try:
            index = self.allInfoList[smfNum]["meshMtrlCntIndex"]
            index += 1
            newByteArr = self.byteArr[0:index]

            newByteArr.extend(struct.pack("<b", smfType))
            index += 1

            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def updateSmfDetail(self, smfNum, smfDetailNum, pos, valueList):
        try:
            newByteArr = bytearray()
            smfCntIndex = self.allInfoList[smfNum]["smfDetailListIndex"]
            index = 0

            if pos == 1:
                smfDetailNum += 1

            if smfDetailNum >= len(self.allInfoList[smfNum]["smfDetailList"]):
                index = self.allInfoList[smfNum]["binInfoIndex"]
            else:
                index = self.allInfoList[smfNum]["smfDetailList"][smfDetailNum]["smfDetailIndex"]

            newByteArr = self.byteArr[0:index]

            if valueList is not None:
                newByteArr.append(len(valueList[0]))
                newByteArr.extend(self.encObj.convertByteArray(valueList[0]))
                for v in valueList[1:]:
                    f = struct.pack("<f", v)
                    newByteArr.extend(f)

                if pos != 0:
                    newByteArr[smfCntIndex] += 1
                else:
                    smfDetailNum += 1
            else:
                newByteArr[smfCntIndex] -= 1
                smfDetailNum += 1

            if smfDetailNum >= len(self.allInfoList[smfNum]["smfDetailList"]):
                index = self.allInfoList[smfNum]["binInfoIndex"]
            else:
                index = self.allInfoList[smfNum]["smfDetailList"][smfDetailNum]["smfDetailIndex"]
            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def updateBinFileOrFlag(self, smfNum, valueList):
        try:
            index = self.allInfoList[smfNum]["smfIndex"]
            newByteArr = self.byteArr[0:index]
            newByteArr.append(len(valueList[0]))
            newByteArr.extend(self.encObj.convertByteArray(valueList[0]))

            oldLen = self.byteArr[index]
            index += 1
            index += oldLen
            startIdx = index

            index = self.allInfoList[smfNum]["binInfoIndex"]
            newByteArr.extend(self.byteArr[startIdx:index])

            newByteArr.append(len(valueList[1]))
            newByteArr.extend(self.encObj.convertByteArray(valueList[1]))
            h = struct.pack("<h", valueList[2])
            newByteArr.extend(h)

            binFileLen = self.byteArr[index]
            index += 1
            index += binFileLen
            index += 2

            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def copy(self, byteArr):
        try:
            index = 16
            newByteArr = self.byteArr[0:index]
            allcnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            index += 2

            allcnt += 1
            h = struct.pack("<h", allcnt)
            newByteArr.extend(h)

            newByteArr.extend(self.byteArr[index:])
            newByteArr.extend(byteArr)

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def delete(self, num):
        try:
            index = 16
            newByteArr = self.byteArr[0:index]
            allcnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            index += 2

            allcnt -= 1
            h = struct.pack("<h", allcnt)
            newByteArr.extend(h)

            smfIndex = self.allInfoList[num]["smfIndex"]
            newByteArr.extend(self.byteArr[index:smfIndex])

            num += 1
            if num < len(self.allInfoList):
                smfNextIndex = self.allInfoList[num]["smfIndex"]
                newByteArr.extend(self.byteArr[smfNextIndex:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def copySaveFile(self, num, copyByteArr):
        try:
            index = 16
            newByteArr = self.byteArr[0:index]
            allcnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            index += 2

            allcnt += 1
            h = struct.pack("<h", allcnt)
            newByteArr.extend(h)

            if num >= len(self.allInfoList):
                newByteArr.extend(self.byteArr[index:])
                newByteArr.extend(copyByteArr)
            else:
                smfIndex = self.allInfoList[num]["smfIndex"]
                newByteArr.extend(self.byteArr[index:smfIndex])

                newByteArr.extend(copyByteArr)
                newByteArr.extend(self.byteArr[smfIndex:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def readSMFSave(self, filename, meshInfoList):
        try:
            smfByteArr = bytearray()
            # 小文字の「.smf」にする
            ext = os.path.splitext(filename)[1]
            filename = os.path.splitext(filename)[0] + ext.lower()
            bFilename = self.encObj.convertByteArray(filename)
            smfByteArr.append(len(bFilename))
            smfByteArr.extend(bFilename)
            allCount = 0
            for meshInfo in meshInfoList:
                allCount += len(meshInfo["mtrlList"])
            smfByteArr.append(allCount)
            smfByteArr.append(0xFF)

            for index, meshInfo in enumerate(meshInfoList):
                mtrlList = meshInfo["mtrlList"]
                for midx, mtrl in enumerate(mtrlList):
                    smfByteArr.append(index)
                    smfByteArr.append(midx)
                    smfByteArr.append(1)
                    smfByteArr.append(1)
                    smfByteArr.append(0)
                    smfByteArr.append(0)

                    diffList = mtrl["diff"]
                    for diff in diffList:
                        fDiff = struct.pack("<f", diff)
                        smfByteArr.extend(fDiff)
                    smfByteArr.append(0)
                    emisList = mtrl["emis"]
                    for emis in emisList:
                        fEmis = struct.pack("<f", emis)
                        smfByteArr.extend(fEmis)
                    smfByteArr.append(0)
                    hNum2 = struct.pack("<h", -1)
                    smfByteArr.extend(hNum2)
                    smfByteArr.append(0)
            smfByteArr.append(0)
            smfByteArr.append(0)
            bFlag = struct.pack("<h", 0)
            smfByteArr.extend(bFlag)

            index = 16
            newByteArr = self.byteArr
            allcnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]

            allcnt += 1
            hAllcnt = struct.pack("<h", allcnt)
            for n in hAllcnt:
                newByteArr[index] = n
                index += 1
            newByteArr.extend(smfByteArr)
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
