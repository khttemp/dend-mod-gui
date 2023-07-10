import os
import codecs
import tkinter
import traceback
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from program.ssUnity.importPy.tkinterScrollbarTreeviewSSUnity import ScrollbarTreeviewSSUnity

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
contentsLf = None
frame = None
extractBtn = None
loadAndSaveBtn = None
assetsSaveBtn = None
decryptFile = None


def deleteAllWidget():
    global contentsLf

    for children in contentsLf.winfo_children():
        children.destroy()


def createWidget():
    global v_radio
    global v_select
    global v_btnList
    global contentsLf
    global decryptFile
    global frame

    frame = ScrollbarTreeviewSSUnity(contentsLf, v_select, v_btnList)
    col_tuple = ("番号", "名前", "種類", "サイズ")
    frame.tree['columns'] = col_tuple
    frame.tree.column('#0', width=0, stretch=False)

    frame.tree.column('番号', anchor=tkinter.CENTER, width=50, minwidth=50)
    frame.tree.column('名前', anchor=tkinter.CENTER)
    frame.tree.column('種類', anchor=tkinter.CENTER)
    frame.tree.column('サイズ', anchor=tkinter.CENTER)
    frame.tree.heading('番号', text='番号', anchor=tkinter.CENTER)
    frame.tree.heading('名前', text='名前', anchor=tkinter.CENTER)
    frame.tree.heading('種類', text='種類', anchor=tkinter.CENTER)
    frame.tree.heading('サイズ', text='サイズ', anchor=tkinter.CENTER)

    if v_radio.get() == 0:
        for index, dataList in enumerate(decryptFile.allList):
            data = (index, )
            data += (dataList[0], dataList[1], dataList[2])
            frame.tree.insert(parent='', index='end', iid=index, values=data)
    elif v_radio.get() == 1:
        for index, dataList in enumerate(decryptFile.trainOrgInfoList):
            data = (index, )
            data += (dataList[0], dataList[1], dataList[2])
            frame.tree.insert(parent='', index='end', iid=index, values=data)


def selectGame():
    deleteAllWidget()
    changeButton()


def changeButton():
    global v_radio
    global v_fileName
    global v_select
    global extractBtn
    global loadAndSaveBtn
    global assetsSaveBtn

    v_select.set("")
    v_fileName.set("")
    if v_radio.get() == 0:
        extractBtn["text"] = "ファイルを取り出す"
        extractBtn["command"] = extract
        extractBtn["state"] = "disabled"
        loadAndSaveBtn["text"] = "ファイルを上書きする"
        loadAndSaveBtn["command"] = loadAndSave
        loadAndSaveBtn["state"] = "disabled"
        assetsSaveBtn.place_forget()
    elif v_radio.get() == 1:
        extractBtn["text"] = "CSVとして取り出す"
        extractBtn["command"] = csvExtract
        extractBtn["state"] = "disabled"
        loadAndSaveBtn["text"] = "CSV情報で上書きする"
        loadAndSaveBtn["command"] = csvLoadAndSave
        loadAndSaveBtn["state"] = "disabled"
        assetsSaveBtn.place(relx=0.78, rely=0.09)
        assetsSaveBtn["state"] = "disabled"


def extract():
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])
    data = decryptFile.allList[num][-1]
    fileType = selectItem["種類"]
    if fileType == "TextAsset":
        ext = ".txt"
    elif fileType == "TextAsset(bytes)":
        ext = ".png"
    elif fileType == "AudioClip":
        ext = ".wav"
    filename = selectItem["名前"] + ext
    file_path = fd.asksaveasfilename(initialfile=filename, defaultextension='txt', filetypes=[('ファイル', '*' + ext)])
    errorMsg = "バイナリで取り出す機能が失敗しました。\n権限問題の可能性があります。"
    if file_path:
        try:
            if fileType == "AudioClip":
                for name, d in data.samples.items():
                    w = open(file_path, "wb")
                    w.write(d)
                    w.close()
            else:
                w = open(file_path, "wb")
                w.write(data.script)
                w.close()
            mb.showinfo(title="成功", message="バイナリで取り出しました")
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def loadAndSave():
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])
    data = decryptFile.allList[num][-1]
    fileType = selectItem["種類"]
    if fileType == "TextAsset":
        ext = ".txt"
    elif fileType == "TextAsset(bytes)":
        ext = ".png"
    elif fileType == "AudioClip":
        errorMsg = "AudioClipはサポートしていません"
        mb.showerror(title="エラー", message=errorMsg)
        return
    file_path = fd.askopenfilename(defaultextension='csv', filetypes=[("ファイル", "*" + ext)])
    if not file_path:
        return
    result = mb.askquestion(title="確認", message="denファイルを上書きします\nそれでもよろしいでしょうか？\n(権限問題で上書き失敗することもあります)", icon="warning")
    if result == "no":
        return

    try:
        if fileType != "AudioClip":
            with open(file_path, "rb") as f:
                data.script = f.read()
            data.save()
        with open(decryptFile.filePath, "wb") as w:
            w.write(decryptFile.env.file.save())
        mb.showinfo(title="成功", message="denファイルを上書きしました")
        reloadFile()
    except Exception:
        w = open("error.log", "a")
        w.write(traceback.format_exc())
        w.close()
        mb.showerror(title="エラー", message="予想外のエラーです")


def csvExtract():
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])
    data = decryptFile.trainOrgInfoList[num][-1]
    filename = selectItem["名前"] + ".csv"
    file_path = fd.asksaveasfilename(initialfile=filename, defaultextension='csv', filetypes=[('trainOrgInfo', '*.csv')])
    errorMsg = "CSVで取り出す機能が失敗しました。\n権限問題の可能性があります。"
    if file_path:
        try:
            w = codecs.open(file_path, "w", "utf-8-sig", "strict")
            trainOrgInfo = decryptFile.getTrainOrgInfo(data)
            w.write("ノッチ数,{0}\n".format(trainOrgInfo[1]))
            w.write("編成数,{0}\n".format(trainOrgInfo[5]))
            w.write("bodyClass\n")
            w.write(",".join(trainOrgInfo[6]))
            w.write("\n")
            w.write("bodyモデル\n")
            w.write(",".join(trainOrgInfo[7]))
            w.write("\n")
            w.write("pantaモデル\n")
            w.write(",".join(trainOrgInfo[8]))
            w.write("\n")
            w.write("bodyClass indexリスト\n")
            w.write(",".join([str(x) for x in trainOrgInfo[9]]))
            w.write("\n")
            w.write("bodyモデル indexリスト\n")
            w.write(",".join([str(x) for x in trainOrgInfo[10]]))
            w.write("\n")
            w.write("pantaモデル indexリスト\n")
            w.write(",".join([str(x) for x in trainOrgInfo[11]]))
            w.close()
            mb.showinfo(title="成功", message="CSVで取り出しました")
        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def csvLoadAndSave():
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])
    file_path = fd.askopenfilename(defaultextension='csv', filetypes=[("trainOrgInfo", "*.csv")])
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
            mb.showerror(title="エラー", message=decryptFile.error)
        if not decryptFile.saveCsv(num):
            decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーです")
            return
        mb.showinfo(title="成功", message="CSVで上書きした\n保存するボタンで【resources_new.assets】を作成します")
    except Exception:
        w = open("error.log", "a")
        w.write(traceback.format_exc())
        w.close()
        mb.showerror(title="エラー", message="予想外のエラーです")


def assetsSave():
    global decryptFile
    global assetsSaveBtn

    assetsSaveBtn["state"] = "disabled"
    assetsSaveBtn.update()
    try:
        if not decryptFile.saveAssets():
            decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーです")
            return
        mb.showinfo(title="成功", message="resources_new.assetsを作成しました。")
        reloadFile()
    except Exception:
        w = open("error.log", "a")
        w.write(traceback.format_exc())
        w.close()
        mb.showerror(title="エラー", message="予想外のエラーです")
    assetsSaveBtn["state"] = "normal"


def reloadFile():
    global v_radio
    global v_select
    global decryptFile
    global frame

    errorMsg = "予想外のエラーが出ました。"
    if decryptFile.filePath:
        try:
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return

            selectId = None
            if v_select.get() != "":
                selectId = int(v_select.get())

            deleteAllWidget()
            createWidget()

            if selectId is not None:
                if v_radio.get() == 0:
                    maxLen = len(decryptFile.allList)
                elif v_radio.get() == 1:
                    maxLen = len(decryptFile.trainOrgInfoList)

                if selectId >= maxLen:
                    selectId = maxLen - 1
                if selectId - 3 < 0:
                    frame.tree.see(0)
                else:
                    frame.tree.see(selectId - 3)
                frame.tree.selection_set(selectId)

        except Exception:
            w = open("error.log", "a")
            w.write(traceback.format_exc())
            w.close()
            mb.showerror(title="エラー", message=errorMsg)


def openFile():
    global unityFlag
    global v_radio
    global v_fileName
    global decryptFile

    if not unityFlag:
        msg = "UnityPyがインストールされていません。\nsetup.batでインストールしてください"
        mb.showerror("エラー", message=msg)
        return

    errorMsg = "予想外のエラーが出ました。"
    if v_radio.get() == 0:
        file_path = fd.askopenfilename(filetypes=[("DEND_SS", "*.den")])
        if file_path:
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            del decryptFile
            decryptFile = DenDecrypt(file_path)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
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
                mb.showerror(title="エラー", message=errorMsg)
                return
            deleteAllWidget()
            createWidget()


def call_ssUnity(rootTk, programFrame):
    global unityFlag
    global root
    global v_radio
    global v_fileName
    global v_select
    global v_btnList
    global extractBtn
    global loadAndSaveBtn
    global assetsSaveBtn
    global contentsLf

    if not unityFlag:
        msg = "UnityPyがインストールされていません。\nsetup.batでインストールしてください"
        mb.showerror("エラー", message=msg)
        return

    root = rootTk
    v_radio = tkinter.IntVar()
    v_radio.set(0)

    v_fileName = tkinter.StringVar()
    fileNameEt = ttk.Entry(programFrame, textvariable=v_fileName, font=("", 14), width=23, state="readonly", justify="center")
    fileNameEt.place(relx=0.053, rely=0.03)

    selectLb = ttk.Label(programFrame, text="選択した行番号：", font=("", 14))
    selectLb.place(relx=0.05, rely=0.09)

    v_select = tkinter.StringVar()
    selectEt = ttk.Entry(programFrame, textvariable=v_select, font=("", 14), width=6, state="readonly", justify="center")
    selectEt.place(relx=0.22, rely=0.09)

    denRb = tkinter.Radiobutton(programFrame, text="denファイルを修正する", command=selectGame, variable=v_radio, value=0)
    denRb.place(relx=0.42, rely=0.03)
    resourcesRb = tkinter.Radiobutton(programFrame, text="車両編成を修正する(resources.assets)", command=selectGame, variable=v_radio, value=1)
    resourcesRb.place(relx=0.60, rely=0.03)

    extractBtn = ttk.Button(programFrame, text="ファイルを取り出す", width=25, state="disabled", command=extract)
    extractBtn.place(relx=0.42, rely=0.09)
    loadAndSaveBtn = ttk.Button(programFrame, text="ファイルを上書きする", width=25, state="disabled", command=loadAndSave)
    loadAndSaveBtn.place(relx=0.60, rely=0.09)

    assetsSaveBtn = ttk.Button(programFrame, text="resources.assetsを保存する", width=25, state="disabled", command=assetsSave)
    assetsSaveBtn.place(relx=0.78, rely=0.09)
    assetsSaveBtn.place_forget()

    v_btnList = [
        extractBtn,
        loadAndSaveBtn,
        assetsSaveBtn
    ]

    contentsLf = ttk.LabelFrame(programFrame, text="ファイル内容")
    contentsLf.place(relx=0.03, rely=0.15, relwidth=0.95, relheight=0.82)
