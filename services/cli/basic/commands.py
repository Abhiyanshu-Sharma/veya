class BasicCommands:

    def __init__(self, output):
        self.output = output

    def help(self, arguments=None):

        self.output.append("""
Available commands:

  help      Show available commands
  clear     Clear terminal output

Navigation:
  pwd       Display current directory
  cd        Change current directory
  ls        List directory contents
  ls -a     Include hidden files
  ls -l     Detailed listing
  ls -la    Detailed listing with hidden files

Git:
  git status    Show working tree status
  git status -s                 Show short working tree status
  git status --short            Show short working tree status
  git add <file>                Stage file or folder changes
  git add .                     Stage all changes
  git restore --staged <file>   Unstage file changes
""")

    def clear(self, arguments=None):
        self.output.clear()
        self.output.setTextColor("#E6EDF3")