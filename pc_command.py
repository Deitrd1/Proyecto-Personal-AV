import os
import platform
import subprocess

class PcCommand:
    def __init__(self):
        self.chrome_paths = {
            "Windows": "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "Linux": "/usr/bin/google-chrome",
        }

    def open_chrome(self, website):
        if not website:
            return "No se proporcionó un sitio web válido."
        os_name = platform.system()
        chrome_path = self.chrome_paths.get(os_name)
        if not chrome_path or not os.path.exists(chrome_path):
            return f"No se encontró Google Chrome en {chrome_path}. Verifica la instalación."
        subprocess.call([chrome_path, website])
        return f"Abriendo Chrome en {website}."
