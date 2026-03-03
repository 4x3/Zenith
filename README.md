# Zenith

[![GitHub release](https://img.shields.io/github/v/release/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/releases)
[![GitHub stars](https://img.shields.io/github/stars/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/stargazers)
[![GitHub license](https://img.shields.io/github/license/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-white?style=flat-square)](https://www.python.org/downloads/)

> A fully external, high-performance Minecraft autoclicker.

Zenith is a lightweight, multithreaded autoclicker built specifically for Minecraft PvP. Because it operates completely externally and does not inject into the Java Virtual Machine (JVM), it is safe to use on major servers like Hypixel. It utilizes advanced randomized CPS generation to seamlessly bypass server-side anti-cheats and heuristic detection.

## Features

* **Fully External:** Runs entirely outside of the Minecraft process, making it completely invisible to client-side injection checks.
* **Anti-Cheat Bypass:** Utilizes intelligent, randomized click delays to simulate legitimate human input and bypass server-side detection on servers like Hypixel.
* **Smart Window Targeting:** Only clicks when a Minecraft client (`java`, `AZ-Launcher`) is your active, focused window.
* **Advanced PvP Mechanics:** Built-in toggles for realistic cursor shake and automated block-hitting to give you an edge in combat.
* **Persistent Configuration:** Automatically saves your module settings, binds, and CPS values locally.
* **Discord RPC:** Optional Discord Rich Presence integration to show your status.

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
