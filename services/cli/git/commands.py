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
                output = result.stdout.strip() or result.stderr.strip()
                return True, output

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

    def restore(self, arguments=None):
        arguments = arguments or []

        if "--staged" not in arguments or len(arguments) < 2:
            return False, "Usage: git restore --staged <file>"

        return self.run_git(["restore"] + arguments)

    def commit(self, arguments=None):
        arguments = arguments or []

        if ("-m" not in arguments and "--message" not in arguments) or len(arguments) < 2:
            return False, 'Usage: git commit -m "message"'

        return self.run_git(["commit"] + arguments)

    def push(self, arguments=None):
        arguments = arguments or []
        return self.run_git(["push"] + arguments)

    def pull(self, arguments=None):
        arguments = arguments or []
        return self.run_git(["pull"] + arguments)

    def get_file_changes(self):
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.navigation.current_directory,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return False, result.stderr.strip()

            staged = []
            unstaged = []

            for line in result.stdout.splitlines():
                if len(line) < 4:
                    continue

                index_status = line[0]
                worktree_status = line[1]
                filepath = line[3:].strip('"')

                if index_status == "?" and worktree_status == "?":
                    unstaged.append(filepath)
                else:
                    if index_status != " ":
                        staged.append(filepath)
                    if worktree_status != " ":
                        unstaged.append(filepath)

            return True, {"staged": staged, "unstaged": unstaged}

        except Exception as error:
            return False, str(error)