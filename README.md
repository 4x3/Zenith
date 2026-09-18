# Zenith

[![GitHub release](https://img.shields.io/github/v/release/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/releases)
[![GitHub stars](https://img.shields.io/github/stars/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/stargazers)
[![GitHub license](https://img.shields.io/github/license/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-white?style=flat-square)](https://www.python.org/downloads/)

> A fully external autoclicker for Minecraft PvP.

Zenith runs outside the Minecraft process entirely — no JVM injection, so it doesn't trip client-side checks on servers like Hypixel. Click timing is randomized per-press instead of a fixed interval, which is what actually matters for staying under server-side heuristics.

## Features

* Runs as a separate process; nothing gets injected into the game
* Randomized click delays instead of a fixed CPS, to look less like a bot on servers that watch for that
* Only fires while a Minecraft client (`java`, `AZ-Launcher`) is the focused window
* Cursor shake and auto block-hit toggles for PvP
* Config (binds, CPS, module settings) is saved locally between runs
* Optional Discord Rich Presence

## Prerequisites

To run Zenith from the source code, ensure you have Python 3.8 or higher installed on a Windows environment. Install the required dependencies using pip:

```bash
pip install dearpygui pymeow pypresence psutil pywin32

```

## Usage

Run the core engine from your terminal:

```bash
python Zenith.py

```

### Interface Guide

1. **Modules:** Left and Right clicker modules can be toggled independently.
2. **Blatant Mode:** Bypasses organic randomization for raw, static interval clicking.
3. **Advanced Parameters:** Expand the header to access Cursor Shake (force adjustments) and Block-hitting (probability scaling).
4. **Audio Routing:** Input a local `.wav` file path to replace standard system click sounds.

## Legal Disclaimer

Zenith is a third-party utility developed for educational purposes and personal use. This project is not affiliated with, endorsed by, or connected to Mojang AB, Microsoft Corporation, or Hypixel Inc. Use this software at your own risk. The developer assumes no responsibility for account bans, punishments, or damages resulting from the use of this tool.

## License

Distributed under the MIT License. See `LICENSE` for more information.
