import csv

import program.sub.textSetting as textSetting


def extractCsv(filePath, else3List):
    header = [
        "railNo",
        "num",
        "type",
        "railPos",
        "binIndex",
        "anime1",
        "anime2"
    ]
    with open(filePath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for else3Info in else3List:
            writer.writerow([else3Info[0], len(else3Info[1])] + else3Info[1][0])
            for j in range(1, len(else3Info[1])):
                writer.writerow(["", ""] + else3Info[1][j])


def loadCsv(filePath):
    count = 0
    else3List = []
    else3Info = []
    tempList = []
    firstReadFlag = True
    num = 0
    readNum = 0

    with open(filePath, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)

        try:
            count += 1
            next(reader)
        except StopIteration:
            pass

        for row in reader:
            if len(row) < 7:
                errorMsg = textSetting.textList["errorList"]["E15"].format(count + 1)
                return None, errorMsg

            if firstReadFlag:
                else3Info = []
                if row[0] == "" or row[1] == "":
                    errorMsg = textSetting.textList["errorList"]["E15"].format(count + 1)
                    return None, errorMsg
                num = int(row[1])
                else3Info.append(int(row[0]))
                tempList = []
                firstReadFlag = False
            else:
                if row[0] != "" or row[1] != "":
                    errorMsg = textSetting.textList["errorList"]["E92"].format(count + 1)
                    return None, errorMsg
            tempList.append([int(x) for x in row[2:]])
            readNum += 1
            if readNum == num:
                readNum = 0
                num = 0
                firstReadFlag = True
                else3Info.append(tempList)
                else3List.append(else3Info)
            count += 1
        
        if readNum != num:
            errorMsg = textSetting.textList["errorList"]["E92"].format(count)
            return None, errorMsg

        else3Obj = {"csvLines":count, "data":else3List}
        return else3Obj, None
