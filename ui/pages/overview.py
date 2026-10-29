import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

from services.github_user import get_github_user
from services.token_store import get_token


class OverviewPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        header = QVBoxLayout()
        header.setSpacing(6)

        self.title = QLabel("Welcome to Veya")
        self.title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #E6EDF3;
            background-color: transparent;
        """)

        self.subtitle = QLabel("Where would you like to work today?")
        self.subtitle.setStyleSheet("""
            font-size: 14px;
            color: #8B949E;
            background-color: transparent;
        """)

        header.addWidget(self.title)
        header.addWidget(self.subtitle)

        layout.addLayout(header)


    def load_github_profile(self):
        token = get_token()

        if not token:
            self.subtitle.setText(
                "Connect your GitHub account to get started."
            )
            return

        try:
            user = get_github_user(token)
            self.subtitle.setText(f"Welcome {user['login']}")

        except requests.HTTPError as error:
            status_code = (
                error.response.status_code
                if error.response is not None
                else None
            )

            if status_code == 401:
                from services.token_store import delete_token
                delete_token()
                self.subtitle.setText(
                    "Your GitHub session has expired. Please reconnect."
                )
            elif status_code == 403:
                self.subtitle.setText(
                    "GitHub denied the request. Please try again later."
                )
            else:
                self.subtitle.setText(
                    "Couldn't load your GitHub profile. Please try again."
                )

            print(f"GitHub profile error: {type(error).__name__}: {error}")

        except requests.RequestException as error:
            self.subtitle.setText(
                "Couldn't connect to GitHub. Check your internet connection."
            )
            print(f"GitHub connection error: {error}")

        except (KeyError, TypeError) as error:
            self.subtitle.setText("GitHub returned an unexpected profile response.")
            print(f"GitHub profile response error: {error}")
