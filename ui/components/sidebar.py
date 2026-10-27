
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class Sidebar(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(220)

        self.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border-right: 1px solid #30363D;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(16, 24, 16, 16)

        title = QLabel("Veya")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #E6EDF3;
        """)
        layout.addWidget(title)

        tagline = QLabel("Your Github workspace")
        tagline.setStyleSheet("""
            font-size: 11px;
            color: #8B949E;
        """)
        layout.addWidget(tagline)

        layout.addSpacing(24)

        self.overview_btn = QPushButton("Overview")
        self.overview_btn.setCheckable(True)
        self.overview_btn.setChecked(True)
        self.overview_btn.setStyleSheet("""
            QPushButton {
                background-color: #21262D;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #292F36;
            }
        """)
        layout.addWidget(self.overview_btn)

        self.repositories_btn = QPushButton("Repositories")
        self.repositories_btn.setCheckable(True)
        self.repositories_btn.setStyleSheet("""
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
        """)
        layout.addWidget(self.repositories_btn)
