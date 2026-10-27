from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget)

from ui.components.sidebar import Sidebar
from ui.pages.overview import OverviewPage
from ui.pages.repositories import RepositoriesPage

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

        self.pages = QStackedWidget()

        self.overview_page = OverviewPage()
        self.repositories_page = RepositoriesPage()

        self.overview_page.load_github_profile()

        self.pages.addWidget(self.overview_page)
        self.pages.addWidget(self.repositories_page)

        main_layout.addWidget(self.pages)

        sidebar.overview_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.overview_page)
        )

        sidebar.repositories_btn.clicked.connect(
            self.show_repositories
        )

        central_widget.setStyleSheet("background-color: #0D1117;")

    def show_repositories(self):
        self.repositories_page.load_repositories()
        self.pages.setCurrentWidget(self.repositories_page)