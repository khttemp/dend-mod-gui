import tkinter
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget

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


def tab1AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)

    MusicWidget(root, frame.interior, decryptFile, rootFrameAppearance, reloadFunc)
    TrainCountWidget(root, frame.interior, decryptFile, rootFrameAppearance, reloadFunc)
    RailPosWidget(root, frame.interior, textSetting.textList["railEditor"]["initPos"], 0, decryptFile, decryptFile.trainList, rootFrameAppearance, reloadFunc)

    if decryptFile.game in ["BS", "CS", "RS"]:
        RailPosWidget(root, frame.interior, textSetting.textList["railEditor"]["dummyPos"], 1, decryptFile, decryptFile.trainList2, rootFrameAppearance, reloadFunc)
        RailPosWidget(root, frame.interior, textSetting.textList["railEditor"]["pracOrVsPos"], 2, decryptFile, decryptFile.trainList3, rootFrameAppearance, reloadFunc)
        StationNoWidget(root, frame.interior, decryptFile, decryptFile.stationNo, 0, rootFrameAppearance, reloadFunc)

        if decryptFile.game == "BS":
            separator = ttkCustomWidget.CustomTtkSeparator(frame.interior, orient="horizontal")
            separator.pack(fill=tkinter.X)
            RailPosWidget(root, frame.interior, textSetting.textList["railEditor"]["dummyPos"], 3, decryptFile, decryptFile.trainList4, rootFrameAppearance, reloadFunc)
            StationNoWidget(root, frame.interior, decryptFile, decryptFile.stationNo2, 1, rootFrameAppearance, reloadFunc)


def tab2AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    Else1ListWidget(root, frame.interior, decryptFile, decryptFile.else1List, rootFrameAppearance, reloadFunc)

    if decryptFile.game in ["BS", "CS", "RS"]:
        simpleListFrame = ttkCustomWidget.CustomTtkFrame(frame.interior)
        simpleListFrame.pack(anchor=tkinter.NW)
        SimpleListWidget(root, simpleListFrame, textSetting.textList["railEditor"]["lightInfo"], decryptFile, decryptFile.lightList, decryptFile.lightIdx, 1, rootFrameAppearance, reloadFunc)
        if decryptFile.game in ["CS", "RS"]:
            SimpleListWidget(root, simpleListFrame, textSetting.textList["railEditor"]["stationInfo"], decryptFile, decryptFile.pngList, decryptFile.pngIdx, 2, rootFrameAppearance, reloadFunc)
            StationWidget(root, frame.interior, decryptFile, decryptFile.stationList, rootFrameAppearance, reloadFunc)

    simpleListFrame2 = ttkCustomWidget.CustomTtkFrame(frame.interior)
    simpleListFrame2.pack(anchor=tkinter.NW)
    if decryptFile.game in ["BS", "CS", "RS"]:
        SimpleListWidget(root, simpleListFrame2, textSetting.textList["railEditor"]["baseBinInfo"], decryptFile, decryptFile.baseBinList, decryptFile.binIdx, 1, rootFrameAppearance, reloadFunc)
    BinAnimeListWidget(root, simpleListFrame2, decryptFile, decryptFile.binAnimeList, rootFrameAppearance, reloadFunc)


def tab3AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    SmfListWidget(root, tabFrame, decryptFile, decryptFile.smfList, rootFrameAppearance, reloadFunc, selectId)


def tab4AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    StationNameWidget(root, tabFrame, decryptFile, decryptFile.stationNameList, rootFrameAppearance, reloadFunc, selectId)


def tab5AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    Else2ListWidget(root, tabFrame, decryptFile, decryptFile.else2List, rootFrameAppearance, reloadFunc)


def tab6AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    CpuWidget(root, tabFrame, decryptFile, decryptFile.cpuList, rootFrameAppearance, reloadFunc, selectId)


def tab7AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    ComicScriptWidget(root, tabFrame, decryptFile, decryptFile.comicScriptList, rootFrameAppearance, reloadFunc)
    if decryptFile.game in ["CS", "RS"]:
        DosansenListWidget(root, tabFrame, decryptFile, decryptFile.dosansenList, rootFrameAppearance, reloadFunc)


def tab8AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, True, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    RailListWidget(frame.interior, decryptFile, decryptFile.railList, rootFrameAppearance, reloadFunc)


def tab9AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    Else3ListWidget(root, tabFrame, decryptFile, decryptFile.else3List, rootFrameAppearance, reloadFunc, selectId)


def tab10AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    Else4ListWidget(root, tabFrame, decryptFile, decryptFile.else4List, rootFrameAppearance, reloadFunc)


def tab11AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    AmbListWidget(frame.interior, decryptFile, decryptFile.ambList, rootFrameAppearance, reloadFunc)
