import os
import json

JSON_CACHE_PATH = os.path.join("app", "static", "ol_json_cache.json")

def create_cache():
    os.makedirs(os.path.dirname(JSON_CACHE_PATH), exist_ok=True)

    if not os.path.exists(JSON_CACHE_PATH):
        with open(JSON_CACHE_PATH, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)

    return load_cache()


def load_cache():
    if not os.path.exists(JSON_CACHE_PATH):
        return create_cache()

    try:
        with open(JSON_CACHE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, dict):
                return data
            else:
                return {}
    except (json.JSONDecodeError, FileNotFoundError):
        with open(JSON_CACHE_PATH, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)
        return {}


def save_cache(json_cache):
    with open(JSON_CACHE_PATH, "w", encoding="utf-8") as file:
        json.dump(json_cache, file, indent=4)


def cache(search_query, search_results=None):
    #search_query = search_json["Search_Query"]
    #search_results = search_json["Results"]

    json_cache = load_cache()

    if search_query in json_cache:
        return json_cache[search_query]
    # Prevents an edge case where an empty response could be added to the cache
    elif search_results is not None or len(json_cache[search_query]) != 0:
        json_cache[search_query] = search_results
        save_cache(json_cache)
        return json_cache[search_query]
    else:
        return None # Denotes query not in cache and
                    # nothing should be added to cache


def purge_cache():
    if not os.path.exists(JSON_CACHE_PATH):
        create_cache()
        return {"Success": True, "Message": "Cache created and is empty."}
    else:
        json_cache = {}
        save_cache(json_cache)
        return {"Success": True, "Message": "Cache purged successfully."}