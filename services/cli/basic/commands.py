class BasicCommands:

    def __init__(self, output):
        self.output = output

    def help(self, arguments=None):

        self.output.append("""
Available commands:

  help    Show available commands
  clear   Clear terminal output
  pwd     Display current working directory
  cd      Change current working directory
""")

    def clear(self, arguments=None):
        self.output.clear()