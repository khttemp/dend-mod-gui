import os
import codecs
import copy
import traceback
import time
from pymem import Pymem
from pymem.process import module_from_name


class GetMemory:
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileDir = os.path.dirname(filePath)
        self.fileName = os.path.basename(filePath)
        self.filenameAndExt = os.path.splitext(os.path.basename(filePath))
        self.railMemory = []
        self.mem = None
        self.game_module = None
        self.error = ""

        self.railMemory = [
            0x000CA558,
            [
                0x30,
                0x38,
                0x840,
                0x350,
                0x108,
                0xF8,
                0x8
            ]
        ]

        self.ambMemory = [
            0x000CA558,
            [
                0x30,
                0x38,
                0x14,
                0xFC,
                0x108,
                0x100,
                0x4
            ]
        ]

        self.rail1pMemory = [
            0x000CA558,
            [
                0x30,
                0x38,
                0x20,
                0x100,
                0x14,
                0xFC,
                0x10
            ]
        ]

        self.rail2pMemory = [
            0x000CA558,
            [
                0xBC,
                0x4,
                0x30,
                0x154,
                0x14,
                0xFC,
                0x10
            ]
        ]

    def open(self):
        try:
            self.mem = Pymem(self.fileName)
            self.game_module = module_from_name(self.mem.process_handle, self.fileName).lpBaseOfDll
        except Exception as e:
            if "Could not find process" in str(e):
                self.error = "ゲームを見つけられませんでした。"
            elif "Could not open process" in str(e):
                self.error = "ゲームのメモリーを参照できません\n管理者権限で実行してください"
            else:
                self.error = "予想外のエラーです\n"
                self.error += traceback.format_exc()
            return False
        return True

    def getRailMemory(self, railNo):
        copyMemoryAddr = copy.deepcopy(self.railMemory)
        copyMemoryAddr[1][-1] += (railNo * 0xC8)

        try:
            railAddr = self.getPtrAddr(self.game_module + copyMemoryAddr[0], copyMemoryAddr[1])
            valList = []
            for i in range(3):
                dirVal = self.mem.read_float(railAddr)
                valList.append(dirVal)
                railAddr += 4

            railAddr += 4
            perVal = self.mem.read_float(railAddr)
            valList.append(perVal)

            return valList
        except Exception:
            self.error = traceback.format_exc()
            return None

    def getAMBMemory(self, ambNo):
        copyMemoryAddr = copy.deepcopy(self.ambMemory)
        copyMemoryAddr[1][-1] += (ambNo * 0x124)

        try:
            ambAddr = self.getPtrAddr(self.game_module + copyMemoryAddr[0], copyMemoryAddr[1])
            valList = []
            length = self.mem.read_float(ambAddr)
            valList.append(length)
            ambAddr += 4

            for i in range(2):
                railVal = self.mem.read_short(ambAddr)
                valList.append(railVal)
                ambAddr += 2

            for i in range(6):
                fVal = self.mem.read_float(ambAddr)
                valList.append(fVal)
                ambAddr += 4
            ambAddr += 8
            for i in range(10):
                fVal = self.mem.read_float(ambAddr)
                valList.append(fVal)
                ambAddr += 4
            ambAddr += 196

            childCount = int.from_bytes(self.mem.read_bytes(ambAddr, 1), "little")
            ambAddr += 4
            childPointerAddr = self.mem.read_int(ambAddr)

            ambAddr = childPointerAddr
            ambAddr += 4
            childValList = []
            for i in range(childCount):
                childList = []
                for j in range(10):
                    fVal = self.mem.read_float(ambAddr)
                    childList.append(fVal)
                    ambAddr += 4
                ambAddr += 200
                childValList.append(childList)
            valList.append(childValList)
            return valList
        except Exception:
            self.error = traceback.format_exc()
            return None

    def saveMemory(self, railNo, valList):
        copyMemoryAddr = copy.deepcopy(self.railMemory)
        copyMemoryAddr[1][-1] += (railNo * 0xC8)

        try:
            railAddr = self.getPtrAddr(self.game_module + copyMemoryAddr[0], copyMemoryAddr[1])
            for i in range(3):
                self.mem.write_float(railAddr, valList[i])
                railAddr += 4

            railAddr += 4
            self.mem.write_float(railAddr, valList[-1])

            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveAMBMemory(self, ambNo, valList, delay=0.3):
        copyMemoryAddr = copy.deepcopy(self.ambMemory)
        copyMemoryAddr[1][-1] += (ambNo * 0x124)

        try:
            ambAddr = self.getPtrAddr(self.game_module + copyMemoryAddr[0], copyMemoryAddr[1])
            lengthAmbAddr = copy.deepcopy(ambAddr)
            lengthValue = valList[0]
            offIdx = 0
            self.mem.write_float(ambAddr, 0.0)
            ambAddr += 4
            offIdx += 1

            for i in range(2):
                self.mem.write_short(ambAddr, valList[offIdx + i])
                ambAddr += 2
            offIdx += 2

            for i in range(6):
                self.mem.write_float(ambAddr, valList[offIdx + i])
                ambAddr += 4
            offIdx += 6
            ambAddr += 8

            for i in range(10):
                self.mem.write_float(ambAddr, valList[offIdx + i])
                ambAddr += 4
            offIdx += 10
            ambAddr += 196

            ambAddr += 4
            childPointerAddr = self.mem.read_int(ambAddr)

            ambAddr = childPointerAddr
            ambAddr += 4
            for valInfo in valList[-1]:
                childList = valInfo
                for j in range(10):
                    self.mem.write_float(ambAddr, childList[j])
                    ambAddr += 4
                ambAddr += 200
            time.sleep(delay)
            self.mem.write_float(lengthAmbAddr, lengthValue)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def getRailPos(self, playerNum):
        if playerNum == 0:
            copyMemoryAddr = copy.deepcopy(self.rail1pMemory)
        elif playerNum == 1:
            copyMemoryAddr = copy.deepcopy(self.rail2pMemory)

        try:
            railAddr = self.getPtrAddr(self.game_module + copyMemoryAddr[0], copyMemoryAddr[1])
            valList = []

            railNum = self.mem.read_short(railAddr)
            valList.append(railNum)
            railAddr += 2

            railPos = self.mem.read_short(railAddr)
            valList.append(railPos)

            return valList
        except Exception:
            self.error = traceback.format_exc()
            return None

    def getPtrAddr(self, address, offsets):
        addr = self.mem.read_int(address)
        for offset in offsets:
            if offset != offsets[-1]:
                addr = self.mem.read_int(addr + offset)
        addr = addr + offsets[-1]
        return addr

    def printError(self):
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(self.error)
        w.close()
