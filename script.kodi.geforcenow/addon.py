import xbmc
import xbmcaddon
import xbmcgui

import platform
import os.path
import subprocess


# Getting addon constants
ADDON = xbmcaddon.Addon('script.kodi.launches.steam')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_VERSION = ADDON.getAddonInfo('version')
MSG = ADDON.getLocalizedString

# Getting main settings
useCustomExecutable = ADDON.getSetting('useCustomExecutable')


####################### Defining common methods #######################

# Method to print logs on a standard way
def log(message, level=xbmc.LOGNOTICE):
    xbmc.log("[{0}:v{1}] {2}".format(ADDON_ID, ADDON_VERSION, message), level)
# log

# Method to show when addon couldn't detect the executable in the default directory
def showExecutableNotFoundDialog():
    title = MSG(32003)
    message = MSG(32004)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()
# showExecutableNotFoundDialog

# Method to ask if user wants to open Addon Settings
def showOpenSettingsDialog():
    title = MSG(32005)
    message = MSG(32006)
    if xbmcgui.Dialog().yesno(title, message):
        ADDON.openSettings()
# showOpenSettingsDialog

# Method to show when addon is launched on Linux / Mac (as only Windows is supported)
def showWindowsNotDetected():
    title = MSG(32007)
    message = MSG(32008)
    xbmcgui.Dialog().ok(title, message)
# showWindowsNotDetected

# Method to show when user has provided a custom executable path that doesn't exist
def showCustomExecutableNotFoundDialog():
    title = MSG(32009)
    message = MSG(32010)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()
# showCustomExecutableNotFoundDialog

# Method to stop media playback in Kodi
def stopMediaPlayback():
    player = xbmc.Player()
    player.stop()
# stopMediaPlayback

# Method to execute GeForceNOW using provided executable
def execute(executable):
    parameters = ''
    log('Calling executable: {0}  with parameters: {1}'.format(executable,parameters))
    stopMediaPlayback()
    subprocess.call([executable, parameters])
# execute

####################### Addon entrypoint #######################

# Starting the Addon
log("Starting Addon")

# Calling custom executable (if it is activated on Addon Settings)
if useCustomExecutable == 'true':
    customExecutable = ADDON.getSetting('customExecutable')
    if os.path.isfile(customExecutable):
        execute(customExecutable)
    else:
        log('Executable not found on the custom location provided by user', xbmc.LOGERROR)
        showCustomExecutableNotFoundDialog()

# Finding default GeForceNOW executable location
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