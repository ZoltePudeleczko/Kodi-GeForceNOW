import xbmc
import xbmcaddon
import xbmcgui

import platform
import os.path
import subprocess
from typing import Optional

ADDON: xbmcaddon.Addon = xbmcaddon.Addon("script.geforcenow")
ADDON_ID: str = ADDON.getAddonInfo("id")
ADDON_NAME: str = ADDON.getAddonInfo("name")
ADDON_VERSION: str = ADDON.getAddonInfo("version")
MSG = ADDON.getLocalizedString

useCustomExecutable: bool = ADDON.getSetting("useCustomExecutable") == "true"
stopMedia: bool = ADDON.getSetting("stopMedia") == "true"


def log(message: str, level: int = xbmc.LOGINFO) -> None:
    """Log a message to Kodi's log system."""
    xbmc.log(f"[{ADDON_ID}:v{ADDON_VERSION}] {message}", level)


def showExecutableNotFoundDialog() -> None:
    """Show dialog when executable is not found and offer to open settings."""
    title: str = MSG(32003)
    message: str = MSG(32004)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()


def showOpenSettingsDialog() -> None:
    """Show dialog asking user if they want to open addon settings."""
    title: str = MSG(32005)
    message: str = MSG(32006)
    if xbmcgui.Dialog().yesno(title, message):
        ADDON.openSettings()


def showWindowsNotDetected() -> None:
    """Show dialog when Windows platform is not detected."""
    title: str = MSG(32007)
    message: str = MSG(32008)
    xbmcgui.Dialog().ok(title, message)


def showCustomExecutableNotFoundDialog() -> None:
    """Show dialog when custom executable is not found and offer to open settings."""
    title: str = MSG(32009)
    message: str = MSG(32010)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()


def stopMediaPlayback() -> None:
    """Stop any currently playing media in Kodi."""
    player: xbmc.Player = xbmc.Player()
    player.stop()


def find_executable() -> Optional[str]:
    """Find the GeForce NOW executable on the system.
    
    Returns:
        Path to the executable if found, None otherwise.
    """
    if platform.system() == "Windows":
        default_path: str = os.path.expandvars(
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


def execute(executable: str, parameters: str = "") -> None:
    """Execute the GeForce NOW application.
    
    Args:
        executable: Path to the executable file to run.
        parameters: Optional command line parameters to pass to the executable.
    """
    log(f"Calling executable: {executable} with parameters: {parameters}")

    if stopMedia:
        stopMediaPlayback()

    try:
        subprocess.run([executable] + parameters.split(), check=True)
    except subprocess.CalledProcessError as e:
        log(f"Error executing {executable}: {e}", xbmc.LOGERROR)


log("Starting GeForceNOW launcher addon")

if useCustomExecutable:
    customExecutable: str = ADDON.getSetting("customExecutable")
    if os.path.isfile(customExecutable):
        execute(customExecutable)
    else:
        log(
            "Executable not found on the custom location provided by user",
            xbmc.LOGERROR,
        )
        showCustomExecutableNotFoundDialog()
else:
    executable: Optional[str] = find_executable()
    if executable:
        execute(executable)
