from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from services.settings.settings_service import SettingsService
from ui.components.sidebar import Sidebar
from ui.pages.cli import CLIPage
from ui.pages.gui_workspace import GUIWorkspacePage
from ui.pages.overview import OverviewPage
from ui.pages.repositories import RepositoriesPage
from ui.pages.repository_details import RepositoryDetailsPage
from ui.pages.settings import SettingsPage
from ui.theme import build_global_stylesheet


class MainWindow(QMainWindow):

    def __init__(self, github_client_id):
        super().__init__()

        self.github_client_id = github_client_id
        self.settings_service = SettingsService()

        self.setWindowTitle("Veya")
        self.resize(1000, 650)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()

        self.overview_page = OverviewPage(github_client_id)
        self.repositories_page = RepositoriesPage()
        self.repository_details_page = RepositoryDetailsPage()
        self.cli_page = CLIPage()
        self.gui_workspace = GUIWorkspacePage()
        self.settings_page = SettingsPage(self.settings_service)

        self.repository_details_page.back_requested.connect(self.show_repositories)
        self.repositories_page.repository_selected.connect(self.show_repository_details)

        self.overview_page.load_github_profile()

        self.overview_page.gui_requested.connect(
            lambda: self.pages.setCurrentWidget(self.gui_workspace)
        )
        self.overview_page.cli_requested.connect(
            lambda: self.pages.setCurrentWidget(self.cli_workspace if hasattr(self, "cli_workspace") else self.cli_page)
        )

        self.pages.addWidget(self.overview_page)
        self.pages.addWidget(self.repositories_page)
        self.pages.addWidget(self.repository_details_page)
        self.pages.addWidget(self.cli_page)
        self.pages.addWidget(self.gui_workspace)
        self.pages.addWidget(self.settings_page)

        main_layout.addWidget(self.pages)

        self.sidebar.overview_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.overview_page)
        )
        self.sidebar.repositories_btn.clicked.connect(self.show_repositories)
        self.sidebar.settings_btn.clicked.connect(self.show_settings)

        self.settings_page.theme_changed.connect(self.apply_theme)

        # Apply saved theme and startup page
        saved_theme = self.settings_service.get("theme", "Dark")
        self.apply_theme(saved_theme)
        self._open_startup_page()

    def apply_theme(self, theme_name):
        app = QApplication.instance()
        if app:
            app.setStyleSheet(build_global_stylesheet(theme_name))
        self.sidebar.apply_theme(theme_name)

    def _open_startup_page(self):
        startup = self.settings_service.get("startup_page", "Overview")
        if startup == "Repositories":
            self.sidebar.repositories_btn.setChecked(True)
            self.show_repositories()
        elif startup == "GUI Workspace":
            self.pages.setCurrentWidget(self.gui_workspace)
        elif startup == "CLI Workspace":
            self.pages.setCurrentWidget(self.cli_page)
        else:
            self.sidebar.overview_btn.setChecked(True)
            self.pages.setCurrentWidget(self.overview_page)

    def show_repositories(self):
        self.repositories_page.load_repositories()
        self.pages.setCurrentWidget(self.repositories_page)

    def show_repository_details(self, repo):
        self.repository_details_page.set_repository(repo)
        self.pages.setCurrentWidget(self.repository_details_page)

    def show_settings(self):
        self.settings_page.load_values()
        self.pages.setCurrentWidget(self.settings_page)