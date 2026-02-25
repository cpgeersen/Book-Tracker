DEFAULT_GENRES = ("Literature", "Nonfiction", "Fiction")


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
