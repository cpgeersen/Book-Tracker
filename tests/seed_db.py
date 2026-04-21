"""
Seed the Book-Tracker database with synthetic records for load testing.

Usage (from repository root):
    python tests/seed_db.py [--records N]

Defaults to 500 records. Existing bt.db is removed so each run starts fresh.
"""
import argparse
import os
import sys

# Ensure the repo root is on the path so app imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = "bt.db"


def main():
    parser = argparse.ArgumentParser(description="Seed bt.db for load testing.")
    parser.add_argument("--records", type=int, default=500,
                        help="Number of synthetic book records to insert (default: 500)")
    args = parser.parse_args()

    # Remove any existing database so we start clean
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing {DB_PATH}")

    # Re-create the schema
    from app.services.create_db import create_db
    create_db()

    # Seed with synthetic records
    from app.services.mocking.create_many_records import create_many_records
    print(f"Inserting {args.records} synthetic book records…")
    create_many_records(args.records)
    print("Seeding complete.")


if __name__ == "__main__":
    main()
