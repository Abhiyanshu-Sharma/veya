
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


class GitHubStatus(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)

        self.status_label = QLabel("GitHub: Checking connection...")
        self.status_label.setStyleSheet("""
            color: #8B949E;
            font-size: 12px;
            background-color: transparent;
        """)

        self.reconnect_button = QPushButton("Reconnect")
        self.reconnect_button.setStyleSheet("""
            QPushButton {
                color: #58A6FF;
                background-color: transparent;
                border: none;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                color: #79C0FF;
            }
        """)

        self.reconnect_button.hide()

        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.reconnect_button)

    def set_status(self, message, color):
        self.status_label.setText(f"●  GitHub: {message}")
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-size: 12px;
            background-color: transparent;
        """)
