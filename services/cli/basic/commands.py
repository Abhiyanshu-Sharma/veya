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
""")

    def clear(self, arguments=None):
        self.output.clear()
        self.output.setTextColor("#E6EDF3")