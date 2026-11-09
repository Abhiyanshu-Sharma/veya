from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

class RepositoryDetailsPage(QWidget):

    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

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

        self.back_button = QPushButton("← Back to Repositories")
        self.back_button.clicked.connect(self.back_requested.emit)

        layout.addWidget(self.back_button)

        layout.addWidget(self.repository_name)
        layout.addWidget(self.repository_description)

    def set_repository(self, repo):
        self.repository_name.setText(repo["name"])
    
        description = repo.get("description")
        self.repository_description.setText(
            description if description else "No description provided."
        )