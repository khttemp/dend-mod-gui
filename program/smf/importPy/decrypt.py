import os
import struct
import codecs
import copy
import traceback
import math
import program.textSetting as textSetting


class SmfDecrypt:
    def __init__(self, filePath, frameFlag=False, meshFlag=False, xyzFlag=False, mtrlFlag=False, v_process=None, processBar=None, writeFlag=True):
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
        self.d4NarrowGuageList = [
            "H2000_TRACK_LOWD4.SMF",
            "K8000_TRACK_LOWD4.SMF",
            "JR2000_TRACK_LOWD4.SMF",
            "KQ2100_TRACK_LOWD4.SMF",
            "UV_TRACK_LOWD4.SMF",
            "K800_TRACK_LOWD4.SMF",
            "K8000_TRACK.SMF",
        ]
        self.d4StandardGuageList = [
            "H2000_TRACK_D4.SMF",
            "K8000_TRACK_D4.SMF",
            "JR2000_Track_D4.SMF",
            "KQ2100_TRACK_D4.SMF",
            "UV_TRACK_D4.SMF",
            "K800_TRACK_D4.SMF",
            "Mu_Track_D4.SMF",
        ]
        self.texList = set()
        self.lastParentIdx = 0
        self.popFrameByteArr = bytearray()
        self.popMeshByteArr = bytearray()
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
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(self.error)
        w.close()

    def writeInfo(self, text="", end="\n"):
        if self.writeFlag:
            f = codecs.open(os.path.join(self.directory, self.originFilename), "a", "utf-8", "strict")
            f.write("{0}".format(text).encode().decode("utf-8"))
            f.write(end)
            f.close()

    def decrypt(self):
        self.processFlag = False
        if self.v_process is not None or self.processBar is not None:
            self.processFlag = True
        if self.writeFlag:
            w = codecs.open(os.path.join(self.directory, self.originFilename), "w", "utf-8", "strict")
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
        fName = fName.decode("shift-jis").rstrip("\x00")
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
        mName = mName.decode("shift-jis").rstrip("\x00")
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
        mName = mName.decode("shift-jis").rstrip("\x00")
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
            for i in range(count):
                vPC = []
                colorInfo = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vPC.append(vec)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["vPCLabel"].format(vPC))

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
                    self.writeInfo(list1)

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
            for i in range(count):
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["idxLabel"], end=", ")
                h = struct.unpack("<h", self.byteArr[index:index+2])[0]
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
            for i in range(count):
                if self.printMESH and self.printXYZ:
                    self.writeInfo(textSetting.textList["smf"]["idxLabel"], end=", ")
                long = struct.unpack("<l", self.byteArr[index:index+4])[0]
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
        mName = mName.decode("shift-jis").rstrip("\x00")
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
            mName = mName.decode("shift-jis").rstrip("\x00")
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
            mName = mName.decode("shift-jis").rstrip("\x00")
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
            mName = mName.decode("shift-jis").rstrip("\x00")
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
            mName = mName.decode("shift-jis").rstrip("\x00")
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
            mName = mName.decode("shift-jis").rstrip("\x00")
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

    def createStandardGauge(self, d4DecryptFile):
        newByteArr = bytearray()
        self.index = self.frameStartIdx
        newByteArr.extend(self.byteArr[0:self.index])

        deleteMeshCount = 0
        originMeshIndexList = []
        for frame in range(self.frameCount):
            self.frameList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readFRM(frame, nameAndLength[1]):
                return False
            frameInfo = self.frameList[0]
            frameName = frameInfo[1]
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            if frameName in ["Fire0_R_1", "Fire1_R_1", "Fire0_L_1", "Fire1_L_1"]:
                originMeshIndexList.append(frameInfo[2])
                deleteMeshCount += 1
                continue
            elif frameName in ["Fire0_R_0", "Fire1_R_0", "Fire0_L_0", "Fire1_L_0"]:
                if frameName == "Fire0_R_0":
                    startIdx = 8
                    startIdx += 64
                    newFrameName = "Mesh3"
                    for n in newFrameName.encode("shift-jis"):
                        insertByteArr[startIdx] = n
                        startIdx += 1
                    for n in range(64 - len(newFrameName.encode("shift-jis"))):
                        insertByteArr[startIdx] = 0
                        startIdx += 1
                elif frameName == "Fire1_R_0":
                    startIdx = 8
                    startIdx += 64
                    newFrameName = "Mesh4"
                    for n in newFrameName.encode("shift-jis"):
                        insertByteArr[startIdx] = n
                        startIdx += 1
                    for n in range(64 - len(newFrameName.encode("shift-jis"))):
                        insertByteArr[startIdx] = 0
                        startIdx += 1
                elif frameName == "Fire0_L_0":
                    startIdx = 8
                    startIdx += 64
                    newFrameName = "Mesh1"
                    for n in newFrameName.encode("shift-jis"):
                        insertByteArr[startIdx] = n
                        startIdx += 1
                    for n in range(64 - len(newFrameName.encode("shift-jis"))):
                        insertByteArr[startIdx] = 0
                        startIdx += 1
                elif frameName == "Fire1_L_0":
                    startIdx = 8
                    startIdx += 64
                    newFrameName = "Mesh2"
                    for n in newFrameName.encode("shift-jis"):
                        insertByteArr[startIdx] = n
                        startIdx += 1
                    for n in range(64 - len(newFrameName.encode("shift-jis"))):
                        insertByteArr[startIdx] = 0
                        startIdx += 1

            if deleteMeshCount > 0:
                meshNo = frameInfo[2]
                if meshNo != -1:
                    meshNo -= deleteMeshCount
                parentNo = frameInfo[3]
                if parentNo >= 15:
                    parentNo -= deleteMeshCount
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
        newAllFrameCount = self.frameCount - deleteMeshCount
        iNewAllFrameCount = struct.pack("<i", newAllFrameCount)
        for iN in iNewAllFrameCount:
            newByteArr[startIdx] = iN
            startIdx += 1

        if self.filename.upper() == "MUTRACK_LOW.SMF":
            for mesh in range(self.meshCount - 1):
                startIdx = self.index
                nameAndLength = self.getStructNameAndLength()
                if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                    return False
                insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                newByteArr.extend(insertByteArr)

            d4DecryptFile.index = d4DecryptFile.meshStartIdx
            for d4Mesh in range(d4DecryptFile.meshCount):
                d4StartIdx = d4DecryptFile.index
                nameAndLength = d4DecryptFile.getStructNameAndLength()
                if not d4DecryptFile.readMESH(d4Mesh, nameAndLength[1], int(50 / d4DecryptFile.meshCount)):
                    return False
                if d4Mesh == d4DecryptFile.meshCount - 1:
                    insertByteArr = copy.deepcopy(d4DecryptFile.byteArr[d4StartIdx:d4DecryptFile.index])
                    newByteArr.extend(insertByteArr)
        else:
            d4DecryptFile.index = d4DecryptFile.meshStartIdx
            for d4Mesh in range(d4DecryptFile.meshCount - 1):
                d4StartIdx = d4DecryptFile.index
                nameAndLength = d4DecryptFile.getStructNameAndLength()
                if not d4DecryptFile.readMESH(d4Mesh, nameAndLength[1], int(50 / d4DecryptFile.meshCount)):
                    return False
                insertByteArr = copy.deepcopy(d4DecryptFile.byteArr[d4StartIdx:d4DecryptFile.index])
                newByteArr.extend(insertByteArr)

            for mesh in range(self.meshCount):
                startIdx = self.index
                nameAndLength = self.getStructNameAndLength()
                if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                    return False
                if mesh == self.meshCount - 1:
                    insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                    newByteArr.extend(insertByteArr)

        newFilename = self.d4StandardGuageList[self.standardGuageList.index(self.filename)]
        w = open(newFilename, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def saveSwap(self, frameIdx, parentIdx):
        if not self.deleteFrame(frameIdx, parentIdx):
            return False
        if not self.open():
            return False
        if not self.addFrame(self.lastParentIdx, parentIdx):
            return False
        return True

    def deleteFrame(self, frameIdx, parentIdx):
        newByteArr = bytearray()
        self.lastParentIdx = parentIdx
        self.index = self.frameStartIdx
        newByteArr.extend(self.byteArr[0:self.index])

        deleteMeshNo = -1
        deleteFrameNo = -1
        deleteMeshCount = 0
        deleteFrameCount = 0
        self.popFrameByteArr = bytearray()
        self.popMeshByteArr = bytearray()
        for frame in range(self.frameCount):
            self.frameList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readFRM(frame, nameAndLength[1]):
                return False
            frameInfo = self.frameList[0]
            if frame == frameIdx:
                self.popFrameByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                meshNo = frameInfo[2]
                if meshNo != -1:
                    deleteMeshCount += 1
                    deleteMeshNo = meshNo
                deleteFrameCount += 1
                deleteFrameNo = frameIdx
                continue
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            meshNo = frameInfo[2]
            if meshNo != -1 and meshNo >= deleteMeshNo:
                meshNo -= deleteMeshCount
            parentNo = frameInfo[3]
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
            if mesh == deleteMeshNo:
                self.popMeshByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                continue
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

        currentMeshNo = -1
        addMeshNo = self.meshCount + 1
        addFrameNo = self.frameCount + 1
        addMeshCount = 0
        addFrameCount = 0
        for frame in range(self.frameCount):
            self.frameList = []
            startIdx = self.index
            nameAndLength = self.getStructNameAndLength()
            if not self.readFRM(frame, nameAndLength[1]):
                return False
            insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
            frameInfo = self.frameList[0]
            meshNo = frameInfo[2]
            if meshNo != -1 and meshNo >= addMeshNo:
                meshNo += addMeshCount
            if meshNo != -1:
                currentMeshNo = meshNo
            parentNo = frameInfo[3]
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
                if meshNo != -1:
                    meshNo = currentMeshNo + 1
                    addMeshNo = meshNo
                    addMeshCount += 1
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
        newAllMeshCount = self.meshCount + addMeshCount
        iNewAllMeshCount = struct.pack("<i", newAllMeshCount)
        for iN in iNewAllMeshCount:
            newByteArr[startIdx] = iN
            startIdx += 1
        newAllFrameCount = self.frameCount + addFrameCount
        iNewAllFrameCount = struct.pack("<i", newAllFrameCount)
        for iN in iNewAllFrameCount:
            newByteArr[startIdx] = iN
            startIdx += 1

        if self.meshCount == 0:
            newByteArr.extend(self.popMeshByteArr)
        else:
            for mesh in range(self.meshCount):
                startIdx = self.index
                nameAndLength = self.getStructNameAndLength()
                if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                    return False
                insertByteArr = copy.deepcopy(self.byteArr[startIdx:self.index])
                newByteArr.extend(insertByteArr)
                if mesh == currentMeshNo:
                    newByteArr.extend(self.popMeshByteArr)
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        return True

    def getQuaternion(self, m):
        tr = m[0][0] + m[1][1] + m[2][2]
        q = [0.0, 0.0, 0.0, 0.0]

        if tr > 0:
            s = math.sqrt(tr + 1.0) * 2 # S=4*qw
            q[3] = 0.25 * s
            q[0] = m[2][1] - m[1][2]
            q[1] = m[0][2] - m[2][0]
            q[2] = m[1][0] - m[0][1]
        elif (m[0][0] > m[1][1]) and (m[0][0] > m[2][2]):
            s = math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2 # S=4*qx
            q[3] = m[2][1] - m[1][2]
            q[0] = 0.25 * s
            q[1] = m[0][1] + m[1][0]
            q[2] = m[0][2] + m[2][0]
        elif m[1][1] > m[2][2]:
            s = math.sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2 # S=4*qy
            q[3] = m[0][2] - m[2][0]
            q[0] = m[0][1] + m[1][0]
            q[1] = 0.25 * s
            q[2] = m[1][2] + m[2][1]
        else:
            s = math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2 # S=4*qz
            q[3] = m[1][0] - m[0][1]
            q[0] = m[0][2] + m[2][0]
            q[1] = m[1][2] + m[2][1]
            q[2] = 0.25 * s

        return q

    def matrixToPos(self, inMat):
        return "{0} {1} {2}".format(inMat[3][0], inMat[3][1], inMat[3][2])

    def matrixToRot(self, inMat):
        q = self.getQuaternion(inMat)
        return "{0} {1} {2} {3}".format(q[0], q[1], q[2], q[3])

    def turnModelMesh(self, meshNo):
        self.index = self.meshStartIdx
        newByteArr = bytearray(self.byteArr)
        for mesh in range(self.meshCount):
            if mesh == meshNo:
                break
            nameAndLength = self.getStructNameAndLength()
            if not self.readMESH(mesh, nameAndLength[1], int(50 / self.meshCount)):
                return False
        searchIdx = newByteArr.find("CP_V".encode("shift-jis"))
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