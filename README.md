# Kodi GeForceNOW Addon

![Addon banner](/script.geforcenow/resources/banner.jpg)

[![GitHub release](https://img.shields.io/github/v/release/ZoltePudeleczko/Kodi-GeForceNOW.svg)](https://github.com/ZoltePudeleczko/Kodi-GeForceNOW/releases)

A simple and effective Kodi addon for launching the NVIDIA GeForce NOW app.

Supports both Windows and Linux (via unofficial app - [gfn_electron][gfn_electron]). Updated for and fully compatible with Kodi 21.2 (Omega).

## Which version should I get?

The version you need depends on your Kodi version, as the Python library version
changes with some Kodi updates.

| Kodi Version         | Addon Release             |
| -------------------- | ------------------------- |
| Kodi 21.x (Omega)    | [Latest Release][latest]  |
| Kodi 20.x (Nexus)    | [Latest Release][latest]  |
| Kodi 19.x (Matrix)   | [Latest Release][latest]  |
| Older Kodi Versions  | [v1.2 Release][v1_2] (supports Windows only)|

[latest]: https://github.com/ZoltePudeleczko/Kodi-GeForceNOW/releases/latest
[v1_2]: https://github.com/ZoltePudeleczko/Kodi-GeForceNOW/releases/tag/v1.2

## Requirements

### Windows

- Install official NVIDIA GeForce NOW app from NVIDIA website: [nvidia.com GeForce NOW download][nvidia_download]

Addon automatically detects app installed in the default directory. If it differs for you you can override the launcher in the addon settings.

### Linux

- Make sure you have Flatpak installed - [flatpak.org][flatpak_download]
- Install unofficial Electron NVIDIA GeForce NOW app by [@hmlendea][hmlendea] - [gfn-electron][gfn_electron]
- You can verify that everything is setup correctly by running `flatpak run io.github.hmlendea.geforcenow-electron` command in the terminal

In the addon settings you can provide a custom executable - other app / script that you use for launching GeForce NOW.

[nvidia_download]: https://www.nvidia.com/en-us/geforce-now/download
[flatpak_download]: https://flatpak.org/setup/
[hmlendea]: https://github.com/hmlendea
[gfn_electron]: https://github.com/hmlendea/gfn-electron

## What's next?

Please share your feedback and report any bugs on the
[Issues](https://github.com/ZoltePudeleczko/Kodi-GeForceNOW/issues) page.

### Changelog

For the full changelog checkout [changelog.md](/script.geforcenow/changelog.md)

## Also check out

Check out my simple yet effective script for combating GeForceNOW's AFK system:
[GeForceNOW-AFK](https://github.com/ZoltePudeleczko/GeForce-NOW-AntiAFK).

## Disclaimer

This plugin is not officially commissioned or supported by NVIDIA.
