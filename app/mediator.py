# Module to mediate calls from the frontend and backend
# Will take JSON from frontend and call relevant query functions and return the result as JSON to frontend

# POST - Takes JSON as input
def create(json,create_type):
    create_type = create_type.lower()
    if create_type == 'book':
        if 'isbn' not in json or len(str(json['isbn'])) != 13:
            return 'ISBN is required for creating a book(must be 13 numbers)', 400
        else:
            json['isbn'] = int(json['isbn'])


        if 'title' not in json or len(json['title']) == 0:
            return 'Title is required for creating a book', 400
        else:
            json['title'] = json['title'].strip()


        if 'author' not in json or len(json['author']) == 0:
            return 'Author is required for creating a book', 400
        else:
            json['author'] = json['author'].strip()


        if 'author2' not in json or len(json['author2']) == 0:
            json['author2'] = ''
        else:
            json['author2'] = json['author2'].strip()


        if 'year-published' not in json or len(json['year-published']) == 0:
            return 'Year published is required for creating a book(YYYY)', 400
        else:
            json['year-published'] = int(json['year-published'])
    

        if 'publisher' not in json or len(json['publisher']) == 0:
            return 'Publisher is required for creating a book', 400
        else:
            json['publisher'] = json['publisher'].strip()


        if 'chapters' not in json or int(json['chapters']) <= 0:
            return 'Number of chapters is required for creating a book', 400
        else:
            json['chapters'] = int(json['chapters'])


        if 'fiction-or-nonfiction' not in json or json['fiction-or-nonfiction'].lower() not in ['fiction', 'nonfiction']:
            return 'Fiction or nonfiction is required for creating a book', 400
        else:
            json['fiction-or-nonfiction'] = json['fiction-or-nonfiction'].lower()


        if 'owned' not in json or json['owned'].lower() not in ['on', 'off']:
            return 'Owned is required for creating a book (on/off)', 400
        else:
            json['owned'] = json['owned'].lower()
            json['owned'] = True if json['owned'] == 'on' else False


        if 'favorite' not in json:
            json['favorite'] = False
        else:
            json['favorite'] = json['favorite'].lower() == 'on'
        
        if 'personal-or-academic' not in json or json['personal-or-academic'].lower() not in ['personal', 'academic']:
            return 'Personal or academic is required for creating a book (personal/academic)', 400
        else:
            json['personal-or-academic'] = json['personal-or-academic'].lower()
            json['personal-or-academic'] = True if json['personal-or-academic'] == 'academic' else False
        return create_type + 'Success', 200

    # Can directly get values from keys
    number_of_chapters = json['chapters']
    # So just focus on parsing all json values from the book JSON and validating them
    # i.e. ISBN should be 13 numbers, etc.

    # Call database functions

    # Just demonstrating, can remove this
    return number_of_chapters


# GET - Takes JSON as input
def read(json):
    return str(json)


# PATCH - Takes JSON as input
def update(json):
    return str(json)


# DELETE - Takes JSON as input
def delete(json):
    return str(json)
