import tkinter
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget
from program.sub.encodingClass import SJISEncodingObject


class CsvWidget(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, headerList, dataList):
        super().__init__(master)

        mainFrame = ttkCustomWidget.CustomTtkFrame(self)
        mainFrame.pack()

        for i, header in enumerate(headerList):
            headerLb = ttkCustomWidget.CustomTtkLabel(mainFrame, text=header, font=textSetting.textList["font3"], anchor=tkinter.CENTER, borderwidth=1, relief="solid")
            headerLb.grid(row=0, column=i, ipadx=5, sticky=tkinter.W+tkinter.E)

        for i, dataInfo in enumerate(dataList):
            for j, data in enumerate(dataInfo):
                dataLb = ttkCustomWidget.CustomTtkLabel(mainFrame, text=str(data), font=textSetting.textList["font3"], borderwidth=1, relief="solid")
                if j != len(dataInfo) - 1:
                    dataLb.config(anchor=tkinter.CENTER)
                dataLb.grid(row=i + 1, column=j, ipadx=5, sticky=tkinter.W+tkinter.E)


class DescWidget(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, master, fvtImageInfo, game, rootFrameAppearance):
        super().__init__(master)

        self.LS = 1
        self.BS = 2
        self.CS = 3
        self.RS = 4

        mainFrame = ttkCustomWidget.CustomTtkFrame(self)
        mainFrame.pack()

        descFrame = ttkCustomWidget.CustomTtkFrame(mainFrame)
        descFrame.grid(row=0, column=0, sticky=tkinter.NSEW)
        imageFrame = ttkCustomWidget.CustomTtkFrame(mainFrame)
        imageFrame.grid(row=0, column=1, sticky=tkinter.NSEW)

        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(1, weight=1)

        faceNumLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceNum2"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        faceNumLb.grid(row=0, column=0, ipadx=5, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        faceNumDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceNumDesc"], font=textSetting.textList["font4"], width=44, borderwidth=1, relief="solid", anchor="w", justify="left")
        faceNumDescLb.grid(row=0, column=1, ipadx=5, sticky=tkinter.W+tkinter.E)

        faceSizeLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceSize"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        faceSizeLb.grid(row=1, column=0, ipadx=5, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        faceSizeDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["faceSizeDesc"], font=textSetting.textList["font4"], borderwidth=1, relief="solid", anchor="w", justify="left")
        faceSizeDescLb.grid(row=1, column=1, ipadx=5, sticky=tkinter.W+tkinter.E)

        effectLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["effect"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        effectLb.grid(row=2, column=0, ipadx=5, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        effectDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["effectDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        effectDescLb.grid(row=2, column=1, ipadx=5, sticky=tkinter.W+tkinter.E)

        voiceLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["voNum2"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        voiceLb.grid(row=3, column=0, ipadx=5, sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        voiceDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["voNumDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        voiceDescLb.grid(row=3, column=1, ipadx=5, sticky=tkinter.W+tkinter.E)

        txtLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["textTag"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid")
        txtLb.grid(row=4, column=0, ipadx=5, sticky=tkinter.W+tkinter.E)
        txtDescLb = ttkCustomWidget.CustomTtkLabel(descFrame, text=textSetting.textList["fvtMaker"]["textTagDesc"], font=textSetting.textList["font4"], anchor="w", borderwidth=1, relief="solid", justify="left")
        txtDescLb.grid(row=4, column=1, ipadx=5, sticky=tkinter.W+tkinter.E)

        if game > self.LS:
            if game == self.BS:
                path = fvtImageInfo["BS"]
            elif game == self.CS:
                path = fvtImageInfo["CS"]
            else:
                path = fvtImageInfo["RS"]

            canvas = tkinter.Canvas(imageFrame, width=300, height=300, bg=rootFrameAppearance.bgColor)
            canvas.pack(padx=3)

            image = tkinter.PhotoImage(file=path)
            canvas.photo = image
            canvas.create_image(160, 160, image=canvas.photo)
