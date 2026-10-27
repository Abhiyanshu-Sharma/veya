
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from services.github_user import get_github_user
from services.token_store import get_token


class OverviewPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("Veya")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #E6EDF3;
        """)

        self.subtitle = QLabel("Your GitHub workspace, your rules.")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet("""
            font-size: 14px;
            color: #8B949E;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

    def load_github_profile(self):
        token = get_token()

        if not token:
            self.subtitle.setText("Connect your GitHub account to get started.")
            return

        try:
            user = get_github_user(token)
            self.subtitle.setText(f"Welcome {user['login']}")

        except Exception:
            self.subtitle.setText("Couldn't load your GitHub profile.")
