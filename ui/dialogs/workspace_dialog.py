from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog)
from PySide6.QtCore import Qt

class WorkspaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Workspace")
        self.setFixedSize(450, 220)

        self.workspace_path = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

        title = QLabel("Select Workspace")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        description = QLabel("Choose a folder to use as your Veya workspace.")
        description.setStyleSheet("color: #8B949E;")

        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setPlaceholderText("No workspace selected")

        self.browse_button = QPushButton("Browse")

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.path_input)
        folder_layout.addWidget(self.browse_button)

        self.cancel_button = QPushButton("Cancel")
        self.confirm_button = QPushButton("Select Workspace")
        self.confirm_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.confirm_button)

        self.layout.addWidget(title)
        self.layout.addWidget(description)
        self.layout.addLayout(folder_layout)
        self.layout.addStretch()
        self.layout.addLayout(button_layout)

        self.browse_button.clicked.connect(self.browse_folder)
        self.cancel_button.clicked.connect(self.reject)
        self.confirm_button.clicked.connect(self.accept)

    def browse_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Workspace"
        )

        if folder:
            self.workspace_path = folder
            self.path_input.setText(folder)
            self.confirm_button.setEnabled(True)