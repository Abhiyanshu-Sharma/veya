import os
import ctypes
from dotenv import load_dotenv
import sys
import requests
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PySide6.QtGui import QIcon

load_dotenv()
DEFAULT_GITHUB_CLIENT_ID = "Ov23liUnqTOHa2OJH7YC"
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID") or DEFAULT_GITHUB_CLIENT_ID

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def get_github_profile(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()

    print(f"GitHub API error: {response.status_code}")
    return None



def main():
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("abhiyanshu.veya.desktop.1")

    app = QApplication(sys.argv)
    icon = QIcon(resource_path("assets/icon.ico"))
    app.setWindowIcon(icon)

    window = MainWindow(GITHUB_CLIENT_ID)
    window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()