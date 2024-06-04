import tkinter
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

from program.tkinterScrollbarFrameClass import ScrollbarFrame
import program.orgInfoEditor.importPy.gameDefine as gameDefine

from program.orgInfoEditor.importPy.tab1.notchWidget import NotchWidget
from program.orgInfoEditor.importPy.tab1.perfWidget import PerfWidget
from program.orgInfoEditor.importPy.tab1.hurikoWidget import HurikoWidget
from program.orgInfoEditor.importPy.tab1.tab1EditWidget import setDefault, extractCsvTrainInfo, saveCsvTrainInfo, editTrain, editAllTrain

from program.orgInfoEditor.importPy.tab2.countWidget import CountWidget
from program.orgInfoEditor.importPy.tab2.modelWidget import TrainModelWidget
from program.orgInfoEditor.importPy.tab2.fixedListWidget import FixedListWidget
from program.orgInfoEditor.importPy.tab2.fixedList2Widget import FixedList2Widget
from program.orgInfoEditor.importPy.tab2.elsePerfWidget import ElsePerfWidget

from program.orgInfoEditor.importPy.tab3.lensListWidget import LensListWidget
from program.orgInfoEditor.importPy.tab3.tailListWidget import TailListWidget

gameDefine.load()


def tab1AllWidget(tabFrame, decryptFile, trainIdx, game, varList, btnList, defaultData, widgetList, rootFrameAppearance, reloadFunc):
    trainInfo = decryptFile.trainInfoList[trainIdx]
    if trainInfo is None:
        return

    btnFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    btnFrame.pack(fill=tkinter.X, anchor=tkinter.NW, padx=10, pady=5)

    set_default_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, command=lambda: setDefault(tabFrame, decryptFile, game, trainIdx, defaultData, rootFrameAppearance, reloadFunc), text=textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"])
    set_default_train_info_button.grid(row=0, column=0, padx=5, sticky=tkinter.NSEW)

    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        extract_csv_train_info_text = textSetting.textList["orgInfoEditor"]["extractCsv"]
    else:
        extract_csv_train_info_text = textSetting.textList["orgInfoEditor"]["extractText"]
    extract_csv_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=extract_csv_train_info_text, command=lambda: extractCsvTrainInfo(game, trainIdx, decryptFile))
    extract_csv_train_info_button.grid(row=0, column=1, padx=5, sticky=tkinter.NSEW)

    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        save_csv_train_info_text = textSetting.textList["orgInfoEditor"]["saveCsv"]
    else:
        save_csv_train_info_text = textSetting.textList["orgInfoEditor"]["saveText"]
    save_csv_train_info_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=save_csv_train_info_text, command=lambda: saveCsvTrainInfo(game, trainIdx, decryptFile, reloadFunc))
    save_csv_train_info_button.grid(row=0, column=2, padx=5, sticky=tkinter.NSEW)

    v_edit = widgetList[0]
    v_edit.set(textSetting.textList["orgInfoEditor"]["trainModify"])
    edit_button = ttkCustomWidget.CustomTtkButton(btnFrame, textvariable=v_edit)
    edit_button.grid(row=0, column=3, padx=5, sticky=tkinter.NSEW)

    edit_all_button = ttkCustomWidget.CustomTtkButton(btnFrame, text=textSetting.textList["orgInfoEditor"]["allSave"], command=lambda: editAllTrain(tabFrame, decryptFile, rootFrameAppearance, reloadFunc))
    edit_all_button.grid(row=0, column=4, padx=5, sticky=tkinter.NSEW)

    innerButtonList = [
        set_default_train_info_button,
        extract_csv_train_info_button,
        save_csv_train_info_button,
        edit_button,
        edit_all_button
    ]
    edit_button["command"] = lambda: editTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc)

    btnFrame.grid_columnconfigure(0, weight=1)
    btnFrame.grid_columnconfigure(1, weight=1)
    btnFrame.grid_columnconfigure(2, weight=1)
    btnFrame.grid_columnconfigure(3, weight=1)
    btnFrame.grid_columnconfigure(4, weight=1)

    speed = trainInfo[0]
    perf = trainInfo[1]

    notchPerfFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    notchPerfFrame.pack(anchor=tkinter.NW, padx=10, pady=5, expand=True, fill=tkinter.BOTH)

    speedLf = ttkCustomWidget.CustomTtkLabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["speedLfLabel"])
    speedLf.grid(row=0, column=0, padx=5, sticky=tkinter.NSEW)
    speedScrollFrame = ScrollbarFrame(speedLf, bgColor=rootFrameAppearance.bgColor)
    speedScrollFrame.pack(expand=True, fill=tkinter.BOTH)

    notchCnt = len(speed) // decryptFile.notchContentCnt
    for i in range(notchCnt):
        NotchWidget(tabFrame, trainIdx, i, notchCnt, speedScrollFrame.interior, speed, decryptFile, decryptFile.notchContentCnt, varList, btnList, defaultData, rootFrameAppearance)

    perfLf = ttkCustomWidget.CustomTtkLabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["perfLfLabel"])
    perfLf.grid(row=0, column=1, padx=5, sticky=tkinter.NSEW)
    perfScrollFrame = ScrollbarFrame(perfLf, bgColor=rootFrameAppearance.bgColor)
    perfScrollFrame.pack(expand=True, fill=tkinter.BOTH)

    perfCnt = len(perf)
    for i in range(perfCnt):
        PerfWidget(tabFrame, trainIdx, i, perfScrollFrame.interior, perf, decryptFile, varList, btnList, defaultData, rootFrameAppearance)

    if game in [gameDefine.CS, gameDefine.RS]:
        huriko = trainInfo[2]
        for i in range(len(huriko)):
            HurikoWidget(tabFrame, trainIdx, i, perfCnt, perfScrollFrame.interior, huriko, decryptFile, varList, btnList, defaultData, rootFrameAppearance)

    notchPerfFrame.grid_columnconfigure(0, weight=3)
    notchPerfFrame.grid_columnconfigure(1, weight=4)
    notchPerfFrame.grid_rowconfigure(0, weight=1)


def tab2AllWidget(tabFrame, decryptFile, trainIdx, game, defaultData, widgetList, rootFrameAppearance, reloadFunc):
    tab_two_frame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    tab_two_frame.pack(anchor=tkinter.NW, fill=tkinter.X)

    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        countModelLf = ttkCustomWidget.CustomTtkLabelFrame(tab_two_frame, text=textSetting.textList["orgInfoEditor"]["trainLfLabel"], height=250)
        countModelLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.X)
        countModelLf.propagate(False)

        countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, rootFrameAppearance, reloadFunc)

        v_edit = widgetList[0]
        v_edit.set(textSetting.textList["orgInfoEditor"]["orgModify"])
        edit_hensei_button = ttkCustomWidget.CustomTtkButton(countWidget.countFrame, textvariable=v_edit)
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


def tab3AllWidget(tabFrame, decryptFile, trainIdx, game, widgetList, rootFrameAppearance, reloadFunc):
    tab3frame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    tab3frame.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

    lensList = decryptFile.trainModelList[trainIdx]["lensList"]
    LensListWidget(tab3frame, decryptFile, trainIdx, lensList, rootFrameAppearance, reloadFunc)

    tailList = decryptFile.trainModelList[trainIdx]["tailList"]
    TailListWidget(tab3frame, decryptFile, trainIdx, tailList, rootFrameAppearance, reloadFunc)
