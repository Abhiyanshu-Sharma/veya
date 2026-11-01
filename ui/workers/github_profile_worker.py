
import requests

from PySide6.QtCore import QThread, Signal

from services.github_user import get_github_user
from services.token_store import get_token


class GitHubProfileWorker(QThread):

    profile_loaded = Signal(dict)
    profile_failed = Signal(str, str)

    def run(self):
        token = get_token()

        if not token:
            self.profile_failed.emit("disconnected", "No GitHub token found.")
            return

        try:
            user = get_github_user(token)
            self.profile_loaded.emit(user)

        except requests.HTTPError as error:
            status_code = (
                error.response.status_code
                if error.response is not None
                else None
            )

            if status_code == 401:
                self.profile_failed.emit(
                    "unauthorized",
                    "Your GitHub session has expired."
                )

            elif status_code == 403:
                self.profile_failed.emit(
                    "forbidden",
                    "GitHub denied the request."
                )

            else:
                self.profile_failed.emit(
                    "http_error",
                    str(error)
                )

        except requests.RequestException as error:
            self.profile_failed.emit(
                "network_error",
                str(error)
            )

        except (KeyError, TypeError) as error:
            self.profile_failed.emit(
                "invalid_response",
                str(error)
            )
