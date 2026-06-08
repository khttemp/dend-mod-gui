import configparser
import csv

import program.sub.textSetting as textSetting


def getGameOption(configPath):
    try:
        configRead = configparser.ConfigParser()
        configRead.read(configPath, encoding="utf-8")
        game = int(configRead.get("COMICSCRIPT_GAME", "mode"))
    except Exception:
        game = 0

    return textSetting.textList["menu"]["comicscript"]["gameList"][game]


def writeCsv(filePath, comicDataList):
    with open(filePath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        for comicData in comicDataList:
            writer.writerow(comicData)


def loadCsvData(filePath, cmdList):
    with open(filePath, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)

        csvComicDataList = []
        count = 0
        try:
            for i, row in enumerate(reader):
                cmdName = row[0]
                if cmdName not in cmdList:
                    errorMsg = textSetting.textList["errorList"]["E8"].format(i + 1, cmdName)
                    return False, {"message": errorMsg}

                csvScriptData = [
                    cmdName
                ]
                comicDataParaList = []
                for j in range(1, len(row)):
                    try:
                        if row[j] == "":
                            break
                        comicDataParaList.append(float(row[j]))
                    except ValueError:
                        errorMsg = textSetting.textList["errorList"]["E9"].format(i + 1, row[j])
                        return False, {"message": errorMsg}
                csvScriptData.append(len(comicDataParaList))
                csvScriptData.extend(comicDataParaList)
                csvComicDataList.append(csvScriptData)
                count += 1
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E15"].format(i + 1)
            return False, {"message": errorMsg}

        obj = {"csvLines":count, "data":csvComicDataList}
        return True, obj
