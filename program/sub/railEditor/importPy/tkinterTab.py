import tkinter
import program.sub.textSetting as textSetting
import program.sub.appearance.ttkCustomWidget as ttkCustomWidget

from program.sub.tkinterScrollbarFrameClass import ScrollbarFrame

from program.sub.railEditor.importPy.tab1.musicWidget import MusicWidget
from program.sub.railEditor.importPy.tab1.trainCountWidget import TrainCountWidget
from program.sub.railEditor.importPy.tab1.railPosWidget import RailPosWidget
from program.sub.railEditor.importPy.tab1.stationNoWidget import StationNoWidget

from program.sub.railEditor.importPy.tab2.else1ListWidget import Else1ListWidget
from program.sub.railEditor.importPy.tab2.simpleListWidget import SimpleListWidget
from program.sub.railEditor.importPy.tab2.stationAmbWidget import StationAmbWidget
from program.sub.railEditor.importPy.tab2.binAnimeListWidget import BinAnimeListWidget

from program.sub.railEditor.importPy.tab3.smfListWidget import SmfListWidget

from program.sub.railEditor.importPy.tab4.stationNameWidget import StationNameWidget

from program.sub.railEditor.importPy.tab5.else2ListWidget import Else2ListWidget

from program.sub.railEditor.importPy.tab6.cpuWidget import CpuWidget

from program.sub.railEditor.importPy.tab7.comicScriptWidget import ComicScriptWidget
from program.sub.railEditor.importPy.tab7.dosansenListWidget import DosansenListWidget

from program.sub.railEditor.importPy.tab8.railListWidget import RailListWidget

from program.sub.railEditor.importPy.tab9.else3ListWidget import Else3ListWidget

from program.sub.railEditor.importPy.tab10.else4ListWidget import Else4ListWidget

from program.sub.railEditor.importPy.tab11.ambListWidget import AmbListWidget


def tab1AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)

    MusicWidget(frame.interior, decryptFile, rootFrameAppearance, reloadFunc)
    TrainCountWidget(frame.interior, decryptFile, rootFrameAppearance, reloadFunc)
    RailPosWidget(frame.interior, textSetting.textList["railEditor"]["initPos"], 0, decryptFile, decryptFile.trainList, rootFrameAppearance, reloadFunc)

    if decryptFile.game in ["BS", "CS", "RS"]:
        RailPosWidget(frame.interior, textSetting.textList["railEditor"]["dummyPos"], 1, decryptFile, decryptFile.trainList2, rootFrameAppearance, reloadFunc)
        RailPosWidget(frame.interior, textSetting.textList["railEditor"]["pracOrVsPos"], 2, decryptFile, decryptFile.trainList3, rootFrameAppearance, reloadFunc)
        StationNoWidget(frame.interior, 0, decryptFile, decryptFile.stationNo, rootFrameAppearance, reloadFunc)

        if decryptFile.game == "BS":
            separator = ttkCustomWidget.CustomTtkSeparator(frame.interior, orient="horizontal")
            separator.pack(fill=tkinter.X)
            RailPosWidget(frame.interior, textSetting.textList["railEditor"]["dummyPos"], 3, decryptFile, decryptFile.trainList4, rootFrameAppearance, reloadFunc)
            StationNoWidget(frame.interior, 1, decryptFile, decryptFile.stationNo2, rootFrameAppearance, reloadFunc)


def tab2AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    Else1ListWidget(frame.interior, decryptFile, rootFrameAppearance, reloadFunc)

    if decryptFile.game in ["BS", "CS", "RS"]:
        simpleListFrame = ttkCustomWidget.CustomTtkFrame(frame.interior)
        simpleListFrame.pack(anchor=tkinter.NW)
        SimpleListWidget(simpleListFrame, textSetting.textList["railEditor"]["lightInfo"], decryptFile, decryptFile.lightList, decryptFile.lightIdx, 1, rootFrameAppearance, reloadFunc)
        if decryptFile.game in ["CS", "RS"]:
            SimpleListWidget(simpleListFrame, textSetting.textList["railEditor"]["stationInfo"], decryptFile, decryptFile.pngList, decryptFile.pngIdx, 2, rootFrameAppearance, reloadFunc)
            StationAmbWidget(frame.interior, decryptFile, rootFrameAppearance, reloadFunc)

    simpleListFrame2 = ttkCustomWidget.CustomTtkFrame(frame.interior)
    simpleListFrame2.pack(anchor=tkinter.NW)
    if decryptFile.game in ["BS", "CS", "RS"]:
        SimpleListWidget(simpleListFrame2, textSetting.textList["railEditor"]["baseBinInfo"], decryptFile, decryptFile.baseBinList, decryptFile.binIdx, 1, rootFrameAppearance, reloadFunc)
    BinAnimeListWidget(simpleListFrame2, decryptFile, rootFrameAppearance, reloadFunc)


def tab3AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    SmfListWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId)


def tab4AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    StationNameWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId)


def tab5AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    Else2ListWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc)


def tab6AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    CpuWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId)


def tab7AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    ComicScriptWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc)
    if decryptFile.game in ["CS", "RS"]:
        DosansenListWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc)


def tab8AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, True, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    RailListWidget(frame.interior, decryptFile, rootFrameAppearance, reloadFunc)


def tab9AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    Else3ListWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId)


def tab10AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    Else4ListWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc)


def tab11AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    AmbListWidget(frame.interior, decryptFile, rootFrameAppearance, reloadFunc)
