def validate_book(json, create_type):
    try:
        if 'isbn' in json and len(str(json['isbn'])) == 13:
            json['isbn'] = int(json['isbn'])
        else:
            return 'ISBN is required for creating a book(must be 13 numbers)', 400
    except TypeError and ValueError:
        return 'Error: ISBN must be valid 13 integers.', 400

    try:
        if 'title' in json and len(json['title']) != 0:
            json['title'] = json['title'].strip()
        else:
            return 'Title is required for creating a book', 400
    except TypeError and ValueError:
        return 'Title must be valid characters', 400

    try:
        if 'author' in json and len(json['author']) != 0:
            json['author'] = json['author'].strip()
        else:
            return 'Author is required for creating a book', 400
    except TypeError and ValueError:
        return 'Author must be valid characters', 400

    try:
        if 'author2' in json and len(json['author2']) != 0:
            json['author2'] = json['author2'].strip()
        else:
            json['author2'] = ''
    except TypeError and ValueError:
        return 'Author must be valid characters', 400

    try:
        if 'year-published' in json and len(json['year-published']) != 0:
            json['year-published'] = int(json['year-published'])
        else:
            return 'Year published is required for creating a book(YYYY)', 400
    except TypeError and ValueError:
        return 'Year must be valid integers', 400

    try:
        if 'publisher' in json and len(json['publisher']) != 0:
            json['publisher'] = json['publisher'].strip()
        else:
            return 'Publisher is required for creating a book', 400
    except TypeError and ValueError:
        return 'Publisher must be valid characters', 400

    try:
        if 'chapters' in json and int(json['chapters']) > 0:
            json['chapters'] = int(json['chapters'])
        else:
            return 'Number of chapters is required for creating a book', 400
    except TypeError and ValueError:
        return 'Chapters must be valid integers', 400

    try:
        if 'fiction-or-nonfiction' in json and json['fiction-or-nonfiction'].lower() in ['fiction', 'nonfiction']:
            json['fiction-or-nonfiction'] = json['fiction-or-nonfiction'].lower()
        else:
            return 'Fiction or nonfiction is required for creating a book', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'owned' in json and json['owned'].lower() in ['on', 'off']:
            json['owned'] = json['owned'].lower()
            json['owned'] = True if json['owned'] == 'on' else False
        else:
            return 'Owned is required for creating a book (on/off)', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'favorite' in json:
            json['favorite'] = json['favorite'].lower() == 'on'
        else:
            json['favorite'] = False
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'personal-or-academic' in json and json['personal-or-academic'].lower() in ['personal', 'academic']:
            json['personal-or-academic'] = json['personal-or-academic'].lower()
            json['personal-or-academic'] = True if json['personal-or-academic'] == 'academic' else False
        else:
            return 'Personal or academic is required for creating a book (personal/academic)', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    return json, create_type + 'Success', 200


if __name__ == '__main__':
    pass
