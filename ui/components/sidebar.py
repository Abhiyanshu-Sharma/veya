from PySide6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QStyle)
from PySide6.QtCore import Qt


class Sidebar(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(220)

        self.setStyleSheet("""
            QFrame#sidebar {
                background-color: #161B22;
                border-right: 1px solid #30363D;
            }

            QLabel {
                border: none;
            }

            QPushButton {
                background-color: transparent;
                color: #C9D1D9;
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #21262D;
                border: 1px solid #30363D;
            }

            QPushButton:checked {
                background-color: #21262D;
                color: #E6EDF3;
                border: 1px solid #30363D;
                font-weight: 600;
            }
        """)

        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(8)

        title = QLabel("Veya")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #E6EDF3;
            background-color: transparent;
        """)
        layout.addWidget(title)

        tagline = QLabel("Your GitHub workspace")
        tagline.setStyleSheet("""
            font-size: 11px;
            color: #8B949E;
            background-color: transparent;
        """)
        layout.addWidget(tagline)

        layout.addSpacing(24)

        self.overview_btn = QPushButton("Overview")
        self.overview_btn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.overview_btn.setCheckable(True)
        self.overview_btn.setChecked(True)
        layout.addWidget(self.overview_btn)

        self.repositories_btn = QPushButton("Repositories")
        self.repositories_btn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )
        self.repositories_btn.setCheckable(True)
        layout.addWidget(self.repositories_btn)

        layout.addStretch()

        self.account_btn = QPushButton("Account")
        self.account_btn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)
)
        layout.addWidget(self.account_btn)
