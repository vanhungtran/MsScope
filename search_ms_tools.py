import os
import requests

TOKEN = os.environ.get("GITHUB_TOKEN")
QUERY = "mass spectrometry tool in:name,description,topics"
CREATED_FILTER = "created:2025-08-01..*"
SORT = "created"
ORDER = "desc"
PER_PAGE = 20
PAGES = 2

def search(page: int = 1) -> dict:
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{QUERY} {CREATED_FILTER}",
        "sort": SORT,
        "order": ORDER,
        "per_page": PER_PAGE,
        "page": page,
    }
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    for page in range(1, PAGES + 1):
        data = search(page)
        for repo in data.get("items", []):
            topics = ", ".join(repo.get("topics", []))
            print(f"{repo['full_name']}  stars: {repo['stargazers_count']}")
            print(f"  {repo.get('description') or 'no description'}")
            print(f"  {repo['html_url']}")
            if topics:
                print(f"  topics: {topics}")
            print("-" * 60)


if __name__ == "__main__":
    main()
