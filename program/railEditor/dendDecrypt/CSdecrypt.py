import os
import struct
import traceback
import copy
from program.encodingClass import SJISEncodingObject
from program.errorLogClass import ErrorLogObj


class RailDecrypt:
    def __init__(self, filePath):
        self.game = "CS"
        self.encObj = SJISEncodingObject()
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.directory = os.path.dirname(self.filePath)
        self.filename = os.path.splitext(os.path.basename(self.filePath))[0]
        self.byteArr = bytearray()
        self.musicCnt = 0
        self.musicList = []
        self.trainCnt = 0
        self.trainList = []
        self.trainList2 = []
        self.trainList3 = []
        self.stationNo = 0
        self.else1List = []
        self.lightList = []
        self.pngList = []
        self.stationList = []
        self.baseBinList = []
        self.binAnimeList = []
        self.smfList = []
        self.stationNameList = []
        self.cpuList = []
        self.else2List = []
        self.comicScriptList = []
        self.dosansenList = []
        self.railList = []
        self.else3List = []
        self.else4List = []
        self.ambList = []
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

    def decrypt(self):
        self.game = "CS"
        self.ver = ""
        self.musicCnt = 0
        self.musicList = []
        self.trainCnt = 0
        self.trainList = []
        self.trainList2 = []
        self.trainList3 = []
        self.stationNo = 0
        self.else1List = []
        self.lightList = []
        self.pngList = []
        self.stationList = []
        self.baseBinList = []
        self.binAnimeList = []
        self.smfList = []
        self.stationNameList = []
        self.cpuList = []
        self.else2List = []
        self.comicScriptList = []
        self.dosansenList = []
        self.railList = []
        self.else3List = []
        self.else4List = []
        self.ambList = []

        index = 16

        header = self.encObj.convertString(self.byteArr[0:index])
        if header != "DEND_MAP_VER0110":
            return False

        self.ver = header

        # 使う音楽(ダミーデータ?)
        self.musicIdx = index
        self.musicCnt = self.byteArr[index]
        index += 1
        for i in range(self.musicCnt):
            self.musicList.append(self.byteArr[index])
            index += 1

        # 配置する車両カウント
        self.trainCntIdx = index
        self.trainCnt = self.byteArr[index]
        index += 1

        # 3車両の初期レール位置
        for i in range(self.trainCnt):
            trainInfo = []
            railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            trainInfo.append(railNo)
            index += 2
            boneNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            trainInfo.append(boneNo)
            index += 2

            # rail pos unknown
            temp = self.byteArr[index]
            trainInfo.append(temp)
            index += 1

            tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            tempF = round(tempF, 5)
            trainInfo.append(tempF)
            index += 4

            # rail pos unknown
            self.trainList.append(trainInfo)

        self.trainCntIdx2 = index
        trainInfo2 = []
        # ダミー位置？
        railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        trainInfo2.append(railNo)
        index += 2

        boneNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        trainInfo2.append(boneNo)
        index += 2

        temp = self.byteArr[index]
        trainInfo2.append(temp)
        index += 1

        tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
        tempF = round(tempF, 5)
        trainInfo2.append(tempF)
        index += 4

        self.trainList2.append(trainInfo2)

        # 試運転、二人バトルの初期レール位置
        self.trainCntIdx3 = index
        for i in range(2):
            trainInfo3 = []
            railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            trainInfo3.append(railNo)
            index += 2
            boneNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            trainInfo3.append(boneNo)
            index += 2

            # unknown
            temp = self.byteArr[index]
            trainInfo3.append(temp)
            index += 1

            tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            tempF = round(tempF, 5)
            trainInfo3.append(tempF)
            index += 4

            self.trainList3.append(trainInfo3)
            # unknown

        # 駅表示を始める番号
        self.stationNoIndex = index
        self.stationNo = self.byteArr[index]
        index += 1

        # unknown
        self.elseIdx = index
        tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
        tempF = round(tempF, 5)
        self.else1List.append(tempF)
        index += 4

        cnt = self.byteArr[index]
        index += 1
        for i in range(cnt):
            else1Info = []
            for j in range(2):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                else1Info.append(tempF)
                index += 4
            for j in range(3):
                else1Info.append(self.byteArr[index])
                index += 1
            self.else1List.append(else1Info)
        # unknown

        self.lightIdx = index
        # Light情報
        lightCnt = self.byteArr[index]
        index += 1
        for i in range(lightCnt):
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index + b].decode()
            self.lightList.append(text)
            index += b

        # 駅名標画像情報
        self.pngIdx = index
        pngCnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        index += 2
        for i in range(pngCnt):
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index + b].decode()
            self.pngList.append(text)
            index += b

        # 駅名標AMB情報
        self.stationIdx = index
        cnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        index += 2
        for i in range(cnt):
            stationInfo = []
            stationInfo.append(self.byteArr[index])
            index += 1
            for j in range(4):
                tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                stationInfo.append(tempH)
                index += 2
            self.stationList.append(stationInfo)

        # base bin
        self.binIdx = index
        binCnt = self.byteArr[index]
        index += 1
        for i in range(binCnt):
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index + b].decode()
            self.baseBinList.append(text)
            index += b

        # bin ANIME
        self.binAnimeIdx = index
        cnt = self.byteArr[index]
        index += 1
        for i in range(cnt):
            binAnimeInfo = []
            binAnimeInfo.append(self.byteArr[index])
            index += 1
            tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            binAnimeInfo.append(tempH)
            index += 2
            tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            binAnimeInfo.append(tempH)
            index += 2
            self.binAnimeList.append(binAnimeInfo)
        # bin ANIME

        # smf
        self.smfIdx = index
        smfCnt = self.byteArr[index]
        index += 1
        for i in range(smfCnt):
            smfInfo = []
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index + b].decode()
            smfInfo.append(text)
            index += b
            for j in range(5):
                res = self.byteArr[index]
                smfInfo.append(res)
                index += 1
            kasenchu = self.byteArr[index]
            smfInfo.append(kasenchu)
            index += 1
            kasenNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            smfInfo.append(kasenNo)
            index += 2
            self.smfList.append(smfInfo)

        # stationName
        self.stationNameIdx = index
        snameCnt = self.byteArr[index]
        index += 1
        for i in range(snameCnt):
            stationNameInfo = []
            b = self.byteArr[index]
            index += 1
            text = self.encObj.convertString(self.byteArr[index:index + b])
            stationNameInfo.append(text)
            index += b

            stFlag = self.byteArr[index]
            stationNameInfo.append(stFlag)
            index += 1
            railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            stationNameInfo.append(railNo)
            index += 2
            for i in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                stationNameInfo.append(tempF)
                index += 4
            for i in range(3):
                tempI = struct.unpack("<i", self.byteArr[index:index + 4])[0]
                stationNameInfo.append(tempI)
                index += 4
            tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            stationNameInfo.append(tempH)
            index += 2
            self.stationNameList.append(stationNameInfo)

        # unknown
        self.else2Idx = index
        cnt = self.byteArr[index]
        index += 1
        for c in range(cnt):
            elseInfo2 = []
            for i in range(2):
                tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                elseInfo2.append(tempH)
                index += 2
            for i in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                elseInfo2.append(tempF)
                index += 4
            elseInfo2.append(self.byteArr[index])
            index += 1
            self.else2List.append(elseInfo2)
        # unknown

        # cpu
        self.cpuIdx = index
        cpuCnt = self.byteArr[index]
        index += 1
        for i in range(cpuCnt):
            cpuInfo = []
            railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            cpuInfo.append(railNo)
            index += 2

            org = self.byteArr[index]
            index += 1
            cpuInfo.append(org)
            mode = self.byteArr[index]
            index += 1
            cpuInfo.append(mode)

            for j in range(5):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                index += 4
                cpuInfo.append(tempF)
            self.cpuList.append(cpuInfo)

        # comic bin data
        self.comicScriptIdx = index
        comicbinCnt = self.byteArr[index]
        index += 1

        for i in range(comicbinCnt):
            comicScriptInfo = []
            comicNum = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            comicScriptInfo.append(comicNum)
            index += 2
            comicType = self.byteArr[index]
            comicScriptInfo.append(comicType)
            index += 1
            railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            comicScriptInfo.append(railNo)
            index += 2
            self.comicScriptList.append(comicScriptInfo)

        # Dosan data
        self.dosansenIdx = index
        dosanCnt = self.byteArr[index]
        index += 1

        for i in range(dosanCnt):
            dosanInfo = []

            sRailNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(sRailNo)
            index += 2
            sRailFrom = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(sRailFrom)
            index += 2
            sRailTo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(sRailTo)
            index += 2

            eRailNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(eRailNo)
            index += 2
            eRailFrom = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(eRailFrom)
            index += 2
            eRailTo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(eRailTo)
            index += 2

            tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(tempH)
            index += 2

            for j in range(4):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                dosanInfo.append(tempF)
                index += 4

            tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            dosanInfo.append(tempH)
            index += 2

            tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            tempF = round(tempF, 5)
            dosanInfo.append(tempF)
            index += 4

            self.dosansenList.append(dosanInfo)

        self.railIdx = index
        # Map
        mapCnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        index += 2

        for i in range(mapCnt):
            readFlag = False

            railInfo = []
            railInfo.append(i)

            prev_rail = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            railInfo.append(prev_rail)
            index += 2

            if prev_rail == -1:
                readFlag = True

            block = struct.unpack("<b", self.byteArr[index].to_bytes(1, "little"))[0]
            railInfo.append(block)
            index += 1

            for j in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                railInfo.append(tempF)
                index += 4

            mdl_no = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
            railInfo.append(mdl_no)
            index += 1

            mdl_kasen = struct.unpack("<b", self.byteArr[index].to_bytes(1, "little"))[0]
            railInfo.append(mdl_kasen)
            index += 1

            mdl_kasenchu = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
            if mdl_kasenchu in [254, 255]:
                if mdl_kasenchu == 254:
                    mdl_kasenchu = -2
                else:
                    mdl_kasenchu = -1
            railInfo.append(mdl_kasenchu)
            index += 1

            perF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            perF = round(perF, 5)
            railInfo.append(perF)
            index += 4

            for j in range(4):
                flag = self.byteArr[index]
                railInfo.append(flag)
                index += 1

            rail_data = self.byteArr[index]
            railInfo.append(rail_data)
            index += 1

            for j in range(rail_data):
                next_rail = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                railInfo.append(next_rail)
                index += 2
                next_no = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                railInfo.append(next_no)
                index += 2
                prev_rail = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                railInfo.append(prev_rail)
                index += 2
                prev_no = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                railInfo.append(prev_no)
                index += 2

            endcnt = self.byteArr[index]
            index += 1

            else3Info = []
            if endcnt > 0:
                else3Info.append(i)
                tempList = []

                for endc in range(endcnt):
                    tempInfo = []
                    type1 = self.byteArr[index]
                    tempInfo.append(type1)
                    index += 1
                    type2 = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                    tempInfo.append(type2)
                    index += 2
                    binType = self.byteArr[index]
                    tempInfo.append(binType)
                    index += 1
                    for k in range(2):
                        animeNum = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                        tempInfo.append(animeNum)
                        index += 2
                    tempList.append(tempInfo)
                else3Info.append(tempList)
                self.else3List.append(else3Info)
                else3Info = else3Info[1]
            railInfo.append(else3Info)

            else4Info = []
            if readFlag:
                else4Info.append(i)
                prevRail = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                else4Info.append(prevRail)
                index += 2
                for j in range(6):
                    tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                    tempF = round(tempF, 5)
                    else4Info.append(tempF)
                    index += 4
                self.else4List.append(else4Info)
            railInfo.append(else4Info[1:])

            self.railList.append(railInfo)

        self.ambIdx = index
        ambcnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        index += 2

        for i in range(ambcnt):
            ambInfo = []

            # type
            temp = self.byteArr[index]
            ambInfo.append(temp)
            index += 1

            # length
            tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            tempF = round(tempF, 5)
            ambInfo.append(tempF)
            index += 4

            # RailNo, RailPos
            for j in range(2):
                temp = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                ambInfo.append(temp)
                index += 2

            # base pos_xyz base rot_xyz
            for j in range(6):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                ambInfo.append(tempF)
                index += 4

            temp = self.byteArr[index]
            ambInfo.append(temp)
            index += 1

            temp = self.byteArr[index]
            ambInfo.append(temp)
            index += 1

            # mdl_no
            temp = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            ambInfo.append(temp)
            index += 2

            # pos xyz, dir xyz dir2 xyz
            for j in range(9):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                ambInfo.append(tempF)
                index += 4

            # per
            tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            tempF = round(tempF, 5)
            ambInfo.append(tempF)
            index += 4

            # AMB子mdl_no数
            cnta = self.byteArr[index]
            ambInfo.append(cnta)
            index += 1

            for j in range(cnta):
                # mdl_no
                temp = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                ambInfo.append(temp)
                index += 2

                # pos xyz, dir xyz, dir2 xyz
                for k in range(9):
                    tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                    tempF = round(tempF, 5)
                    ambInfo.append(tempF)
                    index += 4

                # per
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                ambInfo.append(tempF)
                index += 4
            self.ambList.append(ambInfo)
        return True

    def extractRailCsv(self, file_path):
        try:
            w = open(file_path, "w")
            w.write("index,prev_rail,block,")
            w.write("dir_x,dir_y,dir_z,")
            w.write("mdl_no,mdl_kasen,mdl_kasenchu,per,")
            w.write("flg,flg,flg,flg,")
            w.write("rail_data,")
            w.write("next_rail,next_no,prev_rail,prev_no,\n")
        except PermissionError:
            return False

        for railInfo in self.railList:
            for i in range(10):
                w.write("{0},".format(railInfo[i]))
            # flg
            for i in range(4):
                w.write("0x{0:02x},".format(railInfo[10 + i]))
            # raildata
            raildata = railInfo[14]
            w.write("{0},".format(raildata))

            for i in range(raildata):
                for j in range(4):
                    w.write("{0},".format(railInfo[15 + 4*i + j]))
            w.write("\n")
        w.close()
        return True

    def extractAmbCsv(self, file_path):
        try:
            w = open(file_path, "w")
            w.write("index,type,length,")
            w.write("rail_no,rail_pos,")
            w.write("base_pos_x,base_pos_y,base_pos_z,")
            w.write("base_dir_x,base_dir_y,base_dir_z,")
            w.write("priority,fog|child count,")
            w.write("mdl_no,")
            w.write("pos_x,pos_y,pos_z,")
            w.write("dir_x,dir_y,dir_z,")
            w.write("dir_x2,dir_y2,dir_z2,")
            w.write("per,\n")
        except PermissionError:
            return False

        for ambIdx, ambInfo in enumerate(self.ambList):
            w.write("{0},".format(ambIdx))
            for i in range(23):
                w.write("{0},".format(ambInfo[i]))
            w.write("\n")
            w.write("," * 12)

            childCount = ambInfo[23]
            w.write("{0},".format(childCount))

            for i in range(childCount):
                for j in range(11):
                    w.write("{0},".format(ambInfo[24 + 11*i + j]))

                if i < (childCount - 1):
                    w.write("\n")
                    w.write("," * 13)
            w.write("\n")
        w.close()
        return True

    def saveMusic(self, cnt):
        try:
            index = self.musicIdx
            newByteArr = self.byteArr[0:index]

            newByteArr.append(cnt)
            for i in range(cnt):
                newByteArr.append(i)

            index = self.trainCntIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveTrainCnt(self, cnt):
        try:
            index = self.trainCntIdx
            index += 1
            newByteArr = bytearray()

            if cnt > self.trainCnt:
                index = self.trainCntIdx2
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - self.trainCnt):
                    tempH = struct.pack("<h", 0)
                    tempF = struct.pack("<f", 0)
                    newByteArr.extend(tempH)
                    newByteArr.extend(tempH)
                    newByteArr.append(1)
                    newByteArr.extend(tempF)
            else:
                for i in range(cnt):
                    index += 2
                    index += 2
                    index += 1
                    index += 4
                newByteArr = self.byteArr[0:index]

            index = self.trainCntIdx2
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.trainCntIdx] = cnt
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveRailPos(self, num, trainList):
        try:
            if num == 0:
                index = self.trainCntIdx
                index += 1
            elif num == 1:
                index = self.trainCntIdx2
            elif num == 2:
                index = self.trainCntIdx3

            newByteArr = self.byteArr[0:index]

            for i in range(len(trainList)):
                trainInfo = trainList[i]
                for j in range(len(trainInfo)):
                    if j == 2:
                        newByteArr.append(trainInfo[j])
                        index += 1
                    elif j == 3:
                        tempF = struct.pack("<f", trainInfo[j])
                        newByteArr.extend(tempF)
                        index += 4
                    else:
                        tempH = struct.pack("<h", trainInfo[j])
                        newByteArr.extend(tempH)
                        index += 2

            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveStationNo(self, num, stationNo):
        try:
            index = self.stationNoIndex

            newByteArr = self.byteArr[0:index]
            newByteArr.append(stationNo)
            index += 1

            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse1List(self, else1List):
        try:
            index = self.elseIdx
            newByteArr = self.byteArr[0:index]

            for i in range(len(else1List)):
                eleInfo = else1List[i]
                if i == 0:
                    eleInfo
                    tempF = struct.pack("<f", eleInfo)
                    newByteArr.extend(tempF)
                    newByteArr.append(4)
                    continue

                for j in range(len(eleInfo)):
                    if j < 2:
                        tempF = struct.pack("<f", eleInfo[j])
                        newByteArr.extend(tempF)
                    else:
                        newByteArr.append(eleInfo[j])

            index = self.lightIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveSimpleList(self, index, listCntVer, simpleList):
        try:
            newByteArr = self.byteArr[0:index]
            if listCntVer == 1:
                newByteArr.append(len(simpleList))
            elif listCntVer == 2:
                tempH = struct.pack("<h", len(simpleList))
                newByteArr.extend(tempH)

            for i in range(len(simpleList)):
                name = simpleList[i]
                newByteArr.append(len(name))
                newByteArr.extend(self.encObj.convertByteArray(name))

            cnt = 0
            if listCntVer == 1:
                cnt = self.byteArr[index]
                index += 1
            elif listCntVer == 2:
                cnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                index += 2

            for i in range(cnt):
                nameLen = self.byteArr[index]
                index += 1
                index += nameLen

            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveStationCnt(self, cnt):
        try:
            index = self.stationIdx
            stationCnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            index += 2

            if cnt > stationCnt:
                index = self.binIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - stationCnt):
                    tempH0 = struct.pack("<h", 0)
                    tempHM1 = struct.pack("<h", -1)
                    tempH100 = struct.pack("<h", 100)
                    newByteArr.append(0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempHM1)
                    newByteArr.extend(tempH100)
                    newByteArr.extend(tempH0)
            else:
                for i in range(cnt):
                    index += 1
                    index += 2
                    index += 2
                    index += 2
                    index += 2
                newByteArr = self.byteArr[0:index]

            index = self.binIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.stationIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveStation(self, valList):
        try:
            index = self.stationIdx
            # stationCnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            index += 2

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j == 0:
                        newByteArr.append(valInfo[j])
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.binIdx
            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveBinAnimeCnt(self, cnt):
        try:
            index = self.binAnimeIdx
            binAnimeCnt = self.byteArr[index]
            index += 1

            if cnt > binAnimeCnt:
                index = self.smfIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - binAnimeCnt):
                    tempH0 = struct.pack("<h", 0)
                    newByteArr.append(1)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempH0)
            else:
                for i in range(cnt):
                    index += 1
                    index += 2
                    index += 2
                newByteArr = self.byteArr[0:index]

            index = self.smfIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.binAnimeIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveBinAnime(self, valList):
        try:
            index = self.binAnimeIdx
            # binAnimeCnt = self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j == 0:
                        newByteArr.append(valInfo[j])
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.smfIdx
            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveSmfInfo(self, num, mode, smfInfo):
        try:
            index = self.smfIdx
            cnt = self.byteArr[index]
            index += 1
            for i in range(num):
                b = self.byteArr[index]
                index += 1
                index += b
                for j in range(5):
                    index += 1
                index += 1
                index += 2

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                newByteArr.append(len(smfInfo[0]))
                newByteArr.extend(self.encObj.convertByteArray(smfInfo[0]))
                for i in range(5):
                    newByteArr.append(smfInfo[1 + i])
                newByteArr.append(smfInfo[6])
                tempH = struct.pack("<h", smfInfo[7])
                newByteArr.extend(tempH)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    for j in range(5):
                        index += 1
                    index += 1
                    index += 2
                else:
                    cnt += 1
            elif mode == "delete":
                b = self.byteArr[index]
                index += 1
                index += b
                for j in range(5):
                    index += 1
                index += 1
                index += 2
                cnt -= 1

            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.smfIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveStationNameInfo(self, num, mode, stationNameInfo):
        try:
            index = self.stationNameIdx
            cnt = self.byteArr[index]
            index += 1
            for i in range(num):
                b = self.byteArr[index]
                index += 1
                index += b
                index += 1
                index += 2
                for j in range(6):
                    index += 4
                index += 2

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                encodeName = self.encObj.convertByteArray(stationNameInfo[0])
                newByteArr.append(len(encodeName))
                newByteArr.extend(encodeName)
                newByteArr.append(int(stationNameInfo[1]))
                tempH = struct.pack("<h", int(stationNameInfo[2]))
                newByteArr.extend(tempH)
                for i in range(3):
                    tempF = struct.pack("<f", float(stationNameInfo[3 + i]))
                    newByteArr.extend(tempF)
                for i in range(3):
                    tempI = struct.pack("<i", int(stationNameInfo[6 + i]))
                    newByteArr.extend(tempI)
                tempH = struct.pack("<h", int(stationNameInfo[9]))
                newByteArr.extend(tempH)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    index += 1
                    index += 2
                    for j in range(6):
                        index += 4
                    index += 2
                else:
                    cnt += 1
            elif mode == "delete":
                b = self.byteArr[index]
                index += 1
                index += b
                index += 1
                index += 2
                for j in range(6):
                    index += 4
                index += 2
                cnt -= 1

            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.stationNameIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse2Cnt(self, cnt):
        try:
            index = self.else2Idx
            else2Cnt = self.byteArr[index]
            index += 1

            if cnt > else2Cnt:
                index = self.cpuIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - else2Cnt):
                    tempH0 = struct.pack("<h", 0)
                    tempF0 = struct.pack("<f", 0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempF0)
                    newByteArr.extend(tempF0)
                    newByteArr.extend(tempF0)
                    newByteArr.append(0)
            else:
                for i in range(cnt):
                    index += 2
                    index += 2
                    index += 4
                    index += 4
                    index += 4
                    index += 1
                newByteArr = self.byteArr[0:index]

            index = self.cpuIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.else2Idx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse2List(self, valList):
        try:
            index = self.else2Idx
            # else2Cnt = self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j in [2, 3, 4]:
                        tempF = struct.pack("<f", valInfo[j])
                        newByteArr.extend(tempF)
                    elif j == 5:
                        newByteArr.append(valInfo[j])
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.cpuIdx
            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveCpuInfo(self, num, mode, smfInfo):
        try:
            index = self.cpuIdx
            cnt = self.byteArr[index]
            index += 1
            for i in range(num):
                index += 2
                index += 1
                index += 1
                for j in range(5):
                    index += 4

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                tempH = struct.pack("<h", smfInfo[0])
                newByteArr.extend(tempH)
                newByteArr.append(smfInfo[1])
                newByteArr.append(smfInfo[2])
                for i in range(5):
                    tempF = struct.pack("<f", smfInfo[3 + i])
                    newByteArr.extend(tempF)

                if mode == "modify":
                    index += 2
                    index += 1
                    index += 1
                    for j in range(5):
                        index += 4
                else:
                    cnt += 1
            elif mode == "delete":
                index += 2
                index += 1
                index += 1
                for j in range(5):
                    index += 4
                cnt -= 1

            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.cpuIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveComicScriptList(self, comicScriptList):
        try:
            index = self.comicScriptIdx
            newByteArr = self.byteArr[0:index]

            newByteArr.append(len(comicScriptList))
            for i in range(len(comicScriptList)):
                comicScriptInfo = comicScriptList[i]
                for j in range(len(comicScriptInfo)):
                    if j == 1:
                        newByteArr.append(comicScriptInfo[j])
                    else:
                        tempH = struct.pack("<h", comicScriptInfo[j])
                        newByteArr.extend(tempH)

            index = self.dosansenIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveDosansenCnt(self, cnt):
        try:
            index = self.dosansenIdx
            dosansenCnt = self.byteArr[index]
            index += 1

            if cnt > dosansenCnt:
                index = self.railIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - dosansenCnt):
                    tempH0 = struct.pack("<h", 0)
                    tempF0 = struct.pack("<f", 0)
                    for j in range(7):
                        newByteArr.extend(tempH0)
                    for j in range(4):
                        newByteArr.extend(tempF0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempF0)
            else:
                for i in range(cnt):
                    for j in range(7):
                        index += 2
                    for j in range(4):
                        index += 4
                    index += 2
                    index += 4
                newByteArr = self.byteArr[0:index]

            index = self.railIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.dosansenIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveDosansenList(self, valList):
        try:
            index = self.dosansenIdx
            # dosansenCnt = self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j in [7, 8, 9, 10, 12]:
                        tempF = struct.pack("<f", valInfo[j])
                        newByteArr.extend(tempF)
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.railIdx
            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveRailCsv(self, railList):
        try:
            index = self.railIdx
            newByteArr = self.byteArr[0:index]

            railCnt = len(railList)
            railCntH = struct.pack("<h", railCnt)
            newByteArr.extend(railCntH)

            for i in range(len(railList)):
                railInfo = railList[i]

                prev_rail = railInfo[0]
                prev_railH = struct.pack("<h", prev_rail)
                newByteArr.extend(prev_railH)

                block = struct.pack("<b", railInfo[1])
                newByteArr.extend(block)

                for j in range(3):
                    dirF = struct.pack("<f", railInfo[2 + j])
                    newByteArr.extend(dirF)

                mdl_no = railInfo[5]
                newByteArr.append(mdl_no)

                kasen = struct.pack("<b", railInfo[6])
                newByteArr.extend(kasen)

                kasenchu = struct.pack("<b", railInfo[7])
                newByteArr.extend(kasenchu)

                perF = struct.pack("<f", railInfo[8])
                newByteArr.extend(perF)

                for j in range(4):
                    flag = railInfo[9 + j]
                    newByteArr.append(flag)

                rail_data = railInfo[13]
                newByteArr.append(rail_data)

                for j in range(rail_data * 4):
                    railH = struct.pack("<h", railInfo[14 + j])
                    newByteArr.extend(railH)

                endcntIndex = 14 + rail_data * 4
                else3List = railInfo[endcntIndex]

                newByteArr.append(len(else3List))
                for j in range(len(else3List)):
                    tempInfo = else3List[j]
                    for k in range(len(tempInfo)):
                        if k in [0, 2]:
                            newByteArr.append(tempInfo[k])
                        else:
                            tempH = struct.pack("<h", tempInfo[k])
                            newByteArr.extend(tempH)

                if prev_rail == -1:
                    if i < len(self.railList):
                        originRailInfo = self.railList[i]
                        originPrevRail = originRailInfo[1]
                        if originPrevRail == -1:
                            else4ListIndex = 15 + rail_data * 4
                            else4Info = railInfo[else4ListIndex]
                            prevRailH = struct.pack("<h", else4Info[0])
                            newByteArr.extend(prevRailH)
                            for j in range(6):
                                tempF = struct.pack("<f", else4Info[1 + j])
                                newByteArr.extend(tempF)
                        else:
                            prevRailH = struct.pack("<h", -1)
                            newByteArr.extend(prevRailH)
                            for j in range(6):
                                tempF = struct.pack("<f", 0)
                                newByteArr.extend(tempF)
                    else:
                        prevRailH = struct.pack("<h", -1)
                        newByteArr.extend(prevRailH)
                        for j in range(6):
                            tempF = struct.pack("<f", 0)
                            newByteArr.extend(tempF)

            index = self.ambIdx
            newByteArr.extend(self.byteArr[index:])

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse3Cnt(self, cnt):
        try:
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse3List(self, valList):
        try:
            else3RailList = []
            for i in range(len(valList)):
                railNo = valList[i][0]
                else3RailList.append(railNo)

            railList = []
            for i in range(len(self.railList)):
                railInfo = self.railList[i]
                copyRailInfo = copy.deepcopy(railInfo)
                copyRailData = copyRailInfo[14]
                copyElse3ListIndex = 15 + copyRailData * 4
                if copyRailInfo[0] in else3RailList:
                    railListIndex = [index for (index, item) in enumerate(else3RailList) if item == copyRailInfo[0]][0]
                    copyRailInfo[copyElse3ListIndex] = valList[railListIndex][1]
                else:
                    copyRailInfo[copyElse3ListIndex] = []

                copyRailInfo.pop(0)
                railList.append(copyRailInfo)
            return self.saveRailCsv(railList)
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse4Cnt(self, cnt):
        try:
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveElse4List(self, valList):
        try:
            else4RailList = []
            for i in range(len(valList)):
                railNo = valList[i][0]
                else4RailList.append(railNo)

            railList = []
            for i in range(len(self.railList)):
                railInfo = self.railList[i]
                copyRailInfo = copy.deepcopy(railInfo)
                if railInfo[0] in else4RailList:
                    railListIndex = [index for (index, item) in enumerate(else4RailList) if item == railInfo[0]][0]
                    copyRailData = copyRailInfo[14]
                    copyElse4ListIndex = 16 + copyRailData * 4
                    copyRailInfo[copyElse4ListIndex] = valList[railListIndex][1:]

                copyRailInfo.pop(0)
                railList.append(copyRailInfo)
            return self.saveRailCsv(railList)
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveAmbCsv(self, ambList):
        try:
            index = self.ambIdx
            newByteArr = self.byteArr[0:index]

            ambCnt = len(ambList)
            ambCntH = struct.pack("<h", ambCnt)
            newByteArr.extend(ambCntH)

            for i in range(len(ambList)):
                ambInfo = ambList[i]

                const0 = ambInfo[0]
                newByteArr.append(const0)

                length = struct.pack("<f", ambInfo[1])
                newByteArr.extend(length)

                railNoH = struct.pack("<h", ambInfo[2])
                newByteArr.extend(railNoH)
                railPosH = struct.pack("<h", ambInfo[3])
                newByteArr.extend(railPosH)

                for j in range(6):
                    tempF = struct.pack("<f", ambInfo[4 + j])
                    newByteArr.extend(tempF)

                priority = ambInfo[10]
                newByteArr.append(priority)

                fog = ambInfo[11]
                newByteArr.append(fog)

                mdlNoH = struct.pack("<h", ambInfo[12])
                newByteArr.extend(mdlNoH)

                for j in range(10):
                    tempF = struct.pack("<f", ambInfo[13 + j])
                    newByteArr.extend(tempF)

                ambChildData = ambInfo[23]
                newByteArr.append(ambChildData)

                for j in range(ambChildData):
                    mdlNoH = struct.pack("<h", ambInfo[11 * j + 24])
                    newByteArr.extend(mdlNoH)

                    for k in range(10):
                        tempF = struct.pack("<f", ambInfo[11 * j + 25 + k])
                        newByteArr.extend(tempF)

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def csToRs(self):
        try:
            index = self.railIdx
            newByteArr = self.byteArr[0:index]

            header = "DEND_MAP_VER0300"
            headerH = self.encObj.convertByteArray(header)

            for i in range(len(headerH)):
                newByteArr[i] = headerH[i]

            railCnt = len(self.railList)
            railCntH = struct.pack("<h", railCnt)
            newByteArr.extend(railCntH)

            for i in range(railCnt):
                railInfo = self.railList[i][1:]

                prev_rail = railInfo[0]
                prev_railH = struct.pack("<h", prev_rail)
                newByteArr.extend(prev_railH)

                block = struct.pack("<b", railInfo[1])
                newByteArr.extend(block)

                for j in range(3):
                    dirF = struct.pack("<f", railInfo[2 + j])
                    newByteArr.extend(dirF)

                mdl_no = railInfo[5]
                newByteArr.append(mdl_no)

                kasen = struct.pack("<b", railInfo[6])
                newByteArr.extend(kasen)

                kasenchu = struct.pack("<b", railInfo[7])
                newByteArr.extend(kasenchu)

                perF = struct.pack("<f", railInfo[8])
                newByteArr.extend(perF)

                for j in range(4):
                    flag = railInfo[9 + j]
                    newByteArr.append(flag)

                rail_data = railInfo[13]
                newByteArr.append(rail_data)

                for j in range(rail_data * 4):
                    railH = struct.pack("<h", railInfo[14 + j])
                    newByteArr.extend(railH)

            else3Cnt = len(self.else3List)
            else3CntH = struct.pack("<h", else3Cnt)
            newByteArr.extend(else3CntH)

            for i in range(else3Cnt):
                else3List = self.else3List[i]

                railNo = else3List[0]
                railNoH = struct.pack("<h", railNo)
                newByteArr.extend(railNoH)

                newByteArr.append(len(else3List[1]))
                for j in range(len(else3List[1])):
                    tempInfo = else3List[1][j]
                    for k in range(8):
                        newByteArr.append(tempInfo[k])

            copyElse4List = copy.deepcopy(self.else4List)
            else4List = []
            for i in range(len(copyElse4List)):
                else4Info = copyElse4List[i]

                railNo = else4Info[0]
                prevRail = else4Info[1]

                if railNo == 0 and prevRail == -1:
                    continue
                else4List.append(else4Info)

            else4Cnt = len(else4List)
            else4CntH = struct.pack("<h", else4Cnt)
            newByteArr.extend(else4CntH)

            for i in range(else4Cnt):
                else4Info = else4List[i]

                railNo = else4Info[0]
                railNoH = struct.pack("<h", railNo)
                newByteArr.extend(railNoH)

                prevRail = else4Info[1]
                prevRailH = struct.pack("<h", prevRail)
                newByteArr.extend(prevRailH)

                for j in range(6):
                    tempF = struct.pack("<f", else4Info[2 + j])
                    newByteArr.extend(tempF)

            index = self.ambIdx
            newByteArr.extend(self.byteArr[index:])

            return newByteArr
        except Exception:
            self.error = traceback.format_exc()
            return None

    def reload(self):
        self.open()
        return self

    def save(self, newByteArr):
        self.byteArr = newByteArr
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
