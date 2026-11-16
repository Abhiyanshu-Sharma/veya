import os
from datetime import datetime

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

    def ls(self, arguments=None):

        arguments = arguments or []

        flags = "".join(
            arg[1:] for arg in arguments if arg.startswith("-")
        )

        show_hidden = "a" in flags
        detailed = "l" in flags
        try:
            items = os.listdir(self.current_directory)

            if not show_hidden:
                items = [
                    item for item in items
                    if not item.startswith(".")
                ]

            directories = []
            files = []

            for item in items:
                item_path = os.path.join(self.current_directory, item)

                if os.path.isdir(item_path):
                    directories.append(item)
                else:
                    files.append(item)

            items = (
                sorted(directories, key=str.lower)
                + sorted(files, key=str.lower)
            )

            if not detailed:
                return [
                    item + "/" if os.path.isdir(
                        os.path.join(self.current_directory, item)
                    ) else item
                    for item in items
                ]

            results = []

            for item in items:
                item_path = os.path.join(self.current_directory, item)
                stats = os.stat(item_path)

                item_type = "DIR" if os.path.isdir(item_path) else "FILE"
                size = stats.st_size
                modified = datetime.fromtimestamp(
                    stats.st_mtime
                ).strftime("%Y-%m-%d %H:%M")

                results.append(
                    f"{item_type:<6} {size:>12} "
                    f"{modified}  {item}"
                )

            return results

        except OSError as error:
            return f"Error: {error}"