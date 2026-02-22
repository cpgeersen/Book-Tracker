# from CRUD_Full_Read import read_book_table

# Uses mock data endpoints until create functions are finished, then it will use the read implementations

MAX_AUTHORS = 2

json_data = {"isbn": "user_provided_isbn",
             "title": "SomeBook",
             "publish_date": "2026",
             "publisher_id": "3",
             "summary": "asdfdasadfsdfsafds",
             "tag_id": "4",
             "chapters": "23",
             "chapters_completed": "3",
             "cover_image_bytes": "",
             "AuthorID_1": "1",
             "Author_First_Name_1": "John",
             "Author_Last_Name_1": "Doe",
             "AuthorID_2": "4",
             "Author_First_Name_2": "Jane",
             "Author_Last_Name_3": "Doe",
             "Publisher_Name": "SomePublisher",
             "Owned": "yes",
             "Favorite": "yes",
             "Completed": "no",
             "Currently_Reading": "yes",
             "PersonalOrAcademic": "personal",
             "GenreID_1": "1",
             "Genre_1": "fiction",
             "GenreID_2": "3",
             "Genre_2": "fantasy",
             "GenreID_3": "6",
             "Genre_3": "humor",
             "GenreID_4": "4",
             "Genre_4": "drama"}

def read_book_record_by_isbn(isbn):
    # Empty dict that will be built upon
    json_result = {}

    # Get the base information from the book table
    # read_book_table_result = read_book_table(isbn)
    read_book_table_result = {"isbn": "1234567890123",
                              "title": "SomeBook",
                              "publish_date": "2026",
                              "publisher_id": "3",
                              "summary": "asdfdasadfsdfsafds",
                              "tag_id": "4",
                              "chapters": "23",
                              "chapters_completed": "3",
                              "cover_image_bytes": ""}

    # Add the base book table keys and values
    json_result.update(read_book_table_result)

    # Next use the BookAuthor table to get the associated AuthorIDs
    # author_ids_for_book = read_author_id(isbn)
    author_ids_for_book = {'AuthorIDs': ['1', '4']}

    # Using the AuthorIDs, get the author first and last names
    # author_names = read_author_name(author_ids_for_book)
    author_names = {'1': ['John', 'Doe'], '4': ['Jane', 'Doe']}

    # Add the AuthorIDs and AuthorNames to result
    if len(author_names) > MAX_AUTHORS:
        print(f'Error: Can only have {MAX_AUTHORS} authors.')
    else:
        author_number = 1
        # For each author add the correct names and IDs
        for key, value in author_names.items():
            json_result[f'AuthorID_{author_number}'] = key
            json_result[f'Author_First_Name_{author_number}'] = value[0]
            json_result[f'Author_Last_Name_{author_number}'] = value[1]
            author_number += 1

    # Next use the Publishers table with PublisherID to get Publisher_Name
    publisher_id = read_book_table_result['publisher_id']
    # json_result['Publisher_Name'] = read_publisher_name(publisher_id)['PublisherID']
    read_publisher_name = {"Publisher_Name": "RandomHouse"}

    # Update json_result with Publisher Name
    json_result.update(read_publisher_name)

    # Next get Tag information from Tag Table using TagID
    tag_id = read_book_table_result['tag_id']
    # tag_values = read_tag_table(tag_id)
    tag_values = {"Owned": "yes",
                      "Favorite": "yes",
                      "Completed": "no",
                      "Currently_Reading": "yes",
                      "PersonalOrAcademic": "personal"}
    # Add Tags to json_result
    json_result.update(tag_values)

    # Next get GenreID using ISBN from BookGenre Table
    #genre_ids = read_genre_ids(isbn)
    genre_ids = {"GenreIDs": ["1", "3", "6", "4"]}

    #genres_book_has = read_genres(genre_ids)
    genres_book_has = {"1": "fiction", "3": "fantasy", "6": "humor", "4": "drama"}

    # Now add the genre_ids and genres to json_result
    genre_number = 1
    for key, value in genres_book_has.items():
        json_result[f'GenreID_{genre_number}'] = key
        json_result[f'Genre_{genre_number}'] = value
        genre_number += 1

    # Final JSON result
    return json_result


if __name__ == '__main__':
    sample_json = read_book_record_by_isbn(1234567890123)
    print(sample_json)
