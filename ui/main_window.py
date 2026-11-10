from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget)

from ui.components.sidebar import Sidebar
from ui.pages.overview import OverviewPage
from ui.pages.repositories import RepositoriesPage
from ui.pages.repository_details import RepositoryDetailsPage

from ui.pages.cli import CLIPage

class MainWindow(QMainWindow):
    
    def __init__(self, github_client_id):
        super().__init__()

        self.github_client_id = github_client_id

        self.setWindowTitle("Veya")
        self.resize(1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        sidebar = Sidebar()
        main_layout.addWidget(sidebar)

        self.pages = QStackedWidget()

        self.overview_page = OverviewPage(github_client_id)
        self.repositories_page = RepositoriesPage()
        self.repository_details_page = RepositoryDetailsPage()
        self.cli_page = CLIPage()
        
        self.repository_details_page.back_requested.connect(self.show_repositories)
        self.repositories_page.repository_selected.connect(self.show_repository_details)

        self.overview_page.load_github_profile()

        self.overview_page.cli_requested.connect(
            lambda: self.pages.setCurrentWidget(self.cli_page)
        )

        self.pages.addWidget(self.overview_page)
        self.pages.addWidget(self.repositories_page)
        self.pages.addWidget(self.repository_details_page)
        self.pages.addWidget(self.cli_page)

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

    def show_repository_details(self, repo):
        self.repository_details_page.set_repository(repo)
        self.pages.setCurrentWidget(self.repository_details_page)
