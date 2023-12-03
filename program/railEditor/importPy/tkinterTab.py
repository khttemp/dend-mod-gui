import tkinter
from tkinter import ttk
import program.textSetting as textSetting

from program.tkinterScrollbarFrameClass import ScrollbarFrame

from program.railEditor.importPy.tab1.musicWidget import MusicWidget
from program.railEditor.importPy.tab1.trainCountWidget import TrainCountWidget
from program.railEditor.importPy.tab1.railPosWidget import RailPosWidget
from program.railEditor.importPy.tab1.stationNoWidget import StationNoWidget

from program.railEditor.importPy.tab2.else1ListWidget import Else1ListWidget
from program.railEditor.importPy.tab2.simpleListWidget import SimpleListWidget
from program.railEditor.importPy.tab2.stationWidget import StationWidget
from program.railEditor.importPy.tab2.binAnimeListWidget import BinAnimeListWidget

from program.railEditor.importPy.tab3.smfListWidget import SmfListWidget

from program.railEditor.importPy.tab4.stationNameWidget import StationNameWidget

from program.railEditor.importPy.tab5.else2ListWidget import Else2ListWidget

from program.railEditor.importPy.tab6.cpuWidget import CpuWidget

from program.railEditor.importPy.tab7.comicScriptWidget import ComicScriptWidget
from program.railEditor.importPy.tab7.dosansenListWidget import DosansenListWidget

from program.railEditor.importPy.tab8.railListWidget import RailListWidget

from program.railEditor.importPy.tab9.else3ListWidget import Else3ListWidget

from program.railEditor.importPy.tab10.else4ListWidget import Else4ListWidget

from program.railEditor.importPy.tab11.ambListWidget import AmbListWidget


def tab1AllWidget(tabFrame, decryptFile, reloadFunc):
    tab_one_frame = ttk.Frame(tabFrame)
    tab_one_frame.pack(expand=True, fill=tkinter.BOTH)
    frame = ScrollbarFrame(tab_one_frame)

    musicExcelFrame = ttk.Frame(frame.frame)
    musicExcelFrame.pack(anchor=tkinter.NW)

    musicFrame = ttk.Frame(musicExcelFrame)
    musicFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)
    MusicWidget(musicFrame, decryptFile, reloadFunc)

    TrainCountWidget(frame.frame, decryptFile, reloadFunc)

    railPosFrame = ttk.Frame(frame.frame)
    railPosFrame.pack(anchor=tkinter.NW, padx=10, pady=5)

    railPos1Frame = ttk.Frame(railPosFrame)
    railPos1Frame.grid(sticky=tkinter.NW, row=0, column=0, pady=3)

    RailPosWidget(railPos1Frame, textSetting.textList["railEditor"]["initPos"], 0, decryptFile, decryptFile.trainList, reloadFunc)

    if decryptFile.game in ["BS", "CS", "RS"]:
        railPos2Frame = ttk.Frame(railPosFrame)
        railPos2Frame.grid(sticky=tkinter.NW, row=1, column=0, pady=3)
        RailPosWidget(railPos2Frame, textSetting.textList["railEditor"]["dummyPos"], 1, decryptFile, decryptFile.trainList2, reloadFunc)

        railPos3Frame = ttk.Frame(railPosFrame)
        railPos3Frame.grid(sticky=tkinter.NW, row=2, column=0, pady=3)
        RailPosWidget(railPos3Frame, textSetting.textList["railEditor"]["pracOrVsPos"], 2, decryptFile, decryptFile.trainList3, reloadFunc)

        stationNoFrame = ttk.Frame(railPosFrame)
        stationNoFrame.grid(sticky=tkinter.NW, row=3, column=0, pady=3)
        StationNoWidget(stationNoFrame, decryptFile, decryptFile.stationNo, 0, reloadFunc)

        if decryptFile.game == "BS":
            separator = ttk.Separator(frame.frame, orient="horizontal")
            separator.pack(fill=tkinter.X)

            railPosDummyFrame = ttk.Frame(frame.frame)
            railPosDummyFrame.pack(anchor=tkinter.NW, padx=10, pady=5)

            railPos4Frame = ttk.Frame(railPosDummyFrame)
            railPos4Frame.grid(sticky=tkinter.NW, row=0, column=0, pady=3)
            RailPosWidget(railPos4Frame, textSetting.textList["railEditor"]["dummyPos"], 3, decryptFile, decryptFile.trainList4, reloadFunc)

            stationNo2Frame = ttk.Frame(railPosDummyFrame)
            stationNo2Frame.grid(sticky=tkinter.NW, row=1, column=0, pady=3)
            StationNoWidget(stationNo2Frame, decryptFile, decryptFile.stationNo2, 1, reloadFunc)


def tab2AllWidget(tabFrame, decryptFile, reloadFunc):
    tab_two_frame = ttk.Frame(tabFrame)
    tab_two_frame.pack(expand=True, fill=tkinter.BOTH)
    frame = ScrollbarFrame(tab_two_frame)

    Else1ListWidget(frame.frame, decryptFile, decryptFile.else1List, reloadFunc)

    if decryptFile.game in ["BS", "CS", "RS"]:
        simpleListFrame = ttk.Frame(frame.frame)
        simpleListFrame.pack(anchor=tkinter.NW)
        SimpleListWidget(simpleListFrame, textSetting.textList["railEditor"]["lightInfo"], decryptFile, decryptFile.lightList, decryptFile.lightIdx, 1, reloadFunc)
        if decryptFile.game in ["CS", "RS"]:
            SimpleListWidget(simpleListFrame, textSetting.textList["railEditor"]["stationInfo"], decryptFile, decryptFile.pngList, decryptFile.pngIdx, 2, reloadFunc)
            StationWidget(frame.frame, decryptFile, decryptFile.stationList, reloadFunc)

    simpleListFrame2 = ttk.Frame(frame.frame)
    simpleListFrame2.pack(anchor=tkinter.NW)

    if decryptFile.game in ["BS", "CS", "RS"]:
        SimpleListWidget(simpleListFrame2, textSetting.textList["railEditor"]["baseBinInfo"], decryptFile, decryptFile.baseBinList, decryptFile.binIdx, 1, reloadFunc)
    BinAnimeListWidget(simpleListFrame2, decryptFile, decryptFile.binAnimeList, reloadFunc)


def tab3AllWidget(tabFrame, decryptFile, reloadFunc, selectId):
    SmfListWidget(tabFrame, decryptFile, decryptFile.smfList, reloadFunc, selectId)


def tab4AllWidget(tabFrame, decryptFile, reloadFunc, selectId):
    StationNameWidget(tabFrame, decryptFile, decryptFile.stationNameList, reloadFunc, selectId)


def tab5AllWidget(tabFrame, decryptFile, reloadFunc):
    Else2ListWidget(tabFrame, decryptFile, decryptFile.else2List, reloadFunc)


def tab6AllWidget(tabFrame, decryptFile, reloadFunc, selectId):
    CpuWidget(tabFrame, decryptFile, decryptFile.cpuList, reloadFunc, selectId)


def tab7AllWidget(tabFrame, decryptFile, reloadFunc):
    ComicScriptWidget(tabFrame, decryptFile, decryptFile.comicScriptList, reloadFunc)
    if decryptFile.game in ["CS", "RS"]:
        DosansenListWidget(tabFrame, decryptFile, decryptFile.dosansenList, reloadFunc)


def tab8AllWidget(tabFrame, decryptFile, reloadFunc):
    frame = ScrollbarFrame(tabFrame, True, True)
    RailListWidget(frame.frame, decryptFile, decryptFile.railList, reloadFunc)


def tab9AllWidget(tabFrame, decryptFile, reloadFunc, selectId):
    Else3ListWidget(tabFrame, decryptFile, decryptFile.else3List, reloadFunc, selectId)


def tab10AllWidget(tabFrame, decryptFile, reloadFunc):
    Else4ListWidget(tabFrame, decryptFile, decryptFile.else4List, reloadFunc)


def tab11AllWidget(tabFrame, decryptFile, reloadFunc):
    frame = ScrollbarFrame(tabFrame)
    AmbListWidget(frame.frame, decryptFile, decryptFile.ambList, reloadFunc)
