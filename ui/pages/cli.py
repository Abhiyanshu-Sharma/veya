import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit,)

from services.cli.parser import parse_command
from services.cli.dispatcher import CommandDispatcher

from services.cli.basic.commands import BasicCommands
from services.cli.navigation.commands import NavigationCommands


class CLIPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.workspace_path = None

        self.default_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )


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

        self.basic_commands = BasicCommands(self.output)
        self.navigation = NavigationCommands(self.default_directory)

        # Command registry
        self.commands = {
            "help": self.basic_commands.help,
            "clear": self.basic_commands.clear,
            "pwd": self.navigation.pwd,
            "cd": self.navigation.cd,
        }

        self.dispatcher = CommandDispatcher(self.commands)

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
            parts = parse_command(command)
        except (ValueError, OSError):
            self.output.append("Error: Invalid command syntax.")
            self.command_input.clear()
            return

        if not parts:
            self.command_input.clear()
            return

        command_found, result = self.dispatcher.execute(parts)

        command_name = parts[0].lower()

        if not command_found:
            self.output.append(
                f"Command not found: {command_name}"
            )

        elif command_name == "pwd":
            self.output.append(result)

        elif command_name == "cd":
            success, message = result

            if not success:
                self.output.append(message)

        self.command_input.clear()