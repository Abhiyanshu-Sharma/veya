import os
from dotenv import load_dotenv
import sys
import requests
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")

def get_github_profile(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()

    print(f"GitHub API error: {response.status_code}")
    return None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()