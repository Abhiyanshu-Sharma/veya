
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class OverviewHeader(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

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

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
