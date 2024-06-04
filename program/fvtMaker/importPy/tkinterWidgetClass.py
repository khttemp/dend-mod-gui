import random
import os
import sys
import codecs
import tkinter
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

LS = 0
BS = 1
CS = 2
RS = 3


def resource_path(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(os.path.abspath(os.path.dirname(__file__)), "resource"))
    return os.path.join(bundle_dir, relative_path)


class CsvWidget():
    def __init__(self, frame, content):
        csvNumHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["fvtNum"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
        csvNumHeaderLb.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)

        faceNumHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["faceNum"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
        faceNumHeaderLb.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

        if content > LS:
            faceImgXposHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["faceWidth"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            faceImgXposHeaderLb.grid(row=0, column=2, sticky=tkinter.W+tkinter.E)

            faceImgYposHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["faceHeight"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            faceImgYposHeaderLb.grid(row=0, column=3, sticky=tkinter.W+tkinter.E)

            faceImgWidthHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["faceX"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            faceImgWidthHeaderLb.grid(row=0, column=4, sticky=tkinter.W+tkinter.E)

            faceImgHeightHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["faceY"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
            faceImgHeightHeaderLb.grid(row=0, column=5, sticky=tkinter.W+tkinter.E)

        columnCnt = 0
        if content > LS:
            columnCnt = 4

        effectHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["effect"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
        effectHeaderLb.grid(row=0, column=columnCnt + 2, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)

        voiceNumHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["voNum"], font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
        voiceNumHeaderLb.grid(row=0, column=columnCnt + 3, sticky=tkinter.W+tkinter.E)

        txtHeaderLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["fvtMaker"]["text"], font=textSetting.textList["font3"], width=10, borderwidth=1, relief="solid")
        txtHeaderLb.grid(row=0, column=columnCnt + 4, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)

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

            csvNumLb = ttkCustomWidget.CustomTtkLabel(frame, text=fvtNum, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
            csvNumLb.grid(row=row, column=0, sticky=tkinter.W+tkinter.E)

            faceNumLb = ttkCustomWidget.CustomTtkLabel(frame, text=faceNum, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
            faceNumLb.grid(row=row, column=1, sticky=tkinter.W+tkinter.E)

            if content > LS:
                faceImgXposLb = ttkCustomWidget.CustomTtkLabel(frame, text=faceX, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
                faceImgXposLb.grid(row=row, column=2, sticky=tkinter.W+tkinter.E)

                faceImgYposLb = ttkCustomWidget.CustomTtkLabel(frame, text=faceY, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
                faceImgYposLb.grid(row=row, column=3, sticky=tkinter.W+tkinter.E)

                faceImgWidthLb = ttkCustomWidget.CustomTtkLabel(frame, text=faceW, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
                faceImgWidthLb.grid(row=row, column=4, sticky=tkinter.W+tkinter.E)

                faceImgHeightLb = ttkCustomWidget.CustomTtkLabel(frame, text=faceH, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=6, borderwidth=1, relief="solid")
                faceImgHeightLb.grid(row=row, column=5, sticky=tkinter.W+tkinter.E)

            effectLb = ttkCustomWidget.CustomTtkLabel(frame, text=effect, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
            effectLb.grid(row=row, column=columnCnt + 2, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)

            voiceNumLb = ttkCustomWidget.CustomTtkLabel(frame, text=voNum, font=textSetting.textList["font3"], anchor=tkinter.CENTER, width=5, borderwidth=1, relief="solid")
            voiceNumLb.grid(row=row, column=columnCnt + 3, sticky=tkinter.W+tkinter.E)

            txtLb = ttkCustomWidget.CustomTtkLabel(frame, text=text, font=textSetting.textList["font3"], width=maxNum, borderwidth=1, relief="solid", anchor="w")
            txtLb.grid(row=row, column=columnCnt + 4, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)


class DescWidget():
    def __init__(self, frame, content, rootFrameAppearance):
        descFrame = ttkCustomWidget.CustomTtkFrame(frame)
        descFrame.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        imageFrame = ttkCustomWidget.CustomTtkFrame(frame)
        imageFrame.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        faceNumLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceNum2"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        faceNumLb.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        faceNumDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceNumDesc"], font=textSetting.textList["font4"], width=44, borderwidth=1, relief="solid", anchor="w", justify="left")
        faceNumDescLb.grid(row=0, column=1, sticky=tkinter.W+tkinter.E)

        faceSizeLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceSize"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        faceSizeLb.grid(row=1, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        faceSizeDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceSizeDesc"], font=textSetting.textList["font4"], borderwidth=1, relief="solid", anchor="w", justify="left")
        faceSizeDescLb.grid(row=1, column=1, sticky=tkinter.W+tkinter.E)

        effectLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["effect"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        effectLb.grid(row=2, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        effectDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["effectDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        effectDescLb.grid(row=2, column=1, sticky=tkinter.W+tkinter.E)

        voiceLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["voNum2"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        voiceLb.grid(row=3, column=0, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        voiceDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["voNumDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        voiceDescLb.grid(row=3, column=1, sticky=tkinter.W+tkinter.E)

        txtLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["textTag"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        txtLb.grid(row=4, column=0, sticky=tkinter.W+tkinter.E)
        txtDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["textTagDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        txtDescLb.grid(row=4, column=1, sticky=tkinter.W+tkinter.E)

        if content > LS:
            canvas = tkinter.Canvas(imageFrame, width=300, height=300, bg=rootFrameAppearance.bgColor)
            canvas.pack(padx=3)

            path = ""
            if content == BS:
                path = resource_path("BS.png")
            elif content == CS:
                path = resource_path("CS.png")
            elif content == RS:
                path = resource_path("RS.png")
            image = tkinter.PhotoImage(file=path)
            canvas.photo = image
            canvas.create_image(160, 160, image=canvas.photo)
