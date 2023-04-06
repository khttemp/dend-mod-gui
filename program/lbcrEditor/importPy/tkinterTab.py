import tkinter
from tkinter import ttk

from program.lbcrEditor.importPy.tkinterScrollbarFrameClass import ScrollbarFrame

from program.lbcrEditor.importPy.tab1.notchWidget import NotchWidget
from program.lbcrEditor.importPy.tab1.perfWidget import PerfWidget
from program.lbcrEditor.importPy.tab1.hurikoWidget import HurikoWidget
from program.lbcrEditor.importPy.tab1.tab1EditWidget import setDefault, extractCsvTrainInfo, saveCsvTrainInfo, editTrain, editAllTrain

from program.lbcrEditor.importPy.tab2.countWidget import CountWidget
from program.lbcrEditor.importPy.tab2.modelWidget import TrainModelWidget
from program.lbcrEditor.importPy.tab2.fixedListWidget import FixedListWidget
from program.lbcrEditor.importPy.tab2.fixedList2Widget import FixedList2Widget

from program.lbcrEditor.importPy.tab3.lensListWidget import LensListWidget
from program.lbcrEditor.importPy.tab3.tailListWidget import TailListWidget


def tab1AllWidget(tabFrame, decryptFile, trainIdx, varList, btnList, defaultData, widgetList, reloadFunc):
    tab_one_frame = ttk.Frame(tabFrame)
    tab_one_frame.pack(expand=True, fill=tkinter.BOTH)

    btnFrame = ttk.Frame(tab_one_frame)
    btnFrame.pack(anchor=tkinter.NW, padx=10, pady=5)

    set_default_train_info_button = ttk.Button(btnFrame, width=25, command=lambda: setDefault(tabFrame, decryptFile, defaultData, reloadFunc), text="車両の性能をデフォルトに戻す")
    set_default_train_info_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    extract_csv_train_info_button = ttk.Button(btnFrame, width=25, text="車両情報をCSVで取り出す", command=lambda: extractCsvTrainInfo(trainIdx, decryptFile))
    extract_csv_train_info_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    save_csv_train_info_button = ttk.Button(btnFrame, width=25, text="車両情報をCSVで上書きする", command=lambda: saveCsvTrainInfo(trainIdx, decryptFile, reloadFunc))
    save_csv_train_info_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    v_edit = widgetList[0]
    v_edit.set("この車両を修正する")
    edit_button = ttk.Button(btnFrame, textvariable=v_edit, width=25)
    edit_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    edit_all_button = ttk.Button(btnFrame, width=25, text="同じ倍率で全部修正する", command=lambda: editAllTrain(tabFrame, decryptFile, reloadFunc))
    edit_all_button.pack(side=tkinter.LEFT, padx=15, pady=5)

    innerButtonList = [
        set_default_train_info_button,
        extract_csv_train_info_button,
        save_csv_train_info_button,
        edit_button,
        edit_all_button
    ]
    edit_button["command"] = lambda: editTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc)

    if decryptFile.trainHurikoNameList != "":
        speed = decryptFile.trainInfoList[3 * trainIdx]
        perf = decryptFile.trainInfoList[3 * trainIdx + 1]
        huriko = decryptFile.trainInfoList[3 * trainIdx + 2]
    else:
        speed = decryptFile.trainInfoList[2 * trainIdx]
        perf = decryptFile.trainInfoList[2 * trainIdx + 1]
        huriko = ""

    notchPerfFrame = ttk.Frame(tab_one_frame)
    notchPerfFrame.pack(anchor=tkinter.NW, padx=10, pady=5, expand=True, fill=tkinter.BOTH)

    speedLf = ttk.LabelFrame(notchPerfFrame, text="速度")
    speedLf.place(relx=0, rely=0, relwidth=0.4, relheight=0.98)
    speedScrollFrame = ScrollbarFrame(speedLf)

    notchCnt = len(speed) // decryptFile.notchContentCnt
    for i in range(notchCnt):
        NotchWidget(tabFrame, trainIdx, i, notchCnt, speedScrollFrame.frame, speed, decryptFile, decryptFile.notchContentCnt, varList, btnList, defaultData)

    perfLf = ttk.LabelFrame(notchPerfFrame, text="性能")
    perfLf.place(relx=0.43, rely=0, relwidth=0.56, relheight=0.98)
    perfScrollFrame = ScrollbarFrame(perfLf)

    perfCnt = len(perf)
    for i in range(perfCnt):
        PerfWidget(tabFrame, trainIdx, i, perfScrollFrame.frame, perf, decryptFile, varList, btnList, defaultData)

    if huriko != "":
        for i in range(len(huriko)):
            HurikoWidget(tabFrame, trainIdx, i, perfCnt, perfScrollFrame.frame, huriko, decryptFile, varList, btnList, defaultData)


def tab2AllWidget(tabFrame, decryptFile, trainIdx, game, widgetList, reloadFunc):
    tab_two_frame = ttk.Frame(tabFrame)
    tab_two_frame.pack(anchor=tkinter.NW, fill=tkinter.X)

    countModelLf = ttk.LabelFrame(tab_two_frame, text="車両", height=250)
    countModelLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.X)
    countModelLf.propagate(False)

    countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, reloadFunc)

    v_edit = widgetList[0]
    v_edit.set("この編成を修正する")
    edit_hensei_button = ttk.Button(countWidget.countFrame, textvariable=v_edit)
    edit_hensei_button.grid(columnspan=3, row=3, column=0, sticky=tkinter.W + tkinter.E, pady=15)

    edit_model_button = ttk.Button(countWidget.countFrame, text="モデル情報を修正")
    edit_model_button.grid(columnspan=3, row=4, column=0, sticky=tkinter.W + tkinter.E, pady=5)

    countModelScrollFrame = ScrollbarFrame(countModelLf, True, False)

    innerButtonList = [
        countWidget.notchBtn,
        countWidget.henseiBtn,
        countWidget.colorBtn,
        edit_hensei_button,
        edit_model_button,
    ]

    TrainModelWidget(tabFrame, trainIdx, game, countModelScrollFrame.frame, widgetList, innerButtonList, decryptFile, reloadFunc)

    elseFrame = ttk.Frame(tabFrame)
    elseFrame.pack(anchor=tkinter.NW, fill=tkinter.X)

    elseModel = decryptFile.trainModelList[trainIdx]["elseModel"]
    else2Model = decryptFile.trainModelList[trainIdx]["else2Model"]

    if len(elseModel) > 0:
        FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else1", elseModel, 1, reloadFunc)
    FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else2", else2Model, 2, reloadFunc)

    elseFrame2 = ttk.Frame(tabFrame)
    elseFrame2.pack(anchor=tkinter.NW, fill=tkinter.X)

    elseList2 = decryptFile.trainModelList[trainIdx]["elseList2"]
    FixedList2Widget(elseFrame2, trainIdx, decryptFile, "else3", elseList2, reloadFunc)


def tab3AllWidget(tabFrame, decryptFile, trainIdx, game, widgetList, reloadFunc):
    tab3frame = ttk.Frame(tabFrame)
    tab3frame.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

    lensList = decryptFile.trainModelList[trainIdx]["lensList"]
    LensListWidget(tab3frame, decryptFile, trainIdx, lensList, reloadFunc)

    tailList = decryptFile.trainModelList[trainIdx]["tailList"]
    TailListWidget(tab3frame, decryptFile, trainIdx, tailList, reloadFunc)
