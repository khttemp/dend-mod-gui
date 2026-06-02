import configparser
import csv

import program.sub.textSetting as textSetting
from program.sub.encodingClass import SJISEncodingObject

encObj = SJISEncodingObject()


def getSmfFlagOption(configPath):
    try:
        configRead = configparser.ConfigParser()
        configRead.read(configPath, encoding="utf-8")
        frameFlag = int(configRead.get("SMF_FRAME", "mode"))
        meshFlag = int(configRead.get("SMF_MESH", "mode"))
        xyzFlag = int(configRead.get("SMF_XYZ", "mode"))
        mtrlFlag = int(configRead.get("SMF_MTRL", "mode"))

        return [frameFlag == 1, meshFlag == 1, xyzFlag == 1, mtrlFlag == 1]
    except Exception:
        return [False, False, False, False]


def getSwapMeshByteArr(swapMeshNo, swapDecryptFile):
    swapDecryptFile.index = swapDecryptFile.meshStartIdx
    swapMeshStartIdx = -1
    swapMeshEndIdx = -1

    for meshNo in range(swapDecryptFile.meshCount):
        if meshNo == swapMeshNo:
            swapMeshStartIdx = swapDecryptFile.index
        nameAndLength = swapDecryptFile.getStructNameAndLength()
        if nameAndLength[1] == -1:
            return (False, {"message":textSetting.textList["errorList"]["E14"]})

        if not swapDecryptFile.readMESH(meshNo, nameAndLength[1]):
            return (False, {"message":textSetting.textList["errorList"]["E14"]})

        if meshNo == swapMeshNo:
            swapMeshEndIdx = swapDecryptFile.index
            break

    if swapMeshStartIdx == -1 or swapMeshEndIdx == -1:
        return (False, {"message":textSetting.textList["errorList"]["E14"]})

    return (True, {"data":swapDecryptFile.byteArr[swapMeshStartIdx:swapMeshEndIdx]})


def writeMaterialCsv(filePath, mtrlList):
    with open(filePath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        header = [
            "mtrlNo",
            "texc",
            "diff_r",
            "diff_g",
            "diff_b",
            "diff_a",
            "emis_r",
            "emis_g",
            "emis_b"
        ]
        writer.writerow(header)

        for mIdx, mtrlInfo in enumerate(mtrlList):
            texc = ""
            if "texc" in mtrlInfo:
                texc = mtrlInfo["texc"]

            rowList = [
                mIdx,
                texc
            ]
            rowList.extend(mtrlInfo["diff"])
            rowList.extend(mtrlInfo["emis"])
            writer.writerow(rowList)


def loadCsvData(filePath, originMtrlList):
    count = 0
    mtrlList = []
    noTexcInputFlag = False
    with open(filePath, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)

        try:
            count += 1
            next(reader)
        except StopIteration:
            pass

        for row in reader:
            idx = reader.line_num - 2
            originMtrlInfo = originMtrlList[idx]
            mtrlInfo = {}
            if row[1] != "":
                mtrlInfo["texc"] = row[1]
                bTexc = encObj.convertByteArray(mtrlInfo["texc"])
                if len(bTexc) > 64:
                    return (False, {"message": textSetting.textList["errorList"]["E127"].format(idx)})

            if "texc" in originMtrlInfo and "texc" not in mtrlInfo:
                return (False, {"message": textSetting.textList["errorList"]["E126"].format(idx)})

            if "texc" not in originMtrlInfo and "texc" in mtrlInfo:
                noTexcInputFlag = True

            diff = [0.0, 0.0, 0.0, 0.0]
            if row[2] != "":
                diff[0] = float(row[2])
            if row[3] != "":
                diff[1] = float(row[3])
            if row[4] != "":
                diff[2] = float(row[4])
            if row[5] != "":
                diff[3] = float(row[5])
            mtrlInfo["diff"] = diff

            emis = [0.0, 0.0, 0.0]
            if row[6] != "":
                emis[0] = float(row[6])
            if row[7] != "":
                emis[1] = float(row[7])
            if row[8] != "":
                emis[2] = float(row[8])
            mtrlInfo["emis"] = emis
            mtrlList.append(mtrlInfo)
    
    if len(originMtrlList) != len(mtrlList):
        return (False, {"message":textSetting.textList["errorList"]["E125"].format(len(mtrlList), len(originMtrlList))})
    return (True, {"data":mtrlList, "noTexcInputFlag":noTexcInputFlag})
