import requests
import json
#from app.services.create_complete_book import is_isbn_in_book_table
from app.services.Book.Book import read_book, is_isbn_present

BASE_URL = "https://openlibrary.org"

#search books by author OLID (author ID in OpenLibrary)
def search_books_by_authorid(author_id, limit=5):
    params = {
        "author": author_id,
        "limit": limit,
    }
    try:
        response = requests.get(f"{BASE_URL}/search.json", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        return {"error": f"Failed to retrieve data: {err}"}
#search books by author name (first name and last name)
def search_books_by_author(first_name, last_name, limit=5):
    params = {
        "author": f"{first_name} {last_name}",
        "limit": limit,
    }
    try:
        response = requests.get(f"{BASE_URL}/search.json", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        return {"error": f"Failed to retrieve data: {err}"}
#search books by ISBN
def search_books_by_isbn(isbn):
    try:
        response = requests.get(f"{BASE_URL}/isbn/{isbn}.json", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        return {
            "error": f"Failed to retrieve data: {err}"
        }
#search books by title
def search_books_by_title(query, limit=5):
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

# helper function to get work data (e.g. description) using the work key from the initial search result
def get_work_data(work_key):
    try:
        url = f"https://openlibrary.org{work_key}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        return {"error": f"Failed to retrieve work data: {err}"}
# helper function to get author info using the author OLID (author ID in OpenLibrary)
def get_author_info_from_authorid(author_olid):
    try:
        response = requests.get(f"{BASE_URL}{author_olid}.json", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        return {"error": f"Failed to retrieve author info: {err}"}
# helper function to check if author OLID is already in database, if so return it
def get_books_from_author_ol(first_name, last_name):
    author_OLID = author_OLID_in_database(first_name, last_name)
    if author_OLID and author_OLID != "None":
        return search_books_by_authorid(author_OLID)
    else:
        return search_books_by_author(first_name, last_name)
        


# OL = OpenLibrary
#get book data from isbn
def get_book_data_from_isbn_OL(isbn):
    try:
        # First call if the ISBN is already in database
        isbn_present_json = is_isbn_present(isbn)

        if not isinstance(isbn_present_json, dict):
            raise ValueError("Database returned invalid format")

        isbn_present = isbn_present_json.get("is_isbn_present", False)

    except Exception as db_error:
        print(f"Warning: DB lookup failed: {db_error}")
        isbn_present = False

    if isbn_present:
        # If ISBN present in DB, return full DB record
        return read_book(isbn)

    else:
        # Send GET request with ISBN to OL API
        ol_data = search_books_by_isbn(isbn)

        # Step 2: If ISBN not present:
        if "error" in ol_data:
            return {
                "error": "ISBN not present in OpenLibrary, please use another ISBN or search via Title"
            }

        # Try to get the work key for additional details needed for author OLIDs, if available. If not, we can still return the basic data from the initial search result, just without author OLIDs.
        # Note: This is because the author OLIDs are nested within the work data, so we need the work key to get them. If no work key is available, we won't be able to get author OLIDs, but we can still return other data like title, publish year, publishers, and ISBNs from the initial search result.
        work_key = None
        work_author_olids = []

        if "works" in ol_data and isinstance(ol_data["works"], list) and len(ol_data["works"]) > 0:
            work_key = ol_data["works"][0].get("key")

        # Fetch work data ONLY to extract author OLIDs
        if work_key:
            work_data = get_work_data(work_key)
            if isinstance(work_data, dict) and "authors" in work_data:
                for a in work_data["authors"]:
                    if "author" in a and "key" in a["author"]:
                        work_author_olids.append(a["author"]["key"])

        #Get information from ol response to return in json later
        title = ol_data.get("title")
        publish_year = ol_data.get("publish_date")
        authors_olids = [a.get("key") for a in ol_data.get("authors", []) if "key" in a]
        publishers = ol_data.get("publishers", [])
        isbn_list = ol_data.get("isbn_10", []) + ol_data.get("isbn_13", [])

        # Step 4: Using received information, return JSON (including OLIDs, will be used later)
        return {
            "title": title,
            "publish_year": publish_year,
            "authors_olids": authors_olids,
            "work_authors_olids": work_author_olids,
            "publishers": publishers,
            "isbn_list": isbn_list,
            "work_key": work_key
        }


if __name__ == "__main__":
    isbn = input("Enter an ISBN to search for: ").strip()
    results = get_book_data_from_isbn_OL(isbn)
    print(json.dumps(results, indent=2))