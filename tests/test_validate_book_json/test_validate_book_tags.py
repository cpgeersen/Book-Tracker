
import json

from app.services.validate_json.validate_book_json import validate_tags, validate_book_for_frontend

backend_tags = {"Owned": "yes",
                "Favorite": "yes",
                "Completed": "yes",
                "Currently_Reading": "no"}

frontend_tags = {"Owned": "on",
                "Favorite": "on",
                "Completed": "on",
                "Currently_Reading": "off"}

missing_tags = {}

def test_validate_tags():
    result = validate_tags(frontend_tags)
    assert result['Owned'] == 'yes'
    assert result['Favorite'] == 'yes'
    assert result['Completed'] == 'yes'
    assert result['Currently_Reading'] == 'no'

def test_validate_book_for_frontend_str():
    backend_tags_str = json.dumps(backend_tags)
    result = json.loads(validate_book_for_frontend(backend_tags_str))
    assert result['Owned'] == 'on'
    assert result['Favorite'] == 'on'
    assert result['Completed'] == 'on'
    assert result['Currently_Reading'] == 'off'

def test_validate_book_for_frontend():
    result = json.loads(validate_book_for_frontend(backend_tags))
    assert result['Owned'] == 'on'
    assert result['Favorite'] == 'on'
    assert result['Completed'] == 'on'
    assert result['Currently_Reading'] == 'off'

def test_validate_tags_missing():
    result = validate_tags(missing_tags)
    assert result['Owned'] == 'no'
    assert result['Favorite'] == 'no'
    assert result['Completed'] == 'no'
    assert result['Currently_Reading'] == 'no'
    assert result['Personal_Or_Academic'] == 'personal'