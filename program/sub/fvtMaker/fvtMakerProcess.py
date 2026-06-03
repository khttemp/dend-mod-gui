import random

LS = 1
BS = 2
CS = 3
RS = 4


def getCsvInfo(game, fvtInfo):
    headerList = fvtInfo.pop(0)

    fvtNumList = list(range(0, len(fvtInfo)))
    randList = []
    if game == BS:
        randList = [0]
        fvtNumList.pop(0)
    elif game == CS:
        randList = [31]
        fvtNumList.pop(31)
    elif game == RS:
        randList = [574]
        fvtNumList.pop(574)
    randList.extend(random.sample(fvtNumList, 4 - len(randList)))
    randList.sort()

    dataList = [fvtInfo[x] for x in randList]
    return headerList, dataList
