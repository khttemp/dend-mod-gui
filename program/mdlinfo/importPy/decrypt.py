import struct
import traceback


class MdlDecrypt:
    def __init__(self, filePath):
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
        f = open("error.log", "w")
        f.write(self.error)
        f.close()

    def decrypt(self, line):
        self.allInfoList = []
        self.error = ""

        index = 16
        header = line[0:index].decode("shift-jis")
        if header != "MDL_INFO_VER_100":
            self.error = "ヘッダー一致しない"
            raise False

        allcnt = struct.unpack("<h", line[index:index + 2])[0]
        index += 2

        for i in range(allcnt):
            mdlInfo = {}
            mdlInfo["smfIndex"] = index
            smfLen = line[index]
            index += 1
            smfName = line[index:index + smfLen].decode("shift-jis")
            index += smfLen
            mdlInfo["smfName"] = smfName

            mdlcnt = line[index]
            index += 1
            mdlInfo["detailMdlList"] = []
            for j in range(mdlcnt):
                detailMdlInfo = {}
                detailMdlInfo["detailImgIndex"] = index

                b = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                detailMdlInfo["colorCnt"] = b
                index += 1
                detailMdlInfo["textureImgList"] = []
                if j > 0 and b > 0:
                    for k in range(b):
                        imgLen = line[index]
                        index += 1
                        imgName = line[index:index + imgLen].decode("shift-jis")
                        index += imgLen
                        detailMdlInfo["textureImgList"].append(imgName)

                detailMdlInfo["detailTexIndex"] = index
                detailMdlInfo["textureList"] = []
                for k in range(6):
                    b = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                    detailMdlInfo["textureList"].append(b)
                    index += 1

                for k in range(4):
                    f = struct.unpack("<f", line[index:index + 4])[0]
                    f = round(f, 5)
                    detailMdlInfo["textureList"].append(f)
                    index += 4

                detailMdlInfo["textureList"].append(line[index])
                index += 1

                for k in range(3):
                    f = struct.unpack("<f", line[index:index + 4])[0]
                    f = round(f, 5)
                    detailMdlInfo["textureList"].append(f)
                    index += 4

                b = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
                detailMdlInfo["textureList"].append(b)
                index += 1

                h = struct.unpack("<h", line[index:index + 2])[0]
                detailMdlInfo["textureList"].append(h)
                index += 2

                mdlInfo["detailMdlList"].append(detailMdlInfo)

            mdlInfo["imgList"] = []
            mdlInfo["imgIndex"] = index
            imgCnt = struct.unpack("<b", line[index].to_bytes(1, "big"))[0]
            index += 1
            if imgCnt > 0:
                for j in range(imgCnt):
                    imgLen = line[index]
                    index += 1
                    imgName = line[index:index + imgLen].decode("shift-jis")
                    index += imgLen
                    mdlInfo["imgList"].append(imgName)

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
                mdlName = line[index:index + mdlLen].decode("shift-jis")
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
            binFileName = line[index:index + binFileLen].decode("shift-jis")
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
                newByteArr.extend(img.encode("shift-jis"))

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

    def updateTex(self, smfNum, detailInfoNum, varList):
        try:
            index = self.allInfoList[smfNum]["detailMdlList"][detailInfoNum]["detailTexIndex"]
            index += 2
            newByteArr = self.byteArr[0:index]

            varIdx = 0
            for i in range(4):
                b = struct.pack("<b", varList[varIdx])
                newByteArr.extend(b)
                varIdx += 1
                index += 1

            for i in range(4):
                f = struct.pack("<f", varList[varIdx])
                newByteArr.extend(f)
                varIdx += 1
                index += 4

            b = struct.pack("<b", varList[varIdx])
            newByteArr.extend(b)
            varIdx += 1
            index += 1

            for i in range(3):
                f = struct.pack("<f", varList[varIdx])
                newByteArr.extend(f)
                varIdx += 1
                index += 4

            b = struct.pack("<b", varList[varIdx])
            newByteArr.extend(b)
            varIdx += 1
            index += 1

            h = struct.pack("<h", varList[varIdx])
            newByteArr.extend(h)
            varIdx += 1
            index += 2

            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def updateImage(self, smfNum, imgList):
        try:
            index = self.allInfoList[smfNum]["imgIndex"]
            newByteArr = self.byteArr[0:index]

            newByteArr.append(len(imgList))
            for img in imgList:
                newByteArr.append(len(img))
                newByteArr.extend(img.encode("shift-jis"))

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
                newByteArr.extend(valueList[0].encode("shift-jis"))
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
            newByteArr.extend(valueList[0].encode("shift-jis"))

            oldLen = self.byteArr[index]
            index += 1
            index += oldLen
            startIdx = index

            index = self.allInfoList[smfNum]["binInfoIndex"]
            newByteArr.extend(self.byteArr[startIdx:index])

            newByteArr.append(len(valueList[1]))
            newByteArr.extend(valueList[1].encode("shift-jis"))
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

            smfIndex = self.allInfoList[num]["smfIndex"]
            newByteArr.extend(self.byteArr[index:smfIndex])

            newByteArr.extend(copyByteArr)

            if num < len(self.allInfoList):
                smfNextIndex = self.allInfoList[num]["smfIndex"]
                newByteArr.extend(self.byteArr[smfNextIndex:])

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
