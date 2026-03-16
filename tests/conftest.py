import os
import pytest
from app import create_app

def delete_database():
    try:
        os.remove('bt.db')
    except OSError:
        pass

@pytest.fixture(autouse=True)
def reset_database():
    delete_database()
    import app.services.create_db
    app.services.create_db()
    yield
    delete_database()


@pytest.fixture(autouse=True)
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    delete_database()
    yield app
    delete_database()

@pytest.fixture()
def client(app):
    return app.test_client()