import csv
import os
import struct
import traceback
import program.sub.textSetting as textSetting
from program.sub.encodingClass import SJISEncodingObject
from program.sub.errorLogClass import ErrorLogObj


class FvtConvert:
    def __init__(self, filePath, game):
        self.LS = 1
        self.BS = 2
        self.CS = 3
        self.RS = 4
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.error = ""
        self.game = game
        self.fvtList = []

    def open(self):
        try:
            if not self.makeFvtInfo():
                return False
            return True
        except UnicodeDecodeError:
            self.error = traceback.format_exc()
            return False
        except Exception:
            self.error = traceback.format_exc()
            return False

    def makeFvtInfo(self):
        count = 0
        self.fvtList = []
        with open(self.filePath, encoding=self.encObj.enc) as f:
            reader = csv.reader(f, doublequote=True)
            
            try:
                count += 1
                next(reader)
            except StopIteration:
                pass

            for row in reader:
                try:
                    fvtNum = int(row[0])
                    fvtNumList = [d["fvtNum"] for d in self.fvtList]
                    if fvtNum in fvtNumList:
                        self.error = textSetting.textList["errorList"]["E10"].format(fvtNum)
                        return False
                    faceNum = int(row[1])

                    contentCnt = 0
                    if self.game > self.LS:
                        contentCnt = 4
                        faceW = int(row[2])
                        faceH = int(row[3])
                        faceX = int(row[4])
                        faceY = int(row[5])

                    effect = int(row[contentCnt + 2])
                    voNum = int(row[contentCnt + 3])
                except Exception:
                    self.error = textSetting.textList["errorList"]["E11"].format(count)
                    return False

                text = self.encObj.convertByteArray(row[contentCnt + 4])
                if text is None:
                    self.error = textSetting.textList["errorList"]["E12"].format(count)
                    return False

                newLine = bytearray()
                header = ""
                if self.game == self.LS:
                    header = "DEND_FVT"
                elif self.game == self.BS:
                    header = "D2_FVT"
                elif self.game == self.CS:
                    header = "D3_FVT"
                elif self.game == self.RS:
                    header = "D4_FVT"

                newLine.extend(self.encObj.convertByteArray(header))
                newLine.extend(struct.pack("<h", faceNum))
                if self.game > self.LS:
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
