# This file is simply an external function that is referenced when the create book entry function runs.
# This file should insert 3 standard genres into the book Genre table. 

DEFAULT_GENRES = ("literature", "nonfiction", "fiction")


def seed_default_genres(cursor):
    for genre_name in DEFAULT_GENRES:
        cursor.execute(
            '''
            INSERT INTO Genre (GENRE)
            SELECT ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM Genre
                WHERE LOWER(TRIM(GENRE)) = LOWER(TRIM(?))
            )
            ''',
            (genre_name, genre_name)
        )
