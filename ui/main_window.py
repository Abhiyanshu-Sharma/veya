from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Veya")
        self.resize(1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Veya")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 36px;"
            "font-weight: bold;"
            "color: #E6EDF3;"
        )

        subtitle = QLabel("Your GitHub workspace, your rules.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #8B949E;
        """)

        central_widget.setStyleSheet("background-color: #0D1117;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
    