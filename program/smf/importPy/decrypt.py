import os
import struct
import copy
import traceback
import math
from fbx import FbxAMatrix
from fbx import FbxVector4
import program.textSetting as textSetting
from program.encodingClass import SJISEncodingObject
from program.errorLogClass import ErrorLogObj


class SmfDecrypt:
    def __init__(self, filePath, frameFlag=False, meshFlag=False, xyzFlag=False, mtrlFlag=False, v_process=None, processBar=None, writeFlag=True):
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.directory = os.path.dirname(self.filePath)
        self.filename = os.path.basename(self.filePath)
        self.originFilename = os.path.splitext(os.path.basename(self.filename))[0] + ".txt"
        self.byteArr = bytearray()
        self.MAX_BONE_COUNT = 40
        self.MAX_NAME_SIZE = 64
        self.index = 0
        #
        self.guid = ""
        self.meshCount = 0
        self.frameCount = 0
        self.animationSetCount = 0
        #
        self.frameStartIdx = 0
        self.meshStartIdx = 0
        self.frameList = []
        self.meshList = []
        self.frameFormatList = [
            "OBB"
        ]
        self.meshFormatList = [
            "OBB",
            "BONE",
            "V_PC",
            "V_N",
            "V_B",
            "V_A",
            "V_UV",
            "IDX2",
            "IDX4",
            "MTRL",
            "C_AT",
            "C_FC",
            "C_VX"
        ]
        self.mtrlFormatList = [
            "TEXC",
            "TEXL",
            "TEXE",
            "TEXS",
            "TEXN",
            "DRAW",
            "ZTES",
            "ZWRI",
            "ATES",
            "ABND",
            "CULL",
            "LGT",
            "DIFF",
            "EMIS",
            "SPEC",
            "BUMP"
        ]
        self.writeFlag = writeFlag
        self.printFRM = frameFlag
        self.printMESH = meshFlag
        self.printXYZ = xyzFlag
        self.printMTRL = mtrlFlag
        self.processFlag = False
        self.v_process = v_process
        self.processBar = processBar
        self.standardGuageList = [
            "H2000_TRACK.SMF",
            "K8000_TRACK.SMF",
            "JR2000_TRACK_LOW2.SMF",
            "K2100_TRACK.SMF",
            "UV_TRACK.SMF",
            "K800_TRACK.SMF",
            "MUTRACK_LOW.SMF",
        ]
        for i in range(len(self.standardGuageList)):
            self.standardGuageList[i] = self.standardGuageList[i].upper()
        self.d4NarrowGuageList = [
            "H2000_Track_LowD4.SMF",
            "K8000_Track_LowD4.SMF",
            "JR2000_Track_LowD4.SMF",
            "KQ2100_Track_LowD4.SMF",
            "UV_Track_LowD4.SMF",
            "K800_Track_LowD4.SMF",
            "",
        ]
        for i in range(len(self.d4NarrowGuageList)):
            self.d4NarrowGuageList[i] = self.d4NarrowGuageList[i].upper()

        self.d4StandardGuageList = [
            "H2000_Track_D4.SMF",
            "K8000_Track_D4.SMF",
            "JR2000_Track_D4.SMF",
            "KQ2100_Track_D4.SMF",
            "UV_Track_D4.SMF",
            "K800_Track_D4.SMF",
            "Mu_Track_D4.SMF",
        ]
        self.adjustFrameList = [
            "LW_POS",
            "RW_POS",
            "FIRE_CENTER",
            "FIRE_R00",
            "FIRE_R01",
            "FIRE_L00",
            "FIRE_L01",
            "R"
        ]
        self.adjustFireLeft = -2.427
        self.adjustFireRight = 2.427
        self.adjustHurikoX = 0.85
        self.adjustMuTrackbaseScale = 2.3 / 1.69
        self.adjustMuTrackbaseDistance = 2.3 - 1.69

        self.texList = set()
        self.lastParentIdx = 0
        self.popFrameByteArr = bytearray()
        self.error = ""

    def open(self):
        try:
            f = open(self.filePath, "rb")
            line = f.read()
            f.close()
            self.byteArr = bytearray(line)
            return self.decrypt()
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        self.errObj.write(self.error)

    def writeInfo(self, text="", end="\n"):
        if self.writeFlag:
            f = open(os.path.join(self.directory, self.originFilename), "a", encoding="utf-8")
            f.write("{0}".format(text).encode().decode("utf-8"))
            f.write(end)
            f.close()

    def decrypt(self):
        self.processFlag = False
        if self.v_process is not None or self.processBar is not None:
            self.processFlag = True
        if self.writeFlag:
            w = open(os.path.join(self.directory, self.originFilename), "w", encoding="utf-8")
            w.close()
        self.texList = set()
        self.frameList = []
        self.meshList = []
        self.index = 0

        nameAndLength = self.getStructNameAndLength()
        if not self.readSMF(nameAndLength[1]):
            return False
        if self.processFlag:
            self.v_process.set(25)
            self.processBar.update()

        self.frameStartIdx = self.index
        for frame in range(self.frameCount):
            nameAndLength = self.getStructNameAndLength()
            if self.printFRM:
                self.writeInfo("="*20)
                self.writeInfo("{0}, 0x{1:02x}".format(nameAndLength[0], nameAndLength[1]))
            if not self.readFRM(frame, nameAndLength[1]):
                return False
            if self.processFlag:
                self.v_process.set(25 + 25 * (frame / self.frameCount))
                self.processBar.update()
        if self.processFlag:
            self.v_process.set(50)
            self.processBar.update()

        self.anisStartIdx = self.index
        for anis in range(self.animationSetCount):
            nameAndLength = self.getStructNameAndLength()
            if self.printFRM:
                self.writeInfo("="*20)
                self.writeInfo("{0}, 0x{1:02x}".format(nameAndLength[0], nameAndLength[1]))
            if not self.readANIS(anis, nameAndLength[1]):
                return False

        self.meshStartIdx = self.index
        self.writeInfo("="*30)
        for mesh in range(self.meshCount):
            nameAndLength = self.getStructNameAndLength()
            if self.printMESH:
                self.writeInfo("="*20)
                self.writeInfo("{0}, 0x{1:02x}".format(nameAndLength[0], nameAndLength[1]))
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return False
            if self.processFlag:
                self.processBar.update()
        if self.processFlag:
            self.v_process.set(100)
            self.processBar.update()
        return True

    def getStructNameAndLength(self):
        index = self.index

        if index >= len(self.byteArr):
            return ("SMF READ END!", 0)
        nameAndLength = struct.unpack("<ll", self.byteArr[index:index+8])
        nameChar4 = str(hex(nameAndLength[0]))[2:]
        index += 4
        index += 4
        nameList = [int(nameChar4[x:x+2], 16) for x in range(0, len(nameChar4), 2)]
        name = ""
        for n in nameList:
            name += chr(n)
        structLen = nameAndLength[1]
        self.index = index
        return (name, structLen)

    def readSMF(self, length):
        index = self.index

        self.guid = hex(struct.unpack("<L", self.byteArr[index:index+4])[0])
        self.writeInfo(textSetting.textList["smf"]["smfVersion"].format(self.guid))
        index += 4

        self.meshCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        self.writeInfo(textSetting.textList["smf"]["meshNum"].format(self.meshCount))
        index += 4

        self.frameCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        self.writeInfo(textSetting.textList["smf"]["frameNum"].format(self.frameCount))
        index += 4

        self.animationSetCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        self.writeInfo(textSetting.textList["smf"]["animeNum"].format(self.animationSetCount))
        index += 4

        if self.index + length == index:
            self.index = index
            return True
        else:
            return False

    def readFRM(self, frame, length):
        index = self.index
        startIndex = self.index
        frameObj = {}

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["frameNumFormat"].format(frame, self.frameCount-1))
            self.writeInfo(textSetting.textList["smf"]["frameMatrixLabel"])

        matrix = []
        for i in range(4):
            rowList = []
            for j in range(4):
                column = struct.unpack("<f", self.byteArr[index:index+4])[0]
                rowList.append(column)
                index += 4
                if self.printFRM:
                    self.writeInfo(column, end=", ")
            matrix.append(rowList)
            if self.printFRM:
                self.writeInfo()
        frameObj["matrix"] = matrix

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["frameName"], end=", ")
        fName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
        fName = self.encObj.convertString(fName).rstrip("\x00")
        frameObj["name"] = fName
        index += self.MAX_NAME_SIZE
        if self.printFRM:
            self.writeInfo(fName)

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["frameMeshIndex"], end=", ")
        meshNo = struct.unpack("<l", self.byteArr[index:index+4])[0]
        frameObj["meshNo"] = meshNo
        index += 4
        if self.printFRM:
            self.writeInfo(meshNo)

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["parentFrameIndex"], end=", ")
        parentFrameNo = struct.unpack("<l", self.byteArr[index:index+4])[0]
        frameObj["parentFrameNo"] = parentFrameNo
        index += 4
        if self.printFRM:
            self.writeInfo(parentFrameNo)

        obbInfo = []
        self.index = index
        if length > 0x88:
            obbNameAndLength = self.getStructNameAndLength()
            index = self.index
            if self.printFRM and obbNameAndLength[0] in self.frameFormatList:
                self.writeInfo("{0}, 0x{1:02x}".format(obbNameAndLength[0], obbNameAndLength[1]))

            vCenter = []
            for i in range(3):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                vCenter.append(vec)
            obbInfo.append(vCenter)
            if self.printFRM:
                self.writeInfo(textSetting.textList["smf"]["vCenterLabel"].format(vCenter))

            vAxisList = []
            for i in range(3):
                vAxis = []
                for j in range(3):
                    axis = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vAxis.append(axis)
                vAxisList.append(vAxis)
                if self.printFRM:
                    self.writeInfo(textSetting.textList["smf"]["vAxisLabel"].format(vAxis))
            obbInfo.append(vAxisList)

            fLength = []
            for i in range(3):
                fLen = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                fLength.append(fLen)
            if self.printFRM:
                self.writeInfo(textSetting.textList["smf"]["fLengthLabel"].format(fLength))
            obbInfo.append(fLength)
        frameObj["obbInfo"] = obbInfo
        self.frameList.append(frameObj)

        if startIndex + length == index:
            self.index = index
            return True
        else:
            return False

    def readANIS(self, anis, length):
        index = self.index
        startIndex = self.index

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["anisNumFormat"].format(anis, self.animationSetCount-1))

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["anisName"], end=", ")
        mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
        mName = self.encObj.convertString(mName).rstrip("\x00")
        index += self.MAX_NAME_SIZE
        if self.printFRM:
            self.writeInfo(mName)

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["anisCount"], end=", ")
        animationCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        index += 4
        if self.printFRM:
            self.writeInfo(animationCount)

        if self.printFRM:
            self.writeInfo(textSetting.textList["smf"]["anisTime"], end=", ")
        lastTime = struct.unpack("<l", self.byteArr[index:index+4])[0]
        index += 4
        if self.printFRM:
            self.writeInfo(lastTime)

        for ani in range(animationCount):
            self.index = index
            nextNameAndLength = self.getStructNameAndLength()

            index = self.index
            subStartIdx = self.index
            if self.printFRM:
                self.writeInfo(textSetting.textList["smf"]["aniNumFormat"].format(nextNameAndLength[0], ani, animationCount-1))

            targetFrame = struct.unpack("<l", self.byteArr[index:index+4])[0]
            index += 4
            if self.printFRM:
                self.writeInfo(textSetting.textList["smf"]["anisTargetFrameIndex"].format(targetFrame))

            keyMaxScale = struct.unpack("<l", self.byteArr[index:index+4])[0]
            index += 4
            keyMaxRotate = struct.unpack("<l", self.byteArr[index:index+4])[0]
            index += 4
            keyMaxTranslate = struct.unpack("<l", self.byteArr[index:index+4])[0]
            index += 4

            for keyScale in range(keyMaxScale):
                keyScaleList = []
                tempL = struct.unpack("<l", self.byteArr[index:index+4])[0]
                keyScaleList.append(tempL)
                index += 4
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    keyScaleList.append(vec)
                    index += 4
                if self.printFRM:
                    self.writeInfo(keyScaleList)

            for keyRotate in range(keyMaxRotate):
                keyRotateList = []
                tempL = struct.unpack("<l", self.byteArr[index:index+4])[0]
                keyRotateList.append(tempL)
                index += 4
                for i in range(4):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    keyRotateList.append(vec)
                    index += 4
                if self.printFRM:
                    self.writeInfo(keyRotateList)

            for keyTransLate in range(keyMaxTranslate):
                keyTransLateList = []
                tempL = struct.unpack("<l", self.byteArr[index:index+4])[0]
                keyTransLateList.append(tempL)
                index += 4
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    keyTransLateList.append(vec)
                    index += 4
                if self.printFRM:
                    self.writeInfo(keyTransLateList)

            if subStartIdx + nextNameAndLength[1] == index:
                self.index = index
            else:
                return False

        if startIndex + length == index:
            self.index = index
            return True
        else:
            return False

    def readMESH(self, mesh, length, meshCountRatio):
        index = self.index
        startIndex = self.index
        subName = ""
        self.meshInfo = {}

        if self.printMESH:
            self.writeInfo(textSetting.textList["smf"]["meshNumFormat"].format(mesh, self.meshCount-1))

        if self.printMESH:
            self.writeInfo(textSetting.textList["smf"]["meshName"], end=", ")
        mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
        mName = self.encObj.convertString(mName).rstrip("\x00")
        self.meshInfo["name"] = mName
        index += self.MAX_NAME_SIZE
        if self.printMESH:
            self.writeInfo(mName)

        if self.printMESH:
            self.writeInfo(textSetting.textList["smf"]["meshMtrlNum"], end=", ")
        materialCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        index += 4
        if self.printMESH:
            self.writeInfo(materialCount)

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        if self.processFlag:
            v_process = self.v_process.get()
        obbInfo = []
        if subName == "OBB":
            index = self.index
            vCenter = []
            for i in range(3):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                vCenter.append(vec)
            obbInfo.append(vCenter)
            if self.printMESH and self.printXYZ:
                self.writeInfo(textSetting.textList["smf"]["vCenterLabel"].format(vCenter))

            vAxisList = []
            for i in range(3):
                vAxis = []
                for j in range(3):
                    axis = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vAxis.append(axis)
                vAxisList.append(vAxis)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vAxisLabel"].format(vAxis))
            obbInfo.append(vAxisList)

            fLength = []
            for i in range(3):
                fLen = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                fLength.append(fLen)
            obbInfo.append(fLength)
            if self.printMESH and self.printXYZ:
                self.writeInfo(textSetting.textList["smf"]["fLengthLabel"].format(fLength))
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        boneList = []
        if subName == "BONE":
            index = self.index

            count = nextNameAndLength[1] // 68
            for i in range(count):
                boneObj = {}
                matrix = []
                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["boneLocalMatrix"])
                for j in range(4):
                    rows = []
                    for k in range(4):
                        column = struct.unpack("<f", self.byteArr[index:index+4])[0]
                        index += 4
                        rows.append(column)
                        if self.printMESH:
                            self.writeInfo(column, end=", ")
                    matrix.append(rows)
                    if self.printMESH:
                        self.writeInfo()
                boneObj["matrixOffset"] = matrix
                if self.printMESH:
                    self.writeInfo()

                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["boneFrameIndex"], end=", ")
                frameNo = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                boneObj["frameNo"] = frameNo
                if self.printMESH:
                    self.writeInfo(frameNo)
                    self.writeInfo()
                boneList.append(boneObj)

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo["boneList"] = boneList
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        coordList = []
        colorInfoList = []
        if subName == "V_PC":
            index = self.index

            count = nextNameAndLength[1] // 16
            if self.printMESH and self.printXYZ:
                self.writeInfo(count)
            for i in range(count):
                vPC = []
                colorInfo = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vPC.append(vec)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vPCLabel"].format(vPC), end=" / ")

                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vPCColor"], end=", ")
                for i in range(4):
                    vPCcolor = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
                    colorInfo.append(vPCcolor)
                    index += 1
                coordList.append(vPC)
                colorInfoList.append(colorInfo)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(colorInfo)
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo["coordList"] = coordList
        self.meshInfo["colorInfoList"] = colorInfoList
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        vNInfo = []
        if subName == "V_N":
            index = self.index

            count = nextNameAndLength[1] // 12
            if self.printMESH and self.printXYZ:
                self.writeInfo(count)
            for i in range(count):
                vN = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vN.append(vec)
                vNInfo.append(vN)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vNLabel"].format(vN))
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo["normalList"] = vNInfo
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        vBInfo = []
        if subName == "V_B":
            index = self.index

            count = nextNameAndLength[1] // 12
            if self.printMESH and self.printXYZ:
                self.writeInfo(count)
            for i in range(count):
                vB = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vB.append(vec)
                vBInfo.append(vB)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vBLabel"].format(vB))
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        vAInfo = []
        if subName == "V_A":
            index = self.index

            count = nextNameAndLength[1] // 8
            if self.printMESH and self.printXYZ:
                self.writeInfo(count)
            for i in range(count):
                f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH and self.printXYZ:
                    self.writeInfo(f, end=", ")

                charList = []
                for j in range(4):
                    charList.append(self.byteArr[index])
                    index += 1
                vAInfo.append([f, charList])
                if self.printMESH and self.printXYZ:
                    self.writeInfo(charList)
            if self.printMESH:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo["boneWeightList"] = vAInfo
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        vUVInfo = []
        if subName == "V_UV":
            index = self.index

            count = nextNameAndLength[1] // 16
            if self.printMESH and self.printXYZ:
                self.writeInfo(count)
            for i in range(count):
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["uvLabel"], end=", ")
                list1 = []
                for j in range(2):
                    f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    list1.append(f)
                vUVInfo.append(list1)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(list1, end=" / ")

                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["lightMapUvLabel"], end=", ")
                list2 = []
                for j in range(2):
                    f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    list2.append(f)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(list2)

            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo["uvList"] = vUVInfo
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        coordIndexList = []
        idx2Info = []
        if subName == "IDX2":
            index = self.index

            count = nextNameAndLength[1] // 2
            if self.printMESH and self.printXYZ:
                self.writeInfo(count)
            for i in range(count):
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["idxLabel"], end=", ")
                h = struct.unpack("<H", self.byteArr[index:index+2])[0]
                index += 2
                idx2Info.append(h)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(h)

            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        if len(idx2Info) > 0:
            coordIndexList.extend(idx2Info)

        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        idx4Info = []
        if subName == "IDX4":
            index = self.index

            count = nextNameAndLength[1] // 4
            if self.printMESH and self.printXYZ:
                self.writeInfo(count)
            for i in range(count):
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["idxLabel"], end=", ")
                long = struct.unpack("<L", self.byteArr[index:index+4])[0]
                index += 4
                idx4Info.append(long)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(long)
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        if len(idx4Info) > 0:
            coordIndexList.extend(idx4Info)
        self.meshInfo["coordIndexList"] = coordIndexList
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        mtrlList = []
        for i in range(materialCount):
            self.index = index
            nextNameAndLength = self.getStructNameAndLength()
            if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
                self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
            if nextNameAndLength[0] in self.meshFormatList:
                subName = nextNameAndLength[0]

            if subName == "MTRL":
                mtrlInfo = self.readMTRL(mesh, i, nextNameAndLength[1])
                if mtrlInfo is None:
                    return False
                index = self.index
                mtrlList.append(mtrlInfo)
                subName = ""

            if materialCount > 1 and i < materialCount - 1:
                if self.printMTRL:
                    self.writeInfo()
        self.meshInfo["mtrlList"] = mtrlList
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        cATInfo = []
        if subName == "C_AT":
            index = self.index

            count = nextNameAndLength[1] // 12
            for i in range(count):
                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["colStart"], end=", ")
                colStart = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colStart)

                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["colCount"], end=", ")
                colCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colCount)

                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["colAttribute"], end=", ")
                colAttribute = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colAttribute)
                cATInfo.append([colStart, colCount, colAttribute])

            if self.index + nextNameAndLength[1] != index:
                return False
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        cFCInfo = []
        if subName == "C_FC":
            index = self.index

            count = nextNameAndLength[1] // 32
            for i in range(count):
                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["colAttribute"], end=", ")
                colAttribute = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colAttribute)

                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["colIndexList"], end=", ")
                indexList = []
                for i in range(3):
                    iindex = struct.unpack("<l", self.byteArr[index:index+4])[0]
                    index += 4
                    indexList.append(iindex)
                if self.printMESH:
                    self.writeInfo(indexList)

                if self.printMESH:
                    self.writeInfo(textSetting.textList["smf"]["plainLabel"], end=", ")
                planeList = []
                for i in range(4):
                    f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    planeList.append(f)
                if self.printMESH:
                    self.writeInfo(planeList)
                cFCInfo.append([colAttribute, indexList, planeList])

            if self.index + nextNameAndLength[1] != index:
                return False
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMESH and nextNameAndLength[0] in self.meshFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}, 0x{1:02x}".format(nextNameAndLength[0], nextNameAndLength[1]))
        if nextNameAndLength[0] in self.meshFormatList:
            subName = nextNameAndLength[0]

        cVXInfo = []
        if subName == "C_VX":
            index = self.index

            count = nextNameAndLength[1] // 28
            for i in range(count):
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vxLabel"], end=", ")
                vecList = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vecList.append(iindex)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(vecList)

                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vxColor"], end=", ")
                colColor = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH and self.printXYZ:
                    self.writeInfo(colColor)

                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vxNLabel"], end=", ")
                vecList = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vecList.append(iindex)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(vecList)
                cVXInfo.append([vecList, colColor, vecList])

            if self.index + nextNameAndLength[1] != index:
                return False
        if self.processFlag:
            v_process += (meshCountRatio / len(self.meshFormatList))
            self.v_process.set(round(v_process))
            self.processBar.update()

        self.meshList.append(self.meshInfo)
        if startIndex + length == index:
            self.index = index
            return True
        else:
            return False

    def readMTRL(self, mesh, mtrl, length):
        index = self.index
        startIndex = self.index
        subName = ""
        mtrlInfo = {}

        if self.printMTRL:
            self.writeInfo("MESH, MTRL:{0}-{1}".format(mesh, mtrl))
            self.writeInfo(textSetting.textList["smf"]["mtrlName"], end=", ")
        mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
        mName = self.encObj.convertString(mName).rstrip("\x00")
        mtrlInfo["name"] = mName
        index += self.MAX_NAME_SIZE
        if self.printMTRL:
            self.writeInfo(mName)

        if self.printMTRL:
            self.writeInfo(textSetting.textList["smf"]["polyStart"], end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo["polyIndexStart"] = long
        index += 4
        if self.printMTRL:
            self.writeInfo(long)

        if self.printMTRL:
            self.writeInfo(textSetting.textList["smf"]["polyCount"], end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo["polyCount"] = long
        index += 4
        if self.printMTRL:
            self.writeInfo(long)

        if self.printMTRL:
            self.writeInfo(textSetting.textList["smf"]["mtrlPStart"], end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo["coordIndexStart"] = long
        index += 4
        if self.printMTRL:
            self.writeInfo(long)

        if self.printMTRL:
            self.writeInfo(textSetting.textList["smf"]["mtrlPCount"], end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo["coordCount"] = long
        index += 4
        if self.printMTRL:
            self.writeInfo(long)

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        texcInfo = []
        if subName == "TEXC":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["texCommon"], end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = self.encObj.convertString(mName).rstrip("\x00")
            mtrlInfo["texc"] = mName
            texcInfo.append(mName)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        self.texList |= set(texcInfo)

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        texlInfo = []
        if subName == "TEXL":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["texLight"], end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = self.encObj.convertString(mName).rstrip("\x00")
            texlInfo.append(mName)
            mtrlInfo["texl"] = mName
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        self.texList |= set(texlInfo)

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        texeInfo = []
        if subName == "TEXE":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["texDds"], end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = self.encObj.convertString(mName).rstrip("\x00")
            texeInfo.append(mName)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        self.texList |= set(texeInfo)

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        texsInfo = []
        if subName == "TEXS":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["texSpe"], end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = self.encObj.convertString(mName).rstrip("\x00")
            texsInfo.append(texsInfo)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        self.texList |= set(texsInfo)

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        texnInfo = []
        if subName == "TEXN":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["texN"], end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = self.encObj.convertString(mName).rstrip("\x00")
            texnInfo.append(mName)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        self.texList |= set(texnInfo)

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        drawInfo = []
        if subName == "DRAW":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["mtrlDraw"], end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            drawInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        ztesInfo = []
        if subName == "ZTES":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["zTest"], end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            ztesInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        zwriInfo = []
        if subName == "ZWRI":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["zWrite"], end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            zwriInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        atesInfo = []
        if subName == "ATES":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["alphaTest"], end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            atesInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        abndInfo = []
        if subName == "ABND":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["alphaBND"], end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            abndInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        cullInfo = []
        if subName == "CULL":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["cull"], end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            cullInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        lgtInfo = []
        if subName == "LGT":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["lgt"], end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            lgtInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        diffInfo = []
        if subName == "DIFF":
            index = self.index

            vecList = []
            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["diffLabel"])
            for i in range(4):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                vecList.append(vec)
                index += 4
                if self.printMTRL:
                    self.writeInfo(vec, end=", ")
            mtrlInfo["diff"] = vecList
            diffInfo.append(vecList)
            if self.printMTRL:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        emisInfo = []
        if subName == "EMIS":
            index = self.index

            vecList = []
            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["emisLabel"])
            for i in range(3):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                vecList.append(vec)
                index += 4
                if self.printMTRL:
                    self.writeInfo(vec, end=", ")
            mtrlInfo["emis"] = vecList
            emisInfo.append(vecList)
            if self.printMTRL:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        specList = []
        if subName == "SPEC":
            index = self.index

            vecList = []
            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["speColor"], end=", ")
            for i in range(3):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                vecList.append(vec)
                index += 4
                if self.printMTRL:
                    self.writeInfo(vec, end=", ")
            mtrlInfo["spec"] = vecList
            if self.printMTRL:
                self.writeInfo()

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["refractive"], end=", ")
            fRefractive = struct.unpack("<f", self.byteArr[index:index+4])[0]
            index += 4
            if self.printMTRL:
                self.writeInfo(fRefractive)

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["roughly"], end=", ")
            fRoughly = struct.unpack("<f", self.byteArr[index:index+4])[0]
            index += 4
            if self.printMTRL:
                self.writeInfo(fRoughly)
            specList.append([vecList, fRefractive, fRoughly])

            if self.index + nextNameAndLength[1] != index:
                return False

        self.index = index
        nextNameAndLength = self.getStructNameAndLength()
        if self.printMTRL and nextNameAndLength[0] in self.mtrlFormatList and subName != nextNameAndLength[0] and nextNameAndLength[1] != 0:
            self.writeInfo("{0}".format(nextNameAndLength[0]), end=", ")
        if nextNameAndLength[0] in self.mtrlFormatList:
            subName = nextNameAndLength[0]

        bumpInfo = []
        if subName == "BUMP":
            index = self.index

            if self.printMTRL:
                self.writeInfo(textSetting.textList["smf"]["bump"], end=", ")
            fParallaxDepth = struct.unpack("<f", self.byteArr[index:index+4])[0]
            bumpInfo.append(fParallaxDepth)
            index += 4
            if self.printMTRL:
                self.writeInfo(fParallaxDepth)

            if self.index + nextNameAndLength[1] != index:
                return False

        if startIndex + length != index:
            return None
        self.index = index
        return mtrlInfo

    def detectGauge(self):
        if self.filename.upper() not in self.standardGuageList:
            return False
        else:
            return True

    def detectMuTrack(self):
        if self.filename.upper() == "MUTRACK_LOW.SMF":
            return True
        else:
            return False

    def getFrameByteArrByName(self, searchFrameName):
        self.index = self.frameStartIdx
        for frame in range(self.frameCount):
            self.frameList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readFRM(frame, nameAndLength[1]):
                return None
            frameInfo = self.frameList[0]
            frameName = frameInfo["name"]
            if frameName == searchFrameName:
                insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                return insertByteArr
        return None

    def getTrackBaseMeshInfo(self):
        self.index = self.meshStartIdx
        for mesh in range(self.meshCount):
            self.meshList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return None
            if mesh == self.meshCount - 1:
                insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                return (insertByteArr, self.meshList[0]["mtrlList"])
        return None

    def createRSTrackbase(self, d4DecryptFile):
        newByteArr = bytearray()
        # MESH
        newByteArr.extend(bytearray([0x48, 0x53, 0x45, 0x4D]))
        meshLengthAddress = len(newByteArr)
        newByteArr.extend(struct.pack("<i", 0))

        getStandardMeshInfo = self.getTrackBaseMeshInfo()
        if getStandardMeshInfo is None:
            return False
        getStandardByteArr = getStandardMeshInfo[0]
        getStandardMtrlList = getStandardMeshInfo[1]
        insertCoordIndex = getStandardMtrlList[2]["coordIndexStart"]
        insertPolyIndex = getStandardMtrlList[2]["polyIndexStart"]

        d4TrackbaseMeshInfo = d4DecryptFile.getTrackBaseMeshInfo()
        if d4TrackbaseMeshInfo is None:
            return False
        d4ByteArr = d4TrackbaseMeshInfo[0]
        d4MtrlList = d4TrackbaseMeshInfo[1]
        d4AddMtrlInfo = d4MtrlList[2]
        d4AddPolyIndexStart = d4AddMtrlInfo["polyIndexStart"]
        d4AddPolyCount = d4AddMtrlInfo["polyCount"]
        d4AddCoordIndexStart = d4AddMtrlInfo["coordIndexStart"]
        d4AddCoordIndexEnd = d4AddCoordIndexStart + d4AddMtrlInfo["coordCount"]
        d4AddCoordCount = d4AddMtrlInfo["coordCount"]

        # Name
        index = 8
        newByteArr.extend(getStandardByteArr[index:index + 64])
        index += 64
        # MtrlCount
        newByteArr.extend(struct.pack("<i", len(d4MtrlList)))
        index += 4
        # OBB
        newByteArr.extend(getStandardByteArr[index:index + 0x44])
        index += 0x44
        # V_PC
        index += 4
        newCoordByteArr = bytearray()
        length = struct.unpack("<i", getStandardByteArr[index:index + 4])[0]
        d4Index = index
        d4Length = struct.unpack("<i", d4ByteArr[d4Index:d4Index + 4])[0]
        index += 4
        d4Index += 4
        newCoordByteArr.extend(getStandardByteArr[index:index + length])
        index += length
        vPCSize = 16
        newCoordByteArr[vPCSize*insertCoordIndex:vPCSize*insertCoordIndex] = d4ByteArr[d4Index + vPCSize*d4AddCoordIndexStart:d4Index + vPCSize*d4AddCoordIndexEnd]
        d4Index += d4Length
        newByteArr.extend(bytearray([0x43, 0x50, 0x5F, 0x56]))
        newByteArr.extend(struct.pack("<i", len(newCoordByteArr)))
        newByteArr.extend(newCoordByteArr)
        # V_N
        index += 4
        d4Index += 4
        newNormalByteArr = bytearray()
        length = struct.unpack("<i", getStandardByteArr[index:index + 4])[0]
        d4Length = struct.unpack("<i", d4ByteArr[d4Index:d4Index + 4])[0]
        index += 4
        d4Index += 4
        newNormalByteArr.extend(getStandardByteArr[index:index + length])
        index += length
        vNSize = 12
        newNormalByteArr[vNSize*insertCoordIndex:vNSize*insertCoordIndex] = d4ByteArr[d4Index + vNSize*d4AddCoordIndexStart:d4Index + vNSize*d4AddCoordIndexEnd]
        d4Index += d4Length
        newByteArr.extend(bytearray([0x4E, 0x5F, 0x56, 0x00]))
        newByteArr.extend(struct.pack("<i", len(newNormalByteArr)))
        newByteArr.extend(newNormalByteArr)
        # V_B
        index += 4
        d4Index += 4
        newVBByteArr = bytearray()
        length = struct.unpack("<i", getStandardByteArr[index:index + 4])[0]
        d4Length = struct.unpack("<i", d4ByteArr[d4Index:d4Index + 4])[0]
        index += 4
        d4Index += 4
        newVBByteArr.extend(getStandardByteArr[index:index + length])
        index += length
        vBSize = 12
        newVBByteArr[vBSize*insertCoordIndex:vBSize*insertCoordIndex] = d4ByteArr[d4Index + vBSize*d4AddCoordIndexStart:d4Index + vBSize*d4AddCoordIndexEnd]
        d4Index += d4Length
        newByteArr.extend(bytearray([0x42, 0x5F, 0x56, 0x00]))
        newByteArr.extend(struct.pack("<i", len(newVBByteArr)))
        newByteArr.extend(newVBByteArr)
        # V_UV
        index += 4
        d4Index += 4
        newUVByteArr = bytearray()
        length = struct.unpack("<i", getStandardByteArr[index:index + 4])[0]
        d4Length = struct.unpack("<i", d4ByteArr[d4Index:d4Index + 4])[0]
        index += 4
        d4Index += 4
        newUVByteArr.extend(getStandardByteArr[index:index + length])
        index += length
        vUVSize = 16
        newUVByteArr[vUVSize*insertCoordIndex:vUVSize*insertCoordIndex] = d4ByteArr[d4Index + vUVSize*d4AddCoordIndexStart:d4Index + vUVSize*d4AddCoordIndexEnd]
        d4Index += d4Length
        newByteArr.extend(bytearray([0x56, 0x55, 0x5F, 0x56]))
        newByteArr.extend(struct.pack("<i", len(newUVByteArr)))
        newByteArr.extend(newUVByteArr)
        # IDX2
        index += 4
        d4Index += 4
        newIdx2Arr = []
        length = struct.unpack("<i", getStandardByteArr[index:index + 4])[0]
        d4Length = struct.unpack("<i", d4ByteArr[d4Index:d4Index + 4])[0]
        index += 4
        d4Index += 4
        idx2Size = 6
        for i in range(length // idx2Size):
            idxList = []
            for j in range(3):
                idx = struct.unpack("<h", getStandardByteArr[index:index + 2])[0]
                index += 2
                if i >= insertPolyIndex:
                    idx += d4AddCoordCount
                idxList.append(idx)
            newIdx2Arr.append(idxList)

        d4MtrlIndex = d4Index + d4Length
        d4Index = d4Index + idx2Size*d4AddPolyIndexStart
        insertNewIdx2Arr = []
        for i in range(d4AddPolyCount):
            idxList = []
            for j in range(3):
                idx = struct.unpack("<h", d4ByteArr[d4Index:d4Index + 2])[0]
                idx = idx - d4AddCoordIndexStart + insertCoordIndex
                idxList.append(idx)
                d4Index += 2
            insertNewIdx2Arr.append(idxList)
        newIdx2Arr[insertPolyIndex:insertPolyIndex] = insertNewIdx2Arr

        newByteArr.extend(bytearray([0x32, 0x58, 0x44, 0x49]))
        newByteArr.extend(struct.pack("<i", len(newIdx2Arr) * 6))
        for idxList in newIdx2Arr:
            for idx in idxList:
                newByteArr.extend(struct.pack("<h", idx))

        # MTRL
        d4Index = d4MtrlIndex
        d4AddMtrlByteArr = bytearray()
        for mtrlNo in range(len(d4MtrlList)):
            d4Length = struct.unpack("<i", d4ByteArr[d4Index + 4:d4Index + 8])[0]
            if mtrlNo == 2:
                d4AddMtrlByteArr = d4ByteArr[d4Index:d4Index + 8 + d4Length]
                iPolyStartIndex = struct.pack("<i", insertPolyIndex)
                for addr, val in enumerate(iPolyStartIndex):
                    d4AddMtrlByteArr[0x48 + addr] = val
                iCoordStartIndex = struct.pack("<i", insertCoordIndex)
                for addr, val in enumerate(iCoordStartIndex):
                    d4AddMtrlByteArr[0x50 + addr] = val
                break
            d4Index += (8 + d4Length)

        for mtrlNo in range(len(getStandardMtrlList)):
            length = struct.unpack("<i", getStandardByteArr[index + 4:index + 8])[0]
            mtrlByteArr = getStandardByteArr[index:index + 8 + length]
            if mtrlNo >= 2:
                polyStartIndex = struct.unpack("<i", mtrlByteArr[0x48:0x48 + 4])[0]
                iPolyStartIndex = struct.pack("<i", polyStartIndex + d4AddPolyCount)
                for addr, val in enumerate(iPolyStartIndex):
                    mtrlByteArr[0x48 + addr] = val
                coordStartIndex = struct.unpack("<i", mtrlByteArr[0x50:0x50 + 4])[0]
                iCoordStartIndex = struct.pack("<i", coordStartIndex + d4AddCoordCount)
                for addr, val in enumerate(iCoordStartIndex):
                    mtrlByteArr[0x50 + addr] = val
            newByteArr.extend(mtrlByteArr)
            index += (8 + length)

            if mtrlNo == 1:
                newByteArr.extend(d4AddMtrlByteArr)

        meshLength = len(newByteArr) - meshLengthAddress - 4
        iMeshLength = struct.pack("<i", meshLength)
        for addr, val in enumerate(iMeshLength):
            newByteArr[meshLengthAddress + addr] = val

        return newByteArr

    def adjustMuHuriko(self, byteArr):
        # OBB
        index = 0x84
        boxXSize = struct.unpack("<f", byteArr[index:index + 4])[0]
        boxXSize += (self.adjustHurikoX * 2)
        fBoxXSize = struct.pack("<f", boxXSize)
        for addr, val in enumerate(fBoxXSize):
            byteArr[index + addr] = val
        index += 12
        # V_PC
        index += 4
        length = struct.unpack("<i", byteArr[index:index + 4])[0]
        index += 4
        for i in range(length // 16):
            coordX = struct.unpack("<f", byteArr[index:index + 4])[0]
            if coordX >= 0:
                coordX += self.adjustHurikoX
            else:
                coordX -= self.adjustHurikoX
            fCoordX = struct.pack("<f", coordX)
            for addr, val in enumerate(fCoordX):
                byteArr[index + addr] = val
            index += 16
        return byteArr

    def adjustMuTrackbase(self, byteArr):
        # OBB
        index = 0x84
        boxXSize = struct.unpack("<f", byteArr[index:index + 4])[0]
        boxXSize *= self.adjustMuTrackbaseScale
        fBoxXSize = struct.pack("<f", boxXSize)
        for addr, val in enumerate(fBoxXSize):
            byteArr[index + addr] = val
        index += 12
        # V_PC
        index += 4
        length = struct.unpack("<i", byteArr[index:index + 4])[0]
        index += 4
        mtrlList = self.meshList[-1]["mtrlList"]
        coordIndex = mtrlList[3]["coordIndexStart"]
        for i in range(length // 16):
            coordX = struct.unpack("<f", byteArr[index:index + 4])[0]
            if i < coordIndex:
                coordX *= self.adjustMuTrackbaseScale
            else:
                if coordX >= 0:
                    coordX += self.adjustMuTrackbaseDistance
                else:
                    coordX -= self.adjustMuTrackbaseDistance
            fCoordX = struct.pack("<f", coordX)
            for addr, val in enumerate(fCoordX):
                byteArr[index + addr] = val
            index += 16
        return byteArr

    def createStandardGauge(self, d4DecryptFile):
        newByteArr = bytearray()

        if self.filename.upper() == "MUTRACK_LOW.SMF":
            newByteArr.extend(self.byteArr[0:self.frameStartIdx])
            self.index = self.frameStartIdx
            for frame in range(self.frameCount):
                self.frameList = []
                startIdx = self.index
                nameAndLength = self.getStructNameAndLength()
                if not self.readFRM(frame, nameAndLength[1]):
                    return False
                frameInfo = self.frameList[0]
                frameName = frameInfo["name"]
                insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                if frameName in self.adjustFrameList and frameName in ["FIRE_R00", "FIRE_R01", "FIRE_L00", "FIRE_L01"]:
                    if frameName in ["FIRE_L00", "FIRE_L01"]:
                        fCoordX = struct.pack("<f", self.adjustFireLeft)
                    else:
                        fCoordX = struct.pack("<f", self.adjustFireRight)
                    for addr, val in enumerate(fCoordX):
                        insertByteArr[0x38 + addr] = val
                newByteArr.extend(insertByteArr)

            self.index = self.meshStartIdx
            for d4Mesh in range(0, 4):
                startIdx = self.index
                nameAndLength = self.getStructNameAndLength()
                if not self.readMESH(d4Mesh, nameAndLength[1], int(50 / self.meshCount)):
                    return False
                insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                newByteArr.extend(insertByteArr)

            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(4, nameAndLength[1], int(50 / self.meshCount)):
                return False
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            newByteArr.extend(self.adjustMuHuriko(insertByteArr))

            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(5, nameAndLength[1], int(50 / self.meshCount)):
                return False
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            newByteArr.extend(self.adjustMuTrackbase(insertByteArr))
        else:
            newByteArr.extend(d4DecryptFile.byteArr[0:d4DecryptFile.frameStartIdx])
            d4DecryptFile.index = d4DecryptFile.frameStartIdx
            for d4Frame in range(d4DecryptFile.frameCount):
                d4DecryptFile.frameList = []
                startIdx = d4DecryptFile.index
                nameAndLength = d4DecryptFile.getStructNameAndLength()
                if not d4DecryptFile.readFRM(d4Frame, nameAndLength[1]):
                    return False
                frameInfo = d4DecryptFile.frameList[0]
                frameName = frameInfo["name"]
                insertByteArr = copy.deepcopy(d4DecryptFile.byteArr[startIdx:d4DecryptFile.index])
                if frameName in self.adjustFrameList:
                    getByteArr = self.getFrameByteArrByName(frameName)
                    if getByteArr is None:
                        return False
                    for b in range(8, 72):
                        insertByteArr[b] = getByteArr[b]
                newByteArr.extend(insertByteArr)

            d4DecryptFile.index = d4DecryptFile.meshStartIdx
            for d4Mesh in range(d4DecryptFile.meshCount):
                d4StartIdx = d4DecryptFile.index
                nameAndLength = d4DecryptFile.getStructNameAndLength()
                if not d4DecryptFile.readMESH(d4Mesh, nameAndLength[1], int(50 / d4DecryptFile.meshCount)):
                    return False
                insertByteArr = copy.deepcopy(d4DecryptFile.byteArr[d4StartIdx:d4DecryptFile.index])
                if d4Mesh == d4DecryptFile.meshCount - 1:
                    newByteArr.extend(self.createRSTrackbase(d4DecryptFile))
                else:
                    newByteArr.extend(insertByteArr)

        newFilename = self.d4StandardGuageList[self.standardGuageList.index(self.filename.upper())]
        w = open(os.path.join(self.directory, newFilename), "wb")
        w.write(newByteArr)
        w.close()
        return True

    def saveSwap(self, frameIdx, parentIdx):
        if not self.deleteFrame(frameIdx, parentIdx, False):
            return False
        if not self.open():
            return False
        if not self.deleteAfterAddFrame(self.lastParentIdx, parentIdx):
            return False
        return True

    def deleteFrame(self, frameIdx, parentIdx, flag=True):
        newByteArr = bytearray()
        self.lastParentIdx = parentIdx
        self.index = self.frameStartIdx
        newByteArr.extend(self.byteArr[0:self.index])

        deleteMeshNo = self.frameList[frameIdx]["meshNo"]
        deleteFrameNo = frameIdx
        deleteMeshCount = 0
        if deleteMeshNo != -1 and flag:
            deleteMeshCount = 1
        deleteFrameCount = 1
        self.popFrameByteArr = bytearray()
        for frame in range(self.frameCount):
            self.frameList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readFRM(frame, nameAndLength[1]):
                return False
            frameInfo = self.frameList[0]
            if frame == frameIdx:
                self.popFrameByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                continue
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            meshNo = frameInfo["meshNo"]
            if meshNo != -1 and meshNo >= deleteMeshNo and flag:
                meshNo -= deleteMeshCount
            parentNo = frameInfo["parentFrameNo"]
            if parentNo == parentIdx:
                self.lastParentIdx = frame
            if parentNo >= deleteFrameNo:
                parentNo -= deleteFrameCount
            startIdx = 8
            startIdx += (64 + 64)
            iMeshNo = struct.pack("<i", meshNo)
            for iM in iMeshNo:
                insertByteArr[startIdx] = iM
                startIdx += 1
            iParentNo = struct.pack("<i", parentNo)
            for iP in iParentNo:
                insertByteArr[startIdx] = iP
                startIdx += 1
            newByteArr.extend(insertByteArr)

        startIdx = 12
        newAllMeshCount = self.meshCount - deleteMeshCount
        iNewAllMeshCount = struct.pack("<i", newAllMeshCount)
        for iN in iNewAllMeshCount:
            newByteArr[startIdx] = iN
            startIdx += 1
        newAllFrameCount = self.frameCount - deleteFrameCount
        iNewAllFrameCount = struct.pack("<i", newAllFrameCount)
        for iN in iNewAllFrameCount:
            newByteArr[startIdx] = iN
            startIdx += 1

        for mesh in range(self.meshCount):
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return False
            if mesh == deleteMeshNo and flag:
                continue
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            newByteArr.extend(insertByteArr)
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def deleteAfterAddFrame(self, frameIdx, parentIdx):
        newByteArr = bytearray()
        self.index = self.frameStartIdx
        newByteArr.extend(self.byteArr[0:self.index])

        addFrameNo = self.frameCount + 1
        addFrameCount = 0
        for frame in range(self.frameCount):
            self.frameList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readFRM(frame, nameAndLength[1]):
                return False
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            frameInfo = self.frameList[0]
            meshNo = frameInfo["meshNo"]
            parentNo = frameInfo["parentFrameNo"]
            if parentNo >= addFrameNo:
                parentNo += addFrameCount
            startIdx = 8
            startIdx += (64 + 64)
            iMeshNo = struct.pack("<i", meshNo)
            for iM in iMeshNo:
                insertByteArr[startIdx] = iM
                startIdx += 1
            iParentNo = struct.pack("<i", parentNo)
            for iP in iParentNo:
                insertByteArr[startIdx] = iP
                startIdx += 1
            newByteArr.extend(insertByteArr)
            if frame == frameIdx:
                startIdx = 8
                startIdx += (64 + 64)
                meshNo = struct.unpack("<i", self.popFrameByteArr[startIdx:startIdx + 4])[0]
                parentNo = parentIdx
                addFrameNo = frameIdx + 1
                addFrameCount += 1

                iMeshNo = struct.pack("<i", meshNo)
                for iM in iMeshNo:
                    self.popFrameByteArr[startIdx] = iM
                    startIdx += 1
                iParentNo = struct.pack("<i", parentNo)
                for iP in iParentNo:
                    self.popFrameByteArr[startIdx] = iP
                    startIdx += 1
                newByteArr.extend(self.popFrameByteArr)

        startIdx = 12
        iNewAllMeshCount = struct.pack("<i", self.meshCount)
        for iN in iNewAllMeshCount:
            newByteArr[startIdx] = iN
            startIdx += 1
        newAllFrameCount = self.frameCount + addFrameCount
        iNewAllFrameCount = struct.pack("<i", newAllFrameCount)
        for iN in iNewAllFrameCount:
            newByteArr[startIdx] = iN
            startIdx += 1

        for mesh in range(self.meshCount):
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return False
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            newByteArr.extend(insertByteArr)
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def addFrame(self, frameIdx, parentIdx):
        newByteArr = bytearray()
        self.index = self.frameStartIdx
        newByteArr.extend(self.byteArr[0:self.index])

        addFrameNo = self.frameCount + 1
        addFrameCount = 0
        for frame in range(self.frameCount):
            self.frameList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readFRM(frame, nameAndLength[1]):
                return False
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            frameInfo = self.frameList[0]
            meshNo = frameInfo["meshNo"]
            parentNo = frameInfo["parentFrameNo"]
            if parentNo >= addFrameNo:
                parentNo += addFrameCount
            startIdx = 8
            startIdx += (64 + 64)
            iMeshNo = struct.pack("<i", meshNo)
            for iM in iMeshNo:
                insertByteArr[startIdx] = iM
                startIdx += 1
            iParentNo = struct.pack("<i", parentNo)
            for iP in iParentNo:
                insertByteArr[startIdx] = iP
                startIdx += 1
            newByteArr.extend(insertByteArr)
            if frame == frameIdx:
                startIdx = 8
                startIdx += (64 + 64)
                meshNo = -1
                parentNo = parentIdx
                addFrameNo = frameIdx + 1
                addFrameCount += 1

                iMeshNo = struct.pack("<i", meshNo)
                for iM in iMeshNo:
                    insertByteArr[startIdx] = iM
                    startIdx += 1
                iParentNo = struct.pack("<i", parentNo)
                for iP in iParentNo:
                    insertByteArr[startIdx] = iP
                    startIdx += 1
                newByteArr.extend(insertByteArr)

        startIdx = 16
        newAllFrameCount = self.frameCount + addFrameCount
        iNewAllFrameCount = struct.pack("<i", newAllFrameCount)
        for iN in iNewAllFrameCount:
            newByteArr[startIdx] = iN
            startIdx += 1

        newByteArr.extend(self.byteArr[self.meshStartIdx:])
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def getQuaternion(self, m):
        tr = m[0][0] + m[1][1] + m[2][2]
        q = [0.0, 0.0, 0.0, 0.0]

        if tr > 0:
            s = 0.5 / math.sqrt(tr + 1.0)
            q[3] = 0.25 / s
            q[0] = (m[2][1] - m[1][2]) * s
            q[1] = (m[0][2] - m[2][0]) * s
            q[2] = (m[1][0] - m[0][1]) * s
        else:
            if (m[0][0] > m[1][1]) and (m[0][0] > m[2][2]):
                s = 2 * math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2])
                q[3] = (m[2][1] - m[1][2]) / s
                q[0] = 0.25 * s
                q[1] = (m[0][1] + m[1][0]) / s
                q[2] = (m[0][2] + m[2][0]) / s
            elif m[1][1] > m[2][2]:
                s = 2 * math.sqrt(1.0 + m[1][1] - m[0][0] - m[2][2])
                q[3] = (m[0][2] - m[2][0]) / s
                q[0] = (m[0][1] + m[1][0]) / s
                q[1] = 0.25 * s
                q[2] = (m[1][2] + m[2][1]) / s
            else:
                s = 2 * math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1])
                q[3] = (m[1][0] - m[0][1]) / s
                q[0] = (m[0][2] + m[2][0]) / s
                q[1] = (m[1][2] + m[2][1]) / s
                q[2] = 0.25 * s

        return q

    def matrixToPos(self, inMat):
        return "{0} {1} {2}".format(inMat[3][0], inMat[3][1], inMat[3][2])

    def matrixToRot(self, inMat):
        q = self.getQuaternion(inMat)
        return "{0} {1} {2} {3}".format(q[0], q[1], q[2], q[3])

    def matrixToPosInfo(self, inMat):
        return [inMat[3][0], inMat[3][1], inMat[3][2]]

    def matrixToEulerAngleInfo(self, inMat):
        if abs(inMat[0][2]) >= 1 - 1e-6:
            pitch = math.pi/2 if inMat[0][2] > 0 else -math.pi/2
            roll = 0
            yaw = math.atan2(inMat[2][1], -inMat[2][2]) if pitch > 0 else math.atan2(-inMat[2][1], inMat[2][2])
        else:
            pitch = math.atan2(inMat[0][2], math.sqrt(inMat[0][0]**2 + inMat[0][1]**2))
            roll = math.atan2(-inMat[1][2] / math.cos(pitch), inMat[2][2] / math.cos(pitch))
            yaw = math.atan2(-inMat[0][1] / math.cos(pitch), inMat[0][0] / math.cos(pitch))
        return [-math.degrees(roll), -math.degrees(pitch), -math.degrees(yaw)]

    def eulerAngleToMatrix(self, rot):
        matrix = FbxAMatrix()
        euler = FbxVector4(rot[0], rot[1], rot[2])
        matrix.SetR(euler)
        resultMatrix = []
        for i in range(3):
            rows = matrix.GetRow(i)
            resultMatrix.append([rows[0], rows[1], rows[2], 0.0])
        return resultMatrix

    def updateFrameInfo(self, frameIdx, varList, deleteFlag):
        newByteArr = bytearray(self.byteArr)
        self.index = self.frameStartIdx

        index = -1
        for frame in range(self.frameCount):
            nameAndLength = self.getStructNameAndLength()
            index = self.index
            if frame == frameIdx:
                break
            if not self.readFRM(frame, nameAndLength[1]):
                return False

        rotInfo = varList[4:7]
        matrix = self.eulerAngleToMatrix(rotInfo)
        for rows in matrix:
            for val in rows:
                fValue = struct.pack("<f", val)
                for f in fValue:
                    newByteArr[index] = f
                    index += 1
        posInfo = copy.deepcopy(varList[1:4])
        posInfo.append(1)
        for pos in posInfo:
            fValue = struct.pack("<f", pos)
            for f in fValue:
                newByteArr[index] = f
                index += 1
        name = varList[0]
        bName = self.encObj.convertByteArray(name)
        for b in bName:
            newByteArr[index] = b
            index += 1
        for b in range(64 - len(bName)):
            newByteArr[index] = 0
            index += 1
        meshNo = varList[7]
        if meshNo > self.meshCount:
            meshNo = self.meshCount
        iValue = struct.pack("<i", meshNo)
        for i in iValue:
            newByteArr[index] = i
            index += 1

        if meshNo >= self.meshCount:
            # MESH
            newByteArr.extend(bytearray([0x48, 0x53, 0x45, 0x4D]))
            newByteArr.extend(struct.pack("<i", 0x44))
            bName = self.encObj.convertByteArray("No Name")
            newByteArr.extend(bName)
            newByteArr.extend([0x00] * (64 - len(bName)))
            newByteArr.extend(struct.pack("<i", 0))

            # meshCount
            iValue = struct.pack("<i", self.meshCount + 1)
            index = 0xC
            for i in iValue:
                newByteArr[index] = i
                index += 1
        if meshNo == -1 and deleteFlag:
            deleteMeshByteArr = bytearray()
            self.index = self.meshStartIdx
            deleteMeshByteArr.extend(newByteArr[:self.index])
            originMeshNo = self.frameList[frameIdx]["meshNo"]
            self.index = self.frameStartIdx
            for frame in range(self.frameCount):
                self.frameList = []
                startIdx = self.index
                nameAndLength = self.getStructNameAndLength()
                if not self.readFRM(frame, nameAndLength[1]):
                    return False
                frameInfo = self.frameList[0]
                frameMeshNo = frameInfo["meshNo"]
                if frameMeshNo != originMeshNo and frameMeshNo != -1:
                    if frameMeshNo > originMeshNo:
                        frameMeshNo -= 1
                        index = startIdx + 0x88
                        iValue = struct.pack("<i", frameMeshNo)
                        for i in iValue:
                            deleteMeshByteArr[index] = i
                            index += 1

            meshStartIdx = -1
            meshEndIdx = -1
            for mesh in range(self.meshCount):
                meshStartIdx = self.index
                nameAndLength = self.getStructNameAndLength()
                if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                    return False
                meshEndIdx = self.index
                if mesh != originMeshNo:
                    deleteMeshByteArr.extend(newByteArr[meshStartIdx:meshEndIdx])
            deleteMeshByteArr.extend(newByteArr[meshEndIdx:])

            iValue = struct.pack("<i", self.meshCount - 1)
            index = 0xC
            for i in iValue:
                deleteMeshByteArr[index] = i
                index += 1
            newByteArr = deleteMeshByteArr

        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def turnModelMesh(self, meshNo):
        self.index = self.meshStartIdx
        newByteArr = bytearray(self.byteArr)
        for mesh in range(self.meshCount):
            if mesh == meshNo:
                break
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return False
        searchIdx = newByteArr.find(self.encObj.convertByteArray("CP_V"), self.index)
        if searchIdx == -1:
            return False
        self.index = searchIdx

        nextNameAndLength = self.getStructNameAndLength()
        count = nextNameAndLength[1] // 16
        index = self.index
        for i in range(count):
            for j in range(3):
                # x座標とz座標のみマイナスを付ける
                if j == 0 or j == 2:
                    b = newByteArr[index+3]
                    # 正の数の場合
                    if b & 0x80 == 0x00:
                        newByteArr[index+3] |= 0x80
                    # 負の数の場合
                    elif b & 0x80 == 0x80:
                        newByteArr[index+3] &= 0x7F
                index += 4
            index += 4

        if self.index + nextNameAndLength[1] != index:
            return False
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def saveSwapMesh(self, meshNo, swapMeshByteArr):
        self.index = self.meshStartIdx
        meshStartIdx = -1
        meshEndIdx = -1
        for mesh in range(self.meshCount):
            if mesh == meshNo:
                meshStartIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return False
            if mesh == meshNo:
                meshEndIdx = self.index
                break
        if meshStartIdx == -1 or meshEndIdx == -1:
            return False
        newByteArr = bytearray(self.byteArr[:meshStartIdx])
        newByteArr.extend(swapMeshByteArr)
        newByteArr.extend(self.byteArr[meshEndIdx:])

        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def getBoxInfo(self, coordList):
        if len(coordList) == 0:
            return [[0, 0, 0], [0, 0, 0]]

        minX = coordList[0][0]
        minY = coordList[0][1]
        minZ = coordList[0][2]
        maxX = coordList[0][0]
        maxY = coordList[0][1]
        maxZ = coordList[0][2]

        for coord in coordList:
            minX = min(minX, coord[0])
            minY = min(minY, coord[1])
            minZ = min(minZ, coord[2])
            maxX = max(maxX, coord[0])
            maxY = max(maxY, coord[1])
            maxZ = max(maxZ, coord[2])

        center = [(minX + maxX)/2, (minY + maxY)/2, (minZ + maxZ)/2]
        boxSize = [(maxX - minX), (maxY - minY), (maxZ - minZ)]
        return [center, boxSize]

    def saveSwapFbxMesh(self, meshNo, meshObj, vertexFlag):
        self.index = self.meshStartIdx
        meshStartIdx = -1
        meshEndIdx = -1
        for mesh in range(self.meshCount):
            if mesh == meshNo:
                meshStartIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return False
            if mesh == meshNo:
                meshEndIdx = self.index
                break
        if meshStartIdx == -1 or meshEndIdx == -1:
            return False
        newByteArr = bytearray(self.byteArr[:meshStartIdx])

        # FbxMesh start
        index = meshStartIdx
        index += 4
        meshAllLengthIndex = index
        index += 4
        index += 64
        materialCountIndex = index
        index += 4

        newByteArr.extend(self.byteArr[meshStartIdx:index])
        # OBB
        newByteArr.extend(bytearray([0x42, 0x42, 0x4F, 0x00]))
        newByteArr.extend(struct.pack("<i", 60))
        boxInfo = self.getBoxInfo(meshObj["coordList"])
        center = boxInfo[0]
        for i in range(3):
            newByteArr.extend(struct.pack("<f", center[i]))

        # XYZ Axis (size 1)
        axisList = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]
        for axis in axisList:
            for i in range(3):
                newByteArr.extend(struct.pack("<f", axis[i]))

        boxSize = boxInfo[1]
        for i in range(3):
            newByteArr.extend(struct.pack("<f", boxSize[i]))

        iMaterialCount = struct.pack("<i", len(meshObj["mtrlList"]))
        for i in range(4):
            newByteArr[materialCountIndex + i] = iMaterialCount[i]

        # V_PC
        newByteArr.extend(bytearray([0x43, 0x50, 0x5F, 0x56]))
        newByteArr.extend(struct.pack("<i", len(meshObj["coordList"]) * 16))
        for cIdx, coord in enumerate(meshObj["coordList"]):
            for i in range(3):
                newByteArr.extend(struct.pack("<f", coord[i]))
            if cIdx >= len(meshObj["colorInfoList"]):
                newByteArr.extend(struct.pack("<i", -1))
            else:
                colorList = meshObj["colorInfoList"][cIdx]
                newByteArr.append(colorList[2])
                newByteArr.append(colorList[1])
                newByteArr.append(colorList[0])
                newByteArr.append(colorList[3])

        # V_N
        newByteArr.extend(bytearray([0x4E, 0x5F, 0x56, 0x00]))
        newByteArr.extend(struct.pack("<i", len(meshObj["normalList"]) * 12))
        for normal in meshObj["normalList"]:
            for i in range(3):
                newByteArr.extend(struct.pack("<f", normal[i]))

        # V_UV
        newByteArr.extend(bytearray([0x56, 0x55, 0x5F, 0x56]))
        newByteArr.extend(struct.pack("<i", len(meshObj["uvList"]) * 16))
        for uv in meshObj["uvList"]:
            for i in range(2):
                for j in range(2):
                    newByteArr.extend(struct.pack("<f", uv[j]))

        # IDX2
        if not vertexFlag:
            newByteArr.extend(bytearray([0x32, 0x58, 0x44, 0x49]))
            newByteArr.extend(struct.pack("<i", len(meshObj["coordIndexList"]) * 6))
            for indexList in meshObj["coordIndexList"]:
                for coordIndex in indexList:
                    newByteArr.extend(struct.pack("<H", coordIndex))
        # IDX4
        else:
            newByteArr.extend(bytearray([0x34, 0x58, 0x44, 0x49]))
            newByteArr.extend(struct.pack("<i", len(meshObj["coordIndexList"]) * 12))
            for indexList in meshObj["coordIndexList"]:
                for coordIndex in indexList:
                    newByteArr.extend(struct.pack("<L", coordIndex))

        # MTRL
        for mtrl in meshObj["mtrlList"]:
            newByteArr.extend(bytearray([0x4C, 0x52, 0x54, 0x4D]))
            mtrlLengthIndex = len(newByteArr)
            newByteArr.extend(struct.pack("<i", 0))
            newByteArr.extend(self.encObj.convertByteArray("Material"))
            newByteArr.extend(bytearray([0x00]*56))
            newByteArr.extend(struct.pack("<i", mtrl["polyIndexStart"]))
            newByteArr.extend(struct.pack("<i", mtrl["polyCount"]))
            newByteArr.extend(struct.pack("<i", 0))
            newByteArr.extend(struct.pack("<i", 0))
            # TEXC
            if mtrl["texc"] != "":
                newByteArr.extend(bytearray([0x43, 0x58, 0x45, 0x54]))
                newByteArr.extend(struct.pack("<i", 64))
                newByteArr.extend(self.encObj.convertByteArray(mtrl["texc"]))
                newByteArr.extend(bytearray([0x00] * (64 - len(self.encObj.convertByteArray(mtrl["texc"])))))
            # DRAW
            newByteArr.extend(bytearray([0x57, 0x41, 0x52, 0x44]))
            newByteArr.extend(struct.pack("<i", 4))
            newByteArr.extend(struct.pack("<i", 0))
            # ZTES
            newByteArr.extend(bytearray([0x53, 0x45, 0x54, 0x5A]))
            newByteArr.extend(struct.pack("<i", 4))
            newByteArr.extend(struct.pack("<i", 1))
            # ZWRI
            newByteArr.extend(bytearray([0x49, 0x52, 0x57, 0x5A]))
            newByteArr.extend(struct.pack("<i", 4))
            newByteArr.extend(struct.pack("<i", 1))
            # ATES
            newByteArr.extend(bytearray([0x53, 0x45, 0x54, 0x41]))
            newByteArr.extend(struct.pack("<i", 4))
            newByteArr.extend(struct.pack("<i", 1))
            # ABND
            newByteArr.extend(bytearray([0x44, 0x4E, 0x42, 0x41]))
            newByteArr.extend(struct.pack("<i", 4))
            newByteArr.extend(struct.pack("<i", 0))
            # CULL
            newByteArr.extend(bytearray([0x4C, 0x4C, 0x55, 0x43]))
            newByteArr.extend(struct.pack("<i", 4))
            newByteArr.extend(struct.pack("<i", 1))
            # LGT
            newByteArr.extend(bytearray([0x54, 0x47, 0x4C, 0x00]))
            newByteArr.extend(struct.pack("<i", 4))
            newByteArr.extend(struct.pack("<i", 1))
            # DIFF
            newByteArr.extend(bytearray([0x46, 0x46, 0x49, 0x44]))
            newByteArr.extend(struct.pack("<i", 16))
            for diff in mtrl["diff"]:
                newByteArr.extend(struct.pack("<f", diff))
            newByteArr.extend(struct.pack("<f", 1.0))
            # EMIS
            newByteArr.extend(bytearray([0x53, 0x49, 0x4D, 0x45]))
            newByteArr.extend(struct.pack("<i", 12))
            for emis in mtrl["emis"]:
                newByteArr.extend(struct.pack("<f", emis))
            mtrlLength = len(newByteArr) - mtrlLengthIndex - 4
            iMtrlLength = struct.pack("<i", mtrlLength)
            for i in range(4):
                newByteArr[mtrlLengthIndex + i] = iMtrlLength[i]
        meshLength = len(newByteArr) - meshAllLengthIndex - 4
        iMeshLength = struct.pack("<i", meshLength)
        for i in range(4):
            newByteArr[meshAllLengthIndex + i] = iMeshLength[i]
        # FbxMesh end
        newByteArr.extend(self.byteArr[meshEndIdx:])
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True