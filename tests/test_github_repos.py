
from services.github_repos import get_github_repositories
from services.token_store import get_token


token = get_token()

if not token:
    print("No GitHub token found. Please authorize Veya first.")
else:
    try:
        repositories = get_github_repositories(token)

        print("GitHub repository fetch successful!")
        print("Repositories found:", len(repositories))

        for repo in repositories:
            print(
                f"{repo['name']} | "
                f"Private: {repo['private']} | "
                f"Stars: {repo['stargazers_count']}"
            )

    except Exception as error:
        print("Could not fetch repositories:", error)
