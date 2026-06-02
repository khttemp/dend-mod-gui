import struct
import traceback
import program.sub.textSetting as textSetting
from program.sub.encodingClass import SJISEncodingObject
from program.sub.errorLogClass import ErrorLogObj


headerList = [
    [textSetting.textList["musicEditor"]["bgmNo"], 40],
    [textSetting.textList["musicEditor"]["bsTitle"], 200],
    [textSetting.textList["musicEditor"]["bgmFilename"], 200],
    [textSetting.textList["musicEditor"]["bgmName"], 200],
    [textSetting.textList["musicEditor"]["commonTitle"][0], 120],
    [textSetting.textList["musicEditor"]["commonTitle"][1], 120]
]

ver107Music = [
    "Like A Tunder",
    "Dragon Desier",
    "Burning Blue",
    "ひとつだけ Freedom",
    "Out of Sight",
    "Red Line",
    "Sands of Time 2011",
    "架空 〜Going My Way〜",
    "FullNotch",
    "Rail-Roader's shooting star",
    "Sands of Time 電車でＤ Ver",
    "Power-running",
    "r90",
    "Missin"
]


class BSMusicDecrypt():
    def __init__(self, filePath):
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.headerList = headerList
        self.musicList = []
        self.indexList = []
        self.byteArr = []
        self.error = ""

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
        self.musicList = []
        self.indexList = []
        index = 0
        # ver
        line[index]
        index += 1

        tcnt = line[index]
        index += 1
        for j in range(tcnt):
            # track_time
            struct.unpack("<h", line[index:index + 2])[0]
            index += 2
        # total_time
        struct.unpack("<h", line[index:index + 2])[0]
        index += 2

        musicCnt = line[index]
        index += 1

        for i in range(musicCnt):
            self.indexList.append(index)
            musicArr = []
            musicArr.append(ver107Music[i])

            musicFileNameLen = line[index]
            index += 1
            musicFileName = self.encObj.convertString(line[index:index + musicFileNameLen])
            musicArr.append(musicFileName)
            index += musicFileNameLen

            musicNameLen = line[index]
            index += 1
            musicName = self.encObj.convertString(line[index:index + musicNameLen])
            musicArr.append(musicName)
            index += musicNameLen

            start = struct.unpack("<f", line[index:index + 4])[0]
            start = round(start, 4)
            musicArr.append(start)
            index += 4

            loopEnd = struct.unpack("<f", line[index:index + 4])[0]
            loopEnd = round(loopEnd, 4)
            musicArr.append(loopEnd)
            index += 4

            self.musicList.append(musicArr)
        self.indexList.append(index)

    def saveMusic(self, num, musicInfo):
        try:
            index = self.indexList[num]
            newByteArr = bytearray(self.byteArr[0:index])

            for i, music in enumerate(musicInfo):
                if i > 1:
                    fMusic = struct.pack("<f", music)
                    newByteArr.extend(fMusic)
                else:
                    bName = self.encObj.convertByteArray(music)
                    bNameLen = len(bName)
                    newByteArr.append(bNameLen)
                    newByteArr.extend(bName)

            if num + 1 < len(self.indexList):
                index = self.indexList[num + 1]
                newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def swapMusic(self, num, targetNum):
        try:
            index = self.indexList[0]
            newByteArr = bytearray(self.byteArr[0:index])

            tempMusicList = self.musicList[num]
            self.musicList[num] = self.musicList[targetNum]
            self.musicList[targetNum] = tempMusicList

            for i in range(len(self.musicList)):
                for j in range(2, len(headerList)):
                    if j > 3:
                        fMusic = struct.pack("<f", self.musicList[i][j - 1])
                        newByteArr.extend(fMusic)
                    else:
                        bName = self.encObj.convertByteArray(self.musicList[i][j - 1])
                        bNameLen = len(bName)
                        newByteArr.append(bNameLen)
                        newByteArr.extend(bName)
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
