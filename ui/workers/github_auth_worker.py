
import requests

from PySide6.QtCore import QThread, Signal

from services.github_auth import (
    request_device_code,
    poll_for_access_token
)
from services.token_store import save_token


class GitHubAuthWorker(QThread):

    device_code_ready = Signal(dict)
    authentication_success = Signal()
    authentication_failed = Signal(str)

    def __init__(self, client_id, parent=None):
        super().__init__(parent)
        self.client_id = client_id

    def run(self):
        try:
            device_data = request_device_code(self.client_id)

            self.device_code_ready.emit(device_data)

            result = poll_for_access_token(
                self.client_id,
                device_data["device_code"],
                device_data["interval"],
                device_data["expires_in"]
            )

            save_token(result["access_token"])

            self.authentication_success.emit()

        except requests.RequestException:
            self.authentication_failed.emit(
                "Unable to communicate with GitHub. Check your internet connection."
            )

        except TimeoutError as error:
            self.authentication_failed.emit(str(error))

        except PermissionError as error:
            self.authentication_failed.emit(str(error))

        except (KeyError, TypeError):
            self.authentication_failed.emit(
                "GitHub returned an unexpected response."
            )

        except Exception as error:
            self.authentication_failed.emit(
                f"Authentication failed: {error}"
            )
