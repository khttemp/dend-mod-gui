import os
import sys

import program.sub.textSetting as textSetting
from program.sub.orgInfoEditor.dendDecrypt import LSdecrypt as dendLs
from program.sub.orgInfoEditor.dendDecrypt import BSdecrypt as dendBs
from program.sub.orgInfoEditor.dendDecrypt import CSdecrypt as dendCs
from program.sub.orgInfoEditor.dendDecrypt import RSdecrypt as dendRs
from program.sub.orgInfoEditor.dendDecrypt import SSdecrypt as dendSs


def resource_path(localDir, relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", localDir)
    return os.path.join(bundle_dir, relative_path)


def readDefaultData(game):
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "dendData")
    errorMsg = textSetting.textList["errorList"]["E4"]
    defaultData = []
    path = ""
    if game == "SS":
        path = resource_path(filePath, "train_org_data.den")
        defaultDecrypt = dendSs.SSdecrypt(path)
    elif game == "RS":
        path = resource_path(filePath, "TRAIN_DATA4TH.BIN")
        defaultDecrypt = dendRs.RSdecrypt(path)
    elif game == "CS":
        path = resource_path(filePath, "TRAIN_DATA3RD.BIN")
        defaultDecrypt = dendCs.CSdecrypt(path)
    elif game == "BS":
        path = resource_path(filePath, "TRAIN_DATA2ND.BIN")
        defaultDecrypt = dendBs.BSdecrypt(path)
    elif game == "LS":
        path = resource_path(filePath, "TRAIN_DATA.BIN")
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
