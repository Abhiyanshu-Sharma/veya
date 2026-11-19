import subprocess


class GitCommands:

    def __init__(self, output, navigation):
        self.output = output
        self.navigation = navigation

    def run_git(self, arguments):
        try:
            result = subprocess.run(
                ["git"] + arguments,
                cwd=self.navigation.current_directory,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return True, result.stdout.strip()

            return False, result.stderr.strip()

        except Exception as error:
            return False, str(error)

    def status(self, arguments=None):
        arguments = arguments or []

        if "-s" in arguments or "--short" in arguments:
            arguments = ["status", "--short"]
        else:
            arguments = ["status"]

        return self.run_git(arguments)

    def add(self, arguments=None):
        if not arguments:
            return False, "Usage: git add <file>"

        return self.run_git(["add"] + arguments)