import os
import struct
import codecs
import program.textSetting as textSetting

LS = 0
BS = 1
CS = 2
RS = 3


class FvtConvert:
    def __init__(self, filePath, content):
        self.filePath = filePath
        self.error = ""
        self.content = content
        self.fvtList = []

    def open(self):
        try:
            f = open(self.filePath)
            lines = f.readlines()
            f.close()
        except Exception:
            f = codecs.open(self.filePath, "r", "utf-8", "ignore")
            lines = f.readlines()
            f.close()

        lines.pop(0)

        self.fvtList = []
        cnt = 1
        for line in lines:
            cnt += 1
            line = line.strip()
            arr = line.split(",")

            try:
                fvtNum = int(arr[0])
                fvtNumList = [d["fvtNum"] for d in self.fvtList]
                if fvtNum in fvtNumList:
                    self.error = textSetting.textList["errorList"]["E10"].format(fvtNum)
                    return False
                faceNum = int(arr[1])

                contentCnt = 0
                if self.content > LS:
                    contentCnt = 4
                    faceX = int(arr[2])
                    faceY = int(arr[3])
                    faceW = int(arr[4])
                    faceH = int(arr[5])

                effect = int(arr[contentCnt + 2])
                voNum = int(arr[contentCnt + 3])
            except Exception:
                self.error = textSetting.textList["errorList"]["E11"].format(cnt)
                return False

            try:
                text = arr[contentCnt + 4].encode("shift-jis")
            except Exception:
                self.error = textSetting.textList["errorList"]["E12"].format(cnt)
                return False

            newLine = bytearray()
            header = ""
            if self.content == LS:
                header = "DEND_FVT"
            elif self.content == BS:
                header = "D2_FVT"
            elif self.content == CS:
                header = "D3_FVT"
            elif self.content == RS:
                header = "D4_FVT"

            newLine.extend(header.encode("shift-jis"))
            newLine.extend(struct.pack("<h", faceNum))
            if self.content > LS:
                newLine.extend(struct.pack("<h", faceX))
                newLine.extend(struct.pack("<h", faceY))
                newLine.extend(struct.pack("<h", faceW))
                newLine.extend(struct.pack("<h", faceH))
            newLine.extend(struct.pack("<b", effect))
            newLine.extend(struct.pack("<h", voNum))

            newLine.extend(struct.pack("<h", len(text)))
            newLine.extend(text)

            fvtInfo = {"fvtNum": fvtNum, "info": newLine}
            self.fvtList.append(fvtInfo)

        return True

    def write(self):
        for fvt in self.fvtList:
            fvtNum = fvt["fvtNum"]
            path = os.path.join(os.path.dirname(self.filePath), "{0:03}.FVT".format(fvtNum))
            f = open(path, "wb")
            f.write(fvt["info"])
            f.close()
