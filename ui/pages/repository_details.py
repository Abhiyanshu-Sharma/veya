from datetime import datetime
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from services.github.repo_summary_service import RepoSummaryService
from services.settings.settings_service import SettingsService
from ui.components.summary_modal import SummaryModal


class ClickableSummaryCard(QFrame):
    clicked = Signal()

    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 8px;
            }
            QFrame:hover {
                border: 1px solid #58A6FF;
            }
            QLabel#summaryTitle {
                font-size: 15px;
                font-weight: bold;
                color: #E6EDF3;
                background: transparent;
                border: none;
            }
            QLabel#summaryDescription {
                font-size: 13px;
                color: #8B949E;
                background: transparent;
                border: none;
            }
        """)

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("summaryTitle")

        description_label = QLabel(description)
        description_label.setObjectName("summaryDescription")
        description_label.setWordWrap(True)

        card_layout.addWidget(title_label)
        card_layout.addWidget(description_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class RepositoryDetailsPage(QWidget):

    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_repo = None
        self.summary_service = RepoSummaryService()
        self.settings_service = SettingsService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.repository_name = QLabel("Repository Name")
        self.repository_name.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #E6EDF3;
        """)

        self.repository_description = QLabel("Repository description")
        self.repository_description.setStyleSheet("""
            font-size: 14px;
            color: #8B949E;
        """)
        self.repository_description.setWordWrap(True)

        self.back_button = QPushButton("←  Repositories")
        self.back_button.clicked.connect(self.back_requested.emit)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #8B949E;
                font-size: 13px;
                text-align: left;
                padding: 0px;
            }

            QPushButton:hover {
                color: #E6EDF3;
            }
        """)

        layout.addWidget(
            self.back_button,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        layout.addWidget(self.repository_name)
        layout.addWidget(self.repository_description)

        self.metadata_container = QFrame()
        self.metadata_container.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 8px;
            }

            QLabel#metadataTitle {
                font-size: 12px;
                color: #8B949E;
                background: transparent;
                border: none;
            }

            QLabel#metadataValue {
                font-size: 14px;
                font-weight: bold;
                color: #E6EDF3;
                background: transparent;
                border: none;
            }
        """)

        self.metadata_layout = QHBoxLayout(self.metadata_container)
        self.metadata_layout.setContentsMargins(16, 12, 16, 12)
        self.metadata_layout.setSpacing(30)

        layout.addWidget(self.metadata_container)
        self.visibility_value = self.create_metadata_item("Visibility", "Loading...")
        self.branch_value = self.create_metadata_item("Default branch", "Loading...")
        self.language_value = self.create_metadata_item("Language", "Loading...")
        self.updated_value = self.create_metadata_item("Last updated", "Loading...")

        # Workspace section
        self.workspace_heading = QLabel("Workspace")
        self.workspace_heading.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #E6EDF3;
        """)
        layout.addWidget(self.workspace_heading)

        self.workspace_layout = QHBoxLayout()
        self.workspace_layout.setSpacing(16)

        self.gui_card = self.create_summary_card(
            "GUI",
            "Open the graphical repository workspace."
        )
        self.cli_card = self.create_summary_card(
            "CLI",
            "Open the command-line repository workspace."
        )

        self.workspace_layout.addWidget(self.gui_card)
        self.workspace_layout.addWidget(self.cli_card)
        layout.addLayout(self.workspace_layout)

        # Repository Summary section
        self.summary_heading = QLabel("Repository Summary")
        self.summary_heading.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #E6EDF3;
        """)
        layout.addWidget(self.summary_heading)

        self.simple_summary_card = ClickableSummaryCard(
            "Simple Summary",
            "A readable overview of what this repository does, "
            "its purpose, and its main components."
        )
        self.simple_summary_card.clicked.connect(self.open_simple_summary)
        layout.addWidget(self.simple_summary_card)

        self.technical_summary_card = self.create_summary_card(
            "Technical Summary",
            "A technical breakdown of the repository's architecture, "
            "modules, dependencies, and code relationships."
        )
        layout.addWidget(self.technical_summary_card)

    def set_repository(self, repo):
        self.current_repo = repo
        self.repository_name.setText(repo["name"])

        description = repo.get("description")
        self.repository_description.setText(
            description if description else "No description provided."
        )

        self.visibility_value.setText(
            "Public" if repo.get("private") is False else "Private"
        )

        self.branch_value.setText(
            repo.get("default_branch") or "Not available"
        )

        self.language_value.setText(
            repo.get("language") or "Not detected"
        )

        updated_at = repo.get("updated_at")
        if updated_at:
            updated_date = datetime.fromisoformat(
                updated_at.replace("Z", "+00:00")
            ).strftime("%d %b %Y")
        else:
            updated_date = "Not available"

        self.updated_value.setText(updated_date)

    def create_metadata_item(self, title, value):
        item_layout = QVBoxLayout()

        title_label = QLabel(title, self.metadata_container)
        value_label = QLabel(value, self.metadata_container)

        title_label.setObjectName("metadataTitle")
        value_label.setObjectName("metadataValue")

        item_layout.addWidget(title_label)
        item_layout.addWidget(value_label)

        self.metadata_layout.addLayout(item_layout)
        return value_label

    def create_summary_card(self, title, description):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 8px;
            }

            QLabel#summaryTitle {
                font-size: 15px;
                font-weight: bold;
                color: #E6EDF3;
                background: transparent;
                border: none;
            }

            QLabel#summaryDescription {
                font-size: 13px;
                color: #8B949E;
                background: transparent;
                border: none;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("summaryTitle")

        description_label = QLabel(description)
        description_label.setObjectName("summaryDescription")
        description_label.setWordWrap(True)

        card_layout.addWidget(title_label)
        card_layout.addWidget(description_label)

        return card

    def open_simple_summary(self):
        if not self.current_repo:
            return
        current_theme = self.settings_service.get("theme", "Dark")
        modal = SummaryModal(
            summary_service=self.summary_service,
            repo=self.current_repo,
            mode="simple",
            theme_name=current_theme,
            parent=self,
        )
        modal.exec()