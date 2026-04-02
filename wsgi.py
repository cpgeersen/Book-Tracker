from app import create_app
from app.services.create_db import create_db

create_db()
app = create_app()

if __name__ == '__main__':
    app.run()
