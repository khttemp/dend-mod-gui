import os
import struct
import traceback
import program.textSetting as textSetting
from program.encodingClass import SJISEncodingObject
from program.errorLogClass import ErrorLogObj

LS = 0
BS = 1
CS = 2
RS = 3


class FvtConvert:
    def __init__(self, filePath, content):
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.error = ""
        self.content = content
        self.fvtList = []

    def open(self):
        try:
            f = open(self.filePath, encoding=self.encObj.enc)
            lines = f.readlines()
            f.close()
            if not self.makeFvtInfo(lines):
                return False
            return True
        except UnicodeDecodeError:
            self.error = traceback.format_exc()
            return False

    def makeFvtInfo(self, lines):
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
                    faceW = int(arr[2])
                    faceH = int(arr[3])
                    faceX = int(arr[4])
                    faceY = int(arr[5])

                effect = int(arr[contentCnt + 2])
                voNum = int(arr[contentCnt + 3])
            except Exception:
                self.error = textSetting.textList["errorList"]["E11"].format(cnt)
                return False

            text = self.encObj.convertByteArray(arr[contentCnt + 4])
            if text is None:
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

            newLine.extend(self.encObj.convertByteArray(header))
            newLine.extend(struct.pack("<h", faceNum))
            if self.content > LS:
                newLine.extend(struct.pack("<h", faceW))
                newLine.extend(struct.pack("<h", faceH))
                newLine.extend(struct.pack("<h", faceX))
                newLine.extend(struct.pack("<h", faceY))
            newLine.extend(struct.pack("<b", effect))
            newLine.extend(struct.pack("<h", voNum))

            newLine.extend(struct.pack("<h", len(text)))
            newLine.extend(text)

            fvtInfo = {"fvtNum": fvtNum, "info": newLine}
            self.fvtList.append(fvtInfo)

        return True

    def printError(self):
        self.errObj.write(self.error)

    def write(self):
        try:
            for fvt in self.fvtList:
                fvtNum = fvt["fvtNum"]
                path = os.path.join(os.path.dirname(self.filePath), "{0:03}.FVT".format(fvtNum))
                f = open(path, "wb")
                f.write(fvt["info"])
                f.close()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False
