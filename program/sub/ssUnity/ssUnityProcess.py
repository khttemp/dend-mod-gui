import os
import sys
import json

import program.sub.textSetting as textSetting
from program.sub.ssUnity.importPy.excelWidget import ExcelWidget


def resource_path(localDir, relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", localDir)
    return os.path.join(bundle_dir, relative_path)


def readModelInfo(jsonName):
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "importPy")
    path = resource_path(filePath, jsonName)
    f = open(path, "r", encoding="utf-8")
    modelDict = json.load(f)
    f.close()

    railModelInfo = {}
    for model in list(modelDict["railModelInfo"].keys()):
        railModelInfo[model.lower()] = modelDict["railModelInfo"][model]

    ambModelInfo = []
    for model in modelDict["ambModelInfo"]:
        ambModelInfo.append(model.lower())

    return (railModelInfo, ambModelInfo)


def extractDenFile(filePath, fileType, data):
    if fileType == "AudioClip":
        for _, d in data.samples.items():
            w = open(filePath, "wb")
            w.write(d)
            w.close()
        return True

    if os.path.splitext(filePath)[1].lower() != ".xlsx":
        w = open(filePath, "wb")
        w.write(data.script)
        w.close()
        return True
    return False


def extractDenFileByExcel(filePath, data, configPath):
    railModelInfo, ambModelInfo = readModelInfo("model.json")
    excelWidget = ExcelWidget(data.script.tobytes().decode(), filePath, configPath, railModelInfo, ambModelInfo)
    if not excelWidget.extractExcel():
        return (False, excelWidget.errorMessage)
    return (True, excelWidget.warningMessage)


def loadExcelData(filePath, data, configPath):
    railModelInfo, ambModelInfo = readModelInfo("model.json")
    excelWidget = ExcelWidget(data.script.tobytes().decode(), filePath, configPath, railModelInfo, ambModelInfo)
    if not excelWidget.loadExcelAndMerge():
        return (False, {"message":excelWidget.errorMessage})
    return (True, {"message":excelWidget.warningMessage, "data":excelWidget.newLinesObj})


def writeCsv(filePath, trainOrgInfo):
    w = open(filePath, "w", encoding="utf-8-sig")
    w.write("{0},{1}\n".format(textSetting.textList["ssUnity"]["csvNotchNum"], trainOrgInfo[1]))
    w.write("{0},{1}\n".format(textSetting.textList["ssUnity"]["csvOrgNum"], trainOrgInfo[5]))
    w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyClass"]))
    w.write(",".join(trainOrgInfo[6]))
    w.write("\n")
    w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyModel"]))
    w.write(",".join(trainOrgInfo[7]))
    w.write("\n")
    w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvPantaModel"]))
    w.write(",".join(trainOrgInfo[8]))
    w.write("\n")
    w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyClassIndexList"]))
    w.write(",".join([str(x) for x in trainOrgInfo[9]]))
    w.write("\n")
    w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyModelIndexList"]))
    w.write(",".join([str(x) for x in trainOrgInfo[10]]))
    w.write("\n")
    w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvPantaModelIndexList"]))
    w.write(",".join([str(x) for x in trainOrgInfo[11]]))
    w.close()


def writeMeshCsv(filePath, meshTexInfo):
    meshTexTitleList = [
        "デフォルト",
        "回送",
        "試運転",
        "梅田",
        # 未使用
        "未詳1",
        "京橋",
        "名張",
        "難波",
        "三宮",
        "三田",
        "未詳2",
        "梅田",
        "品川",
        "大阪難波",
        "豊橋",
        "岐阜",
        "浅草",
        "日光",
        "池袋",
        # 未使用
        "渋谷(東急東横線)",
        "元町・中華街",
        "渋谷(東急田園都市線)",
        "中央林間",
    ]

    w = open(filePath, "w", encoding="utf-8-sig")
    for index, meshTexTitle in enumerate(meshTexTitleList):
        w.write("{0},{1}\n".format(meshTexTitle, meshTexInfo["data"]["meshData"][-1][index]))
    w.close()


def getScriptData(filePath):
    with open(filePath, "rb") as f:
        return f.read()


def getScriptDataByExcel(newLines):
    return bytearray("\n".join(newLines).encode("utf-8"))


def saveDenFile(data, decryptFile, script):
    data.script = script
    data.save()
    with open(decryptFile.filePath, "wb") as w:
        w.write(decryptFile.env.file.save())
