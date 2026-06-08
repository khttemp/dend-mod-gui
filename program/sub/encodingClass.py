class SJISEncodingObject:
    def __init__(self):
        self.enc = "cp932"

    def convertString(self, byteArr):
        try:
            return byteArr.decode(self.enc)
        except:
            return None

    def convertByteArray(self, text):
        try:
            return text.encode(self.enc)
        except:
            return None
