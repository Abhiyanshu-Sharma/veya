from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class RepositoriesPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        title = QLabel("Your Repositories")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #E6EDF3;
        """)

        layout.addWidget(title)