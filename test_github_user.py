
from services.github_user import get_github_user
from services.token_store import get_token


token = get_token()

if not token:
    print("No GitHub token found. Please authorize Veya first.")
else:
    try:
        user = get_github_user(token)

        print("GitHub connection successful!")
        print("Username:", user["login"])
        print("Name:", user.get("name"))
        print("Public repositories:", user["public_repos"])

    except Exception as error:
        print("Could not fetch GitHub profile:", error)
