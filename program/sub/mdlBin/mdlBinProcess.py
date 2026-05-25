import csv

import program.sub.textSetting as textSetting

def writeCsv(filePath, scriptDataAllInfoList, cmdList):
    with open(filePath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        num = 0
        for scriptDataInfoList in scriptDataAllInfoList:
            listNum = 0
            for scriptDataInfo in scriptDataInfoList:
                headerInfo = [
                    "#{0}-{1}".format(num, listNum),
                ]
                headerInfo.extend(scriptDataInfo[0])
                writer.writerow(headerInfo)
                for scriptData in scriptDataInfo[1:]:
                    dataInfo = [
                        scriptData[0],
                        cmdList[scriptData[1]]
                    ]
                    dataInfo.extend(scriptData[4:])
                    writer.writerow(dataInfo)
                listNum += 1
            num += 1


def loadCsvData(filePath, cmdList):
    with open(filePath, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)

        csvScriptDataAllInfoList = []
        csvScriptDataInfoList = []
        csvScriptDataInfo = []
        csvScriptData = []
        curNum = -1
        curListNum = -1
        count = 0
        try:
            for i, row in enumerate(reader):
                if "#" in row[0]:
                    section = row[0].strip("#").split("-")
                    num = int(section[0])
                    listNum = int(section[1])

                    if curNum == num and curListNum == listNum:
                        errorMsg = textSetting.textList["errorList"]["E143"].format(curNum, curListNum)
                        return False, {"message": errorMsg}

                    if curNum != num:
                        curNum = num
                        curListNum = listNum
                        csvScriptDataInfoList = []
                        csvScriptDataAllInfoList.append(csvScriptDataInfoList)
                        csvScriptDataInfo = []
                        csvScriptDataInfoList.append(csvScriptDataInfo)
                    elif curListNum != listNum:
                        curListNum = listNum
                        csvScriptDataInfo = []
                        csvScriptDataInfoList.append(csvScriptDataInfo)
                    csvScriptDataInfo.append(row[1:])
                    csvScriptData = []
                    csvScriptDataInfo.append(csvScriptData)
                else:
                    cmdName = row[1]
                    if cmdName not in cmdList:
                        errorMsg = textSetting.textList["errorList"]["E8"].format(i + 1, cmdName)
                        return False, {"message": errorMsg}
                    if len(csvScriptData) >= 255:
                        errorMsg = textSetting.textList["errorList"]["E142"].format(curNum, curListNum)
                        return False, {"message": errorMsg}
                    csvScriptData.append(row)
                count += 1
        except Exception:
            errorMsg = textSetting.textList["errorList"]["E15"].format(i + 1)
            return False, {"message": errorMsg}
        
        obj = {"csvLines":count, "data":csvScriptDataAllInfoList}
        return True, obj
