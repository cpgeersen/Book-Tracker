def validate_book(json, create_type):
    try:
        if 'ISBN' in json and len(str(json['ISBN'])) == 13 or len(str(json['ISBN'])) == 10:
            json['ISBN'] = int(json['ISBN'])
        else:
            return 'ISBN is required for creating a book(must be 10 or 13 numbers)', 400
    except TypeError and ValueError:
        return 'Error: ISBN must be 10 or 13 integers.', 400

    try:
        if 'Title' in json and len(json['Title']) != 0:
            json['Title'] = json['Title'].strip()
        else:
            return 'Title is required for creating a book', 400
    except TypeError and ValueError:
        return 'Title must be valid characters', 400

    try:
        if 'Author_First_Name_1' in json and len(json['Author_First_Name_1']) != 0:
            json['Author_First_Name_1'] = json['Author_First_Name_1'].strip()
        else:
            return 'Primary Author First Name is required for creating a book', 400
    except TypeError and ValueError:
        return 'Author must be valid characters', 400

    try:
        if 'Author_Last_Name_1' in json and len(json['Author_Last_Name_1']) != 0:
            json['Author_Last_Name_1'] = json['Author_Last_Name_1'].strip()
        else:
            return 'Primary Author Last Name is required for creating a book', 400
    except TypeError and ValueError:
        return 'Author must be valid characters', 400

    try:
        if 'Author_First_Name_2' in json and len(json['Author_First_Name_2']) != 0:
            json['Author_First_Name_2'] = json['Author_First_Name_2'].strip()
        else:
            json['Author_First_Name_2'] = ''
    except TypeError and ValueError:
        return 'Author must be valid characters', 400

    try:
        if 'Author_Last_Name_2' in json and len(json['Author_Last_Name_2']) != 0:
            json['Author_Last_Name_2'] = json['Author_Last_Name_2'].strip()
        else:
            json['Author_Last_Name_2'] = ''
    except TypeError and ValueError:
        return 'Author must be valid characters', 400

    try:
        if 'Publish_Year' in json and len(json['Publish_Year']) != 0:
            json['Publish_Year'] = int(json['Publish_Year'])
        else:
            return 'Year published is required for creating a book (YYYY)', 400
    except TypeError and ValueError:
        return 'Year must be valid integers', 400

    try:
        if 'Publisher_Name' in json and len(json['Publisher_Name']) != 0:
            json['Publisher_Name'] = json['Publisher_Name'].strip()
        else:
            return 'Publisher is required for creating a book', 400
    except TypeError and ValueError:
        return 'Publisher must be valid characters', 400

    try:
        if 'Chapters' in json and int(json['Chapters']) >= 0:
            json['Chapters'] = int(json['Chapters'])
        else:
            return 'Invalid Number of Chapters, must be 0 or more', 400
    except TypeError and ValueError:
        return 'Chapters must be valid integers', 400

    try:
        if 'Genre_1' in json and json['Genre_1'].lower() in ['fiction', 'nonfiction']:
            json['Genre_1'] = json['Genre_1'].lower()
        else:
            return 'Fiction or nonfiction is required for creating a book', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'Owned' in json and json['Owned'].lower() in ['yes', 'no']:
            json['Owned'] = json['Owned'].lower()
            json['Owned'] = True if json['Owned'] == 'yes' else False
        else:
            return 'Owned is required for creating a book (yes/no)', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'Favorite' in json:
            json['Favorite'] = json['Favorite'].lower() == 'yes'
        else:
            json['Favorite'] = False
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'Personal_Or_Academic' in json and json['Personal_Or_Academic'].lower() in ['personal', 'academic']:
            json['Personal_Or_Academic'] = json['Personal_Or_Academic'].lower()
            json['Personal_Or_Academic'] = True if json['Personal_Or_Academic'] == 'academic' else False
        else:
            return 'Personal or academic is required for creating a book (personal/academic)', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    return json, create_type + 'Success', 200


if __name__ == '__main__':
    pass
