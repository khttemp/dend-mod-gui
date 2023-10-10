import os
import struct
import codecs
import traceback
import copy


class RailDecrypt:
    def __init__(self, filePath):
        self.game = "LS"
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
        self.game = "LS"
        self.ver = ""
        self.musicCnt = 0
        self.musicList = []
        self.trainCnt = 0
        self.trainList = []
        self.trainList2 = []
        self.trainList3 = []
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
        readFlag = False

        header = self.byteArr[0:index].decode("shift-jis")
        if header != "DEND_MAP_VER0100" and header != "DEND_MAP_VER0101":
            return False

        if header == "DEND_MAP_VER0101":
            readFlag = True

        self.ver = header

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
            for j in range(2):
                res = self.byteArr[index]
                smfInfo.append(res)
                index += 1

            cnt = self.byteArr[index]
            index += 1
            if cnt == 255:
                cnt = -1

            tempList = []
            if cnt > 0:
                for j in range(cnt):
                    tempInfo = []
                    for k in range(2):
                        tempH = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                        tempInfo.append(tempH)
                        index += 2
                    tempList.append(tempInfo)
            smfInfo.append(tempList)
            self.smfList.append(smfInfo)

        # 使う音楽
        self.musicIdx = index

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
        self.musicCnt = len(self.musicList)

        self.railStationNameIdx = index
        railStationNameLen = self.byteArr[index]
        index += 1
        self.railStationName = self.byteArr[index:index + railStationNameLen].decode("shift-jis")
        index += railStationNameLen

        # SCENE 3D OBJ(bin ANIME)
        self.binAnimeIdx = index
        binAnimeInfo = []
        binAnimeInfo.append(self.byteArr[index])
        index += 1
        binAnimeInfo.append(self.byteArr[index])
        index += 1
        binAnimeInfo.append(self.byteArr[index])
        index += 1
        self.binAnimeList.append(binAnimeInfo)
        # SCENE 3D OBJ(bin ANIME)

        # unknown
        self.elseIdx = index

        cnt = self.byteArr[index]
        index += 1
        for i in range(cnt):
            tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
            tempF = round(tempF, 5)
            self.else1List.append(tempF)
            index += 4
        # unknown

        # 配置する車両カウント
        self.trainCntIdx = index
        self.trainCnt = self.byteArr[index]
        index += 1

        # 車両の初期レール位置
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

        self.railIdx = index
        # Map
        mapCnt = struct.unpack("<h", self.byteArr[index:index + 2])[0]
        index += 2

        for i in range(mapCnt):
            railInfo = []
            railInfo.append(i)

            if readFlag:
                else4Info = []
                prev_rail2 = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                index += 2
                railInfo.append(prev_rail2)

                if prev_rail2 != -1:
                    else4Info.append(i)
                    else4Info.append(prev_rail2)
                    for j in range(6):
                        tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                        tempF = round(tempF, 5)
                        else4Info.append(tempF)
                        index += 4
                    self.else4List.append(else4Info)
                railInfo.append(else4Info)

            # base_pos
            for j in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                railInfo.append(tempF)
                index += 4

            # base_dir
            for j in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                railInfo.append(tempF)
                index += 4

            mdl_no = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
            railInfo.append(mdl_no)
            index += 1

            prev_rail = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            railInfo.append(prev_rail)
            index += 2

            # base_rot
            if prev_rail == -1:
                for j in range(3):
                    tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                    tempF = round(tempF, 5)
                    railInfo.append(tempF)
                    index += 4

            mdl_kasenchu = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
            if mdl_kasenchu == 255:
                mdl_kasenchu = -1
            railInfo.append(mdl_kasenchu)
            index += 1

            mdl_kasen = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
            if mdl_kasen == 255:
                mdl_kasen = -1
            railInfo.append(mdl_kasen)
            index += 1

            # dummy?
            for j in range(2):
                index += 1
                for k in range(3):
                    index += 4
            # dummy?

            fix_amb_mdl = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
            if fix_amb_mdl == 255:
                fix_amb_mdl = -1
            railInfo.append(fix_amb_mdl)
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

                pos = struct.unpack("<B", self.byteArr[index].to_bytes(1, "little"))[0]
                ambInfo.append(pos)
                index += 1

                railPos = struct.unpack("<h", self.byteArr[index:index + 2])[0]
                ambInfo.append(railPos)
                index += 2

                smfNo = self.byteArr[index]
                ambInfo.append(smfNo)
                index += 1

                animeNo = self.byteArr[index]
                if animeNo == 255:
                    animeNo = -1
                ambInfo.append(animeNo)
                index += 1

                ambList.append(ambInfo)
                self.ambList.append(ambInfo)
            railInfo.append(ambList)

            self.railList.append(railInfo)

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

            for j in range(6):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                stationNameInfo.append(tempF)
                index += 4
            self.stationNameList.append(stationNameInfo)

        # Camera
        self.else3Idx = index
        cameraCnt = self.byteArr[index]
        index += 1
        for i in range(cameraCnt):
            cameraInfo = []
            for j in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                index += 4
                cameraInfo.append(tempF)
            camera2Cnt = self.byteArr[index]
            index += 1

            tempList = []
            for j in range(camera2Cnt):
                tempInfo = []
                for k in range(4):
                    tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                    tempF = round(tempF, 5)
                    index += 4
                    tempInfo.append(tempF)
                cameraNo = self.byteArr[index]
                index += 1
                tempInfo.append(cameraNo)
                tempList.append(tempInfo)
            cameraInfo.append(tempList)
            self.else3List.append(cameraInfo)

        # cpu
        self.cpuIdx = index
        cpuCnt = self.byteArr[index]
        index += 1
        for i in range(cpuCnt):
            cpuInfo = []
            railNo = struct.unpack("<h", self.byteArr[index:index + 2])[0]
            cpuInfo.append(railNo)
            index += 2

            tempList = []
            for j in range(6):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                tempList.append(tempF)
                index += 4
            cpuInfo.append(tempList)

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

            tempList2 = []
            for j in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                tempList2.append(tempF)
                index += 4
            cpuInfo.append(tempList2)
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

            tempList = []
            for j in range(9):
                tempF = struct.unpack("<f", self.byteArr[index:index + 4])[0]
                tempF = round(tempF, 5)
                tempList.append(tempF)
                index += 4
            comicScriptInfo.append(tempList)

            self.comicScriptList.append(comicScriptInfo)
        return True

    def extractRailCsv(self, file_path):
        readFlag = False
        if self.ver == "DEND_MAP_VER0101":
            readFlag = True

        try:
            w = open(file_path, "w")
            w.write("index,prev_rail,")
            w.write("pos_x,pos_y,pos_z,")
            w.write("dir_x,dir_y,dir_z,")
            w.write("mdl_no,mdl_kasen,mdl_kasenchu,")
            w.write("rot_x,rot_y,rot_z,fix_amb_mdl,per,")
            w.write("flg,flg,flg,flg,")
            w.write("rail_data,")
            w.write("next_rail,next_no,prev_rail,prev_no,\n")
        except PermissionError:
            return False

        for railInfo in self.railList:
            offset = 0
            # index
            w.write("{0},".format(railInfo[0]))

            if readFlag:
                offset = 2

            prev_rail = railInfo[8 + offset]
            w.write("{0},".format(prev_rail))

            # pos, dir, mdl_no
            for i in range(7):
                w.write("{0},".format(railInfo[1 + offset + i]))

            # base_rot
            rotList = []
            if prev_rail == -1:
                for i in range(3):
                    rotList.append(railInfo[9 + offset + i])
                offset += 3

            kasenchu = railInfo[9 + offset]
            kasen = railInfo[10 + offset]
            w.write("{0},{1},".format(kasen, kasenchu))

            if len(rotList) > 0:
                for rot in rotList:
                    w.write("{0},".format(rot))
            else:
                w.write("," * 3)

            fix_amb_mdl = railInfo[11 + offset]
            per = railInfo[12 + offset]
            w.write("{0},{1},".format(fix_amb_mdl, per))

            # flg
            for i in range(4):
                w.write("0x{0:02x},".format(railInfo[13 + offset + i]))
            # raildata
            raildata = railInfo[17 + offset]
            w.write("{0},".format(raildata))

            for i in range(raildata):
                for j in range(4):
                    w.write("{0},".format(railInfo[18 + offset + 4*i + j]))

            w.write("\n")
        w.close()
        return True

    def extractAmbCsv(self, file_path):
        try:
            w = open(file_path, "w")
            w.write("rail_no,pos,")
            w.write("rail_pos,smf_no,anime_no,\n")
        except PermissionError:
            return False

        for ambInfo in self.ambList:
            for i in range(5):
                w.write("{0},".format(ambInfo[i]))
            w.write("\n")
        w.close()
        return True

    def saveMusicList(self, musicList):
        try:
            index = self.musicIdx
            newByteArr = self.byteArr[0:index]

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

            index = self.railStationNameIdx
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
                index = self.railIdx
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

            index = self.railIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.trainCntIdx] = cnt
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveRailPos(self, num, trainList):
        try:
            index = self.trainCntIdx
            index += 1

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

    def saveElse1List(self, else1List):
        try:
            index = self.elseIdx
            newByteArr = self.byteArr[0:index]

            newByteArr.append(len(else1List))
            for i in range(len(else1List)):
                tempF = struct.pack("<f", else1List[i])
                newByteArr.extend(tempF)

            index = self.trainCntIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveBinAnime(self, valList):
        try:
            index = self.binAnimeIdx

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    newByteArr.append(valInfo[j])

            index = self.elseIdx
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
                for j in range(2):
                    index += 1
                tempCnt = self.byteArr[index]
                index += 1
                if tempCnt != 255:
                    for j in range(tempCnt):
                        for k in range(2):
                            index += 2

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                newByteArr.append(len(smfInfo[0]))
                newByteArr.extend(smfInfo[0].encode("shift-jis"))
                for i in range(2):
                    newByteArr.append(smfInfo[1 + i])

                if len(smfInfo[3]) != 0:
                    newByteArr.append(len(smfInfo[3]))
                    for i in range(len(smfInfo[3])):
                        tempInfo = smfInfo[3][i]
                        for j in range(len(tempInfo)):
                            tempH = struct.pack("<h", tempInfo[j])
                            newByteArr.extend(tempH)
                else:
                    newByteArr.append(255)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    for j in range(2):
                        index += 1
                    tempCnt = self.byteArr[index]
                    index += 1
                    if tempCnt != 255:
                        for j in range(tempCnt):
                            for k in range(2):
                                index += 2
                else:
                    cnt += 1
            elif mode == "delete":
                b = self.byteArr[index]
                index += 1
                index += b
                for j in range(2):
                    index += 1
                tempCnt = self.byteArr[index]
                index += 1
                if tempCnt != 255:
                    for j in range(tempCnt):
                        for k in range(2):
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
                for j in range(2):
                    index += 1
                tempCnt = self.byteArr[index]
                index += 1
                if tempCnt != 255:
                    for j in range(tempCnt):
                        for k in range(2):
                            index += 2

            b = self.byteArr[index]
            index += 1
            index += b
            for j in range(2):
                index += 1

            newByteArr = self.byteArr[0:index]

            if len(tempList) > 0:
                newByteArr.append(len(tempList))
                for i in range(len(tempList)):
                    tempInfo = tempList[i]
                    for j in range(len(tempInfo)):
                        tempH = struct.pack("<h", tempInfo[j])
                        newByteArr.extend(tempH)
            else:
                newByteArr.append(255)

            originCnt = self.byteArr[index]
            index += 1
            if originCnt != 255:
                for j in range(originCnt):
                    for k in range(2):
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
                for j in range(6):
                    index += 4

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                encodeName = stationNameInfo[0].encode("shift-jis")
                newByteArr.append(len(encodeName))
                newByteArr.extend(encodeName)
                newByteArr.append(int(stationNameInfo[1]))
                tempH = struct.pack("<h", int(stationNameInfo[2]))
                newByteArr.extend(tempH)
                for i in range(6):
                    tempF = struct.pack("<f", float(stationNameInfo[3 + i]))
                    newByteArr.extend(tempF)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    index += 1
                    index += 2
                    for j in range(6):
                        index += 4
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
                cnt -= 1

            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.stationNameIdx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def saveCpuInfo(self, num, mode, cpuInfo):
        try:
            index = self.cpuIdx
            cnt = self.byteArr[index]
            index += 1
            for i in range(num):
                index += 2
                for j in range(6):
                    index += 4
                index += 1
                index += 1
                for j in range(8):
                    index += 4

            newByteArr = self.byteArr[0:index]

            if mode == "modify" or mode == "insert":
                tempH = struct.pack("<h", cpuInfo[0])
                newByteArr.extend(tempH)
                for i in range(len(cpuInfo[1])):
                    tempF = struct.pack("<f", cpuInfo[1][i])
                    newByteArr.extend(tempF)
                newByteArr.append(cpuInfo[2])
                newByteArr.append(cpuInfo[3])
                for i in range(5):
                    tempF = struct.pack("<f", cpuInfo[4 + i])
                    newByteArr.extend(tempF)
                for i in range(len(cpuInfo[9])):
                    tempF = struct.pack("<f", cpuInfo[9][i])
                    newByteArr.extend(tempF)

                if mode == "modify":
                    index += 2
                    for i in range(6):
                        index += 4
                    index += 1
                    index += 1
                    for i in range(8):
                        index += 4
                else:
                    cnt += 1
            elif mode == "delete":
                index += 2
                for i in range(6):
                    index += 4
                index += 1
                index += 1
                for i in range(8):
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
                    if j in [0, 2]:
                        tempH = struct.pack("<h", comicScriptInfo[j])
                        newByteArr.extend(tempH)
                    elif j == 1:
                        newByteArr.append(comicScriptInfo[j])
                    else:
                        tempList = comicScriptInfo[j]
                        for k in range(len(tempList)):
                            tempF = struct.pack("<f", tempList[k])
                            newByteArr.extend(tempF)

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

                railListIdx = 0
                if self.ver == "DEND_MAP_VER0101":
                    prev_rail2 = railInfo[railListIdx]
                    prev_rail2H = struct.pack("<h", prev_rail2)
                    newByteArr.extend(prev_rail2H)
                    railListIdx += 1

                    if prev_rail2 != -1:
                        else4Info = railInfo[railListIdx][2:]
                        for j in range(6):
                            tempF = struct.pack("<f", else4Info[j])
                            newByteArr.extend(tempF)
                    railListIdx += 1

                for j in range(6):
                    tempF = struct.pack("<f", railInfo[railListIdx])
                    newByteArr.extend(tempF)
                    railListIdx += 1

                mdlNo = struct.pack("<b", railInfo[railListIdx])
                newByteArr.extend(mdlNo)
                railListIdx += 1

                prev_rail = railInfo[railListIdx]
                prev_railH = struct.pack("<h", prev_rail)
                newByteArr.extend(prev_railH)
                railListIdx += 1

                if prev_rail == -1:
                    for j in range(3):
                        tempF = struct.pack("<f", railInfo[railListIdx])
                        newByteArr.extend(tempF)
                        railListIdx += 1

                kasenchu = struct.pack("<b", railInfo[railListIdx])
                newByteArr.extend(kasenchu)
                railListIdx += 1

                kasen = struct.pack("<b", railInfo[railListIdx])
                newByteArr.extend(kasen)
                railListIdx += 1

                # dummy?
                for j in range(2):
                    newByteArr.append(255)
                    for k in range(3):
                        tempF = struct.pack("<f", 0)
                        newByteArr.extend(tempF)
                # dummy?

                fixAmbNo = struct.pack("<b", railInfo[railListIdx])
                newByteArr.extend(fixAmbNo)
                railListIdx += 1

                perF = struct.pack("<f", railInfo[railListIdx])
                newByteArr.extend(perF)
                railListIdx += 1

                for j in range(4):
                    flag = railInfo[railListIdx]
                    newByteArr.append(flag)
                    railListIdx += 1

                rail_data = railInfo[railListIdx]
                newByteArr.append(rail_data)
                railListIdx += 1

                for j in range(rail_data * 4):
                    railH = struct.pack("<h", railInfo[railListIdx])
                    newByteArr.extend(railH)
                    railListIdx += 1

                ambList = railInfo[railListIdx]
                newByteArr.append(len(ambList))
                for i in range(len(ambList)):
                    ambInfo = ambList[i][1:]

                    pos = ambInfo[0]
                    newByteArr.append(pos)

                    railPos = ambInfo[1]
                    railPosH = struct.pack("<h", railPos)
                    newByteArr.extend(railPosH)

                    smfNo = ambInfo[2]
                    newByteArr.append(smfNo)

                    animeNo = ambInfo[3]
                    animeNoB = struct.pack("<b", animeNo)
                    newByteArr.extend(animeNoB)

            index = self.stationNameIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    # camera
    def saveElse3Cnt(self, cnt):
        try:
            index = self.else3Idx
            else3Cnt = self.byteArr[index]
            index += 1

            if cnt > else3Cnt:
                index = self.cpuIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - else3Cnt):
                    for j in range(3):
                        tempF = struct.pack("<f", 0)
                        newByteArr.extend(tempF)
                    newByteArr.append(0)
            else:
                for i in range(cnt):
                    for j in range(3):
                        index += 4
                    index += 1
                newByteArr = self.byteArr[0:index]

            index = self.cpuIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.else3Idx] = cnt

            self.save(newByteArr)
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    # camera
    def saveElse3List(self, valList):
        try:
            index = self.else3Idx
            newElse3Cnt = len(valList)
            index += 1
            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                else3Info = valList[i]
                for j in range(3):
                    tempF = struct.pack("<f", else3Info[j])
                    newByteArr.extend(tempF)
                newByteArr.append(len(else3Info[3]))
                for j in range(len(else3Info[3])):
                    tempList = else3Info[3][j]
                    for k in range(4):
                        tempF = struct.pack("<f", tempList[k])
                        newByteArr.extend(tempF)
                    newByteArr.append(tempList[4])

            index = self.else3Idx
            newByteArr[index] = newElse3Cnt

            index = self.cpuIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
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
                    copyRailInfo[2] = valList[railListIndex][2:]

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

                ambList = []
                if i in ambRailDict:
                    ambList = ambRailDict[i]
                copyRailInfo[-1] = ambList

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
