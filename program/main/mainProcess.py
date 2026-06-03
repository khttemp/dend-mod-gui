import os
import sys
import configparser
import datetime
import traceback
import webbrowser
import requests
import json
import csv

import program.sub.textSetting as textSetting
import program.sub.errorLogClass as errorLogClass
import program.sub.encodingClass as encodingClass

errObj = errorLogClass.ErrorLogObj()
encObj = encodingClass.SJISEncodingObject()


def resource_path(localDir, relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", localDir)
    return os.path.join(bundle_dir, relative_path)


def dll_path(rootPath, relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.join(rootPath, "program", "appearance", "dllData"))
    return os.path.join(bundle_dir, relative_path)


def getUpdateVer(rootPath):
    try:
        path = resource_path(rootPath, "ver.txt")
        f = open(path, "r", encoding="utf-8")
        line = f.read()
        f.close()
        version = line.strip()
    except Exception:
        print(traceback.format_exc())
        version = ""

    return version


def getOnlineUpdateVer(configPath):
    onlineUpdateVer = ""
    try:
        configCheckOption(configPath, "UPDATE", "time", "2000/01/01")

        configRead = configparser.ConfigParser()
        configRead.read(configPath, encoding="utf-8")

        localDateStr = configRead.get("UPDATE", "time")
        localDate = datetime.datetime.strptime(localDateStr, "%Y/%m/%d").date()
        currentDate = datetime.datetime.now().date()
        if (currentDate - localDate).days > 0:
            try:
                configRead = configparser.ConfigParser()
                configRead.read(configPath, encoding="utf-8")

                currentTime = datetime.datetime.now()
                currentDate = datetime.datetime.strftime(currentTime, "%Y/%m/%d")
                configRead.set("UPDATE", "time", currentDate)

                f = open(configPath, "w", encoding="utf-8")
                configRead.write(f)
                f.close()

                url = "https://raw.githubusercontent.com/khttemp/dend-mod-gui/main/ver.txt"
                response = requests.get(url)
                if response.status_code != requests.codes.ok:
                    return

                onlineUpdateVer = response.text
            except Exception:
                errObj.write(traceback.format_exc())
    except Exception:
        pass

    return onlineUpdateVer


def writeDefaultConfig(configPath):
    try:
        config_ini_folder = os.path.dirname(configPath)
        if not os.path.exists(config_ini_folder):
            os.makedirs(config_ini_folder)

        config = configparser.RawConfigParser()
        config.add_section("COMICSCRIPT_GAME")
        config.set("COMICSCRIPT_GAME", "mode", 0)

        config.add_section("SMF_FRAME")
        config.set("SMF_FRAME", "mode", 0)
        config.add_section("SMF_MESH")
        config.set("SMF_MESH", "mode", 0)
        config.add_section("SMF_XYZ")
        config.set("SMF_XYZ", "mode", 0)
        config.add_section("SMF_MTRL")
        config.set("SMF_MTRL", "mode", 0)
        config.add_section("GLB_WRITE")
        config.set("GLB_WRITE", "mode", 0)

        config.add_section("MODEL_NAME_MODE")
        config.set("MODEL_NAME_MODE", "mode", 0)
        config.add_section("FLAG_MODE")
        config.set("FLAG_MODE", "mode", 0)
        config.add_section("AMB_READ_MODE")
        config.set("AMB_READ_MODE", "mode", 1)

        config.add_section("UPDATE")
        config.set("UPDATE", "time", "2000/01/01")

        f = open(configPath, "w", encoding="utf-8")
        config.write(f)
        f.close()
    except PermissionError:
        errObj.write(traceback.format_exc())


def configCheckOption(configPath, section, options, defaultValue="0"):
    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    if not configRead.has_option(section, options):
        if not configRead.has_section(section):
            configRead.add_section(section)
        configRead.set(section, options, defaultValue)

        try:
            f = open(configPath, "w", encoding="utf-8")
            configRead.write(f)
            f.close()
        except PermissionError:
            errObj.write(traceback.format_exc())

        return True
    return False


def openReleases():
    try:
        webbrowser.open_new("https://github.com/khttemp/dend-mod-gui/releases")
    except Exception:
        errObj.write(traceback.format_exc())


def readXlsxWriteConfig(configPath):
    if not os.path.exists(configPath):
        writeDefaultConfig(configPath)

    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    reReadFlag = False
    if configCheckOption(configPath, "MODEL_NAME_MODE", "mode"):
        reReadFlag = True
    if configCheckOption(configPath, "FLAG_MODE", "mode"):
        reReadFlag = True
    if configCheckOption(configPath, "AMB_READ_MODE", "mode", "1"):
        reReadFlag = True

    if reReadFlag:
        configRead.read(configPath, encoding="utf-8")

    model = int(configRead.get("MODEL_NAME_MODE", "mode"))
    flag = int(configRead.get("FLAG_MODE", "mode"))
    amb = int(configRead.get("AMB_READ_MODE", "mode"))
    return (model, flag, amb)


def writeXlsxConfig(configPath, section, value):
    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    if section == "model":
        configRead.set("MODEL_NAME_MODE", "mode", str(value))
    if section == "flag":
        configRead.set("FLAG_MODE", "mode", str(value))
    if section == "amb":
        configRead.set("AMB_READ_MODE", "mode", str(value))

    try:
        f = open(configPath, "w", encoding="utf-8")
        configRead.write(f)
        f.close()
    except PermissionError:
        errObj.write(traceback.format_exc())


def readComicscriptConfig(configPath):
    if not os.path.exists(configPath):
        writeDefaultConfig(configPath)

    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    reReadFlag = False
    if configCheckOption(configPath, "COMICSCRIPT_GAME", "mode"):
        reReadFlag = True

    if reReadFlag:
        configRead.read(configPath, encoding="utf-8")

    game = int(configRead.get("COMICSCRIPT_GAME", "mode"))
    return game


def writeComicscriptConfig(configPath, value):
    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    configRead.set("COMICSCRIPT_GAME", "mode", str(value))

    try:
        f = open(configPath, "w", encoding="utf-8")
        configRead.write(f)
        f.close()
    except PermissionError:
        errObj.write(traceback.format_exc())


def readCmdJsonInfo(rootPath):
    jsonName = "cmd.json"
    cmdJsonInfo = None
    try:
        url = "https://raw.githubusercontent.com/khttemp/dendData/refs/heads/main/comicscript/js/" + jsonName
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            cmdJsonInfo = json.loads(response.text)
        else:
            filePath = os.path.join(rootPath, "program", "sub", "comicscript", "importPy")
            path = resource_path(filePath, jsonName)
            f = open(path, "r", encoding="utf-8")
            cmdJsonInfo = json.load(f)
            f.close()
    except Exception:
        pass

    return cmdJsonInfo


def writeSmfFlagConfig(checked, configPath, section):
    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    value = 0
    if checked.get():
        value = 1

    if section == "frame":
        configRead.set("SMF_FRAME", "mode", str(value))
    if section == "mesh":
        configRead.set("SMF_MESH", "mode", str(value))
    if section == "xyz":
        configRead.set("SMF_XYZ", "mode", str(value))
    if section == "mtrl":
        configRead.set("SMF_MTRL", "mode", str(value))

    try:
        f = open(configPath, "w", encoding="utf-8")
        configRead.write(f)
        f.close()
    except PermissionError:
        errObj.write(traceback.format_exc())


def writeGlbConfig(configPath, value):
    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    configRead.set("GLB_WRITE", "mode", str(value))

    try:
        f = open(configPath, "w", encoding="utf-8")
        configRead.write(f)
        f.close()
    except PermissionError:
        errObj.write(traceback.format_exc())


def readSmfWriteConfig(configPath):
    if not os.path.exists(configPath):
        writeDefaultConfig(configPath)

    configRead = configparser.ConfigParser()
    configRead.read(configPath, encoding="utf-8")

    reReadFlag = False
    if configCheckOption(configPath, "SMF_FRAME", "mode"):
        reReadFlag = True
    if configCheckOption(configPath, "SMF_MESH", "mode"):
        reReadFlag = True
    if configCheckOption(configPath, "SMF_XYZ", "mode"):
        reReadFlag = True
    if configCheckOption(configPath, "SMF_MTRL", "mode"):
        reReadFlag = True
    if configCheckOption(configPath, "GLB_WRITE", "mode"):
        reReadFlag = True

    if reReadFlag:
        configRead.read(configPath, encoding="utf-8")

    frameFlag = int(configRead.get("SMF_FRAME", "mode"))
    meshFlag = int(configRead.get("SMF_MESH", "mode"))
    xyzFlag = int(configRead.get("SMF_XYZ", "mode"))
    mtrlFlag = int(configRead.get("SMF_MTRL", "mode"))
    glb = int(configRead.get("GLB_WRITE", "mode"))

    return ([frameFlag, meshFlag, xyzFlag, mtrlFlag], glb)


def readFvtInfo(rootPath):
    fvtInfo = {
        "LS": None,
        "BS": None,
        "CS": None,
        "RS": None,
    }
    try:
        for key in fvtInfo.keys():
            filename = "{0}.csv".format(key)
            filePath = os.path.join(rootPath, "program", "sub", "fvtMaker", "importPy", "resource")
            path = resource_path(filePath, filename)
            with open(path, mode='r', encoding=encObj.enc, newline='') as f:
                reader = csv.reader(f)
                fvtInfo[key] = list(reader)
    except Exception:
        pass

    return fvtInfo


def readFvtImagePath(rootPath):
    fvtImageInfo = {
        "LS": "",
        "BS": "",
        "CS": "",
        "RS": "",
    }
    try:
        for key in fvtImageInfo.keys():
            filename = "{0}.png".format(key)
            filePath = os.path.join(rootPath, "program", "sub", "fvtMaker", "importPy", "resource")
            path = resource_path(filePath, filename)
            fvtImageInfo[key] = path
    except Exception:
        pass

    return fvtImageInfo