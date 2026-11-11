
class CommandDispatcher:

    def __init__(self, commands):
        self.commands = commands

    def execute(self, parts):

        if not parts:
            return False, None

        command_name = parts[0].lower()
        arguments = parts[1:]

        command_function = self.commands.get(command_name)

        if command_function:
            result = command_function(arguments)
            return True, result

        return False, None
