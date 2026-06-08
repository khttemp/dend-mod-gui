import traceback

def extractTrainInfoByDenFile(filePath, data):
    try:
        w = open(filePath, "wb")
        w.write(data.script)
        w.close()
        return True
    except PermissionError:
        return False

def loadTrainInfoTextFile(filePath):
    f = open(filePath, "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    return lines

def saveTrainInfoDenFile(filePath, data, decryptFile):
    try:
        with open(filePath, "rb") as f:
            data.script = f.read()
        data.save()
        with open(decryptFile.filePath, "wb") as w:
            w.write(decryptFile.env.file.save())
        return True
    except Exception:
        print(traceback.format_exc())
        return False
