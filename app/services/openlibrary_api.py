import requests
import json

BASE_URL = "https://openlibrary.org"

def search_books(query, limit=5):
    params = {
        "title": query,
        "limit": limit,
    }
    try:
        response = requests.get(f"{BASE_URL}/search.json", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        return {"error": f"Failed to retrieve data: {err}"}


if __name__ == "__main__":
    query = input("Enter a search query for OpenLibrary: ").strip()
    results = search_books(query)
    print(json.dumps(results, indent=2))