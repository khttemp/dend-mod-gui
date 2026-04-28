import tkinter
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame

from program.sub.orgInfoEditor.importPy.tab1.editOrgButtonWidget import EditOrgButtonWidget
from program.sub.orgInfoEditor.importPy.tab1.notchWidget import NotchWidget
from program.sub.orgInfoEditor.importPy.tab1.perfWidget import PerfWidget
from program.sub.orgInfoEditor.importPy.tab1.hurikoWidget import HurikoWidget

from program.sub.orgInfoEditor.importPy.tab2.countWidget import CountWidget
from program.sub.orgInfoEditor.importPy.tab2.modelWidget import TrainModelWidget
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

    EditOrgButtonWidget(tabFrame, decryptFile, defaultData, rootFrameAppearance, reloadWidget)

    notchPerfFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    notchPerfFrame.pack(anchor=tkinter.NW, padx=10, pady=5, expand=True, fill=tkinter.BOTH)

    speedLf = ttkCustomWidget.CustomTtkLabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["speedLfLabel"])
    speedLf.grid(row=0, column=0, padx=5, sticky=tkinter.NSEW)
    speedScrollFrame = ScrollbarFrame(speedLf, bgColor=rootFrameAppearance.bgColor)
    speedScrollFrame.pack(expand=True, fill=tkinter.BOTH)

    speed = trainInfo[0]
    notchCnt = len(speed) // decryptFile.notchContentCnt
    for notchIndex in range(notchCnt):
        notchWidget = NotchWidget(tabFrame, speedScrollFrame.interior, notchIndex, decryptFile, notchCnt, speed, selectDefaultData, rootFrameAppearance)
        notchWidget.pack(expand=True, fill=tkinter.BOTH)

    perfLf = ttkCustomWidget.CustomTtkLabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["perfLfLabel"])
    perfLf.grid(row=0, column=1, padx=5, sticky=tkinter.NSEW)
    perfScrollFrame = ScrollbarFrame(perfLf, bgColor=rootFrameAppearance.bgColor)
    perfScrollFrame.pack(expand=True, fill=tkinter.BOTH)

    perf = trainInfo[1]
    perfCnt = len(perf)
    for i in range(perfCnt):
        perfWidget = PerfWidget(tabFrame, perfScrollFrame.interior, decryptFile, decryptFile.trainPerfNameList[i], perf[i], selectDefaultData["att"][i], rootFrameAppearance)
        perfWidget.pack(expand=True, fill=tkinter.BOTH)

    if decryptFile.game in ["CS", "RS"]:
        huriko = trainInfo[2]
        for i in range(len(huriko)):
            hurikoWidget = HurikoWidget(tabFrame, perfScrollFrame.interior, decryptFile, decryptFile.trainHurikoNameList[i], huriko[i], selectDefaultData["huriko"][i], rootFrameAppearance)
            hurikoWidget.pack(expand=True, fill=tkinter.BOTH)

    notchPerfFrame.grid_columnconfigure(0, weight=2, uniform="trainOrgData")
    notchPerfFrame.grid_columnconfigure(1, weight=3, uniform="trainOrgData")
    notchPerfFrame.grid_rowconfigure(0, weight=1)


def tab2AllWidget(tabFrame, decryptFile, trainIdx, defaultData, rootFrameAppearance, reloadFunc):
    tab_two_frame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    tab_two_frame.pack(anchor=tkinter.NW, fill=tkinter.X)

    if decryptFile.game in ["RS", "CS", "BS", "LS"]:
        countModelLf = ttkCustomWidget.CustomTtkLabelFrame(tab_two_frame, text=textSetting.textList["orgInfoEditor"]["trainLfLabel"], height=250)
        countModelLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.X)
        countModelLf.propagate(False)

        countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, rootFrameAppearance, reloadFunc)

        edit_hensei_button = ttkCustomWidget.CustomTtkButton(countWidget.countFrame, text=textSetting.textList["orgInfoEditor"]["orgModify"])
        edit_hensei_button.grid(columnspan=3, row=3, column=0, sticky=tkinter.W + tkinter.E, pady=15)

        edit_model_button = ttkCustomWidget.CustomTtkButton(countWidget.countFrame, text=textSetting.textList["orgInfoEditor"]["modelInfoModify"])
        edit_model_button.grid(columnspan=3, row=4, column=0, sticky=tkinter.W + tkinter.E, pady=5)

        sep = ttkCustomWidget.CustomTtkSeparator(countModelLf, orient="vertical")
        sep.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=8)

        countModelScrollFrame = ScrollbarFrame(countModelLf, True, bgColor=rootFrameAppearance.bgColor)
        countModelScrollFrame.pack(expand=True, fill=tkinter.BOTH)

        innerButtonList = [
            countWidget.notchBtn,
            countWidget.henseiBtn,
            countWidget.colorBtn,
            edit_hensei_button,
            edit_model_button,
        ]

        TrainModelWidget(tabFrame, trainIdx, game, countModelScrollFrame.interior, widgetList, innerButtonList, decryptFile, rootFrameAppearance, reloadFunc)

        if game == gameDefine.LS:
            elseScrollFrame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
            elseScrollFrame.pack(expand=True, fill=tkinter.BOTH)
            elseFrame = elseScrollFrame.interior

            elseFrame2 = elseFrame
        else:
            elseFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
            elseFrame.pack(anchor=tkinter.NW, fill=tkinter.X)

            elseFrame2 = ttkCustomWidget.CustomTtkFrame(tabFrame)
            elseFrame2.pack(anchor=tkinter.NW, fill=tkinter.X)

        elseModel = decryptFile.trainModelList[trainIdx]["elseModel"]
        else2Model = decryptFile.trainModelList[trainIdx]["else2Model"]

        if len(elseModel) > 0:
            FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else1", elseModel, 1, rootFrameAppearance, reloadFunc)
        FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else2", else2Model, 2, rootFrameAppearance, reloadFunc)

        elseList2 = decryptFile.trainModelList[trainIdx]["elseList2"]
        FixedList2Widget(elseFrame2, trainIdx, decryptFile, "else3", elseList2, rootFrameAppearance, reloadFunc)
    else:
        trainOrgInfo = decryptFile.trainInfoList[trainIdx]
        if trainOrgInfo is None:
            return

        mainFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
        mainFrame.pack(fill=tkinter.BOTH, expand=True)
        scrollMainFrame = ScrollbarFrame(mainFrame, bgColor=rootFrameAppearance.bgColor)
        scrollMainFrame.pack(expand=True, fill=tkinter.BOTH)
        scrollFrame = scrollMainFrame.interior

        countModelLf = ttkCustomWidget.CustomTtkLabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSTrainLfLabel"])
        countModelLf.pack(anchor=tkinter.NW, padx=10, pady=3)

        countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, rootFrameAppearance, reloadFunc)

        sidePackFrame = ttkCustomWidget.CustomTtkFrame(scrollFrame)
        sidePackFrame.pack(anchor=tkinter.NW)
        rainPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSRainLfLabel"])
        rainPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, rainPerfLf, "rain", decryptFile.trainRainNameList, trainOrgInfo[2], True, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

        carbPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"])
        carbPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, carbPerfLf, "carb", decryptFile.trainCarbNameList, trainOrgInfo[3], True, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

        otherPerfLf = ttkCustomWidget.CustomTtkLabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"])
        otherPerfLf.pack(anchor=tkinter.NW, padx=10, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, otherPerfLf, "other", decryptFile.trainOtherNameList, trainOrgInfo[4], True, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

        sidePackFrame2 = ttkCustomWidget.CustomTtkFrame(scrollFrame)
        sidePackFrame2.pack(anchor=tkinter.NW)
        hurikoPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
        hurikoPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, hurikoPerfLf, "huriko", decryptFile.trainHurikoNameList, trainOrgInfo[5], False, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

        oneWheelPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        oneWheelPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, oneWheelPerfLf, "oneWheel", decryptFile.trainOneWheelNameList, trainOrgInfo[6], False, defaultData, decryptFile, rootFrameAppearance, reloadFunc)


def tab3AllWidget(tabFrame, decryptFile, trainIdx, rootFrameAppearance, reloadFunc):
    tab3frame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    tab3frame.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

    lensList = decryptFile.trainModelList[trainIdx]["lensList"]
    LensListWidget(tab3frame, decryptFile, trainIdx, lensList, rootFrameAppearance, reloadFunc)

    tailList = decryptFile.trainModelList[trainIdx]["tailList"]
    TailListWidget(tab3frame, decryptFile, trainIdx, tailList, rootFrameAppearance, reloadFunc)
