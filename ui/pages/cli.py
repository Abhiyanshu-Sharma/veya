import os
import shlex
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit,)
from PySide6.QtCore import Qt, Signal

from services.cli.parser import parse_command
from services.cli.dispatcher import CommandDispatcher

from services.cli.basic.commands import BasicCommands
from services.cli.navigation.commands import NavigationCommands

from services.cli.git.commands import GitCommands

from ui.dialogs.workspace_dialog import WorkspaceDialog

class CommandInput(QLineEdit):

    tab_pressed = Signal()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Tab:
            self.tab_pressed.emit()
            return

        super().keyPressEvent(event)

    def focusNextPrevChild(self, next):
        return False

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
        self.workspace_button.clicked.connect(self.select_workspace)
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
        self.command_input = CommandInput()
        self.command_input.tab_pressed.connect(self.autocomplete)
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
        self.git_commands = GitCommands(self.output, self.navigation)

        # Command registry
        self.commands = {
            "help": self.basic_commands.help,
            "clear": self.basic_commands.clear,
            "pwd": self.navigation.pwd,
            "cd": self.navigation.cd,
            "ls": self.navigation.ls,
            "git status": self.git_commands.status,
            "git add": self.git_commands.add,
            "git restore": self.git_commands.restore,
            "git commit": self.git_commands.commit,
            "git push": self.git_commands.push,
            "git pull": self.git_commands.pull,
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

        elif command_name == "ls":
            if isinstance(result, str):
                self.output.append(result)
            else:
                for item in result:
                    if item.endswith("/"):
                        self.output.append(
                            f'<span style="color: #58A6FF;">{item}</span>'
                        )
                    else:
                        self.output.append(item)
        elif command_name == "git":
            success, message = result

            if success:
                self.output.append(
                    message if message else "Command executed successfully."
                )
            else:
                self.output.append(
                    f"Error: {message}"
                )

        self.command_input.clear()

    def select_workspace(self):

        dialog = WorkspaceDialog(self)

        if dialog.exec():
            self.workspace_path = dialog.workspace_path

            self.navigation.current_directory = self.workspace_path

            self.output.append(f"Workspace selected: {self.workspace_path}")

    def autocomplete(self):

        command = self.command_input.text()
        cursor = self.command_input.cursorPosition()

        try:
            parts = parse_command(command[:cursor])
        except (ValueError, OSError):
            return

        if not parts:
            return

        command_name = parts[0].lower()

        if command_name not in ("cd", "ls", "git"):
            return

        if command_name == "git":
            if len(parts) < 2:
                return

            subcommand = parts[1].lower()

            if subcommand == "add":
                partial = parts[2] if len(parts) > 2 else ""
            elif subcommand == "restore" and len(parts) >= 3 and parts[2] == "--staged":
                partial = parts[3] if len(parts) > 3 else ""
            else:
                return
        else:
            partial = parts[1] if len(parts) > 1 else ""

        search_directory = os.path.dirname(partial)
        search_name = os.path.basename(partial)

        search_path = os.path.join(
            self.navigation.current_directory,
            search_directory
        )

        try:
            matches = [
                item for item in os.listdir(search_path)
                if item.lower().startswith(search_name.lower())
            ]
        except OSError:
            return

        if len(matches) == 1:
            match = matches[0]
            full_path = os.path.join(search_path, match)

            completed = os.path.join(search_directory, match)

            if " " in completed:
                completed = f'"{completed}"'
            elif os.path.isdir(full_path):
                completed += os.sep
                
            self.command_input.setText(
                command[:command.rfind(partial)] + completed
            )

        elif len(matches) > 1:
            self.output.append("  ".join(sorted(matches)))