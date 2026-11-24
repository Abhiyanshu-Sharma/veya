import json
import os
import subprocess
from services.token_store import delete_token, get_token, save_token


class SettingsService:
    DEFAULT_SETTINGS = {
        "theme": "Dark",
        "default_workspace": "",
        "startup_page": "Overview",
        "github_token": "",
    }

    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".veya")
        self.config_path = os.path.join(self.config_dir, "settings.json")
        self.settings = self._load_settings()

    def _load_settings(self):
        if not os.path.exists(self.config_path):
            return dict(self.DEFAULT_SETTINGS)

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = dict(self.DEFAULT_SETTINGS)
            merged.update(data)
            return merged
        except (OSError, json.JSONDecodeError):
            return dict(self.DEFAULT_SETTINGS)

    def save_settings(self):
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def reset_defaults(self):
        self.settings = dict(self.DEFAULT_SETTINGS)
        self.save_settings()

    def get_effective_workspace(self):
        saved = self.settings.get("default_workspace", "").strip()
        if saved and os.path.isdir(saved):
            return saved
        return os.getcwd()

    # --- Global Git Config Helpers ---

    def _run_git_config(self, args):
        try:
            result = subprocess.run(
                ["git", "config", "--global"] + args,
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except OSError as e:
            return False, "", str(e)

    def get_git_config(self):
        _, name, _ = self._run_git_config(["--get", "user.name"])
        _, email, _ = self._run_git_config(["--get", "user.email"])
        _, branch, _ = self._run_git_config(["--get", "init.defaultBranch"])
        return {
            "user.name": name,
            "user.email": email,
            "init.defaultBranch": branch or "main",
        }

    def update_git_config(self, name, email, default_branch):
        errors = []
        if name.strip():
            ok, _, err = self._run_git_config(["user.name", name.strip()])
            if not ok:
                errors.append(err or "Failed to set user.name")
        if email.strip():
            ok, _, err = self._run_git_config(["user.email", email.strip()])
            if not ok:
                errors.append(err or "Failed to set user.email")
        if default_branch.strip():
            ok, _, err = self._run_git_config(["init.defaultBranch", default_branch.strip()])
            if not ok:
                errors.append(err or "Failed to set init.defaultBranch")

        return len(errors) == 0, "; ".join(errors)

    def get_github_token(self):
        return get_token() or ""

    def set_github_token(self, token):
        clean = token.strip()
        if clean:
            save_token(clean)
        else:
            self.clear_github_token()

    def clear_github_token(self):
        try:
            delete_token()
        except Exception:
            pass