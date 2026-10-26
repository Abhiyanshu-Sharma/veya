from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame,)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Veya")
        self.resize(1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
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
        main_layout.addWidget(content_widget)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        sidebar.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border-right: 1px solid #30363D;
            }
        """)

        layout = QVBoxLayout(sidebar)
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

        overview_btn = QPushButton("Overview")
        overview_btn.setStyleSheet("""
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
        overview_btn.setCheckable(True)
        overview_btn.setChecked(True)

        layout.addWidget(overview_btn)

        repositories_btn = QPushButton("Repositories")
        repositories_btn.setCheckable(True)
        
        repositories_btn.setStyleSheet("""
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

        layout.addWidget(repositories_btn)

        return sidebar
        