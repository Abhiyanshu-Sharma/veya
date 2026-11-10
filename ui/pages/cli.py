from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit,)
from PySide6.QtCore import Qt


class CLIPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.workspace_path = None

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(32, 28, 32, 28)
        self.layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Veya")
        title.setStyleSheet("""
            color: #E6EDF3;
            font-size: 20px;
            font-weight: bold;
        """)

        self.workspace_button = QPushButton("Select Workspace")
        self.workspace_button.setStyleSheet("""
            QPushButton {
                background-color: #21262D;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                background-color: #30363D;
            }
        """)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.workspace_button)

        self.layout.addLayout(header_layout)

        # CLI output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #010409;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 8px;
                padding: 12px;
                font-family: Consolas;
                font-size: 13px;
            }
        """)

        self.layout.addWidget(self.output, 1)

        # Command input
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type a command...")
        self.command_input.setStyleSheet("""
            QLineEdit {
                background-color: #161B22;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 10px;
                font-family: Consolas;
                font-size: 13px;
            }
        """)

        self.layout.addWidget(self.command_input)
        self.command_input.returnPressed.connect(self.execute_command)

        # Command registry
        self.commands = {
            "help": self.help_command,
            "clear": self.clear_command,
        }

        # Initial welcome
        self.show_welcome()

    def show_welcome(self):

        self.output.clear()

        welcome_text = """
██╗   ██╗███████╗██╗   ██╗ █████╗
██║   ██║██╔════╝╚██╗ ██╔╝██╔══██╗
██║   ██║█████╗   ╚████╔╝ ███████║
╚██╗ ██╔╝██╔══╝    ╚██╔╝  ██╔══██║
 ╚████╔╝ ███████╗   ██║   ██║  ██║
  ╚═══╝  ╚══════╝   ╚═╝   ╚═╝  ╚═╝

Welcome to Veya CLI
Type 'help' to see available commands.
"""

        self.output.setPlainText(welcome_text)

    
    def execute_command(self):

        command = self.command_input.text().strip()

        if not command:
            return

        self.output.append(f"veya> {command}")

        command_function = self.commands.get(command)

        if command_function:
            command_function()
        else:
            self.output.append(f"Command not found: {command}")

        self.command_input.clear()

    
    def help_command(self):

        self.output.append("""
Available commands:

  help    Show available commands
  clear   Clear terminal output
""")

    def clear_command(self):

        self.output.clear()
