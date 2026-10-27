
import requests


def get_github_repositories(token):
    url = "https://api.github.com/user/repos"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        params={
            "sort": "updated",
            "per_page": 100,
            "type": "owner",
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json()
