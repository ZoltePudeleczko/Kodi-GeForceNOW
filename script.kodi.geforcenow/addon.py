import xbmc
import xbmcaddon
import xbmcgui

import platform
import os.path
import subprocess

ADDON = xbmcaddon.Addon('script.kodi.geforcenow')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_VERSION = ADDON.getAddonInfo('version')
MSG = ADDON.getLocalizedString

useCustomExecutable = ADDON.getSetting('useCustomExecutable')
stopMedia = ADDON.getSetting('stopMedia')


def log(message, level=xbmc.LOGNOTICE):
    xbmc.log("[{0}:v{1}] {2}".format(ADDON_ID, ADDON_VERSION, message), level)


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


def execute(executable):
    parameters = ''
    log('Calling executable: {0}  with parameters: {1}'.format(executable,parameters))

    if stopMedia:
        stopMediaPlayback()

    subprocess.call([executable, parameters])


log("Starting Addon")

if useCustomExecutable == 'true':
    customExecutable = ADDON.getSetting('customExecutable')
    if os.path.isfile(customExecutable):
        execute(customExecutable)
    else:
        log('Executable not found on the custom location provided by user', xbmc.LOGERROR)
        showCustomExecutableNotFoundDialog()

else:
    executable = ''
    executableTemp = ''

    if platform.system() == 'Windows':
        executableTemp = os.path.expandvars(r'%LOCALAPPDATA%\NVIDIA Corporation\GeForceNOW\CEF\GeForceNOW.exe')
        if os.path.isfile(executableTemp):
            executable = executableTemp
        else:
            log('Windows executable not found on default paths', xbmc.LOGERROR)
            showExecutableNotFoundDialog()
        if executable:
            execute(executable)

    else:
        log('Platforms other than Windows are not supported now', xbmc.LOGERROR)
        showWindowsNotDetected()