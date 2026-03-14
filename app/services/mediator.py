from openlibrary_api import search_books_by_title,get_work_data
from validate_book_json import validate_book
#from Book import create_book


def main():
    pass


#using .get to avoid key errors.
def complete_book_from_ol(query,):
    #searh by title
    search_results = search_books_by_title(query=query)
    #search fails
    if "error" in search_results:
        return search_results
    #search succeeds, return search results for user to select from
    docs = search_results['docs']
    if 'docs' not in search_results:
        return {"error": "No search results found for the given title."}
        #create_book(json) #should we handle 3.2.2 like this ?
    
    if len(docs) == 0:
        return {"error": "No search results found for the given title."}
    #testing first result
    first_result = docs[0]
    book_title = first_result.get('title')
    first_publish_year = first_result.get('first_publish_year')    
    isbn_list = first_result.get('isbn', [])

    # now works api 
    work_key = first_result.get('key')
    author_olids = []
    if work_key:
        # Get work data from imported function, which will include author OLIDs
        work_data = get_work_data(work_key)
        #check if work_data is a dict and contains "authors" key before trying to access it PS. ALL API CALLS IN OL ARE Dictionaries
        if isinstance(work_data, dict) and "authors" in work_data:
            # Loop through authors in work data and extract OLIDs
            for author in work_data["authors"]:
                #check if "author" key exists and is a dict, and if it contains "key" before trying to access it
                if "author" in author and "key" in author["author"]:
                    # If all checks pass, append the author OLID to the list
                    author_olids.append(author["author"]["key"])

    complete_book_json = {
            "title": book_title,
            "publish_year": first_publish_year,
            "isbn_list": isbn_list,
            "work_key": work_key,
            "author_olids": author_olids,
            "first_publish_year": first_publish_year
        }
    return complete_book_json
            

# POST - Takes JSON as input
def create(json, create_type):
    create_type = create_type.lower() 
    if create_type == 'book':
        #return validate_book(json, create_type)  # the validated JSON will then be called with database INSERT here
        pass
    #work in progress 
    if create_type == "book_ol":
        pass

        
    elif create_type == 'note':
        return 'WIP'
    else:
        return 'Error: Not a valid call'


# GET - Takes JSON as input
def read(json):
    return str(json)


# PATCH - Takes JSON as input
def update(json):
    return str(json)


# DELETE - Takes JSON as input
def delete(json):
    return str(json)

json_test = {'Author_First_Name_1': 'John',
             'Author_Last_Name_1':'Doe',
        'Chapters': 30,
        'Genre_1': 'fiction',
        'ISBN': 1234567890123,
        'Owned': 'yes',
        'Personal_Or_Academic': 'personal',
        'Publisher_Name': 'SomePublisher',
        'Title': 'The Hobbit',
        'Publish_Year': '2026',}


json1 = {"ISBN": 1234567890123,
             "Title": "SomeBook",
             "Publish_Year": "2026",
             "Publisher_ID": "3",
             "Summary": "asdfdasadfsdfsafds",
             "Tag_ID": "4",
             "Chapters": "23",
             "Chapters_Completed": "3",
             "Cover_Image_Bytes": "",
             "AuthorID_1": "1",
             "Author_First_Name_1": "John",
             "Author_Last_Name_1": "Doe",
             "AuthorID_2": "4",
             "Author_First_Name_2": "Jane",
             "Author_Last_Name_2": "Doe",
             "Publisher_Name": "SomePublisher",
             "Owned": "yes",
             "Favorite": "yes",
             "Completed": "no",
             "Currently_Reading": "yes",
             "Personal_Or_Academic": "personal",
             "GenreID_1": "1",
             "Genre_1": "fiction",
             "GenreID_2": "3",
             "Genre_2": "fantasy",
             "GenreID_3": "6",
             "Genre_3": "humor",
             "GenreID_4": "4",
             "Genre_4": "drama"}

if __name__ == '__main__':
    main()