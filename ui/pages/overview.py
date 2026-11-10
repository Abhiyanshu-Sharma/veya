from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, Signal

from services.token_store import delete_token

from ui.components.overview.overview_header import OverviewHeader
from ui.components.overview.workspace_card import WorkspaceCard
from ui.components.overview.recent_projects import RecentProjects
from ui.components.overview.github_status import GitHubStatus

from ui.workers.github_profile_worker import GitHubProfileWorker
from ui.dialogs.github_auth_dialog import GitHubAuthDialog
from ui.workers.github_auth_worker import GitHubAuthWorker


class OverviewPage(QWidget):

    cli_requested = Signal()

    def __init__(self, github_client_id, parent=None):
        super().__init__(parent)

        self.github_client_id = github_client_id
        self.auth_worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header = OverviewHeader()
        self.subtitle = self.header.subtitle

        layout.addWidget(self.header)

        workspace_container = QWidget()
        workspace_container.setFixedHeight(190)

        workspace_layout = QHBoxLayout(workspace_container)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(16)

        gui_card = WorkspaceCard(
            "GUI Workspace",
            "Manage your repositories visually through an intuitive interface.",
            "▣"
        )

        cli_card = WorkspaceCard(
            "CLI Workspace",
            "Work with your repositories directly through a terminal.",
            ">_"
        )

        cli_card.clicked.connect(self.cli_requested.emit)

        workspace_layout.addWidget(gui_card, 1)
        workspace_layout.addWidget(cli_card, 1)

        layout.addWidget(workspace_container)

        layout.addSpacing(4)

        self.recent_projects = RecentProjects()
        layout.addWidget(self.recent_projects, 0, Qt.AlignmentFlag.AlignTop)

        layout.addStretch()

        self.github_status = GitHubStatus()
        self.github_status.reconnect_button.clicked.connect(self.start_github_auth)
        self.github_status.logout_button.clicked.connect(self.logout_github)
        layout.addWidget(self.github_status)

    def set_github_status(self, message, color):
        self.github_status.set_status(message, color)


    def start_github_auth(self):

        if not self.github_client_id:
            self.set_github_status("Configuration error", "#F85149")
            return

        if self.auth_worker is not None and self.auth_worker.isRunning():
            return

        self.auth_dialog = GitHubAuthDialog(self)

        self.auth_worker = GitHubAuthWorker(self.github_client_id, self)

        self.auth_dialog.cancel_requested.connect(self.auth_worker.cancel)

        self.auth_worker.device_code_ready.connect(self.auth_dialog.set_device_code)

        self.auth_worker.authentication_success.connect(self.on_authentication_success)

        self.auth_worker.authentication_failed.connect(self.on_authentication_failed)

        self.auth_worker.authentication_cancelled.connect(self.on_authentication_cancelled)

        self.auth_worker.finished.connect(self.on_authentication_finished)

        self.auth_dialog.auth_in_progress = True
        self.auth_dialog.set_auth_status("Requesting GitHub verification code...")

        self.auth_dialog.show()

        self.auth_worker.start()


    def on_authentication_success(self):

        self.auth_dialog.auth_in_progress = False
        self.auth_dialog.cancel_button.setEnabled(False)
        self.auth_dialog.set_auth_status("GitHub connected successfully!", "#3FB950")

        self.auth_dialog.accept()

        self.load_github_profile()


    def on_authentication_failed(self, message):

        self.auth_dialog.auth_in_progress = False
        self.auth_dialog.cancel_button.setEnabled(False)
        self.auth_dialog.set_auth_status(f"Authentication failed: {message}", "#F85149")


    def on_authentication_finished(self):
        self.auth_dialog.auth_in_progress = False
        self.auth_worker.deleteLater()
        self.auth_worker = None
    
    def load_github_profile(self):

        # Avoid starting another request while one is already running.
        if hasattr(self, "profile_worker") and self.profile_worker.isRunning():
            return

        self.set_github_status("Checking connection...", "#8B949E")
        self.github_status.reconnect_button.hide()

        self.profile_worker = GitHubProfileWorker(self)

        self.profile_worker.profile_loaded.connect(
            self.on_profile_loaded
        )

        self.profile_worker.profile_failed.connect(
            self.on_profile_failed
        )

        self.profile_worker.start()


    def on_profile_loaded(self, user):
        self.set_github_status("Connected", "#3FB950")

        self.github_status.reconnect_button.hide()
        self.github_status.logout_button.show()

        self.subtitle.setText(f"Welcome {user['login']}")   


    def on_profile_failed(self, error_type, message):

        if error_type == "disconnected":
            self.set_github_status("Disconnected", "#F85149")
            self.github_status.reconnect_button.show()
            self.github_status.logout_button.hide()
            self.subtitle.setText(
                "Connect your GitHub account to get started."
            )

        elif error_type == "unauthorized":
            delete_token()

            self.set_github_status("Disconnected", "#F85149")
            self.github_status.reconnect_button.show()
            self.github_status.logout_button.hide()
            self.subtitle.setText(
                "Your GitHub session has expired. Please reconnect."
            )

        elif error_type == "forbidden":
            self.set_github_status("Request denied", "#D29922")
            self.github_status.reconnect_button.hide()
            self.subtitle.setText(
                "GitHub denied the request. Please try again later."
            )

        elif error_type == "network_error":
            self.set_github_status("Connection unavailable", "#D29922")
            self.github_status.reconnect_button.hide()
            self.github_status.logout_button.hide()
            self.subtitle.setText(
                "Couldn't connect to GitHub. Check your internet connection."
            )

        else:
            self.set_github_status("Connection error", "#D29922")
            self.github_status.reconnect_button.hide()
            self.github_status.logout_button.hide()
            self.subtitle.setText(
                "Couldn't load your GitHub profile. Please try again."
            )

        print(f"GitHub profile error [{error_type}]: {message}")

    def on_authentication_cancelled(self):
        self.auth_dialog.auth_in_progress = False
        self.auth_dialog.cancel_button.setEnabled(False)
        self.auth_dialog.close()
    
        self.set_github_status("Disconnected", "#F85149")
        self.github_status.reconnect_button.show()
        self.github_status.logout_button.hide()
    
        self.subtitle.setText("Connect your GitHub account to get started.")

    def logout_github(self):

        reply = QMessageBox.question(
            self,
            "Logout from GitHub",
            "Are you sure you want to disconnect your GitHub account?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            delete_token()

            self.subtitle.setText(
                "Connect your GitHub account to get started."
            )

            self.set_github_status("Disconnected", "#F85149")

            self.github_status.logout_button.hide()
            self.github_status.reconnect_button.show()