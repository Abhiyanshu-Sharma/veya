import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

from services.github_user import get_github_user
from services.token_store import get_token


class OverviewPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(12)
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

        self.title.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed
        )

        self.subtitle.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed
        )

        header.addWidget(self.title)
        header.addWidget(self.subtitle)

        layout.addLayout(header)

        workspace_container = QWidget()
        workspace_container.setFixedHeight(190)

        workspace_layout = QHBoxLayout(workspace_container)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(16)

        gui_card = self.create_workspace_card(
            "GUI Workspace",
            "Manage your repositories visually through an intuitive interface.",
            "▣"
        )

        cli_card = self.create_workspace_card(
            "CLI Workspace",
            "Work with your repositories directly through a terminal.",
            ">_"
        )

        workspace_layout.addWidget(gui_card, 1)
        workspace_layout.addWidget(cli_card, 1)

        layout.addWidget(workspace_container)

        layout.addSpacing(4)

        recent_section = QWidget()

        recent_section.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        recent_section_layout = QVBoxLayout(recent_section)
        recent_section_layout.setContentsMargins(0, 0, 0, 0)
        recent_section_layout.setSpacing(12)

        recent_title = QLabel("Recently working on")
        recent_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #E6EDF3;
            background-color: transparent;
        """)

        recent_section_layout.addWidget(recent_title)

        self.recent_container = QFrame()
        self.recent_container.setFixedHeight(56)

        self.recent_container.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 10px;
            }
        """)

        self.recent_layout = QVBoxLayout(self.recent_container)
        self.recent_layout.setContentsMargins(16, 12, 16, 12)
        self.recent_layout.setSpacing(8)

        self.recent_empty_label = QLabel(
            "Your recently opened repositories will appear here."
        )

        self.recent_empty_label.setStyleSheet("""
            color: #8B949E;
            font-size: 13px;
            background-color: transparent;
            border: none;
        """)

        self.recent_layout.addWidget(self.recent_empty_label)

        recent_section_layout.addWidget(self.recent_container)

        layout.addWidget(recent_section, 0 ,Qt.AlignmentFlag.AlignTop)

        layout.addStretch()

        self.status_container = QWidget()

        status_layout = QHBoxLayout(self.status_container)
        status_layout.setContentsMargins(0, 8, 0, 0)

        self.status_label = QLabel("GitHub: Checking connection...")

        self.status_label.setStyleSheet("""
            color: #8B949E;
            font-size: 12px;
            background-color: transparent;
        """)

        self.reconnect_button = QPushButton("Reconnect")

        self.reconnect_button.setStyleSheet("""
            QPushButton {
                color: #58A6FF;
                background-color: transparent;
                border: none;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                color: #79C0FF;
            }
        """)

        self.reconnect_button.hide()

        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.reconnect_button)

        layout.addWidget(self.status_container)

    def create_workspace_card(self, title, description, icon_text):
        card = QFrame()
        card.setFixedHeight(190)

        card.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(10)

        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("""
            font-size: 28px;
            color: #58A6FF;
            background-color: transparent;
            border: none;
        """)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #E6EDF3;
            background-color: transparent;
            border: none;
        """)

        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("""
            font-size: 13px;
            color: #8B949E;
            background-color: transparent;
            border: none;
        """)

        action_label = QLabel("Open workspace →")
        action_label.setStyleSheet("""
            font-size: 13px;
            font-weight: bold;
            color: #58A6FF;
            background-color: transparent;
            border: none;
        """)

        card_layout.addWidget(icon_label)
        card_layout.addWidget(title_label)
        card_layout.addWidget(description_label)
        card_layout.addStretch()
        card_layout.addWidget(action_label)

        return card

    def set_github_status(self, message, color):
        self.status_label.setText(f"●  GitHub: {message}")
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-size: 12px;
            background-color: transparent;
        """)

    def load_github_profile(self):
        token = get_token()

        if not token:
            self.subtitle.setText(
                "Connect your GitHub account to get started."
            )
            self.set_github_status("Disconnected", "#F85149")
            self.reconnect_button.show()
            return

        try:
            user = get_github_user(token)

            self.set_github_status("Connected", "#3FB950")
            self.reconnect_button.hide()

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

                self.set_github_status("Disconnected", "#F85149")
                self.reconnect_button.show()

                self.subtitle.setText(
                    "Your GitHub session has expired. Please reconnect."
                )
            elif status_code == 403:
                self.subtitle.setText(
                    "GitHub denied the request. Please try again later."
                )
                self.set_github_status("Request denied", "#D29922")
            else:
                self.subtitle.setText(
                    "Couldn't load your GitHub profile. Please try again."
                )

            print(f"GitHub profile error: {type(error).__name__}: {error}")

        except requests.RequestException as error:
            self.subtitle.setText(
                "Couldn't connect to GitHub. Check your internet connection."
            )

            self.set_github_status("Connection unavailable", "#D29922")
            self.reconnect_button.hide()

            print(f"GitHub connection error: {error}")

        except (KeyError, TypeError) as error:
            self.subtitle.setText("GitHub returned an unexpected profile response.")
            print(f"GitHub profile response error: {error}")
