from app import create_app
from flask import Flask


def test_flask_create_app():
    app = create_app()
    assert isinstance(app, Flask)