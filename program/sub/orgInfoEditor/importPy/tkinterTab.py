import tkinter
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame

from program.sub.orgInfoEditor.importPy.tab1.editOrgButtonWidget import EditOrgButtonWidget
from program.sub.orgInfoEditor.importPy.tab1.notchWidget import NotchWidget
from program.sub.orgInfoEditor.importPy.tab1.perfWidget import PerfWidget
from program.sub.orgInfoEditor.importPy.tab1.hurikoWidget import HurikoWidget

from program.sub.orgInfoEditor.importPy.tab2.notchCountWidget import NotchCountWidget
from program.sub.orgInfoEditor.importPy.tab2.countWidget import CountWidget
from program.sub.orgInfoEditor.importPy.tab2.trainModelWidget import TrainModelWidget
from program.sub.orgInfoEditor.importPy.tab2.editModelWidget import EditModelWidget
from program.sub.orgInfoEditor.importPy.tab2.fixedListWidget import FixedListWidget
from program.sub.orgInfoEditor.importPy.tab2.fixedList2Widget import FixedList2Widget
from program.sub.orgInfoEditor.importPy.tab2.elsePerfWidget import ElsePerfWidget

from program.sub.orgInfoEditor.importPy.tab3.lensListWidget import LensListWidget
from program.sub.orgInfoEditor.importPy.tab3.tailListWidget import TailListWidget


def tab1AllWidget(tabFrame, decryptFile, trainIndex, defaultData, rootFrameAppearance, reloadWidget):
    trainInfo = decryptFile.trainInfoList[trainIndex]
    if trainInfo is None:
        return
    selectDefaultData = defaultData[trainIndex]

    editOrgButtonWidget = EditOrgButtonWidget(tabFrame, decryptFile, defaultData, rootFrameAppearance, reloadWidget)
    editOrgButtonWidget.pack(fill=tkinter.X)

    notchPerfFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    notchPerfFrame.pack(anchor=tkinter.NW, padx=10, pady=5, expand=True, fill=tkinter.BOTH)

    speedLf = ttkCustomWidget.CustomTtkLabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["speedLfLabel"])
    speedLf.grid(row=0, column=0, padx=5, sticky=tkinter.NSEW)
    speedScrollFrame = ScrollbarFrame(speedLf, bgColor=rootFrameAppearance.bgColor)
    speedScrollFrame.pack(expand=True, fill=tkinter.BOTH)

    speed = trainInfo[0]
    notchCnt = len(speed) // decryptFile.notchContentCnt
    for notchIndex in range(notchCnt):
        notchWidget = NotchWidget(speedScrollFrame.interior, notchIndex, decryptFile, notchCnt, speed, selectDefaultData, rootFrameAppearance)
        notchWidget.pack(expand=True, fill=tkinter.BOTH)

    perfLf = ttkCustomWidget.CustomTtkLabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["perfLfLabel"])
    perfLf.grid(row=0, column=1, padx=5, sticky=tkinter.NSEW)
    perfScrollFrame = ScrollbarFrame(perfLf, bgColor=rootFrameAppearance.bgColor)
    perfScrollFrame.pack(expand=True, fill=tkinter.BOTH)

    perf = trainInfo[1]
    perfCnt = len(perf)
    for i in range(perfCnt):
        perfWidget = PerfWidget(perfScrollFrame.interior, decryptFile, decryptFile.trainPerfNameList[i], perf[i], selectDefaultData["att"][i], rootFrameAppearance)
        perfWidget.pack(expand=True, fill=tkinter.BOTH)

    if decryptFile.game in ["CS", "RS"]:
        huriko = trainInfo[2]
        for i in range(len(huriko)):
            hurikoWidget = HurikoWidget(perfScrollFrame.interior, decryptFile, decryptFile.trainHurikoNameList[i], huriko[i], selectDefaultData["huriko"][i], rootFrameAppearance)
            hurikoWidget.pack(expand=True, fill=tkinter.BOTH)

    notchPerfFrame.grid_columnconfigure(0, weight=2, uniform="trainOrgData")
    notchPerfFrame.grid_columnconfigure(1, weight=3, uniform="trainOrgData")
    notchPerfFrame.grid_rowconfigure(0, weight=1)


def tab2AllWidget(tabFrame, decryptFile, trainIndex, defaultData, rootFrameAppearance, reloadWidget):
    if decryptFile.game in ["RS", "CS", "BS", "LS"]:
        trainLf = ttkCustomWidget.CustomTtkLabelFrame(tabFrame, text=textSetting.textList["orgInfoEditor"]["trainLfLabel"])
        trainLf.grid(row=0, column=0, padx=10, pady=5, sticky=tkinter.NSEW)

        countFrame = ttkCustomWidget.CustomTtkFrame(trainLf)
        countFrame.grid(row=0, column=0, padx=(15, 0), pady=5, sticky=tkinter.NSEW)

        index = decryptFile.indexList[trainIndex]
        notchNum = decryptFile.byteArr[index]
        notchCountWidget = NotchCountWidget(countFrame, trainIndex, notchNum, decryptFile, rootFrameAppearance, reloadWidget)
        notchCountWidget.pack()

        countWidget = CountWidget(countFrame, trainIndex, decryptFile, rootFrameAppearance, reloadWidget)
        countWidget.pack()

        buttonFrame = ttkCustomWidget.CustomTtkFrame(countFrame)
        buttonFrame.pack(expand=True, fill=tkinter.BOTH)

        sep = ttkCustomWidget.CustomTtkSeparator(trainLf, orient="vertical")
        sep.grid(row=0, column=1, padx=8, sticky=tkinter.NS)

        countModelScrollFrame = ScrollbarFrame(trainLf, True, bgColor=rootFrameAppearance.bgColor)
        countModelScrollFrame.grid(row=0, column=2, sticky=tkinter.NSEW)

        trainModelWidget = TrainModelWidget(countModelScrollFrame.interior, trainIndex, buttonFrame, decryptFile, rootFrameAppearance, reloadWidget)
        trainModelWidget.pack()

        editModelButton = EditModelWidget(buttonFrame, trainIndex, decryptFile, rootFrameAppearance, reloadWidget)
        editModelButton.grid(row=1, column=0, sticky=tkinter.W + tkinter.E, pady=5)

        trainLf.rowconfigure(0, weight=1)
        trainLf.columnconfigure(0, weight=4, uniform="trainLf")
        trainLf.columnconfigure(2, weight=11, uniform="trainLf")

        elseScrollFrame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
        elseScrollFrame.grid(row=1, column=0, sticky=tkinter.NSEW)

        elseModel = decryptFile.trainModelList[trainIndex]["elseModel"]
        else2Model = decryptFile.trainModelList[trainIndex]["else2Model"]
        elseList2 = decryptFile.trainModelList[trainIndex]["elseList2"]

        if len(elseModel) > 0:
            FixedListWidget(elseScrollFrame.interior, trainIndex, decryptFile, "else1", elseModel, 1, rootFrameAppearance, reloadWidget)
        FixedListWidget(elseScrollFrame.interior, trainIndex, decryptFile, "else2", else2Model, 2, rootFrameAppearance, reloadWidget)
        FixedList2Widget(elseScrollFrame.interior, trainIndex, decryptFile, "else3", elseList2, rootFrameAppearance, reloadWidget)
    else:
        trainOrgInfo = decryptFile.trainInfoList[trainIndex]
        if trainOrgInfo is None:
            return
        selectDefaultData = defaultData[trainIndex]

        mainFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
        mainFrame.pack(fill=tkinter.BOTH, expand=True)
        scrollMainFrame = ScrollbarFrame(mainFrame, bgColor=rootFrameAppearance.bgColor)
        scrollMainFrame.pack(expand=True, fill=tkinter.BOTH)
        scrollFrame = scrollMainFrame.interior

        countModelLf = ttkCustomWidget.CustomTtkLabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSTrainLfLabel"])
        countModelLf.pack(anchor=tkinter.NW, padx=10, pady=3)

        speedList = trainOrgInfo[0]
        notchNum = len(speedList) // decryptFile.notchContentCnt
        notchCountWidget = NotchCountWidget(countModelLf, trainIndex, notchNum, decryptFile, rootFrameAppearance, reloadWidget)
        notchCountWidget.pack(anchor=tkinter.NW)

        sidePackFrame = ttkCustomWidget.CustomTtkFrame(scrollFrame)
        sidePackFrame.pack(anchor=tkinter.NW)
        rainPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSRainLfLabel"])
        rainPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
        rainPerfWidget = ElsePerfWidget(rainPerfLf, trainIndex, decryptFile, "rain", decryptFile.trainRainNameList, trainOrgInfo[2], True, selectDefaultData, rootFrameAppearance, reloadWidget)
        rainPerfWidget.pack()

        carbPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"])
        carbPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
        carbPerfWidget = ElsePerfWidget(carbPerfLf, trainIndex, decryptFile, "carb", decryptFile.trainCarbNameList, trainOrgInfo[3], True, selectDefaultData, rootFrameAppearance, reloadWidget)
        carbPerfWidget.pack()

        otherPerfLf = ttkCustomWidget.CustomTtkLabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"])
        otherPerfLf.pack(anchor=tkinter.NW, padx=10, pady=3)
        otherPerfWidget = ElsePerfWidget(otherPerfLf, trainIndex, decryptFile, "other", decryptFile.trainOtherNameList, trainOrgInfo[4], True, selectDefaultData, rootFrameAppearance, reloadWidget)
        otherPerfWidget.pack()

        sidePackFrame2 = ttkCustomWidget.CustomTtkFrame(scrollFrame)
        sidePackFrame2.pack(anchor=tkinter.NW)
        hurikoPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
        hurikoPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
        hurikoPerfWidget = ElsePerfWidget(hurikoPerfLf, trainIndex, decryptFile, "huriko", decryptFile.trainHurikoNameList, trainOrgInfo[5], False, selectDefaultData, rootFrameAppearance, reloadWidget)
        hurikoPerfWidget.pack()

        oneWheelPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        oneWheelPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
        oneWheelPerfWidget = ElsePerfWidget(oneWheelPerfLf, trainIndex, decryptFile, "oneWheel", decryptFile.trainOneWheelNameList, trainOrgInfo[6], False, selectDefaultData, rootFrameAppearance, reloadWidget)
        oneWheelPerfWidget.pack()
    tabFrame.grid_rowconfigure(0, weight=2, uniform="trainOrgData")
    tabFrame.grid_rowconfigure(1, weight=3, uniform="trainOrgData")
    tabFrame.grid_columnconfigure(0, weight=1)

def tab3AllWidget(tabFrame, decryptFile, trainIdx, rootFrameAppearance, reloadWidget):
    tab3frame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    tab3frame.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

    lensListWidget = LensListWidget(tab3frame, decryptFile, trainIdx, rootFrameAppearance, reloadWidget)
    lensListWidget.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)

    tailListWidget = TailListWidget(tab3frame, decryptFile, trainIdx, rootFrameAppearance, reloadWidget)
    tailListWidget.pack(anchor=tkinter.NW, padx=10, expand=True, fill=tkinter.BOTH)
