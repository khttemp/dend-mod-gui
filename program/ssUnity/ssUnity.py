import os
import codecs
import tkinter
import json
import sys
import traceback
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import program.textSetting as textSetting

from program.ssUnity.importPy.tkinterScrollbarTreeviewSSUnity import ScrollbarTreeviewSSUnity
from program.ssUnity.importPy.excelWidget import ExcelWidget

unityFlag = True
try:
    from program.ssUnity.SSDecrypt.denDecrypt import DenDecrypt
    from program.ssUnity.SSDecrypt.resourcesDecrypt import ResourcesDecrypt
except ImportError:
    unityFlag = False

root = None
v_radio = None
v_fileName = None
v_select = None
v_search = None
searchEt = None
contentsLf = None
frame = None
monoCombo = None
extractBtn = None
loadAndSaveBtn = None
assetsSaveBtn = None
decryptFile = None
configPath = None
railModelInfo = None
ambModelInfo = None


def resource_path(relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(os.path.abspath(os.path.dirname(__file__)), "importPy"))
    return os.path.join(bundle_dir, relative_path)


def readModelInfo(jsonPath):
    global railModelInfo
    global ambModelInfo

    f = codecs.open(jsonPath, "r", "utf-8", "strict")
    modelDict = json.load(f)
    f.close()

    railModelInfo = {}
    for model in list(modelDict["railModelInfo"].keys()):
        railModelInfo[model.lower()] = modelDict["railModelInfo"][model]

    ambModelInfo = []
    for model in modelDict["ambModelInfo"]:
        ambModelInfo.append(model.lower())


def deleteAllWidget():
    global contentsLf
    global v_btnList

    for children in contentsLf.winfo_children():
        children.destroy()
    
    for btn in v_btnList:
        btn["state"] = "disabled"


def createWidget(reloadFlag = False):
    global v_radio
    global v_select
    global v_btnList
    global v_search
    global searchEt
    global contentsLf
    global decryptFile
    global frame
    global monoCombo

    if not reloadFlag:
        v_search.set("")
        searchEt["state"] = "normal"

    frame = ScrollbarTreeviewSSUnity(contentsLf, v_select, v_btnList)
    col_tuple = (
        "treeNum",
        "treePathId",
        "treeName",
        "treeName2",
        "treeKind",
        "treeSize"
    )
    frame.tree["columns"] = col_tuple
    frame.tree.column("#0", width=0, stretch=False)

    frame.tree.column("treeNum", anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column("treePathId", anchor=tkinter.CENTER)
    frame.tree.column("treeName", anchor=tkinter.CENTER)
    frame.tree.column("treeName2", anchor=tkinter.CENTER)
    frame.tree.column("treeKind", anchor=tkinter.CENTER)
    frame.tree.column("treeSize", anchor=tkinter.CENTER)
    frame.tree.heading("treeNum", text=textSetting.textList["ssUnity"]["headerNum"], anchor=tkinter.CENTER)
    frame.tree.heading("treePathId", text=textSetting.textList["ssUnity"]["headerPathId"], anchor=tkinter.CENTER)
    frame.tree.heading("treeName", text=textSetting.textList["ssUnity"]["headerName"], anchor=tkinter.CENTER)
    frame.tree.heading("treeName2", text=textSetting.textList["ssUnity"]["headerName"], anchor=tkinter.CENTER)
    frame.tree.heading("treeKind", text=textSetting.textList["ssUnity"]["headerKind"], anchor=tkinter.CENTER)
    frame.tree.heading("treeSize", text=textSetting.textList["ssUnity"]["headerSize"], anchor=tkinter.CENTER)

    if v_radio.get() == 0:
        for index, dataList in enumerate(decryptFile.allList):
            data = (index + 1, )
            data += ("", dataList[0], "", dataList[1], dataList[2])
            frame.tree.insert(parent="", index="end", iid=index, values=data)
        frame.tree["displaycolumns"] = (
            "treeNum",
            "treeName",
            "treeKind",
            "treeSize"
        )
    elif v_radio.get() == 1:
        if monoCombo["values"] == "":
            monoCombo["values"] = decryptFile.keyNameList
            monoCombo["state"] = "readonly"
            monoCombo.current(0)

        if monoCombo.current() == 0:
            for index, trainName in enumerate(decryptFile.trainNameList):
                data = (index + 1, )
                trainData = decryptFile.trainOrgInfoList[trainName]
                data += (trainData["num"], trainName, "", trainData["data"]["className"], trainData["data"]["size"])
                frame.tree.insert(parent="", index="end", iid=index, values=data)
            frame.tree["displaycolumns"] = (
                "treeNum",
                "treeName",
                "treeKind",
                "treeSize"
            )
        elif monoCombo.current() == 1:
            index = 0
            trainIdx = 0
            tagList = ["", "gray"]
            for trainModelName in decryptFile.trainModelNameList:
                changeMeshTexInfoList = decryptFile.changeMeshTexList[trainModelName]
                tags = tagList[trainIdx % 2]
                for changeMeshTexInfo in changeMeshTexInfoList:
                    data = (index + 1, )
                    meshTexInfo = changeMeshTexInfo["data"]["meshData"]
                    gameObjectName = changeMeshTexInfo["data"]["monoData"].m_GameObject.read().name
                    meshName = meshTexInfo[3]
                    data += (changeMeshTexInfo["num"], )
                    data += (trainModelName, "{0}({1})".format(gameObjectName, meshName), changeMeshTexInfo["data"]["className"], changeMeshTexInfo["data"]["size"])
                    frame.tree.insert(parent="", index="end", iid=index, values=data, tags=tags)
                    index += 1
                if len(changeMeshTexInfoList) > 0:
                    trainIdx += 1
            frame.tree.tag_configure("gray", background="#CCCCCC")
            frame.tree["displaycolumns"] = (
                "treeNum",
                "treePathId",
                "treeName",
                "treeName2",
                "treeKind",
                "treeSize"
            )


def selectGame():
    deleteAllWidget()
    changeButton()


def changeButton():
    global v_radio
    global v_fileName
    global v_select
    global v_search
    global searchEt
    global monoCombo
    global extractBtn
    global loadAndSaveBtn
    global assetsSaveBtn

    v_select.set("")
    v_fileName.set("")
    v_search.set("")
    searchEt["state"] = "readonly"
    if v_radio.get() == 0:
        extractBtn["text"] = textSetting.textList["ssUnity"]["extractFile"]
        extractBtn["command"] = extract
        extractBtn["state"] = "disabled"
        loadAndSaveBtn["text"] = textSetting.textList["ssUnity"]["saveFile"]
        loadAndSaveBtn["command"] = loadAndSave
        loadAndSaveBtn["state"] = "disabled"
        monoCombo.place_forget()
        assetsSaveBtn.place_forget()
    elif v_radio.get() == 1:
        monoCombo.set("")
        monoCombo["state"] = "disabled"
        monoCombo["values"] = ""
        monoCombo.place(relx=0.30, rely=0.03)
        extractBtn["text"] = textSetting.textList["ssUnity"]["extractCsv"]
        extractBtn["command"] = csvExtract
        extractBtn["state"] = "disabled"
        loadAndSaveBtn["text"] = textSetting.textList["ssUnity"]["saveCsv"]
        loadAndSaveBtn["command"] = csvLoadAndSave
        loadAndSaveBtn["state"] = "disabled"
        assetsSaveBtn.place(relx=0.78, rely=0.09)
        assetsSaveBtn["state"] = "disabled"


def changeResourceMonoEvent(event):
    changeResourceMono()


def changeResourceMono():
    global v_select
    global extractBtn
    global loadAndSaveBtn
    global assetsSaveBtn
    global frame

    v_select.set("")
    extractBtn["state"] = "disabled"
    loadAndSaveBtn["state"] = "disabled"
    assetsSaveBtn["state"] = "disabled"
    deleteAllWidget()
    createWidget()


def extract():
    global decryptFile
    global frame
    global configPath
    global railModelInfo
    global ambModelInfo

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1
    data = decryptFile.allList[num][-1]

    dataName = decryptFile.allList[num][0]
    excelFlag = False
    if dataName == "stagedata":
        excelFlag = True

    fileType = selectItem["treeKind"]
    if fileType == "TextAsset":
        ext = ".txt"
    elif fileType == "TextAsset(bytes)":
        ext = ".png"
    elif fileType == "AudioClip":
        ext = ".wav"
    filename = selectItem["treeName"]

    fileTypes = [(textSetting.textList["ssUnity"]["loadSaveFileLabel"], "*" + ext), ]
    defExt = ext
    if excelFlag:
        fileTypes.insert(0, (textSetting.textList["ssUnity"]["loadSaveFileExcelLabel"], "*.xlsx"))
        defExt = ".xlsx"

    file_path = fd.asksaveasfilename(initialfile=filename, filetypes=fileTypes, defaultextension=defExt)
    errorMsg = textSetting.textList["errorList"]["E89"]
    if file_path:
        try:
            if fileType == "AudioClip":
                for name, d in data.samples.items():
                    w = open(file_path, "wb")
                    w.write(d)
                    w.close()
            else:
                if excelFlag and os.path.splitext(file_path)[1].lower() == ".xlsx":
                    excelWidget = ExcelWidget(data.script.tobytes().decode(), file_path, configPath, railModelInfo, ambModelInfo)
                    excelWidget.extractExcel()
                else:
                    w = open(file_path, "wb")
                    w.write(data.script)
                    w.close()
                    mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I110"])
        except Exception:
            w = codecs.open("error.log", "w", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def loadAndSave():
    global decryptFile
    global frame
    global configPath
    global railModelInfo
    global ambModelInfo

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["treeNum"]) - 1
    data = decryptFile.allList[num][-1]

    dataName = decryptFile.allList[num][0]
    excelFlag = False
    if dataName == "stagedata":
        excelFlag = True

    fileType = selectItem["treeKind"]
    if fileType == "TextAsset":
        ext = ".txt"
    elif fileType == "TextAsset(bytes)":
        ext = ".png"
    elif fileType == "AudioClip":
        errorMsg = textSetting.textList["errorList"]["E90"]
        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        return

    fileTypes = [(textSetting.textList["ssUnity"]["loadSaveFileLabel"], "*" + ext), ]
    defExt = ext
    if excelFlag:
        fileTypes.insert(0, (textSetting.textList["ssUnity"]["loadSaveFileExcelLabel"], "*.xlsx"))
        defExt = ".xlsx"

    file_path = fd.askopenfilename(filetypes=fileTypes, defaultextension=defExt)
    if not file_path:
        return
    if not excelFlag or (excelFlag and os.path.splitext(file_path)[1].lower() != ".xlsx"):
        result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"], icon="warning")
        if result == "no":
            return

    try:
        if fileType != "AudioClip":
            if excelFlag and os.path.splitext(file_path)[1].lower() == ".xlsx":
                errMsgObj = {}
                newLinesObj = {}
                excelWidget = ExcelWidget(data.script.tobytes().decode(), file_path, configPath, railModelInfo, ambModelInfo)
                if not excelWidget.loadExcelAndMerge(newLinesObj, errMsgObj):
                    mb.showerror(title=textSetting.textList["error"], message=errMsgObj["message"])
                    return
                if "warning" in errMsgObj:
                    result = mb.askquestion(title=textSetting.textList["confirm"], message=errMsgObj["warning"], icon="warning")
                    if result == "no":
                        return
                result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"], icon="warning")
                if result == "no":
                    return
                data.script = bytearray("\n".join(newLinesObj["data"]).encode("utf-8"))
            else:
                with open(file_path, "rb") as f:
                    data.script = f.read()
            data.save()
        with open(decryptFile.filePath, "wb") as w:
            w.write(decryptFile.env.file.save())
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
        reloadFile()
    except Exception:
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(traceback.format_exc())
        w.close()
        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])


def csvExtract():
    global monoCombo
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    if monoCombo.current() == 0:
        trainName = selectItem["treeName"]
        data = decryptFile.trainOrgInfoList[trainName]["data"]["monoData"]
        filename = selectItem["treeName"] + ".csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("trainOrgInfo", "*.csv")])
        errorMsg = textSetting.textList["errorList"]["E7"]
        if file_path:
            try:
                w = codecs.open(file_path, "w", "utf-8-sig", "strict")
                trainOrgInfo = decryptFile.getTrainOrgInfo(data.raw_data)
                if trainOrgInfo is None:
                    decryptFile.printError()
                    errorMsg = textSetting.textList["errorList"]["E14"]
                    mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                    return
                w.write("{0},{1}\n".format(textSetting.textList["ssUnity"]["csvNotchNum"], trainOrgInfo[1]))
                w.write("{0},{1}\n".format(textSetting.textList["ssUnity"]["csvOrgNum"], trainOrgInfo[5]))
                w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyClass"]))
                w.write(",".join(trainOrgInfo[6]))
                w.write("\n")
                w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyModel"]))
                w.write(",".join(trainOrgInfo[7]))
                w.write("\n")
                w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvPantaModel"]))
                w.write(",".join(trainOrgInfo[8]))
                w.write("\n")
                w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyClassIndexList"]))
                w.write(",".join([str(x) for x in trainOrgInfo[9]]))
                w.write("\n")
                w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvBodyModelIndexList"]))
                w.write(",".join([str(x) for x in trainOrgInfo[10]]))
                w.write("\n")
                w.write("{0}\n".format(textSetting.textList["ssUnity"]["csvPantaModelIndexList"]))
                w.write(",".join([str(x) for x in trainOrgInfo[11]]))
                w.close()
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
            except Exception:
                w = codecs.open("error.log", "a", "utf-8", "strict")
                w.write(traceback.format_exc())
                w.close()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
    elif monoCombo.current() == 1:
        pathId = int(selectItem["treePathId"])
        trainModelName = selectItem["treeName"]
        meshTexTitleList = [
            "デフォルト",
            "回送",
            "試運転",
            "梅田",
            # 未使用
            "未詳1",
            "京橋",
            "名張",
            "難波",
            "三宮",
            "三田",
            "未詳2",
            "梅田",
            "品川",
            "大阪難波",
            "豊橋",
            "岐阜",
            "浅草",
            "日光",
            "池袋",
            # 未使用
            "渋谷(東急東横線)",
            "元町・中華街",
            "渋谷(東急田園都市線)",
            "中央林間",
        ]
        filename = selectItem["treeName"] + "_" + selectItem["treePathId"] + ".csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("changeMeshTex", "*.csv")])
        errorMsg = textSetting.textList["errorList"]["E7"]
        if file_path:
            try:
                w = codecs.open(file_path, "w", "utf-8-sig", "strict")
                meshTexInfoList = decryptFile.changeMeshTexList[trainModelName]
                meshTexInfo = [item for item in meshTexInfoList if item["num"] == pathId][0]
                for index, meshTexTitle in enumerate(meshTexTitleList):
                    w.write("{0},{1}\n".format(meshTexTitle, meshTexInfo["data"]["meshData"][-1][index]))
                w.close()
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
            except Exception:
                w = codecs.open("error.log", "a", "utf-8", "strict")
                w.write(traceback.format_exc())
                w.close()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def csvLoadAndSave():
    global monoCombo
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    if monoCombo.current() == 0:
        trainName = selectItem["treeName"]
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("trainOrgInfo", "*.csv")])
        if not file_path:
            return
        csvLines = None
        try:
            try:
                f = codecs.open(file_path, "r", "utf-8-sig", "strict")
                csvLines = f.readlines()
                f.close()
            except UnicodeDecodeError:
                f = codecs.open(file_path, "r", "shift-jis", "strict")
                csvLines = f.readlines()
                f.close()
            if not decryptFile.checkCsv(csvLines):
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=decryptFile.error)
            if not decryptFile.saveCsv(trainName):
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I111"])
            frame.tree.set(selectId, column="treeSize", value=str(decryptFile.trainOrgInfoList[trainName]["data"]["size"]))
        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
    elif monoCombo.current() == 1:
        trainModelName = selectItem["treeName"]
        pathId = int(selectItem["treePathId"])
        file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("changeMeshTex", "*.csv")])
        if not file_path:
            return
        try:
            try:
                f = codecs.open(file_path, "r", "utf-8-sig", "strict")
                csvLines = f.readlines()
                f.close()
            except UnicodeDecodeError:
                f = codecs.open(file_path, "r", "shift-jis", "strict")
                csvLines = f.readlines()
                f.close()
            if not decryptFile.saveChangeMeshTex(csvLines, trainModelName, pathId):
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I111"])
            changeMeshTexFilterInfo = [item for item in decryptFile.changeMeshTexList[trainModelName] if item["num"] == pathId][0]
            frame.tree.set(selectId, column="treeSize", value=str(changeMeshTexFilterInfo["data"]["size"]))
        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])


def assetsSave():
    global decryptFile
    global assetsSaveBtn

    assetsSaveBtn["state"] = "disabled"
    assetsSaveBtn.update()
    try:
        if not decryptFile.saveAssets():
            decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I112"])
        reloadFile()
    except Exception:
        w = codecs.open("error.log", "a", "utf-8", "strict")
        w.write(traceback.format_exc())
        w.close()
        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
    assetsSaveBtn["state"] = "normal"


def reloadFile():
    global v_radio
    global v_select
    global v_search
    global decryptFile
    global frame

    errorMsg = textSetting.textList["errorList"]["E14"]
    if decryptFile.filePath:
        try:
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            selectId = None
            if v_select.get() != "":
                selectId = int(v_select.get())

            deleteAllWidget()
            createWidget(True)

            if v_search.get() != "":
                filterData()

            if selectId is not None:
                findFlag = False
                for idx, itemId in enumerate(frame.tree.get_children()):
                    item = frame.tree.item(itemId)
                    num = item["values"][0]
                    if selectId == num:
                        frame.tree.selection_set(itemId)
                        findFlag = True
                        break

                if findFlag:
                    if idx - 3 < 0:
                        frame.tree.see(0)
                    else:
                        frame.tree.see(idx - 3)

        except Exception:
            w = codecs.open("error.log", "a", "utf-8", "strict")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def openFile():
    global unityFlag
    global v_radio
    global v_fileName
    global decryptFile

    if not unityFlag:
        msg = textSetting.textList["errorList"]["E91"]
        mb.showerror(title=textSetting.textList["error"], message=msg)
        return

    errorMsg = textSetting.textList["errorList"]["E14"]
    if v_radio.get() == 0:
        file_path = fd.askopenfilename(filetypes=[("DEND_SS", "*.den")])
        if file_path:
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            del decryptFile
            decryptFile = DenDecrypt(file_path)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            deleteAllWidget()
            createWidget()
    elif v_radio.get() == 1:
        file_path = fd.askopenfilename(filetypes=[("resources.assets", "resources.assets")])
        if file_path:
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            del decryptFile
            decryptFile = ResourcesDecrypt(file_path)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            deleteAllWidget()
            createWidget()


def filterList(event):
    global v_select
    global frame

    v_select.set("")
    if len(frame.tree.selection()) > 0:
        frame.tree.selection_remove(frame.tree.selection())
    filterData()


def filterData():
    global v_radio
    global v_search
    global decryptFile
    global frame
    global monoCombo

    if v_radio.get() == 0:
        for i in range(len(decryptFile.allList)):
            frame.tree.reattach(i, "", tkinter.END)
    elif v_radio.get() == 1:
        if monoCombo.current() == 0:
            for i in range(len(decryptFile.trainNameList)):
                frame.tree.reattach(i, "", tkinter.END)
        elif monoCombo.current() == 1:
            index = 0
            for trainModelName in decryptFile.trainModelNameList:
                changeMeshTexInfoList = decryptFile.changeMeshTexList[trainModelName]
                for changeMeshTexInfo in changeMeshTexInfoList:
                    index += 1
            for i in range(index):
                frame.tree.reattach(i, "", tkinter.END)

    search = v_search.get()
    for i in frame.tree.get_children():
        item = frame.tree.item(i)
        name = item["values"][2]
        if search.upper() not in name.upper():
            if v_radio.get() == 1 and monoCombo.current() == 1:
                name2 = item["values"][3]
                if search.upper() in name2.upper():
                    continue
            frame.tree.detach(i)


def call_ssUnity(rootTk, programFrame, config_ini_path):
    global unityFlag
    global root
    global v_radio
    global v_fileName
    global v_select
    global v_btnList
    global v_search
    global monoCombo
    global extractBtn
    global loadAndSaveBtn
    global assetsSaveBtn
    global searchEt
    global contentsLf
    global configPath

    configPath = config_ini_path

    path = resource_path("model.json")
    readModelInfo(path)

    if not unityFlag:
        msg = textSetting.textList["errorList"]["E91"]
        mb.showerror(title=textSetting.textList["error"], message=msg)
        return

    root = rootTk
    v_radio = tkinter.IntVar()
    v_radio.set(0)

    v_fileName = tkinter.StringVar()
    fileNameEt = ttk.Entry(programFrame, textvariable=v_fileName, font=textSetting.textList["font2"], width=23, state="readonly", justify="center")
    fileNameEt.place(relx=0.053, rely=0.03)

    selectLb = ttk.Label(programFrame, text=textSetting.textList["ssUnity"]["selectNum"], font=textSetting.textList["font2"])
    selectLb.place(relx=0.05, rely=0.09)

    v_select = tkinter.StringVar()
    selectEt = ttk.Entry(programFrame, textvariable=v_select, font=textSetting.textList["font2"], width=6, state="readonly", justify="center")
    selectEt.place(relx=0.22, rely=0.09)

    monoCombo = ttk.Combobox(programFrame, font=textSetting.textList["font2"], state="disabled")
    monoCombo.place(relx=0.30, rely=0.03)
    monoCombo.bind("<<ComboboxSelected>>", changeResourceMonoEvent)
    monoCombo.place_forget()

    denRb = tkinter.Radiobutton(programFrame, text=textSetting.textList["ssUnity"]["editDenFile"], command=selectGame, variable=v_radio, value=0)
    denRb.place(relx=0.60, rely=0.03)
    resourcesRb = tkinter.Radiobutton(programFrame, text=textSetting.textList["ssUnity"]["editResourcesAssets"], command=selectGame, variable=v_radio, value=1)
    resourcesRb.place(relx=0.78, rely=0.03)

    extractBtn = ttk.Button(programFrame, text=textSetting.textList["ssUnity"]["extractFileLabel"], width=25, state="disabled", command=extract)
    extractBtn.place(relx=0.42, rely=0.09)
    loadAndSaveBtn = ttk.Button(programFrame, text=textSetting.textList["ssUnity"]["saveFileLabel"], width=25, state="disabled", command=loadAndSave)
    loadAndSaveBtn.place(relx=0.60, rely=0.09)

    assetsSaveBtn = ttk.Button(programFrame, text=textSetting.textList["ssUnity"]["saveResourcesAssets"], width=25, state="disabled", command=assetsSave)
    assetsSaveBtn.place(relx=0.78, rely=0.09)
    assetsSaveBtn.place_forget()

    v_btnList = [
        extractBtn,
        loadAndSaveBtn,
        assetsSaveBtn
    ]

    searchLb = ttk.Label(programFrame, text=textSetting.textList["ssUnity"]["searchText"], font=textSetting.textList["font2"])
    searchLb.place(relx=0.05, rely=0.15)

    v_search = tkinter.StringVar()
    searchEt = ttk.Entry(programFrame, textvariable=v_search, font=textSetting.textList["font7"], width=23, state="readonly", justify="center")
    searchEt.place(relx=0.10, rely=0.15)
    searchEt.bind("<KeyRelease>", filterList)

    contentsLf = ttk.LabelFrame(programFrame, text=textSetting.textList["ssUnity"]["scriptLabel"])
    contentsLf.place(relx=0.03, rely=0.20, relwidth=0.95, relheight=0.77)
