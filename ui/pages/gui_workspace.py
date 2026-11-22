import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

from services.cli.navigation.commands import NavigationCommands
from services.cli.git.commands import GitCommands
from ui.dialogs.workspace_dialog import WorkspaceDialog


class GUIWorkspacePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.workspace_path = None
        self.default_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )

        self.navigation = NavigationCommands(self.default_directory)
        self.git_commands = GitCommands(None, self.navigation)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(32, 28, 32, 28)
        self.layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("GUI Workspace")
        title.setStyleSheet("color: #E6EDF3; font-size: 20px; font-weight: bold;")

        self.workspace_btn = QPushButton("Select Workspace")
        self.workspace_btn.clicked.connect(self.select_workspace)
        self.workspace_btn.setStyleSheet("""
            QPushButton {
                background-color: #21262D;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #30363D;
            }
        """)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.workspace_btn)

        self.layout.addLayout(header_layout)

        self.workspace_label = QLabel(f"Current Workspace: {self.default_directory}")
        self.workspace_label.setStyleSheet("color: #8B949E; font-size: 13px;")
        self.layout.addWidget(self.workspace_label)

        self.layout.addStretch()

    def select_workspace(self):
        dialog = WorkspaceDialog(self)
        if dialog.exec():
            self.workspace_path = dialog.workspace_path
            self.navigation.current_directory = self.workspace_path
            self.workspace_label.setText(f"Current Workspace: {self.workspace_path}")