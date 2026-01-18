import xbmc
import xbmcaddon
import xbmcgui

import platform
import os
import os.path
import subprocess
import shutil
from typing import Optional
from typing import List
from typing import Callable

ADDON: xbmcaddon.Addon = xbmcaddon.Addon("script.geforcenow")
ADDON_ID: str = ADDON.getAddonInfo("id")
ADDON_NAME: str = ADDON.getAddonInfo("name")
ADDON_VERSION: str = ADDON.getAddonInfo("version")
MSG: Callable[[int], str] = ADDON.getLocalizedString

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

def showFlatpakPermissionRequiredDialog() -> None:
    """Show dialog when Kodi Flatpak lacks permission to control host Flatpak."""
    title: str = MSG(32025)
    message: str = MSG(32026)
    xbmcgui.Dialog().ok(title, message)
    showOpenSettingsDialog()

def _resolve_flatpak_path() -> Optional[str]:
    """
    Resolve an absolute path to `flatpak` on the current filesystem.
    """
    found: Optional[str] = shutil.which("flatpak")
    if found:
        return found
    for candidate in ("/usr/bin/flatpak", "/bin/flatpak", "/usr/local/bin/flatpak"):
        if os.path.isfile(candidate):
            return candidate
    return None

def _flatpak_base_command() -> Optional[List[str]]:
    """
    Return the argv prefix to invoke host flatpak.
    - If Kodi runs as Flatpak, use `flatpak-spawn --host flatpak`
    - Otherwise use `flatpak`
    """
    if os.path.exists("/.flatpak-info"):
        # Avoid hardcoding /usr/bin/flatpak on the host; let the host PATH resolve it.
        return ["flatpak-spawn", "--host", "flatpak"]
    else:
        flatpak_path = _resolve_flatpak_path()
        if flatpak_path is None:
            return None
        return [flatpak_path]

def resolve_launch_command() -> Optional[List[str]]:
    """Resolve the command to launch GeForce NOW."""
    system: str = platform.system()

    if useCustomExecutable:
        customExecutable: str = ADDON.getSetting("customExecutable")
        if os.path.isfile(customExecutable):
            return [customExecutable]
        log(
            "Executable not found on the custom location provided by user",
            xbmc.LOGERROR,
        )
        showExecutableNotFoundDialog()
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
        base_cmd: Optional[List[str]] = _flatpak_base_command()
        if base_cmd is None:
            log(
                f"Flatpak not found/available (PATH={os.environ.get('PATH', '')})",
                xbmc.LOGERROR,
            )
            showFlatpakNotFoundDialog()
            return None

        app_id: str = "io.github.hmlendea.geforcenow-electron"
        return base_cmd + ["run", app_id]

    log(f"Unsupported platform detected: {system}", xbmc.LOGERROR)
    showUnsupportedPlatformDetected()
    return None

def execute(argv: List[str]) -> None:
    """Execute the GeForce NOW application.
    
    Args:
        argv: Command argv to execute (e.g. ["flatpak", "run", "io.github.hmlendea.geforcenow-electron"]).
    """
    log(f"Calling command: {' '.join(argv)}")

    if stopMedia:
        stopMediaPlayback()

    try:
        subprocess.run(argv, check=True)
    except FileNotFoundError as e:
        log(f"Executable not found while executing command ({e})", xbmc.LOGERROR)
        # Most common on Linux is missing flatpak/flatpak-spawn inside the runtime.
        showFlatpakNotFoundDialog()
    except subprocess.CalledProcessError as e:
        log(f"Error executing command {' '.join(argv)}: {e}", xbmc.LOGERROR)


log("Starting GeForceNOW launcher addon")

argv: Optional[List[str]] = resolve_launch_command()
if argv:
    execute(argv)
else:
    log("Failed to resolve launch command", xbmc.LOGERROR)
