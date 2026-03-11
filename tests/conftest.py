import os
import pytest


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

