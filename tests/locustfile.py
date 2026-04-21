"""
Locust load-test file for the Book-Tracker Flask application.

Run from the repository root after seeding the database and starting the server:

    # 1. Seed database
    python tests/seed_db.py

    # 2. Start the app (in a separate terminal)
    python run.py

    # 3a. Baseline – 10 users, 30 seconds
    locust -f tests/locustfile.py --host=http://127.0.0.1:5000 \
        --users=10 --spawn-rate=2 --run-time=30s --headless \
        --csv=/tmp/load_baseline

    # 3b. Stress – 100 users, 2 minutes
    locust -f tests/locustfile.py --host=http://127.0.0.1:5000 \
        --users=100 --spawn-rate=10 --run-time=2m --headless \
        --csv=/tmp/load_stress

    # 3c. Spike – ramp from 1 to 200 users in 10 seconds, run for 1 minute
    locust -f tests/locustfile.py --host=http://127.0.0.1:5000 \
        --users=200 --spawn-rate=20 --run-time=1m --headless \
        --csv=/tmp/load_spike
"""

import random
import sqlite3

from locust import HttpUser, between, task

# ---------------------------------------------------------------------------
# Helpers – read test data from the database at worker startup
# ---------------------------------------------------------------------------

DB_PATH = "bt.db"

# Sample sets populated once per worker when the first user is instantiated
_ISBNS: list[str] = []
_TITLES: list[str] = []
_AUTHORS: list[tuple[str, str]] = []  # (first_name, last_name)


def _load_test_data() -> None:
    """Populate module-level sample sets from bt.db."""
    global _ISBNS, _TITLES, _AUTHORS
    if _ISBNS:
        return  # already loaded

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT ISBN, Title FROM Books LIMIT 500")
        rows = cursor.fetchall()
        _ISBNS = [r[0] for r in rows]
        _TITLES = list({r[1].split()[0] for r in rows if r[1]})  # first word of each title

        cursor.execute("SELECT Author_First_Name, Author_Last_Name FROM Authors LIMIT 200")
        _AUTHORS = cursor.fetchall()

        conn.close()
    except sqlite3.Error as exc:
        print(f"[locustfile] Warning – could not read bt.db: {exc}")


# ---------------------------------------------------------------------------
# Load-test user
# ---------------------------------------------------------------------------

class BookTrackerUser(HttpUser):
    """
    Simulates a realistic mix of read and write traffic against the app.

    Task weight distribution:
        50 % – local-search  (list all, title, author, isbn variants)
        20 % – homepage / dashboard / analytics
        20 % – individual book page (GET)
        10 % – individual book update (POST summary or tag)
    """

    wait_time = between(0.5, 2)  # seconds between consecutive tasks

    def on_start(self) -> None:
        _load_test_data()

    # ------------------------------------------------------------------
    # Local-search tasks (weight 5 × 1 = 5 out of 10 total)
    # ------------------------------------------------------------------

    @task(2)
    def local_search_all(self) -> None:
        """GET /book/local-search – list all books (no search query)."""
        self.client.get("/book/local-search", name="/book/local-search [all]")

    @task(1)
    def local_search_by_title(self) -> None:
        """GET /book/local-search?search_type=title&search=<word>"""
        word = random.choice(_TITLES) if _TITLES else "The"
        self.client.get(
            f"/book/local-search?search_type=title&search={word}",
            name="/book/local-search [title]",
        )

    @task(1)
    def local_search_by_author(self) -> None:
        """GET /book/local-search?search_type=author&search=<name>"""
        if _AUTHORS:
            first, last = random.choice(_AUTHORS)
            name = f"{first}+{last}"
        else:
            name = "John+Doe"
        self.client.get(
            f"/book/local-search?search_type=author&search={name}",
            name="/book/local-search [author]",
        )

    @task(1)
    def local_search_by_isbn(self) -> None:
        """GET /book/local-search?search_type=isbn&search=<isbn>"""
        isbn = random.choice(_ISBNS) if _ISBNS else "0000000000000"
        self.client.get(
            f"/book/local-search?search_type=isbn&search={isbn}",
            name="/book/local-search [isbn]",
        )

    # ------------------------------------------------------------------
    # Static / navigation pages (weight 2)
    # ------------------------------------------------------------------

    @task(1)
    def homepage(self) -> None:
        """GET /"""
        self.client.get("/", name="/")

    @task(1)
    def dashboard(self) -> None:
        """GET /dashboard and GET /analytics (equal chance)."""
        path = random.choice(["/dashboard", "/analytics"])
        self.client.get(path, name="/dashboard|/analytics")

    # ------------------------------------------------------------------
    # Individual book – read (weight 2)
    # ------------------------------------------------------------------

    @task(2)
    def individual_book_get(self) -> None:
        """GET /book/isbn/<isbn>"""
        if not _ISBNS:
            return
        isbn = random.choice(_ISBNS)
        self.client.get(f"/book/isbn/{isbn}", name="/book/isbn/<isbn> [GET]")

    # ------------------------------------------------------------------
    # Individual book – write (weight 1)
    # ------------------------------------------------------------------

    @task(1)
    def individual_book_post_summary(self) -> None:
        """POST /book/isbn/<isbn> – update summary text."""
        if not _ISBNS:
            return
        isbn = random.choice(_ISBNS)
        self.client.post(
            f"/book/isbn/{isbn}",
            data={"summary": "Load test summary update."},
            name="/book/isbn/<isbn> [POST summary]",
        )

    @task(1)
    def individual_book_post_chapters_completed(self) -> None:
        """POST /book/isbn/<isbn> – update chapters_completed."""
        if not _ISBNS:
            return
        isbn = random.choice(_ISBNS)
        self.client.post(
            f"/book/isbn/{isbn}",
            data={"chapters_completed": str(random.randint(0, 20))},
            name="/book/isbn/<isbn> [POST chapters_completed]",
        )

    # ------------------------------------------------------------------
    # Deduplicate scan (weight 1)
    # ------------------------------------------------------------------

    @task(1)
    def deduplicate_get(self) -> None:
        """GET /book/deduplicate"""
        self.client.get("/book/deduplicate", name="/book/deduplicate [GET]")
