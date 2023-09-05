import random
import os
import sys
import codecs
import tkinter
import program.textSetting as textSetting

LS = 0
BS = 1
CS = 2
RS = 3


def resource_path(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(os.path.abspath(os.path.dirname(__file__)), "resource"))
    return os.path.join(bundle_dir, relative_path)


class CsvWidget():
    def __init__(self, frame, content):
        self.csvNumLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["fvtNum"], font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
        self.csvNumLb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)

        self.faceNumLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceNum"], font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
        self.faceNumLb.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

        if content > LS:
            self.faceImgXposLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceWidth"], font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
            self.faceImgXposLb.grid(row=0, column=2, sticky=tkinter.W+tkinter.E)

            self.faceImgYposLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceHeight"], font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
            self.faceImgYposLb.grid(row=0, column=3, sticky=tkinter.W+tkinter.E)

            self.faceImgWidthLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceX"], font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
            self.faceImgWidthLb.grid(row=0, column=4, sticky=tkinter.W+tkinter.E)

            self.faceImgHeightLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceY"], font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
            self.faceImgHeightLb.grid(row=0, column=5, sticky=tkinter.W+tkinter.E)

        columnCnt = 0
        if content > LS:
            columnCnt = 4

        self.effectLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["effect"], font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
        self.effectLb.grid(row=0, column=columnCnt + 2, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)

        self.voiceNumLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["voNum"], font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
        self.voiceNumLb.grid(row=0, column=columnCnt + 3, sticky=tkinter.W+tkinter.E)

        self.txtLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["text"], font=textSetting.textList["font3"], width=10, borderwidth=1, relief="solid")
        self.txtLb.grid(row=0, column=columnCnt + 4, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)

        path = ""
        randList = []
        if content == LS:
            path = resource_path("LS.csv")
        elif content == BS:
            path = resource_path("BS.csv")
        elif content == CS:
            randList = [31]
            path = resource_path("CS.csv")
        elif content == RS:
            path = resource_path("RS.csv")

        f = codecs.open(path, "r", "shift-jis", "ignore")
        lines = f.readlines()
        f.close()
        lines.pop(0)

        fvtNumList = list(range(0, len(lines)))
        if content == BS:
            randList = [0]
            fvtNumList.pop(0)
        elif content == CS:
            randList = [31]
            fvtNumList.pop(31)
        elif content == RS:
            randList = [574]
            fvtNumList.pop(574)
        randList.extend(random.sample(fvtNumList, 3))
        randList.sort()

        row = 0
        maxNum = -1
        for rand in randList:
            row += 1
            line = lines[rand].strip()
            arr = line.split(",")
            fvtNum = int(arr[0])
            faceNum = int(arr[1])

            contentCnt = 0
            if content > LS:
                contentCnt = 4
                faceX = int(arr[2])
                faceY = int(arr[3])
                faceW = int(arr[4])
                faceH = int(arr[5])

            effect = int(arr[contentCnt + 2])
            voNum = int(arr[contentCnt + 3])

            text = arr[contentCnt + 4]
            if maxNum < len(text.encode("shift-jis")):
                maxNum = len(text.encode("shift-jis"))

            self.csvNumLb = tkinter.Label(frame, text=fvtNum, font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
            self.csvNumLb.grid(row=row, column=0, sticky=tkinter.W+tkinter.E)

            self.faceNumLb = tkinter.Label(frame, text=faceNum, font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
            self.faceNumLb.grid(row=row, column=1, sticky=tkinter.W+tkinter.E)

            if content > LS:
                self.faceImgXposLb = tkinter.Label(frame, text=faceX, font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
                self.faceImgXposLb.grid(row=row, column=2, sticky=tkinter.W+tkinter.E)

                self.faceImgYposLb = tkinter.Label(frame, text=faceY, font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
                self.faceImgYposLb.grid(row=row, column=3, sticky=tkinter.W+tkinter.E)

                self.faceImgWidthLb = tkinter.Label(frame, text=faceW, font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
                self.faceImgWidthLb.grid(row=row, column=4, sticky=tkinter.W+tkinter.E)

                self.faceImgHeightLb = tkinter.Label(frame, text=faceH, font=textSetting.textList["font3"], width=6, borderwidth=1, relief="solid")
                self.faceImgHeightLb.grid(row=row, column=5, sticky=tkinter.W+tkinter.E)

            self.effectLb = tkinter.Label(frame, text=effect, font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
            self.effectLb.grid(row=row, column=columnCnt + 2, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)

            self.voiceNumLb = tkinter.Label(frame, text=voNum, font=textSetting.textList["font3"], width=5, borderwidth=1, relief="solid")
            self.voiceNumLb.grid(row=row, column=columnCnt + 3, sticky=tkinter.W+tkinter.E)

            self.txtLb = tkinter.Label(frame, text=text, font=textSetting.textList["font3"], width=maxNum, borderwidth=1, relief="solid", anchor="w")
            self.txtLb.grid(row=row, column=columnCnt + 4, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)


class DescWidget():
    def __init__(self, frame, content):
        self.faceNumLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceNum2"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        self.faceNumLb.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        self.faceNumDescLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceNumDesc"], font=textSetting.textList["font4"], width=44, borderwidth=1, relief="solid", anchor="w", justify="left")
        self.faceNumDescLb.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

        self.faceSizeLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceSize"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        self.faceSizeLb.grid(row=1, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        self.faceSizeDescLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["faceSizeDesc"], font=textSetting.textList["font4"], borderwidth=1, relief="solid", anchor="w", justify="left")
        self.faceSizeDescLb.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

        self.effectLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["effect"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        self.effectLb.grid(row=2, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        self.effectDescLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["effectDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        self.effectDescLb.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)

        self.voiceLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["voNum2"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        self.voiceLb.grid(row=3, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        self.voiceDescLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["voNumDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        self.voiceDescLb.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)

        self.txtLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["textTag"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        self.txtLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)
        self.txtDescLb = tkinter.Label(frame, text=textSetting.textList["fvtMaker"]["textTagDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        self.txtDescLb.grid(row=4, column=1, sticky=tkinter.W+tkinter.E)

        self.padding = tkinter.Label(frame, width=33, font=textSetting.textList["font4"], anchor="w", borderwidth=1)
        self.padding.grid(row=0, column=2, sticky=tkinter.N+tkinter.W+tkinter.E)

        if content > LS:
            self.canvas = tkinter.Canvas(frame, bg="white", width=300, height=300)
            self.canvas.place(relx=1.0, rely=0.0, anchor=tkinter.N+tkinter.E)

            path = ""
            if content == BS:
                path = resource_path("BS.png")
            elif content == CS:
                path = resource_path("CS.png")
            elif content == RS:
                path = resource_path("RS.png")
            image = tkinter.PhotoImage(file=path)
            self.canvas.photo = image
            self.canvas.create_image(160, 160, image=self.canvas.photo)
