import os
import struct
import codecs
import copy
import traceback


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
        self.meshInfo = []
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
        w = open("error.log", "w")
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
            return ('SMF READ END!', 0)
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
        self.writeInfo("SMFバージョン：{0}".format(self.guid))
        index += 4

        self.meshCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        self.writeInfo("メッシュの数：{0}".format(self.meshCount))
        index += 4

        self.frameCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        self.writeInfo("フラームの数：{0}".format(self.frameCount))
        index += 4

        self.animationSetCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        self.writeInfo("アニメーションの数：{0}".format(self.animationSetCount))
        index += 4

        if self.index + length == index:
            self.index = index
            return True
        else:
            return False

    def readFRM(self, frame, length):
        index = self.index
        startIndex = self.index
        frameInfo = []

        if self.printFRM:
            self.writeInfo("Frame No.{0}/{1}".format(frame, self.frameCount-1))
            self.writeInfo("フレーム用変換行列")

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
        frameInfo.append(matrix)

        if self.printFRM:
            self.writeInfo("フレームの名前", end=", ")
        fName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
        fName = fName.decode("shift-jis").rstrip("\x00")
        frameInfo.append(fName)
        index += self.MAX_NAME_SIZE
        if self.printFRM:
            self.writeInfo(fName)

        if self.printFRM:
            self.writeInfo("所持しているメッシュのインデックス", end=", ")
        meshNo = struct.unpack("<l", self.byteArr[index:index+4])[0]
        frameInfo.append(meshNo)
        index += 4
        if self.printFRM:
            self.writeInfo(meshNo)

        if self.printFRM:
            self.writeInfo("親のフレームのインデックス", end=", ")
        parentFrameNo = struct.unpack("<l", self.byteArr[index:index+4])[0]
        frameInfo.append(parentFrameNo)
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
                self.writeInfo("中心座標 {0}".format(vCenter))

            vAxisList = []
            for i in range(3):
                vAxis = []
                for j in range(3):
                    axis = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vAxis.append(axis)
                vAxisList.append(vAxis)
                if self.printFRM:
                    self.writeInfo("ローカルXYZ軸 {0}".format(vAxis))
            obbInfo.append(vAxisList)

            fLength = []
            for i in range(3):
                fLen = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                fLength.append(fLen)
            if self.printFRM:
                self.writeInfo("XYZ軸の長さ {0}".format(fLength))
            obbInfo.append(fLength)
        frameInfo.append(obbInfo)
        self.frameList.append(frameInfo)

        if startIndex + length == index:
            self.index = index
            return True
        else:
            return False

    def readMESH(self, mesh, length, meshCountRatio):
        index = self.index
        startIndex = self.index
        subName = ""
        self.meshInfo = []

        if self.printMESH:
            self.writeInfo("Mesh No.{0}/{1}".format(mesh, self.meshCount-1))

        if self.printMESH:
            self.writeInfo("メッシュの名前", end=", ")
        mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
        mName = mName.decode("shift-jis").rstrip("\x00")
        self.meshInfo.append(mName)
        index += self.MAX_NAME_SIZE
        if self.printMESH:
            self.writeInfo(mName)

        if self.printMESH:
            self.writeInfo("所持しているマテリアルの数", end=", ")
        materialCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
        self.meshInfo.append(materialCount)
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
                self.writeInfo("中心座標 {0}".format(vCenter))

            vAxisList = []
            for i in range(3):
                vAxis = []
                for j in range(3):
                    axis = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vAxis.append(axis)
                vAxisList.append(vAxis)
                if self.printMESH and self.printXYZ:
                    self.writeInfo("ローカルXYZ軸 {0}".format(vAxis))
            obbInfo.append(vAxisList)

            fLength = []
            for i in range(3):
                fLen = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                fLength.append(fLen)
            obbInfo.append(fLength)
            if self.printMESH and self.printXYZ:
                self.writeInfo("XYZ軸の長さ {0}".format(fLength))
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(obbInfo)
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

        boneInfo = []
        if subName == "BONE":
            index = self.index

            count = nextNameAndLength[1] // 68
            for i in range(count):
                matrix = []
                if self.printMESH:
                    self.writeInfo("ボーンのローカルオフセット行列")
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
                boneInfo.append(matrix)
                if self.printMESH:
                    self.writeInfo()

                if self.printMESH:
                    self.writeInfo("骨の対象となるフレームのインデックス", end=", ")
                frameNo = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                boneInfo.append(frameNo)
                if self.printMESH:
                    self.writeInfo(frameNo)
                    self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(boneInfo)
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

        vPCInfo = []
        if subName == "V_PC":
            index = self.index

            count = nextNameAndLength[1] // 16
            for i in range(count):
                vPC = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vPC.append(vec)
                if self.printMESH and self.printXYZ:
                    self.writeInfo("頂点の位置 {0}".format(vPC))

                if self.printMESH and self.printXYZ:
                    self.writeInfo("頂点の色", end=", ")
                vPCcolor = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                vPCInfo.append(vPC)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(vPCcolor)
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(vPCInfo)
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
                    self.writeInfo("頂点の法線 {0}".format(vN))
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(vNInfo)
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
                    self.writeInfo("頂点の接線 {0}".format(vB))
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(vBInfo)
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
        self.meshInfo.append(vAInfo)
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
                    self.writeInfo("頂点のテクスチャUV", end=", ")
                list1 = []
                for j in range(2):
                    f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    list1.append(f)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(list1)

                if self.printMESH and self.printXYZ:
                    self.writeInfo("頂点のライトマップ用テクスチャUV", end=", ")
                list2 = []
                for j in range(2):
                    f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    list2.append(f)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(list2)
                vUVInfo.append([list1, list2])

            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(vUVInfo)
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

        idx2Info = []
        if subName == "IDX2":
            index = self.index

            count = nextNameAndLength[1] // 2
            for i in range(count):
                if self.printMESH and self.printXYZ:
                    self.writeInfo("頂点インデックス", end=", ")
                h = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2
                idx2Info.append(h)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(h)

            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(idx2Info)
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
                    self.writeInfo("頂点インデックス", end=", ")
                long = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                idx4Info.append(long)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(long)
            if self.printMESH and self.printXYZ:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(idx4Info)
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
        self.meshInfo.append(mtrlList)
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
                    self.writeInfo("面の開始位置", end=", ")
                colStart = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colStart)

                if self.printMESH:
                    self.writeInfo("面の数", end=", ")
                colCount = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colCount)

                if self.printMESH:
                    self.writeInfo("面の属性", end=", ")
                colAttribute = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colAttribute)
                cATInfo.append([colStart, colCount, colAttribute])

            if self.index + nextNameAndLength[1] != index:
                return False
        self.meshInfo.append(cATInfo)
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
                    self.writeInfo("面の属性", end=", ")
                colAttribute = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH:
                    self.writeInfo(colAttribute)

                if self.printMESH:
                    self.writeInfo("面を構成する頂点のインデックス", end=", ")
                indexList = []
                for i in range(3):
                    iindex = struct.unpack("<l", self.byteArr[index:index+4])[0]
                    index += 4
                    indexList.append(iindex)
                if self.printMESH:
                    self.writeInfo(indexList)

                if self.printMESH:
                    self.writeInfo("面データ", end=", ")
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
        self.meshInfo.append(cFCInfo)
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
                    self.writeInfo("頂点の位置", end=", ")
                vecList = []
                for i in range(3):
                    vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    vecList.append(iindex)
                if self.printMESH and self.printXYZ:
                    self.writeInfo(vecList)

                if self.printMESH and self.printXYZ:
                    self.writeInfo("頂点の色", end=", ")
                colColor = struct.unpack("<l", self.byteArr[index:index+4])[0]
                index += 4
                if self.printMESH and self.printXYZ:
                    self.writeInfo(colColor)

                if self.printMESH and self.printXYZ:
                    self.writeInfo("頂点の法線", end=", ")
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
        self.meshInfo.append(cVXInfo)
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
        mtrlInfo = []

        if self.printMTRL:
            self.writeInfo("MESH, MTRL:{0}-{1}".format(mesh, mtrl))
            self.writeInfo("マテリアル名", end=", ")
        mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
        mName = mName.decode("shift-jis").rstrip("\x00")
        mtrlInfo.append(mName)
        index += self.MAX_NAME_SIZE
        if self.printMTRL:
            self.writeInfo(mName)

        if self.printMTRL:
            self.writeInfo("ポリゴン開始位置", end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo.append(long)
        index += 4
        if self.printMTRL:
            self.writeInfo(long)

        if self.printMTRL:
            self.writeInfo("ポリゴン数", end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo.append(long)
        index += 4
        if self.printMTRL:
            self.writeInfo(long)

        if self.printMTRL:
            self.writeInfo("頂点開始位置", end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo.append(long)
        index += 4
        if self.printMTRL:
            self.writeInfo(long)

        if self.printMTRL:
            self.writeInfo("頂点数", end=", ")
        long = struct.unpack("<l", self.byteArr[index:index+4])[0]
        mtrlInfo.append(long)
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
                self.writeInfo("テクスチャ名チャンク(通常)", end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = mName.decode("shift-jis").rstrip("\x00")
            texcInfo.append(mName)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(texcInfo)

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
                self.writeInfo("テクスチャ名チャンク(ライトマップ)", end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = mName.decode("shift-jis").rstrip("\x00")
            texlInfo.append(mName)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(texlInfo)

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
                self.writeInfo("テクスチャ名チャンク(DDS)", end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = mName.decode("shift-jis").rstrip("\x00")
            texeInfo.append(mName)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(texeInfo)

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
                self.writeInfo("テクスチャ名チャンク(スペキュラー用)", end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = mName.decode("shift-jis").rstrip("\x00")
            texsInfo.append(texsInfo)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(texsInfo)

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
                self.writeInfo("テクスチャ名チャンク(法線マップ用)", end=", ")
            mName = struct.unpack("<64s", self.byteArr[index:index+self.MAX_NAME_SIZE])[0]
            mName = mName.decode("shift-jis").rstrip("\x00")
            texnInfo.append(mName)
            index += self.MAX_NAME_SIZE
            if self.printMTRL:
                self.writeInfo(mName)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(texnInfo)

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
                self.writeInfo("マテリアルの描画属性", end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            drawInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(drawInfo)

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
                self.writeInfo("Zテスト", end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            ztesInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(ztesInfo)

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
                self.writeInfo("Z書き込み", end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            zwriInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(zwriInfo)

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
                self.writeInfo("アルファテスト", end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            atesInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(atesInfo)

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
                self.writeInfo("アルファテスト(閾値)", end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            abndInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(abndInfo)

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
                self.writeInfo("背面カリング", end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            cullInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(cullInfo)

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
                self.writeInfo("ライティング", end=", ")
            long = struct.unpack("<l", self.byteArr[index:index+4])[0]
            lgtInfo.append(long)
            index += 4
            if self.printMTRL:
                self.writeInfo(long)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(lgtInfo)

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
                self.writeInfo("拡散反射の色")
            for i in range(4):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                vecList.append(vec)
                index += 4
                if self.printMTRL:
                    self.writeInfo(vec, end=", ")
            diffInfo.append(vecList)
            if self.printMTRL:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(diffInfo)

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
                self.writeInfo("自己発光の色")
            for i in range(3):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                vecList.append(vec)
                index += 4
                if self.printMTRL:
                    self.writeInfo(vec, end=", ")
            emisInfo.append(vecList)
            if self.printMTRL:
                self.writeInfo()

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(emisInfo)

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
                self.writeInfo("スペキュラーの色", end=", ")
            for i in range(3):
                vec = struct.unpack("<f", self.byteArr[index:index+4])[0]
                vecList.append(vec)
                index += 4
                if self.printMTRL:
                    self.writeInfo(vec, end=", ")
            if self.printMTRL:
                self.writeInfo()

            if self.printMTRL:
                self.writeInfo("反射率（大きいほど強い反射）", end=", ")
            fRefractive = struct.unpack("<f", self.byteArr[index:index+4])[0]
            index += 4
            if self.printMTRL:
                self.writeInfo(fRefractive)

            if self.printMTRL:
                self.writeInfo("荒さ（大きいほどソフトな反射）", end=", ")
            fRoughly = struct.unpack("<f", self.byteArr[index:index+4])[0]
            index += 4
            if self.printMTRL:
                self.writeInfo(fRoughly)
            specList.append([vecList, fRefractive, fRoughly])

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(specList)

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
                self.writeInfo("視差マップ用の視差", end=", ")
            fParallaxDepth = struct.unpack("<f", self.byteArr[index:index+4])[0]
            bumpInfo.append(fParallaxDepth)
            index += 4
            if self.printMTRL:
                self.writeInfo(fParallaxDepth)

            if self.index + nextNameAndLength[1] != index:
                return False
        mtrlInfo.append(bumpInfo)

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
