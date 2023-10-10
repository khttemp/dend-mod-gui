import os
import struct
import codecs
import traceback
import copy


class RailDecrypt:
    def __init__(self, filePath):
        self.game = "BS"
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
        self.trainList4 = []
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
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(self.error)
        w.close()

    def decrypt(self):
        self.game = "BS"
        self.ver = ""
        self.musicCnt = 0
        self.musicList = []
        self.trainCnt = 0
        self.trainList = []
        self.trainList2 = []
        self.trainList3 = []
        self.trainList4 = []
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

        header = self.byteArr[0:index].decode("shift-jis")
        if header != "DEND_MAP_VER0102":
            return False

        self.ver = header

        railStationNameLen = self.byteArr[index]
        index += 1
        self.railStationName = self.byteArr[index:index + railStationNameLen].decode("shift-jis")
        index += railStationNameLen

        # 使う音楽(ダミーデータ?)
        self.musicIdx = index
        self.musicCnt = self.byteArr[index]
        index += 1
        for i in range(self.musicCnt):
            musicInfo = []
            musicFileLen = self.byteArr[index]
            index += 1
            musicFile = self.byteArr[index:index + musicFileLen].decode("shift-jis")
            musicInfo.append(musicFile)
            index += musicFileLen

            musicNameLen = self.byteArr[index]
            index += 1
            musicName = self.byteArr[index:index + musicNameLen].decode("shift-jis")
            musicInfo.append(musicName)
            index += musicNameLen

            start = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            start = round(start, 5)
            index += 4
            musicInfo.append(start)

            loopStart = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            loopStart = round(loopStart, 5)
            index += 4
            musicInfo.append(loopStart)

            self.musicList.append(musicInfo)

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
        # ダミー位置？
        trainInfo2 = []
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

        self.trainCntIdx4 = index
        trainInfo4 = []
        railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        trainInfo4.append(railNo)
        index += 2

        boneNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        trainInfo4.append(boneNo)
        index += 2

        temp = self.byteArr[index]
        trainInfo4.append(temp)
        index += 1

        tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
        tempF = round(tempF, 5)
        trainInfo4.append(tempF)
        index += 4

        self.trainList4.append(trainInfo4)
        # unknown

        self.stationNo2Index = index
        self.stationNo2 = self.byteArr[index]
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
            text = self.byteArr[index:index + b].decode("shift-jis")
            smfInfo.append(text)
            index += b
            for j in range(3):
                res = self.byteArr[index]
                smfInfo.append(res)
                index += 1

            cnt = self.byteArr[index]
            index += 1
            tempList = []
            for j in range(cnt):
                tempInfo = []
                for k in range(3):
                    tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                    tempInfo.append(tempH)
                    index += 2
                tempList.append(tempInfo)
            smfInfo.append(tempList)
            self.smfList.append(smfInfo)

        # stationName
        self.stationNameIdx = index
        snameCnt = self.byteArr[index]
        index += 1
        for i in range(snameCnt):
            stationNameInfo = []
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index + b].decode("shift-jis")
            stationNameInfo.append(text)
            index += b

            stFlag = self.byteArr[index]
            stationNameInfo.append(stFlag)
            index += 1
            railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            stationNameInfo.append(railNo)
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

            for j in range(4):
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

        self.railIdx = index
        # Map
        mapCnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        index += 2

        for i in range(mapCnt):
            railInfo = []
            railInfo.append(i)

            prev_rail = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            railInfo.append(prev_rail)
            index += 2

            else4Info = []
            if prev_rail == -1:
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
            if mdl_kasenchu == 255:
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

            ambcnt = self.byteArr[index]
            index += 1
            ambList = []
            for j in range(ambcnt):
                ambInfo = []
                ambInfo.append(i)

                for k in range(4):
                    temp = self.byteArr[index]
                    index += 1
                    ambInfo.append(temp)

                for k in range(7):
                    tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                    tempF = round(tempF, 5)
                    index += 4
                    ambInfo.append(tempF)
                ambList.append(ambInfo)
                self.ambList.append(ambInfo)

            endcnt = self.byteArr[index]
            index += 1

            else3Info = []
            if endcnt > 0:
                else3Info.append(i)
                tempList = []

                for endc in range(endcnt):
                    tempInfo = []
                    pos = self.byteArr[index]
                    tempInfo.append(pos)
                    index += 1
                    railPos = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                    tempInfo.append(railPos)
                    index += 2
                    binIndex = self.byteArr[index]
                    tempInfo.append(binIndex)
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
            railInfo.append(else4Info[1:])
            railInfo.append(ambList)
            self.railList.append(railInfo)
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
            w.write("rail_no,priority,fog,")
            w.write("mdl_no,mdl_no2,")
            w.write("pos_x,pos_y,pos_z,")
            w.write("dir_x,dir_y,dir_z,")
            w.write("per,\n")
        except PermissionError:
            return False

        for ambInfo in self.ambList:
            for i in range(12):
                w.write("{0},".format(ambInfo[i]))
            w.write("\n")
        w.close()
        return True

    def saveMusicList(self, musicList):
        try:
            index = self.musicIdx
            newByteArr = self.byteArr[0:index]

            newByteArr.append(len(musicList))
            for i in range(len(musicList)):
                musicInfo = musicList[i]
                for j in range(len(musicInfo)):
                    if j == 2 or j == 3:
                        tempF = struct.pack("<f", musicInfo[j])
                        newByteArr.extend(tempF)
                    else:
                        musicStr = musicInfo[j].encode("shift-jis")
                        newByteArr.append(len(musicStr))
                        newByteArr.extend(musicStr)

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
            elif num == 3:
                index = self.trainCntIdx4

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
            if num == 0:
                index = self.stationNoIndex
            elif num == 1:
                index = self.stationNo2Index

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
                newByteArr.extend(name.encode("shift-jis"))

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
                for j in range(3):
                    index += 1
                tempCnt = self.byteArr[index]
                index += 1
                for j in range(tempCnt):
                    for k in range(3):
                        index += 2

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                newByteArr.append(len(smfInfo[0]))
                newByteArr.extend(smfInfo[0].encode("shift-jis"))
                for i in range(3):
                    newByteArr.append(smfInfo[1 + i])
                newByteArr.append(len(smfInfo[4]))
                for i in range(len(smfInfo[4])):
                    tempInfo = smfInfo[4][i]
                    for j in range(len(tempInfo)):
                        tempH = struct.pack("<h", tempInfo[j])
                        newByteArr.extend(tempH)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    for j in range(3):
                        index += 1
                    tempCnt = self.byteArr[index]
                    index += 1
                    for j in range(tempCnt):
                        for k in range(3):
                            index += 2
                else:
                    cnt += 1
            elif mode == "delete":
                b = self.byteArr[index]
                index += 1
                index += b
                for j in range(3):
                    index += 1
                tempCnt = self.byteArr[index]
                index += 1
                for j in range(tempCnt):
                    for k in range(3):
                        index += 2
                cnt -= 1

            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.smfIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveSmfListElement(self, num, tempList):
        try:
            index = self.smfIdx
            index += 1
            for i in range(num):
                b = self.byteArr[index]
                index += 1
                index += b
                for j in range(3):
                    index += 1
                tempCnt = self.byteArr[index]
                index += 1
                for j in range(tempCnt):
                    for k in range(3):
                        index += 2

            b = self.byteArr[index]
            index += 1
            index += b
            for j in range(3):
                index += 1

            newByteArr = self.byteArr[0:index]

            newByteArr.append(len(tempList))
            for i in range(len(tempList)):
                tempInfo = tempList[i]
                for j in range(len(tempInfo)):
                    tempH = struct.pack("<h", tempInfo[j])
                    newByteArr.extend(tempH)

            originCnt = self.byteArr[index]
            index += 1
            for j in range(originCnt):
                for k in range(3):
                    index += 2

            newByteArr.extend(self.byteArr[index:])
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

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                encodeName = stationNameInfo[0].encode("shift-jis")
                newByteArr.append(len(encodeName))
                newByteArr.extend(encodeName)
                newByteArr.append(int(stationNameInfo[1]))
                tempH = struct.pack("<h", int(stationNameInfo[2]))
                newByteArr.extend(tempH)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    index += 1
                    index += 2
                else:
                    cnt += 1
            elif mode == "delete":
                b = self.byteArr[index]
                index += 1
                index += b
                index += 1
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
                for j in range(4):
                    index += 4

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                tempH = struct.pack("<h", smfInfo[0])
                newByteArr.extend(tempH)
                newByteArr.append(smfInfo[1])
                newByteArr.append(smfInfo[2])
                for i in range(4):
                    tempF = struct.pack("<f", smfInfo[3 + i])
                    newByteArr.extend(tempF)

                if mode == "modify":
                    index += 2
                    index += 1
                    index += 1
                    for j in range(4):
                        index += 4
                else:
                    cnt += 1
            elif mode == "delete":
                index += 2
                index += 1
                index += 1
                for j in range(4):
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

                if prev_rail == -1:
                    if i < len(self.railList):
                        originRailInfo = self.railList[i]
                        originPrevRail = originRailInfo[1]
                        if originPrevRail == -1:
                            railData = railInfo[13]
                            else4ListIndex = 15 + railData * 4
                            else4List = railInfo[else4ListIndex]
                            prevRailH = struct.pack("<h", else4List[0])
                            newByteArr.extend(prevRailH)
                            for j in range(6):
                                tempF = struct.pack("<f", else4List[1 + j])
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

                ambListIndex = 16 + rail_data * 4
                ambList = railInfo[ambListIndex]
                newByteArr.append(len(ambList))
                if len(ambList) > 0:
                    for j in range(len(ambList)):
                        ambInfo = ambList[j][1:]
                        for k in range(4):
                            newByteArr.append(ambInfo[k])

                        for k in range(7):
                            tempF = struct.pack("<f", ambInfo[4 + k])
                            newByteArr.extend(tempF)

                else3ListIndex = 14 + rail_data * 4
                else3List = railInfo[else3ListIndex]

                newByteArr.append(len(else3List))
                for j in range(len(else3List)):
                    tempInfo = else3List[j]
                    for k in range(len(tempInfo)):
                        if k in [0, 2]:
                            newByteArr.append(tempInfo[k])
                        else:
                            tempH = struct.pack("<h", tempInfo[k])
                            newByteArr.extend(tempH)

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
            ambRailDict = {}
            for i in range(len(ambList)):
                railNo = ambList[i][0]
                if railNo not in ambRailDict:
                    ambRailDict[railNo] = []
                ambRailDict[railNo].append(ambList[i])

            railList = []
            for i in range(len(self.railList)):
                railInfo = self.railList[i]
                copyRailInfo = copy.deepcopy(railInfo)
                copyRailData = copyRailInfo[14]
                copyAmbListIndex = 17 + copyRailData * 4

                ambList = []
                if i in ambRailDict:
                    ambList = ambRailDict[i]
                copyRailInfo[copyAmbListIndex] = ambList

                copyRailInfo.pop(0)
                railList.append(copyRailInfo)
            return self.saveRailCsv(railList)
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
