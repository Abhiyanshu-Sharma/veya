import requests

def request_device_code(client_id):
    url = "https://github.com/login/device/code"

    response = requests.post(
        url,
        data={"client_id": client_id},
        headers={"Accept": "application/json"},
        timeout=15
    )

    response.raise_for_status()
    return response.json()


def poll_for_access_token(client_id, device_code, interval, expires_in, cancel_event=None):
    import time

    url = "https://github.com/login/oauth/access_token"
    deadline = time.monotonic() + expires_in

    while time.monotonic() < deadline:
        if cancel_event and cancel_event.wait(interval):
            raise InterruptedError("Authentication was cancelled.")

        response = requests.post(
            url,
            data={
                "client_id": client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
            headers={"Accept": "application/json"},
            timeout=15,
        )

        if cancel_event and cancel_event.is_set():
            raise InterruptedError("Authentication was cancelled.")

        response.raise_for_status()
        result = response.json()

        if "access_token" in result:
            if cancel_event and cancel_event.is_set():
                raise InterruptedError("Authentication was cancelled.")
            return result

        error = result.get("error")

        if error == "authorization_pending":
            continue

        if error == "slow_down":
            interval += 5
            continue

        if error == "expired_token":
            raise TimeoutError("The device code has expired.")

        if error == "access_denied":
            raise PermissionError("GitHub authorization was denied.")

        raise RuntimeError(f"GitHub authorization failed: {error}")

    raise TimeoutError("The authorization request timed out.")
