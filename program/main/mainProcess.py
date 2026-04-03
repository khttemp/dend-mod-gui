import os
import sys
import configparser
import datetime
import traceback
import webbrowser
import requests

import program.sub.textSetting as textSetting
import program.sub.errorLogClass as errorLogClass

errObj = errorLogClass.ErrorLogObj()


def resource_path(localDir, relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", localDir)
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


def confirmUpdate(mb, version, configPath):
    try:
        url = "https://raw.githubusercontent.com/khttemp/dend-mod-gui/main/ver.txt"
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            onlineUpdateVer = response.text
        else:
            onlineUpdateVer = ""

        if version == onlineUpdateVer:
            return
        
        configCheckOption(configPath, "UPDATE", "time", "2000/01/01")

        configRead = configparser.ConfigParser()
        configRead.read(configPath, encoding="utf-8")

        localDateStr = configRead.get("UPDATE", "time")
        localDate = datetime.datetime.strptime(localDateStr, "%Y/%m/%d").date()
        currentDate = datetime.datetime.now().date()
        if (localDate - currentDate).days >= 0:
            return

        msg = textSetting.textList["update"]["message"].format(onlineUpdateVer)
        result = mb.askyesno(title=textSetting.textList["update"]["title"], message=msg)
        if result:
            webbrowser.open_new("https://github.com/khttemp/dend-mod-gui/releases")

        try:
            configRead = configparser.ConfigParser()
            configRead.read(configPath, encoding="utf-8")

            currentTime = datetime.datetime.now()
            currentDate = datetime.datetime.strftime(currentTime, "%Y/%m/%d")
            configRead.set("UPDATE", "time", currentDate)

            f = open(configPath, "w", encoding="utf-8")
            configRead.write(f)
            f.close()
        except PermissionError:
            errObj.write(traceback.format_exc())
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
