import sqlite3

def test_create_database_table_schema():
    # Assert all the tables are present
    assert check_table('Books') == True
    assert check_table('BookAuthor') == True
    assert check_table('Authors') == True
    assert check_table('Publishers') == True
    assert check_table('BookNotes') == True
    assert check_table('Notes') == True
    assert check_table('Tags') == True
    assert check_table('BookGenre') == True
    assert check_table('Genre') == True


def check_table(table_name):
    # Connect to the database
    conn = sqlite3.connect("bt.db")
    cursor = conn.cursor()

    # Query the database for a specific table
    query = '''SELECT name FROM sqlite_master WHERE type='table' AND name= ?;'''
    criteria = (table_name,)
    cursor.execute(query, criteria)

    result = cursor.fetchone()
    conn.close()

    if result:
        return True
    else:
        return False






