
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit)
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices


class GitHubAuthDialog(QDialog):

    cancel_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Connect to GitHub")
        self.setFixedSize(420, 300)

        self.setStyleSheet("""
            QDialog {
                background-color: #0D1117;
                color: #E6EDF3;
            }

            QLabel {
                background-color: transparent;
                color: #E6EDF3;
            }

            QLineEdit {
                background-color: #161B22;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton {
                background-color: #21262D;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #30363D;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel("Connect to GitHub")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        description = QLabel(
            "Enter the code below on GitHub to authorize Veya."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #8B949E; font-size: 13px;")

        self.verification_url = QLabel("https://github.com/login/device")
        self.verification_url.setStyleSheet(
            "color: #58A6FF; font-size: 13px;"
        )

        self.user_code = QLineEdit()
        self.user_code.setReadOnly(True)
        self.user_code.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_code.setPlaceholderText("Waiting for verification code...")

        button_layout = QHBoxLayout()

        self.copy_button = QPushButton("Copy Code")
        self.open_browser_button = QPushButton("Open Browser")
        self.cancel_button = QPushButton("Cancel")

        self.copy_button.clicked.connect(self.copy_code)
        self.open_browser_button.clicked.connect(self.open_browser)
        self.cancel_button.clicked.connect(self.request_cancellation)
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        action_layout.addWidget(self.cancel_button)

        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.open_browser_button)

        self.status_label = QLabel("Preparing GitHub authorization...")
        self.status_label.setStyleSheet(
            "color: #8B949E; font-size: 12px;"
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(4)
        layout.addWidget(self.verification_url)
        layout.addWidget(self.user_code)
        layout.addLayout(button_layout)

        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addLayout(action_layout)

    def request_cancellation(self):
        self.cancel_button.setEnabled(False)
        self.set_auth_status("Cancelling authentication...")
        self.cancel_requested.emit()

    def set_device_code(self, device_data):
        self.verification_url.setText(
            device_data["verification_uri"]
        )
        self.user_code.setText(device_data["user_code"])
        self.status_label.setText(
            "Waiting for authorization on GitHub..."
        )

    def copy_code(self):
        from PySide6.QtWidgets import QApplication

        QApplication.clipboard().setText(self.user_code.text())
        self.status_label.setText("Verification code copied.")

    def open_browser(self):
        url = self.verification_url.text()
        QDesktopServices.openUrl(QUrl(url))

    def set_auth_status(self, message, color="#8B949E"):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            f"color: {color}; font-size: 12px;"
        )


    def closeEvent(self, event):
        if getattr(self, "auth_in_progress", False):
            event.ignore()
        else:
            event.accept()
    