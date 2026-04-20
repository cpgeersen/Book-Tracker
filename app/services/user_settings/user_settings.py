import os
import json

JSON_CACHE_PATH = os.path.join("app", "static", "user_settings.json")

def create_user_settings_json():
    os.makedirs(os.path.dirname(JSON_CACHE_PATH), exist_ok=True)

    if not os.path.exists(JSON_CACHE_PATH):
        with open(JSON_CACHE_PATH, "w", encoding="utf-8") as file:
            json.dump({'Username': 'Default_User', 'Theme': 'Dark Mode'}, file, indent=4)

    return load_user_settings()


def load_user_settings():
    if not os.path.exists(JSON_CACHE_PATH):
        return create_user_settings_json()

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

def update_user_settings(user_name, theme):
    with open(JSON_CACHE_PATH, "w", encoding="utf-8") as file:
        json.dump({'Username': user_name, 'Theme': theme}, file, indent=4)
    return {'Success': 'User Settings Updated'}






