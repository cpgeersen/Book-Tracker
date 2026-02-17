from app.services.validate_book_json import validate_book


# POST - Takes JSON as input
def create(json,create_type):
    create_type = create_type.lower()
    if create_type == 'book':
        return validate_book(json,create_type) # the validated JSON will then be called with database INSERT here
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

json_test = {'author': 'John Doe',
        'author2': '',
        'chapters': 30,
        'fiction-or-nonfiction': 'fiction',
        'isbn': 1234567890123,
        'owned': 'on',
        'personal-or-academic': 'personal',
        'publisher': 'SomePublisher',
        'title': 'BookTitle',
        'year-published': '2026',}




book1 = create(json_test, 'book')
print(book1)
#ref = validate_book_isbn(json_test)
#print(ref)