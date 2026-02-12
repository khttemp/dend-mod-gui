class ErrorLogObj:
    def __init__(self):
        self.errorLogName = "error.log"
        self.enc = "utf-8"

    def write(self, error):
        w = open(self.errorLogName, "w", encoding=self.enc)
        w.write(error)
        w.close()
