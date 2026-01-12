import xbmc
import xbmcaddon
import xbmcgui

import platform
import os.path
import subprocess
import shutil
from typing import Optional
from typing import List

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


def showUnsupportedPlatformDetected() -> None:
    """Show dialog when unsupported platform is detected."""
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


def showFlatpakNotFoundDialog() -> None:
    """Show dialog when Flatpak is not available on the system."""
    title: str = MSG(32012)
    message: str = MSG(32013)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()


def showGeForceNowFlatpakNotInstalledDialog() -> None:
    """Show dialog when the expected GeForce NOW Flatpak is not installed."""
    title: str = MSG(32014)
    message: str = MSG(32015)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()


def is_flatpak_available() -> bool:
    return shutil.which("flatpak") is not None


def is_flatpak_app_installed(app_id: str) -> bool:
    """Check whether a Flatpak app is installed by calling `flatpak info`."""
    try:
        result = subprocess.run(
            ["flatpak", "info", app_id],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception as e:
        log(f"Error while checking flatpak app installation: {e}", xbmc.LOGERROR)
        return False


def resolve_launch_command() -> Optional[List[str]]:
    """Resolve the command to launch GeForce NOW based on platform and settings."""
    system: str = platform.system()

    if useCustomExecutable:
        customExecutable: str = ADDON.getSetting("customExecutable")
        if os.path.isfile(customExecutable):
            return [customExecutable]
        log(
            "Executable not found on the custom location provided by user",
            xbmc.LOGERROR,
        )
        showCustomExecutableNotFoundDialog()
        return None

    if system == "Windows":
        default_path: str = os.path.expandvars(
            r"%LOCALAPPDATA%\\NVIDIA Corporation\\GeForceNOW\\CEF\\GeForceNOW.exe"
        )
        if os.path.isfile(default_path):
            return [default_path]
        log("Windows executable not found on default path", xbmc.LOGERROR)
        showExecutableNotFoundDialog()
        return None

    if system == "Linux":
        app_id: str = "io.github.hmlendea.geforcenow-electron"
        if not is_flatpak_available():
            log("Flatpak not found in PATH", xbmc.LOGERROR)
            showFlatpakNotFoundDialog()
            return None
        if not is_flatpak_app_installed(app_id):
            log(f"Required Flatpak app not installed: {app_id}", xbmc.LOGERROR)
            showGeForceNowFlatpakNotInstalledDialog()
            return None
        return ["flatpak", "run", app_id]

    log(f"Unsupported platform detected: {system}", xbmc.LOGERROR)
    showUnsupportedPlatformDetected()
    return None


def execute(command: List[str]) -> None:
    """Execute the GeForce NOW application.
    
    Args:
        command: Command (argv list) to execute.
    """
    log(f"Calling command: {command}")

    if stopMedia:
        stopMediaPlayback()

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        log(f"Error executing command {command}: {e}", xbmc.LOGERROR)


log("Starting GeForceNOW launcher addon")

command: Optional[List[str]] = resolve_launch_command()
if command:
    execute(command)
