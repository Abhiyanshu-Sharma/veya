import os

class NavigationCommands:

    def __init__(self, default_directory):
        self.default_directory = default_directory
        self.current_directory = default_directory

    def pwd(self, arguments=None):
        return self.current_directory

    def cd(self, arguments=None):

        if not arguments:
            self.current_directory = self.default_directory
            return True, None

        if len(arguments) > 1:
            return False, "Error: cd accepts only one path."

        target_path = arguments[0]

        if os.path.isabs(target_path):
            new_path = os.path.normpath(target_path)
        else:
            new_path = os.path.normpath(
                os.path.join(self.current_directory, target_path)
            )

        if not os.path.exists(new_path):
            return False, f"Error: Directory not found: {target_path}"

        if not os.path.isdir(new_path):
            return False, f"Error: Not a directory: {target_path}"

        self.current_directory = new_path
        return True, None
