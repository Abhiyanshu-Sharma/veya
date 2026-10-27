import os
from dotenv import load_dotenv

from services.github_auth import request_device_code, poll_for_access_token

from services.token_store import save_token

load_dotenv()


client_id = os.getenv("GITHUB_CLIENT_ID")

if not client_id:
    raise ValueError("GITHUB_CLIENT_ID is missing from .env")

device = request_device_code(client_id)

print("Open:", device["verification_uri"])
print("Enter this code:", device["user_code"])
print("Waiting for GitHub authorization...")

result = poll_for_access_token(
    client_id=client_id,
    device_code=device["device_code"],
    interval=device["interval"],
    expires_in=device["expires_in"],
)

if "access_token" in result:
    save_token(result["access_token"])
    print("Veya has been authorized and the token was saved securely.")

