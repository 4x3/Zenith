version = "1.0.0"

import win32api, win32con, win32gui, win32process, psutil, time, threading, random, winsound, os, json, sys
import dearpygui.dearpygui as dpg
from pypresence import Presence

class ClickerConfig(dict):
    """Listens for configuration changes and auto-saves silently."""
    def __init__(self, initial_dict, hwid):
        self.hwid = hwid
        self.save_path = f"{os.environ['LOCALAPPDATA']}\\Temp\\Zenith_{self.hwid}.json"
        
        # Try to load existing config
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r", encoding="utf-8") as f:
                    saved_dict = json.load(f)
                    # Basic validation to ensure keys match
                    if all(k in saved_dict for k in initial_dict):
                        initial_dict = saved_dict
            except Exception:
                pass

        for k, v in initial_dict.items():
            if isinstance(v, dict):
                initial_dict[k] = ClickerConfig(v, self.hwid)
        super().__init__(initial_dict)

    def __setitem__(self, item, value):
        _value = ClickerConfig(value, self.hwid) if isinstance(value, dict) else value
        super().__setitem__(item, _value)
        self.save_config()

    def save_config(self):
        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(self, f, indent=4)
        except Exception:
            pass

class ZenithEngine:
    """Core backend logic. Fully isolated from the GUI for stability."""
    def __init__(self, hwid: str):
        self.hwid = hwid
        
        default_config = {
            "left": {
                "enabled": False, "mode": "hold", "cps": 12, "focus_only": True, 
                "blatant": False, "blockhit": False, "blockhit_chance": 25, 
                "shake": False, "shake_force": 5, "sound_path": ""
            },
            "right": {
                "enabled": False, "mode": "hold", "cps": 12, "focus_only": True, 
                "blatant": False, "shake": False, "shake_force": 5, "sound_path": ""
            },
            "misc": {"rpc": True}
        }
        
        self.config = ClickerConfig(default_config, self.hwid)
        self.focused_process = ""
        self.mc_window = None

        # Daemon threads close automatically when the main program closes
        threading.Thread(target=self.rpc_handler, daemon=True).start()
        threading.Thread(target=self.window_listener, daemon=True).start()
        threading.Thread(target=self.click_loop, args=("left", 0x01), daemon=True).start()
        threading.Thread(target=self.click_loop, args=("right", 0x02), daemon=True).start()

    def rpc_handler(self):
        try:
            rpc = Presence("1044302531272126534") # Replace with your Zenith Discord Client ID
            rpc.connect()
            start_time = time.time()
            while True:
                if self.config["misc"]["rpc"]:
                    rpc.update(state="Premium Interaction.", start=start_time, large_image="logo", large_text="Zenith")
                else:
                    rpc.clear()
                time.sleep(15)
        except Exception:
            pass

    def window_listener(self):
        while True:
            current_window = win32gui.GetForegroundWindow()
            self.mc_window = win32gui.FindWindow("LWJGL", None)
            try:
                self.focused_process = psutil.Process(win32process.GetWindowThreadProcessId(current_window)[-1]).name()
            except Exception:
                self.focused_process = ""
            time.sleep(0.5)

    def apply_shake(self, force):
        current_pos = win32api.GetCursorPos()
        pixels = random.randint(-force, force)
        direction = random.randint(0, 3)
        
        if direction == 0: win32api.SetCursorPos((current_pos[0] + pixels, current_pos[1] - pixels))
        elif direction == 1: win32api.SetCursorPos((current_pos[0] - pixels, current_pos[1] + pixels))
        elif direction == 2: win32api.SetCursorPos((current_pos[0] + pixels, current_pos[1] + pixels))
        else: win32api.SetCursorPos((current_pos[0] - pixels, current_pos[1] - pixels))

    def click_loop(self, button_type, vkey):
        while True:
            cfg = self.config[button_type]
            if cfg["cps"] == 0: cfg["cps"] = 1 # Prevent division by zero
            
            delay = 1 / cfg["cps"] if cfg["blatant"] else random.random() % (2 / cfg["cps"])

            if cfg["enabled"]:
                if cfg["mode"] == "hold" and win32api.GetAsyncKeyState(vkey) >= 0:
                    time.sleep(0.01)
                    continue

                if cfg["focus_only"] and not any(x in self.focused_process for x in ["java", "AZ-Launcher"]):
                    time.sleep(0.5)
                    continue

                self.simulate_click(button_type, vkey, cfg)

            time.sleep(delay)

    def simulate_click(self, button_type, vkey, cfg):
        focused = cfg["focus_only"]
        down = win32con.WM_LBUTTONDOWN if vkey == 0x01 else win32con.WM_RBUTTONDOWN
        up = win32con.WM_LBUTTONUP if vkey == 0x01 else win32con.WM_RBUTTONUP
        me_down = win32con.MOUSEEVENTF_LEFTDOWN if vkey == 0x01 else win32con.MOUSEEVENTF_RIGHTDOWN
        me_up = win32con.MOUSEEVENTF_LEFTUP if vkey == 0x01 else win32con.MOUSEEVENTF_RIGHTUP

        # Execute Click
        if focused and self.mc_window:
            win32api.SendMessage(self.mc_window, down, 0, 0)
            time.sleep(0.02)
            win32api.SendMessage(self.mc_window, up, 0, 0)
        else:
            win32api.mouse_event(me_down, 0, 0)
            time.sleep(0.02)
            win32api.mouse_event(me_up, 0, 0)

        # Advanced Features
        if cfg.get("shake"):
            self.apply_shake(cfg["shake_force"])

        if cfg.get("sound_path") and os.path.isfile(cfg["sound_path"]):
            winsound.PlaySound(cfg["sound_path"], winsound.SND_ASYNC)

        if button_type == "left" and cfg.get("blockhit"):
            if random.uniform(0, 1) <= (cfg["blockhit_chance"] / 100.0):
                if focused and self.mc_window:
                    win32api.SendMessage(self.mc_window, win32con.WM_RBUTTONDOWN, 0, 0)
                    time.sleep(0.02)
                    win32api.SendMessage(self.mc_window, win32con.WM_RBUTTONUP, 0, 0)
                else:
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                    time.sleep(0.02)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

class ZenithGUI:
    """The sleek, dark presentation layer."""
    def __init__(self, engine: ZenithEngine):
        self.engine = engine

    def build_theme(self):
        with dpg.theme() as premium_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (14, 14, 16))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (20, 20, 22))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (30, 30, 34))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (45, 45, 55))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (60, 60, 75))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (24, 24, 28))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (35, 35, 40))
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (110, 120, 255)) 
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (110, 120, 255))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (130, 140, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (30, 30, 34))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (45, 45, 55))
                
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 25, 25)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 12)

        dpg.bind_theme(premium_theme)

    def draw_module(self, title, config_key):
        with dpg.child_window(width=280, height=340, border=False):
            dpg.add_text(title, color=(110, 120, 255))
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="enabled", default_value=self.engine.config[config_key]["enabled"], 
                                 callback=lambda s, d: self.engine.config[config_key].update({"enabled": d}))
                dpg.add_checkbox(label="blatant", default_value=self.engine.config[config_key]["blatant"], 
                                 callback=lambda s, d: self.engine.config[config_key].update({"blatant": d}))
            
            dpg.add_slider_int(label="cps", default_value=self.engine.config[config_key]["cps"], min_value=1, max_value=25, 
                               callback=lambda s, d: self.engine.config[config_key].update({"cps": d}))
            
            with dpg.group(horizontal=True):
                dpg.add_combo(items=["hold", "always"], default_value=self.engine.config[config_key]["mode"], width=100,
                              callback=lambda s, d: self.engine.config[config_key].update({"mode": d}))
                dpg.add_text(" mode")
            
            dpg.add_spacer(height=10)
            
            # Advanced Features Dropdown
            with dpg.collapsing_header(label="advanced parameters"):
                dpg.add_spacer(height=5)
                
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="shake", default_value=self.engine.config[config_key]["shake"],
                                     callback=lambda s, d: self.engine.config[config_key].update({"shake": d}))
                    dpg.add_slider_int(label="force", default_value=self.engine.config[config_key]["shake_force"], min_value=1, max_value=20, width=100,
                                       callback=lambda s, d: self.engine.config[config_key].update({"shake_force": d}))

                if config_key == "left":
                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(label="blockhit", default_value=self.engine.config[config_key]["blockhit"],
                                         callback=lambda s, d: self.engine.config[config_key].update({"blockhit": d}))
                        dpg.add_slider_int(label="chance %", default_value=self.engine.config[config_key]["blockhit_chance"], min_value=1, max_value=100, width=100,
                                           callback=lambda s, d: self.engine.config[config_key].update({"blockhit_chance": d}))

                dpg.add_input_text(hint="audio/click.wav", default_value=self.engine.config[config_key]["sound_path"], width=180,
                                   callback=lambda s, d: self.engine.config[config_key].update({"sound_path": d}))
                dpg.add_text("custom sound path", color=(150, 150, 150))

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title="Zenith", width=640, height=520, resizable=False)
        dpg.setup_dearpygui()

        self.build_theme()

        with dpg.window(tag="primary", width=640, height=520, no_title_bar=True, no_move=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Zenith", color=(255, 255, 255))
                dpg.add_text(f"v{version}", color=(100, 100, 100))
                
            dpg.add_spacer(height=15)

            with dpg.group(horizontal=True):
                self.draw_module("left module", "left")
                dpg.add_spacer(width=10)
                self.draw_module("right module", "right")

            dpg.add_spacer(height=15)
            
            with dpg.child_window(height=80, border=False):
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="discord rpc", default_value=self.engine.config["misc"]["rpc"], 
                                     callback=lambda s, d: self.engine.config["misc"].update({"rpc": d}))
                dpg.add_spacer(height=10)
                dpg.add_text("github.com/4x3/Zenith", color=(100, 100, 100))

        dpg.set_primary_window("primary", True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

if __name__ == "__main__":
    if os.name != "nt":
        sys.exit("Zenith requires a Windows environment.")

    try:
        # Simple local identifier generation. This is where KeyAuth will go later.
        hwid = str(os.getlogin()) 
        
        # Initialize Architecture
        engine = ZenithEngine(hwid)
        gui = ZenithGUI(engine)
        
        gui.run()
    except KeyboardInterrupt:
        os._exit(0)