from read_full_book_by_isbn import read_full_book_by_isbn

# Uses mock data endpoints until create functions are finished, then it will use the read implementations

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

def read_full_book_by_title(title):
    #BLOCK_LIST = []
    # json_result = {}
    # Gives a list of ISBNs that match title search
    # isbn_results = read_isbn_by_title(title) -> JSON
    # for result in isbn_results.values():
    #   json_result.update(read_book_record_by_isbn(result))
    # return json_result
    pass

if __name__ == '__main__':
    pass