import struct
import traceback

from tkinter import messagebox as mb


class ComicDecrypt:
    def __init__(self, filePath, cmdList):
        self.filePath = filePath
        self.cmdList = cmdList
        self.comicCntIndex = 0
        self.byteArr = []
        self.error = ""
        self.max_param = 1
        self.imgList = []
        self.imgSizeList = []
        self.seList = []
        self.bgmList = []

        self.comicCntIndex = 0
        self.indexList = []
        self.comicDataList = []

    def open(self):
        try:
            f = open(self.filePath, "rb")
            self.byteArr = bytearray(f.read())
            f.close()
            if not self.decrypt():
                return False
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        f = open("error.log", "w")
        f.write(self.error)
        f.close()

    def decrypt(self):
        index = 16
        header = self.byteArr[0:index]
        if header != b'DEND_COMICSCRIPT':
            return False
        index += 1

        self.imgList = []
        imgCnt = self.byteArr[index]
        index += 1
        for i in range(imgCnt):
            b = self.byteArr[index]
            index += 1
            imgName = self.byteArr[index:index+b].decode("shift-jis")
            index += b
            self.imgList.append(imgName)

        self.imgSizeList = []
        imgSizeCnt = self.byteArr[index]
        index += 1
        for i in range(imgSizeCnt):
            imgIndex = self.byteArr[index]
            index += 1
            imgSizeInfo = []
            for j in range(4):
                tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
                tempF = round(tempF, 5)
                imgSizeInfo.append(tempF)
                index += 4
            self.imgSizeList.append([imgIndex, imgSizeInfo])

        self.seList = []
        seCnt = self.byteArr[index]
        index += 1
        for i in range(seCnt):
            b = self.byteArr[index]
            index += 1
            seName = self.byteArr[index:index+b].decode("shift-jis")
            index += b
            seFileCnt = self.byteArr[index]
            index += 1
            self.seList.append([seName, seFileCnt])

        self.bgmList = []
        bgmCnt = self.byteArr[index]
        index += 1
        for i in range(bgmCnt):
            b = self.byteArr[index]
            index += 1
            bgmName = self.byteArr[index:index+b].decode("shift-jis")
            index += b
            bgmFileCnt = self.byteArr[index]
            index += 1
            start = struct.unpack("<f", self.byteArr[index:index+4])[0]
            start = round(start, 5)
            index += 4
            loopStart = struct.unpack("<f", self.byteArr[index:index+4])[0]
            loopStart = round(loopStart, 5)
            index += 4
            self.bgmList.append([bgmName, bgmFileCnt, start, loopStart])

        index += 1
        self.comicCntIndex = index
        comicDataCnt = struct.unpack("<h", self.byteArr[index:index+2])[0]
        index += 2

        self.indexList = []
        self.comicDataList = []

        for i in range(comicDataCnt):
            self.indexList.append(index)
            comicData = []
            num2 = struct.unpack("<h", self.byteArr[index:index+2])[0]
            index += 2
            if num2 < 0 or num2 >= len(self.cmdList)-1:
                errorMsg = "定義されてないコマンド番号です({0})。読込を終了します。".format(num2)
                mb.showerror(title="エラー", message=errorMsg)
                return False
            comicData.append(self.cmdList[num2])
            b = self.byteArr[index]
            index += 1
            if b >= 16:
                b = 16
            if self.max_param < b:
                self.max_param = b
            comicData.append(b)
            for j in range(b):
                f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                f = round(f, 5)
                comicData.append(f)

            self.comicDataList.append(comicData)
        return True

    def saveHeader(self, imgList, imgSizeList, seList, bgmList):
        try:
            index = 17
            newByteArr = bytearray(self.byteArr[0:index])

            newByteArr.append(len(imgList))
            for i in range(len(imgList)):
                newByteArr.append(len(imgList[i]))
                newByteArr.extend(imgList[i].encode("shift-jis"))

            newByteArr.append(len(imgSizeList))
            for i in range(len(imgSizeList)):
                newByteArr.append(imgSizeList[i][0])
                for j in range(4):
                    f = struct.pack("<f", imgSizeList[i][1][j])
                    newByteArr.extend(f)

            newByteArr.append(len(seList))
            for i in range(len(seList)):
                newByteArr.append(len(seList[i][0]))
                newByteArr.extend(seList[i][0].encode("shift-jis"))
                newByteArr.append(seList[i][1])

            newByteArr.append(len(bgmList))
            for i in range(len(bgmList)):
                newByteArr.append(len(bgmList[i][0]))
                newByteArr.extend(bgmList[i][0].encode("shift-jis"))
                newByteArr.append(bgmList[i][1])

                for j in range(2):
                    f = struct.pack("<f", bgmList[i][2+j])
                    newByteArr.extend(f)

            index = self.comicCntIndex - 1
            newByteArr.extend(self.byteArr[index:])

            self.byteArr = newByteArr
            self.save()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveFile(self, mode, num, comicData):
        try:
            if num >= len(self.indexList):
                index = len(self.byteArr)
            else:
                index = self.indexList[num]
            newByteArr = bytearray(self.byteArr[0:index])
            if mode == "modify":
                cmdNum = struct.pack("<h", self.cmdList.index(comicData[0]))
                newByteArr.extend(cmdNum)
                paramCnt = comicData[1]
                newByteArr.append(paramCnt)

                for i in range(paramCnt):
                    f = struct.pack("<f", comicData[2+i])
                    newByteArr.extend(f)

                if num < len(self.indexList) - 1:
                    index = self.indexList[num + 1]
                    newByteArr.extend(self.byteArr[index:])
            elif mode == "insert":
                cmdNum = struct.pack("<h", self.cmdList.index(comicData[0]))
                newByteArr.extend(cmdNum)
                paramCnt = comicData[1]
                newByteArr.append(paramCnt)

                for i in range(paramCnt):
                    f = struct.pack("<f", comicData[2+i])
                    newByteArr.extend(f)

                newByteArr.extend(self.byteArr[index:])

                index = self.comicCntIndex
                comicCnt = struct.pack("<h", len(self.comicDataList) + 1)
                for n in comicCnt:
                    newByteArr[index] = n
                    index += 1
            elif mode == "delete":
                if num < len(self.indexList) - 1:
                    index = self.indexList[num + 1]
                    newByteArr.extend(self.byteArr[index:])

                index = self.comicCntIndex
                comicCnt = struct.pack("<h", len(self.comicDataList) - 1)
                for n in comicCnt:
                    newByteArr[index] = n
                    index += 1

            self.byteArr = newByteArr
            self.save()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveComicList(self, comicDataList):
        try:
            index = self.comicCntIndex
            newByteArr = bytearray(self.byteArr[0:index])

            allCntH = struct.pack("<h", len(comicDataList))
            newByteArr.extend(allCntH)

            for comicData in comicDataList:
                cmdNum = struct.pack("<h", self.cmdList.index(comicData[0]))
                newByteArr.extend(cmdNum)
                paramCnt = comicData[1]
                newByteArr.append(paramCnt)

                for i in range(paramCnt):
                    f = struct.pack("<f", comicData[2+i])
                    newByteArr.extend(f)

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
