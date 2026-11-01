import requests
import threading

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
    authentication_cancelled = Signal()

    def __init__(self, client_id, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self._cancel_event = threading.Event()
        self._cancel_lock = threading.Lock()

    def cancel(self):
        with self._cancel_lock:
            self._cancel_event.set()


    def run(self):
        try:
            if self._cancel_event.is_set():
                self.authentication_cancelled.emit()
                return

            device_data = request_device_code(self.client_id)

            if self._cancel_event.is_set():
                self.authentication_cancelled.emit()
                return

            self.device_code_ready.emit(device_data)

            result = poll_for_access_token(
                self.client_id,
                device_data["device_code"],
                device_data["interval"],
                device_data["expires_in"],
                cancel_event=self._cancel_event
            )

            with self._cancel_lock:
                if self._cancel_event.is_set():
                    self.authentication_cancelled.emit()
                    return

                save_token(result["access_token"])

            self.authentication_success.emit()

        except InterruptedError:
            self.authentication_cancelled.emit()

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