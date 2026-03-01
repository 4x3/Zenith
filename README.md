# Zenith

[![GitHub release](https://img.shields.io/github/v/release/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/releases)
[![GitHub stars](https://img.shields.io/github/stars/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/stargazers)
[![GitHub license](https://img.shields.io/github/license/4x3/Zenith?color=white&style=flat-square)](https://github.com/4x3/Zenith/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-white?style=flat-square)](https://www.python.org/downloads/)

> Premium, minimalist interaction utility for competitive environments.

Zenith is a high-performance, multithreaded autoclicker designed with a focus on stability, low-latency execution, and an ultra-minimalist graphical interface. It operates independently of its UI, ensuring uninterrupted background execution even during heavy system loads.

## Architecture & Features

Zenith is built on an object-oriented Python architecture, utilizing `win32api` for hardware-level input simulation and `DearPyGui` for a lightweight, hardware-accelerated presentation layer.

* **Independent Threading:** GUI and clicker loops operate on isolated daemon threads for absolute fault tolerance.
* **Smart Window Targeting:** Only executes inputs when authorized target processes (e.g., `java`, `AZ-Launcher`) are in focus.
* **Persistent Configuration:** Automatically and silently saves user states to localized JSON configuration files.
* **Advanced Randomization:** Context-aware click delays to simulate organic input profiles.
* **Modular Payload:** Support for advanced parameters including dynamic cursor shake, block-hitting, and custom audio feedback.
* **Discord Integration:** Built-in Rich Presence (RPC) functionality to display status.

## Prerequisites

To run Zenith from the source code, ensure you have Python 3.8 or higher installed on a Windows environment. Install the required dependencies using pip:

```bash
pip install dearpygui pymeow pypresence psutil pywin32

```

## Usage

Run the core engine from your terminal:

```bash
python zenith.py

```

### Interface Guide

1. **Modules:** Left and Right clicker modules can be toggled independently.
2. **Blatant Mode:** Bypasses organic randomization for raw, static interval clicking.
3. **Advanced Parameters:** Expand the header to access Cursor Shake (force adjustments) and Block-hitting (probability scaling).
4. **Audio Routing:** Input a local `.wav` file path to replace standard system click sounds.

## Disclaimer

Zenith is developed for educational purposes, macro automation, and personal use. Users are strictly responsible for adhering to the terms of service and end-user license agreements of any third-party software or servers they interact with while using this utility.

## License

Distributed under the MIT License. See `LICENSE` for more information.
