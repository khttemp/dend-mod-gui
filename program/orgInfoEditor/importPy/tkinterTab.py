import tkinter
from tkinter import ttk
import program.textSetting as textSetting

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


def tab1AllWidget(tabFrame, decryptFile, trainIdx, game, varList, btnList, defaultData, widgetList, reloadFunc):
    tab_one_frame = ttk.Frame(tabFrame)
    tab_one_frame.pack(expand=True, fill=tkinter.BOTH)

    btnFrame = ttk.Frame(tab_one_frame)
    btnFrame.pack(anchor=tkinter.NW, padx=10, pady=5)

    set_default_train_info_button = ttk.Button(btnFrame, width=25, command=lambda: setDefault(tabFrame, decryptFile, game, trainIdx, defaultData, reloadFunc), text=textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"])
    set_default_train_info_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        extract_csv_train_info_text = textSetting.textList["orgInfoEditor"]["extractCsv"]
    else:
        extract_csv_train_info_text = textSetting.textList["orgInfoEditor"]["extractText"]
    extract_csv_train_info_button = ttk.Button(btnFrame, width=25, text=extract_csv_train_info_text, command=lambda: extractCsvTrainInfo(game, trainIdx, decryptFile))
    extract_csv_train_info_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        save_csv_train_inf_text = textSetting.textList["orgInfoEditor"]["saveCsv"]
    else:
        save_csv_train_inf_text = textSetting.textList["orgInfoEditor"]["saveText"]
    save_csv_train_info_button = ttk.Button(btnFrame, width=25, text=save_csv_train_inf_text, command=lambda: saveCsvTrainInfo(game, trainIdx, decryptFile, reloadFunc))
    save_csv_train_info_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    v_edit = widgetList[0]
    v_edit.set(textSetting.textList["orgInfoEditor"]["trainModify"])
    edit_button = ttk.Button(btnFrame, textvariable=v_edit, width=25)
    edit_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    edit_all_button = ttk.Button(btnFrame, width=25, text=textSetting.textList["orgInfoEditor"]["allSave"], command=lambda: editAllTrain(tabFrame, decryptFile, reloadFunc))
    edit_all_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    innerButtonList = [
        set_default_train_info_button,
        extract_csv_train_info_button,
        save_csv_train_info_button,
        edit_button,
        edit_all_button
    ]
    edit_button["command"] = lambda: editTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc)

    trainInfo = decryptFile.trainInfoList[trainIdx]
    speed = trainInfo[0]
    perf = trainInfo[1]

    notchPerfFrame = ttk.Frame(tab_one_frame)
    notchPerfFrame.pack(anchor=tkinter.NW, padx=10, pady=5, expand=True, fill=tkinter.BOTH)

    speedLf = ttk.LabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["speedLfLabel"])
    speedLf.place(relx=0, rely=0, relwidth=0.4, relheight=0.98)
    speedScrollFrame = ScrollbarFrame(speedLf)

    notchCnt = len(speed) // decryptFile.notchContentCnt
    for i in range(notchCnt):
        NotchWidget(tabFrame, trainIdx, i, notchCnt, speedScrollFrame.frame, speed, decryptFile, decryptFile.notchContentCnt, varList, btnList, defaultData)

    perfLf = ttk.LabelFrame(notchPerfFrame, text=textSetting.textList["orgInfoEditor"]["perfLfLabel"])
    perfLf.place(relx=0.43, rely=0, relwidth=0.56, relheight=0.98)
    perfScrollFrame = ScrollbarFrame(perfLf)

    perfCnt = len(perf)
    for i in range(perfCnt):
        PerfWidget(tabFrame, trainIdx, i, perfScrollFrame.frame, perf, decryptFile, varList, btnList, defaultData)

    if game in [gameDefine.CS, gameDefine.RS]:
        huriko = trainInfo[2]
        for i in range(len(huriko)):
            HurikoWidget(tabFrame, trainIdx, i, perfCnt, perfScrollFrame.frame, huriko, decryptFile, varList, btnList, defaultData)


def tab2AllWidget(tabFrame, decryptFile, trainIdx, game, defaultData, widgetList, reloadFunc):
    tab_two_frame = ttk.Frame(tabFrame)
    tab_two_frame.pack(anchor=tkinter.NW, fill=tkinter.X)

    if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        countModelLf = ttk.LabelFrame(tab_two_frame, text=textSetting.textList["orgInfoEditor"]["trainLfLabel"], height=250)
        countModelLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.X)
        countModelLf.propagate(False)

        countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, reloadFunc)

        v_edit = widgetList[0]
        v_edit.set(textSetting.textList["orgInfoEditor"]["orgModify"])
        edit_hensei_button = ttk.Button(countWidget.countFrame, textvariable=v_edit)
        edit_hensei_button.grid(columnspan=3, row=3, column=0, sticky=tkinter.W + tkinter.E, pady=15)

        edit_model_button = ttk.Button(countWidget.countFrame, text=textSetting.textList["orgInfoEditor"]["modelInfoModify"])
        edit_model_button.grid(columnspan=3, row=4, column=0, sticky=tkinter.W + tkinter.E, pady=5)

        sep = ttk.Separator(countModelLf, orient="vertical")
        sep.pack(side=tkinter.LEFT, fill=tkinter.Y)

        countModelScrollFrame = ScrollbarFrame(countModelLf, True, False)

        innerButtonList = [
            countWidget.notchBtn,
            countWidget.henseiBtn,
            countWidget.colorBtn,
            edit_hensei_button,
            edit_model_button,
        ]

        TrainModelWidget(tabFrame, trainIdx, game, countModelScrollFrame.frame, widgetList, innerButtonList, decryptFile, reloadFunc)

        if game == gameDefine.LS:
            elseScrollFrame = ScrollbarFrame(tabFrame)
            elseFrame = elseScrollFrame.frame

            elseFrame2 = elseFrame
        else:
            elseFrame = ttk.Frame(tabFrame)
            elseFrame.pack(anchor=tkinter.NW, fill=tkinter.X)

            elseFrame2 = ttk.Frame(tabFrame)
            elseFrame2.pack(anchor=tkinter.NW, fill=tkinter.X)

        elseModel = decryptFile.trainModelList[trainIdx]["elseModel"]
        else2Model = decryptFile.trainModelList[trainIdx]["else2Model"]

        if len(elseModel) > 0:
            FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else1", elseModel, 1, reloadFunc)
        FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else2", else2Model, 2, reloadFunc)

        elseList2 = decryptFile.trainModelList[trainIdx]["elseList2"]
        FixedList2Widget(elseFrame2, trainIdx, decryptFile, "else3", elseList2, reloadFunc)
    else:
        mainFrame = ttk.Frame(tabFrame)
        mainFrame.pack(fill=tkinter.BOTH, expand=True)
        scrollMainFrame = ScrollbarFrame(mainFrame)
        scrollFrame = scrollMainFrame.frame

        countModelLf = ttk.LabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSTrainLfLabel"])
        countModelLf.pack(anchor=tkinter.NW, padx=10, pady=3)

        countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, reloadFunc)

        trainOrgInfo = decryptFile.trainInfoList[trainIdx]

        sidePackFrame = ttk.Frame(scrollFrame)
        sidePackFrame.pack(anchor=tkinter.NW)
        rainPerfLf = ttk.LabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSRainLfLabel"])
        rainPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, rainPerfLf, "rain", decryptFile.trainRainNameList, trainOrgInfo[2], True, defaultData, decryptFile, reloadFunc)

        carbPerfLf = ttk.LabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"])
        carbPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, carbPerfLf, "carb", decryptFile.trainCarbNameList, trainOrgInfo[3], True, defaultData, decryptFile, reloadFunc)

        otherPerfLf = ttk.LabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"])
        otherPerfLf.pack(anchor=tkinter.NW, padx=10, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, otherPerfLf, "other", decryptFile.trainOtherNameList, trainOrgInfo[4], True, defaultData, decryptFile, reloadFunc)

        sidePackFrame2 = ttk.Frame(scrollFrame)
        sidePackFrame2.pack(anchor=tkinter.NW)
        hurikoPerfLf = ttk.LabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
        hurikoPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, hurikoPerfLf, "huriko", decryptFile.trainHurikoNameList, trainOrgInfo[5], False, defaultData, decryptFile, reloadFunc)

        oneWheelPerfLf = ttk.LabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        oneWheelPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
        ElsePerfWidget(tabFrame, trainIdx, game, oneWheelPerfLf, "oneWheel", decryptFile.trainOneWheelNameList, trainOrgInfo[6], False, defaultData, decryptFile, reloadFunc)


def tab3AllWidget(tabFrame, decryptFile, trainIdx, game, widgetList, reloadFunc):
    tab3frame = ttk.Frame(tabFrame)
    tab3frame.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

    lensList = decryptFile.trainModelList[trainIdx]["lensList"]
    LensListWidget(tab3frame, decryptFile, trainIdx, lensList, reloadFunc)

    tailList = decryptFile.trainModelList[trainIdx]["tailList"]
    TailListWidget(tab3frame, decryptFile, trainIdx, tailList, reloadFunc)
