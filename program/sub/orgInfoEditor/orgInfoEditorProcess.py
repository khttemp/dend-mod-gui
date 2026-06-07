import os

import program.sub.textSetting as textSetting
from program.sub.orgInfoEditor.dendDecrypt import LSdecrypt as dendLs
from program.sub.orgInfoEditor.dendDecrypt import BSdecrypt as dendBs
from program.sub.orgInfoEditor.dendDecrypt import CSdecrypt as dendCs
from program.sub.orgInfoEditor.dendDecrypt import RSdecrypt as dendRs
from program.sub.orgInfoEditor.dendDecrypt import SSdecrypt as dendSs


def readDefaultData(rootPath, game):
    filePath = os.path.join(rootPath, "program", "sub", "orgInfoEditor", "dendData")
    errorMsg = textSetting.textList["errorList"]["E4"]
    defaultData = []
    path = ""
    if game == "SS":
        path = os.path.join(filePath, "train_org_data.den")
        defaultDecrypt = dendSs.SSdecrypt(path)
    elif game == "RS":
        path = os.path.join(filePath, "TRAIN_DATA4TH.BIN")
        defaultDecrypt = dendRs.RSdecrypt(path)
    elif game == "CS":
        path = os.path.join(filePath, "TRAIN_DATA3RD.BIN")
        defaultDecrypt = dendCs.CSdecrypt(path)
    elif game == "BS":
        path = os.path.join(filePath, "TRAIN_DATA2ND.BIN")
        defaultDecrypt = dendBs.BSdecrypt(path)
    elif game == "LS":
        path = os.path.join(filePath, "TRAIN_DATA.BIN")
        defaultDecrypt = dendLs.LSdecrypt(path)
    else:
        return False, {"message":errorMsg }

    if not defaultDecrypt.open():
        defaultDecrypt.printError()
        return False, {"message":errorMsg }

    trainOrgInfoList = defaultDecrypt.trainInfoList
    for trainOrgInfo in trainOrgInfoList:
        if game == "SS":
            speedList = trainOrgInfo[0]
            notchCnt = len(speedList) // defaultDecrypt.notchContentCnt
            perfList = trainOrgInfo[1]
            rainList = trainOrgInfo[2]
            carbList = trainOrgInfo[3]
            otherList = trainOrgInfo[4]
            hurikoList = trainOrgInfo[5]
            oneWheelList = trainOrgInfo[6]
            defaultData.append(
                {
                    "notch": speedList[0:notchCnt],
                    "tlk": speedList[notchCnt:notchCnt*2],
                    "soundNum": speedList[notchCnt*2:notchCnt*3],
                    "add": speedList[notchCnt*3:notchCnt*4],
                    "att": perfList,
                    "rain": rainList,
                    "carb": carbList,
                    "other": otherList,
                    "huriko": hurikoList,
                    "oneWheel": oneWheelList
                })
        else:
            speedList = trainOrgInfo[0]
            notchCnt = len(speedList) // defaultDecrypt.notchContentCnt
            perfList = trainOrgInfo[1]
            if defaultDecrypt.game in ["CS", "RS"]:
                hurikoList = trainOrgInfo[2]
                defaultData.append(
                    {
                        "notch": speedList[0:notchCnt],
                        "tlk": speedList[notchCnt:notchCnt*2],
                        "soundNum": speedList[notchCnt*2:notchCnt*3],
                        "add": speedList[notchCnt*3:notchCnt*4],
                        "att": perfList,
                        "huriko": hurikoList,
                    })
            else:
                defaultData.append(
                    {
                        "notch": speedList[0:notchCnt],
                        "tlk": speedList[notchCnt:notchCnt*2],
                        "att": perfList,
                    })

    return True, {"data":defaultData}
