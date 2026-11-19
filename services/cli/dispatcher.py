
class CommandDispatcher:

    def __init__(self, commands):
        self.commands = commands

    def execute(self, parts):

        if not parts:
            return False, None

        command_name = parts[0].lower()
        arguments = parts[1:]

        if len(parts) >= 2:
            grouped_command = f"{parts[0].lower()} {parts[1].lower()}"

            if grouped_command in self.commands:
                command_name = grouped_command
                arguments = parts[2:]

        command_function = self.commands.get(command_name)

        if command_function:
            result = command_function(arguments)
            return True, result

        return False, None