from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame,)
from PySide6.QtCore import Qt

from ui.components.sidebar import Sidebar
from ui.pages.overview import OverviewPage

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Veya")
        self.resize(1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        sidebar = Sidebar()
        main_layout.addWidget(sidebar)

        self.overview_page = OverviewPage()
        self.overview_page.load_github_profile()

        central_widget.setStyleSheet("background-color: #0D1117;")

        main_layout.addWidget(self.overview_page)
        