import requests

def get_github_user(token):
    url = "https://api.github.com/user"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json()