import os
import sys
import json

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
    return excelWidget.extractExcel()


def saveDenFile(filePath, data, decryptFile):
    with open(filePath, "rb") as f:
        data.script = f.read()
    data.save()
    with open(decryptFile.filePath, "wb") as w:
        w.write(decryptFile.env.file.save())


def loadExcelData(filePath, data, configPath):
    railModelInfo, ambModelInfo = readModelInfo("model.json")
    errMsgObj = {}
    newLinesObj = {}
    excelWidget = ExcelWidget(data.script.tobytes().decode(), filePath, configPath, railModelInfo, ambModelInfo)
    result = excelWidget.loadExcelAndMerge(newLinesObj, errMsgObj)
    return (result, newLinesObj, errMsgObj)


def saveDenFileByExcel(data, decryptFile, newLinesObj):
    data.script = bytearray("\n".join(newLinesObj["data"]).encode("utf-8"))
    data.save()
    with open(decryptFile.filePath, "wb") as w:
        w.write(decryptFile.env.file.save())
