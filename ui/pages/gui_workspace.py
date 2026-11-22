import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QTextEdit, QDialog, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt

from services.cli.navigation.commands import NavigationCommands
from services.cli.git.commands import GitCommands
from ui.dialogs.workspace_dialog import WorkspaceDialog

class FilePickerDialog(QDialog):

    def __init__(self, title, action_label, files, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(420, 320)
        self.setStyleSheet("""
            QDialog {
                background-color: #161B22;
                color: #E6EDF3;
            }
            QLabel {
                color: #E6EDF3;
                font-size: 14px;
                font-weight: 600;
            }
            QListWidget {
                background-color: #0D1117;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 6px;
                font-family: Consolas;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 6px 4px;
            }
            QPushButton {
                background-color: #21262D;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 7px 14px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #30363D;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.addWidget(QLabel(title))
        header.addStretch()

        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        header.addWidget(self.select_all_btn)
        layout.addLayout(header)

        self.list_widget = QListWidget()
        for filepath in files:
            item = QListWidgetItem(filepath)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        footer = QHBoxLayout()
        footer.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        confirm_btn = QPushButton(action_label)
        confirm_btn.clicked.connect(self.accept)

        footer.addWidget(cancel_btn)
        footer.addWidget(confirm_btn)
        layout.addLayout(footer)

    def toggle_select_all(self):
        all_checked = all(
            self.list_widget.item(i).checkState() == Qt.CheckState.Checked
            for i in range(self.list_widget.count())
        )
        new_state = Qt.CheckState.Unchecked if all_checked else Qt.CheckState.Checked
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setCheckState(new_state)
        self.select_all_btn.setText(
            "Select All" if new_state == Qt.CheckState.Unchecked else "Deselect All"
        )

    def selected_files(self):
        return [
            self.list_widget.item(i).text()
            for i in range(self.list_widget.count())
            if self.list_widget.item(i).checkState() == Qt.CheckState.Checked
        ]

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

        # Centered Composer Card
        card_wrapper = QHBoxLayout()
        card_wrapper.addStretch()

        self.composer_card = QFrame()
        self.composer_card.setObjectName("composerCard")
        self.composer_card.setFixedWidth(620)
        self.composer_card.setStyleSheet("""
            QFrame#composerCard {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(self.composer_card)
        card_layout.setContentsMargins(20, 20, 20, 18)
        card_layout.setSpacing(14)

        # Commit message box
        self.commit_input = QTextEdit()
        self.commit_input.setFixedHeight(110)
        self.commit_input.setPlaceholderText("What changes are you committing?")
        self.commit_input.setStyleSheet("""
            QTextEdit {
                background-color: #0D1117;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #58A6FF;
            }
        """)
        card_layout.addWidget(self.commit_input)

        # Staged files preview box
        self.staged_title = QLabel("Attached (Staged) Files: 0")
        self.staged_title.setStyleSheet("color: #8B949E; font-size: 12px; font-weight: 600;")
        card_layout.addWidget(self.staged_title)

        self.staged_box = QFrame()
        self.staged_box.setMinimumHeight(64)
        self.staged_box.setStyleSheet("""
            QFrame {
                background-color: #0D1117;
                border: 1px solid #30363D;
                border-radius: 8px;
            }
        """)
        self.staged_layout = QVBoxLayout(self.staged_box)
        self.staged_layout.setContentsMargins(12, 10, 12, 10)
        self.staged_layout.setSpacing(6)
        card_layout.addWidget(self.staged_box)

        # Bottom action buttons
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(10)

        self.add_files_btn = QPushButton("+ Add Files")
        self.restore_btn = QPushButton("Restore")
        self.commit_btn = QPushButton("Commit")
        self.push_btn = QPushButton("Push")

        for btn in (self.add_files_btn, self.restore_btn, self.commit_btn, self.push_btn):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #21262D;
                    color: #E6EDF3;
                    border: 1px solid #30363D;
                    border-radius: 6px;
                    padding: 8px 14px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #30363D;
                }
            """)

        footer_layout.addWidget(self.add_files_btn)
        footer_layout.addWidget(self.restore_btn)
        footer_layout.addStretch()
        footer_layout.addWidget(self.commit_btn)
        footer_layout.addWidget(self.push_btn)
        card_layout.addLayout(footer_layout)

        card_wrapper.addWidget(self.composer_card)
        card_wrapper.addStretch()
        self.layout.addLayout(card_wrapper)

        self.status_banner = QLabel("")
        self.status_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_banner.setStyleSheet("color: #8B949E; font-size: 13px;")
        self.layout.addWidget(self.status_banner)

        self.layout.addStretch()

        self.staged_files = []
        self.unstaged_files = []
        self.add_files_btn.clicked.connect(self.open_add_dialog)
        self.refresh_status()

    def select_workspace(self):
        dialog = WorkspaceDialog(self)
        if dialog.exec():
            self.workspace_path = dialog.workspace_path
            self.navigation.current_directory = self.workspace_path
            self.workspace_label.setText(f"Current Workspace: {self.workspace_path}")
            self.refresh_status()

    def refresh_status(self):
        success, result = self.git_commands.get_file_changes()
        if not success:
            self.staged_files = []
            self.unstaged_files = []
            self.render_staged_files()
            self.status_banner.setText(result or "Not a Git repository.")
            return

        self.staged_files = result["staged"]
        self.unstaged_files = result["unstaged"]
        self.render_staged_files()

    def render_staged_files(self):
        while self.staged_layout.count():
            item = self.staged_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.staged_title.setText(f"Attached (Staged) Files: {len(self.staged_files)}")
        self.add_files_btn.setText(f"+ Add Files ({len(self.unstaged_files)})")

        if not self.staged_files:
            empty = QLabel("No files staged yet.")
            empty.setStyleSheet("color: #8B949E; font-size: 12px; border: none;")
            self.staged_layout.addWidget(empty)
            return

        for filepath in self.staged_files:
            lbl = QLabel(filepath)
            lbl.setStyleSheet("color: #E6EDF3; font-family: Consolas; font-size: 12px; border: none;")
            self.staged_layout.addWidget(lbl)

    def open_add_dialog(self):
        if not self.unstaged_files:
            self.status_banner.setText("No unstaged files available.")
            return

        dialog = FilePickerDialog(
            "Select Files to Stage",
            "Add Selected",
            self.unstaged_files,
            self
        )
        if dialog.exec():
            files = dialog.selected_files()
            if not files:
                return
            success, output = self.git_commands.add(files)
            self.status_banner.setText(
                f"Staged {len(files)} file(s)." if success else output
            )
            self.refresh_status()