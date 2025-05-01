import xbmc
import xbmcaddon
import xbmcgui

import platform
import os.path
import subprocess

ADDON = xbmcaddon.Addon("script.kodi.geforcenow")
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_VERSION = ADDON.getAddonInfo("version")
MSG = ADDON.getLocalizedString

useCustomExecutable = ADDON.getSetting("useCustomExecutable") == "true"
stopMedia = ADDON.getSetting("stopMedia") == "true"


def log(message, level=xbmc.LOGINFO):
    xbmc.log(f"[{ADDON_ID}:v{ADDON_VERSION}] {message}", level)


def showExecutableNotFoundDialog():
    title = MSG(32003)
    message = MSG(32004)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()


def showOpenSettingsDialog():
    title = MSG(32005)
    message = MSG(32006)
    if xbmcgui.Dialog().yesno(title, message):
        ADDON.openSettings()


def showWindowsNotDetected():
    title = MSG(32007)
    message = MSG(32008)
    xbmcgui.Dialog().ok(title, message)


def showCustomExecutableNotFoundDialog():
    title = MSG(32009)
    message = MSG(32010)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()


def stopMediaPlayback():
    player = xbmc.Player()
    player.stop()


def find_executable():
    if platform.system() == "Windows":
        default_path = os.path.expandvars(
            r"%LOCALAPPDATA%\\NVIDIA Corporation\\GeForceNOW\\CEF\\GeForceNOW.exe"
        )
        if os.path.isfile(default_path):
            return default_path
        else:
            log("Windows executable not found on default path", xbmc.LOGERROR)
            showExecutableNotFoundDialog()
    else:
        log("Platforms other than Windows are not supported now, sorry", xbmc.LOGERROR)
        showWindowsNotDetected()
    return None


def execute(executable, parameters=""):
    log(f"Calling executable: {executable} with parameters: {parameters}")

    if stopMedia:
        stopMediaPlayback()

    try:
        subprocess.run([executable] + parameters.split(), check=True)
    except subprocess.CalledProcessError as e:
        log(f"Error executing {executable}: {e}", xbmc.LOGERROR)


log("Starting GeForceNOW launcher addon")

if useCustomExecutable:
    customExecutable = ADDON.getSetting("customExecutable")
    if os.path.isfile(customExecutable):
        execute(customExecutable)
    else:
        log(
            "Executable not found on the custom location provided by user",
            xbmc.LOGERROR,
        )
        showCustomExecutableNotFoundDialog()
else:
    executable = find_executable()
    if executable:
        execute(executable)
