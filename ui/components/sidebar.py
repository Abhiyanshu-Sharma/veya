from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QStyle,
    QVBoxLayout,
)
from ui.theme import get_theme


class Sidebar(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(220)
        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(8)

        self.title = QLabel("Veya")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(self.title)

        self.tagline = QLabel("Your GitHub workspace")
        self.tagline.setStyleSheet("font-size: 11px;")
        layout.addWidget(self.tagline)

        layout.addSpacing(24)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.overview_btn = QPushButton("Overview")
        self.overview_btn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.overview_btn.setCheckable(True)
        self.overview_btn.setChecked(True)
        self.nav_group.addButton(self.overview_btn)
        layout.addWidget(self.overview_btn)

        self.repositories_btn = QPushButton("Repositories")
        self.repositories_btn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )
        self.repositories_btn.setCheckable(True)
        self.nav_group.addButton(self.repositories_btn)
        layout.addWidget(self.repositories_btn)

        layout.addStretch()

        self.account_btn = QPushButton("Account")
        self.account_btn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)
        )
        self.account_btn.setCheckable(True)
        self.nav_group.addButton(self.account_btn)
        layout.addWidget(self.account_btn)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )
        self.settings_btn.setCheckable(True)
        self.nav_group.addButton(self.settings_btn)
        layout.addWidget(self.settings_btn)

    def apply_theme(self, theme_name):
        t = get_theme(theme_name)
        self.title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {t['text_primary']};")
        self.tagline.setStyleSheet(f"font-size: 11px; color: {t['text_secondary']};")