
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy


class RecentProjects(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        recent_title = QLabel("Recently working on")
        recent_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #E6EDF3;
            background-color: transparent;
        """)

        layout.addWidget(recent_title)

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

        self.empty_label = QLabel(
            "Your recently opened repositories will appear here."
        )

        self.empty_label.setStyleSheet("""
            color: #8B949E;
            font-size: 13px;
            background-color: transparent;
            border: none;
        """)

        self.recent_layout.addWidget(self.empty_label)
        layout.addWidget(self.recent_container)