
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from services.github_repos import get_github_repositories
from services.token_store import get_token


class RepositoriesPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        title = QLabel("Your Repositories")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #E6EDF3;
        """)

        self.subtitle = QLabel("Your GitHub projects, all in one place.")
        self.subtitle.setStyleSheet("""
            font-size: 14px;
            color: #8B949E;
        """)

        layout.addWidget(title)
        layout.addWidget(self.subtitle)
        self.repository_list = QVBoxLayout()
        self.repository_list.setSpacing(12)

        self.repository_container = QWidget()
        self.repository_container.setLayout(self.repository_list)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.repository_container)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        layout.addWidget(self.scroll_area)

    def load_repositories(self):
        token = get_token()

        if not token:
            self.subtitle.setText(
                "Connect your GitHub account to view repositories."
            )
            return

        try:
            repositories = get_github_repositories(token)

            self.display_repositories(repositories)

            self.subtitle.setText(
                f"You have {len(repositories)} repositories."
            )

        except Exception:
            self.subtitle.setText(
                "Couldn't load your repositories."
            )

    def display_repositories(self, repositories):
        while self.repository_list.count():
            item = self.repository_list.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        for repo in repositories:
            repo_label = QLabel(repo["name"])
            repo_label.setStyleSheet("""
                padding: 14px;
                font-size: 15px;
                color: #E6EDF3;
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 8px;
            """)

            self.repository_list.addWidget(repo_label)

        self.repository_list.addStretch()