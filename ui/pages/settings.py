import os
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget)
from ui.theme import THEMES, get_theme


class SettingsPage(QWidget):
    theme_changed = Signal(str)

    def __init__(self, settings_service, parent=None):
        super().__init__(parent)
        self.settings_service = settings_service
        self._build_ui()
        self.load_values()

    def _create_card(self, title_text, subtitle_text=None):
        card = QFrame()
        card.setObjectName("settingsCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        title = QLabel(title_text)
        title.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(title)

        if subtitle_text:
            subtitle = QLabel(subtitle_text)
            subtitle.setWordWrap(True)
            subtitle.setObjectName("mutedLabel")
            layout.addWidget(subtitle)

        return card, layout

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer_layout.addWidget(scroll)

        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(32, 28, 32, 32)
        self.main_layout.setSpacing(20)
        scroll.setWidget(container)

        # Page Header
        header = QLabel("Settings")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(header)

        sub_header = QLabel("Customize Veya's appearance, workspace defaults, Git identity, and GitHub API access.")
        sub_header.setObjectName("mutedLabel")
        self.main_layout.addWidget(sub_header)

        # 1. Appearance Card
        appearance_card, appearance_layout = self._create_card(
            "Appearance",
            "Choose a color theme for Veya. Changes apply immediately.",
        )
        theme_row = QHBoxLayout()
        theme_label = QLabel("Color Theme")
        theme_label.setFixedWidth(180)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))
        self.theme_combo.currentTextChanged.connect(self._on_theme_selected)
        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo, 1)
        appearance_layout.addLayout(theme_row)
        self.main_layout.addWidget(appearance_card)

        # 2. Workspace & Startup Card
        workspace_card, workspace_layout = self._create_card(
            "Workspace & Startup",
            "Set your default project folder and initial view when opening Veya.",
        )

        ws_row = QHBoxLayout()
        ws_label = QLabel("Default Workspace")
        ws_label.setFixedWidth(180)
        self.workspace_input = QLineEdit()
        self.workspace_input.setPlaceholderText(os.getcwd())
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self._browse_workspace)
        reset_ws_btn = QPushButton("Reset")
        reset_ws_btn.clicked.connect(self._reset_workspace)
        ws_row.addWidget(ws_label)
        ws_row.addWidget(self.workspace_input, 1)
        ws_row.addWidget(browse_btn)
        ws_row.addWidget(reset_ws_btn)
        workspace_layout.addLayout(ws_row)

        startup_row = QHBoxLayout()
        startup_label = QLabel("Startup Page")
        startup_label.setFixedWidth(180)
        self.startup_combo = QComboBox()
        self.startup_combo.addItems(["Overview", "Repositories", "GUI Workspace", "CLI Workspace"])
        startup_row.addWidget(startup_label)
        startup_row.addWidget(self.startup_combo, 1)
        workspace_layout.addLayout(startup_row)

        ws_actions = QHBoxLayout()
        ws_actions.addStretch()
        save_ws_btn = QPushButton("Save Workspace Preferences")
        save_ws_btn.setObjectName("primaryBtn")
        save_ws_btn.clicked.connect(self._save_workspace_prefs)
        ws_actions.addWidget(save_ws_btn)
        workspace_layout.addLayout(ws_actions)

        self.main_layout.addWidget(workspace_card)

        # 3. Global Git Identity Card
        git_card, git_layout = self._create_card(
            "Git Identity (Global Config)",
            "Synced directly with your system's global Git configuration.",
        )

        name_row = QHBoxLayout()
        name_label = QLabel("Author Name (user.name)")
        name_label.setFixedWidth(180)
        self.git_name_input = QLineEdit()
        self.git_name_input.setPlaceholderText("Your Name")
        name_row.addWidget(name_label)
        name_row.addWidget(self.git_name_input, 1)
        git_layout.addLayout(name_row)

        email_row = QHBoxLayout()
        email_label = QLabel("Author Email (user.email)")
        email_label.setFixedWidth(180)
        self.git_email_input = QLineEdit()
        self.git_email_input.setPlaceholderText("you@example.com")
        email_row.addWidget(email_label)
        email_row.addWidget(self.git_email_input, 1)
        git_layout.addLayout(email_row)

        branch_row = QHBoxLayout()
        branch_label = QLabel("Default Branch")
        branch_label.setFixedWidth(180)
        self.git_branch_input = QLineEdit()
        self.git_branch_input.setPlaceholderText("main")
        branch_row.addWidget(branch_label)
        branch_row.addWidget(self.git_branch_input, 1)
        git_layout.addLayout(branch_row)

        git_actions = QHBoxLayout()
        git_actions.addStretch()
        save_git_btn = QPushButton("Update Global Git Config")
        save_git_btn.setObjectName("primaryBtn")
        save_git_btn.clicked.connect(self._save_git_config)
        git_actions.addWidget(save_git_btn)
        git_layout.addLayout(git_actions)

        self.main_layout.addWidget(git_card)

        # 4. GitHub Connection Card
        gh_card, gh_layout = self._create_card(
            "GitHub API Connection",
            "Optional Personal Access Token (PAT) for higher rate limits and private repository inspection.",
        )

        token_row = QHBoxLayout()
        token_label = QLabel("Personal Access Token")
        token_label.setFixedWidth(180)
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setPlaceholderText("ghp_xxxxxxxxxxxxxxxxxxxx")

        self.toggle_token_btn = QPushButton("Show")
        self.toggle_token_btn.setCheckable(True)
        self.toggle_token_btn.toggled.connect(self._toggle_token_visibility)

        clear_token_btn = QPushButton("Clear")
        clear_token_btn.clicked.connect(self._clear_token)

        token_row.addWidget(token_label)
        token_row.addWidget(self.token_input, 1)
        token_row.addWidget(self.toggle_token_btn)
        token_row.addWidget(clear_token_btn)
        gh_layout.addLayout(token_row)

        gh_actions = QHBoxLayout()
        self.token_status_label = QLabel("")
        self.token_status_label.setObjectName("mutedLabel")
        gh_actions.addWidget(self.token_status_label)
        gh_actions.addStretch()
        save_token_btn = QPushButton("Save Token")
        save_token_btn.setObjectName("primaryBtn")
        save_token_btn.clicked.connect(self._save_token)
        gh_actions.addWidget(save_token_btn)
        gh_layout.addLayout(gh_actions)

        self.main_layout.addWidget(gh_card)

        # 5. About Card
        about_card, about_layout = self._create_card("About Veya")
        version_label = QLabel("Version: v1.0.0")
        version_label.setObjectName("mutedLabel")
        about_layout.addWidget(version_label)

        reset_all_row = QHBoxLayout()
        reset_all_row.addStretch()
        reset_all_btn = QPushButton("Reset All Settings to Default")
        reset_all_btn.clicked.connect(self._reset_all_settings)
        reset_all_row.addWidget(reset_all_btn)
        about_layout.addLayout(reset_all_row)

        self.main_layout.addWidget(about_card)
        self.main_layout.addStretch()

        self.apply_theme_styles(self.settings_service.get("theme", "Dark"))

    def apply_theme_styles(self, theme_name):
        t = get_theme(theme_name)
        for lbl in self.findChildren(QLabel):
            if lbl.objectName() == "mutedLabel":
                lbl.setStyleSheet(f"color: {t['text_secondary']}; font-size: 13px;")

    def load_values(self):
        # Appearance
        current_theme = self.settings_service.get("theme", "Dark")
        self.theme_combo.blockSignals(True)
        idx = self.theme_combo.findText(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.blockSignals(False)

        # Workspace & Startup
        self.workspace_input.setText(self.settings_service.get("default_workspace", ""))
        startup_page = self.settings_service.get("startup_page", "Overview")
        s_idx = self.startup_combo.findText(startup_page)
        if s_idx >= 0:
            self.startup_combo.setCurrentIndex(s_idx)

        # Git Config
        git_cfg = self.settings_service.get_git_config()
        self.git_name_input.setText(git_cfg["user.name"])
        self.git_email_input.setText(git_cfg["user.email"])
        self.git_branch_input.setText(git_cfg["init.defaultBranch"])

        # GitHub Token (from keyring)
        token = self.settings_service.get_github_token()
        self.token_input.setText(token)
        self.token_status_label.setText(
            "Status: Connected (saved in keyring)" if token else "Status: Not connected"
        )

    def _on_theme_selected(self, theme_name):
        self.settings_service.set("theme", theme_name)
        self.apply_theme_styles(theme_name)
        self.theme_changed.emit(theme_name)

    def _browse_workspace(self):
        start_dir = self.workspace_input.text().strip() or os.getcwd()
        folder = QFileDialog.getExistingDirectory(self, "Select Default Workspace", start_dir)
        if folder:
            self.workspace_input.setText(folder)

    def _reset_workspace(self):
        self.workspace_input.clear()

    def _save_workspace_prefs(self):
        ws_path = self.workspace_input.text().strip()
        if ws_path and not os.path.isdir(ws_path):
            QMessageBox.warning(self, "Invalid Directory", "The selected workspace folder does not exist.")
            return
        self.settings_service.set("default_workspace", ws_path)
        self.settings_service.set("startup_page", self.startup_combo.currentText())
        QMessageBox.information(self, "Saved", "Workspace and startup preferences saved.")

    def _save_git_config(self):
        ok, err = self.settings_service.update_git_config(
            self.git_name_input.text(),
            self.git_email_input.text(),
            self.git_branch_input.text(),
        )
        if ok:
            QMessageBox.information(self, "Git Updated", "Global Git configuration updated.")
        else:
            QMessageBox.warning(self, "Git Error", f"Could not update Git config:\n{err}")

    def _toggle_token_visibility(self, checked):
        if checked:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_token_btn.setText("Hide")
        else:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_token_btn.setText("Show")

    def _save_token(self):
        token = self.token_input.text().strip()
        self.settings_service.set_github_token(token)
        self.token_status_label.setText(
            "Status: Connected (saved in keyring)" if token else "Status: Not connected"
        )
        QMessageBox.information(self, "Saved", "GitHub token updated in keyring.")

    def _clear_token(self):
        self.token_input.clear()
        self.settings_service.clear_github_token()
        self.token_status_label.setText("Status: Not connected")

    def _reset_all_settings(self):
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Reset all Veya settings (theme, workspace, startup page, and token) to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.settings_service.reset_defaults()
            self.load_values()
            default_theme = self.settings_service.get("theme", "Dark")
            self.apply_theme_styles(default_theme)
            self.theme_changed.emit(default_theme)