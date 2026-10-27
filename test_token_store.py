
# from services.token_store import get_token

# token = get_token()

# print("Token exists:", token is not None)
# print("Token length:", len(token) if token else 0)
# print("Token has surrounding whitespace:", token != token.strip() if token else False)


import requests
from services.token_store import get_token

token = get_token()

if not token:
    print("No token found.")
else:
    response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )

    print("HTTP status:", response.status_code)
    print("GitHub request ID:", response.headers.get("X-GitHub-Request-Id"))

    if response.status_code != 200:
        print("GitHub error:", response.json().get("message", "Unknown error"))
    else:
        user = response.json()
        print("Username:", user["login"])
        print("Name:", user.get("name"))
        print("Public repositories:", user["public_repos"])
