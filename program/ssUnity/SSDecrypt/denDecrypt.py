import os
import UnityPy
import traceback
from program.errorLogClass import ErrorLogObj


class DenDecrypt:
    def __init__(self, filePath):
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.fileDir = os.path.dirname(filePath)
        self.filenameAndExt = os.path.splitext(os.path.basename(filePath))
        self.env = None
        self.allList = []

    def open(self):
        try:
            self.env = UnityPy.load(self.filePath)
            return self.decrypt()
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        self.errObj.write(self.error)

    def decrypt(self):
        try:
            self.allList = []
            for env in self.env.objects:
                if env.type.name != "AssetBundle":
                    data = env.read()
                    size = data.byte_size
                    fileType = env.type.name
                    if fileType == "AudioClip":
                        for name, d in data.samples.items():
                            size = len(d)
                    container = data.container
                    if ".bytes" in container:
                        fileType = "TextAsset(bytes)"
                    elif ".txt" in container:
                        fileType = "TextAsset"
                    self.allList.append([data.name, fileType, size, data])
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False
