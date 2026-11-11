import os
import shlex
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit,)
from PySide6.QtCore import Qt


class CLIPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.workspace_path = None

        self.default_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )

        self.current_directory = self.default_directory

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
            "pwd": self.pwd_command,
            "cd": self.cd_command,
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

        try:
            parts = shlex.split(command, posix=False)
        except ValueError:
            self.output.append("Error: Invalid command syntax.")
            self.command_input.clear()
            return

        command_name = parts[0].lower()
        arguments = parts[1:]

        command_function = self.commands.get(command_name)

        if command_function:
            command_function(arguments)
        else:
            self.output.append(f"Command not found: {command_name}")

        self.command_input.clear()

    
    def help_command(self, arguments=None):

        self.output.append("""
Available commands:

  help    Show available commands
  clear   Clear terminal output
  pwd     Display current working directory
  cd      Change current working directory
""")

    def clear_command(self, arguments=None):
        self.output.clear()

    def pwd_command(self, arguments=None):
        self.output.append(self.current_directory)

    def cd_command(self, arguments=None):

        if not arguments:
            self.current_directory = self.default_directory
            return

        target_path = " ".join(arguments).strip('"')


        if os.path.isabs(target_path):
            new_path = os.path.normpath(target_path)
        else:
            new_path = os.path.normpath(
                os.path.join(self.current_directory, target_path)
            )

        if not os.path.exists(new_path):
            self.output.append(f"Error: Directory not found: {target_path}")
            return

        if not os.path.isdir(new_path):
            self.output.append(f"Error: Not a directory: {target_path}")
            return

        self.current_directory = new_path