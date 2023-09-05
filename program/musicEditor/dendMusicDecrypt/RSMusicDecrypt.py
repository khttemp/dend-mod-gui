import struct
import codecs
import traceback
import program.textSetting as textSetting


headerList = [
    [textSetting.textList["musicEditor"]["bgmNo"], 40],
    [textSetting.textList["musicEditor"]["rsTitle"], 200],
    [textSetting.textList["musicEditor"]["bgmFilename"], 200],
    [textSetting.textList["musicEditor"]["bgmName"], 200],
    [textSetting.textList["musicEditor"]["commonTitle"][0], 120],
    [textSetting.textList["musicEditor"]["commonTitle"][1], 120],
    [textSetting.textList["musicEditor"]["commonTitle"][2], 120]
]

ver108Music = [
    "Memories(RSのSelect曲)",
    "-",  # CS曲
    "-",  # BS曲
    "-",  # LS曲
    "Through The Night",
    "Be Crazy!",
    "INTENSE",
    "APHESIS",
    "Beyond the Limit",
    "Lonely City Lights",
    "DeadlySmile",
    "MOVE OF THE SOUL",
    "Nightmare Labyrinth",
    "Serious Line",
    "Missin2012 -RisingStage-",
    "Jump!Jump!Jump!",
    "Tenderness -starring Nanako-",
    "SUPER GIRL(Single edit)",
    "Chaser",
    "Mass Driver",
    "Tokyo nights feat.Reica (Ver.5150)",
    "Crazy Damn My Heart",
    "Final Blow",
    "Next 2 You",
    "Riding on the sky",
    "-",  # I just wanna stay with you
    "架空 〜Going My Way〜",
    "FullNotch",
    "Rail-Roader's shooting star",
    "Sands of Time 電車でＤ Ver",
    "Power-running",
    "r90",
    "Missin",
    "Like A Tunder",
    "Dragon Desier",
    "Burning Blue",
    "ひとつだけ Freedom",
    "Out of Sight",
    "Red Line",
    "Sands of Time 2011",
    "Foxy Sexy Lady",
    "Ride On Dream",
    "Childie Sharp",
    "Dracula",
    "未来へ繋ぐ道",
    "Missin 2012",
    "Waiting For You",
    "繰り返す日々",
    "Amore",
    "ひとつだけFreedom",
    "SuganoMusic Origunal EUROBEAT Vol.1 Non-Stop Megamix",
    "Can't You Feel My Heart?",
    "Space Movement"
]


class RSMusicDecrypt():
    def __init__(self, filePath):
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
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(self.error)
        w.close()

    def decrypt(self, line):
        self.musicList = []
        self.indexList = []
        index = 0
        # ver
        line[index]
        index += 1

        cdCnt = line[index]
        index += 1

        for i in range(cdCnt):
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

            musicArr.append(ver108Music[i])

            musicFileNameLen = line[index]
            index += 1
            musicFileName = line[index:index + musicFileNameLen].decode("shift-jis")
            musicArr.append(musicFileName)
            index += musicFileNameLen

            musicNameLen = line[index]
            index += 1
            musicName = line[index:index + musicNameLen].decode("shift-jis")
            musicArr.append(musicName)
            index += musicNameLen

            start = struct.unpack("<f", line[index:index + 4])[0]
            start = round(start, 4)
            musicArr.append(start)
            index += 4

            loopStart = struct.unpack("<f", line[index:index + 4])[0]
            loopStart = round(loopStart, 4)
            musicArr.append(loopStart)
            index += 4

            loopEnd = struct.unpack("<f", line[index:index + 4])[0]
            loopEnd = round(loopEnd, 4)
            musicArr.append(loopEnd)
            index += 4

            self.musicList.append(musicArr)
        self.indexList.append(index)

    def saveMusic(self):
        try:
            newByteArr = bytearray(self.byteArr[0:self.indexList[0]])
            title = textSetting.textList["musicEditor"]["commonTitle"]
            for i in range(len(self.musicList)):
                for j in range(2, len(headerList)):
                    if headerList[j][0] in [title[0], title[1], title[2]]:
                        time = struct.pack("<f", self.musicList[i][j - 1])
                        for n in time:
                            newByteArr.append(n)
                    else:
                        name = self.musicList[i][j - 1].encode("shift-jis")
                        nameLen = len(name)
                        newByteArr.append(nameLen)

                        for n in name:
                            newByteArr.append(n)

            newByteArr.extend(self.byteArr[self.indexList[-1]:])
            w = open(self.filePath, "wb")
            w.write(newByteArr)
            w.close()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False
