from app.services.Book.Book import create_book, read_book

normal_data = {"ISBN": "0061091464",
               "Title": "The Thief of Always",
               "Publish_Year": "1993",
               "Summary": "After a mysterious stranger promises to end"
                          " his boredom with a trip to the magical Holiday"
                          " House, ten-year-old Harvey learns that his fun"
                          " has a high price.",
               "Chapters": "24",
               "Chapters_Completed": "24",
               "Cover_Image": "",
               "Author_First_Name_1": "Clive",
               "Author_Last_Name_1": "Barker",
               "Author_First_Name_2": "",
               "Author_Last_Name_2": "",
               "Publisher_Name": "HarperCollins",
               "Owned": "yes",
               "Favorite": "yes",
               "Completed": "yes",
               "Currently_Reading": "no",
               "Personal_Or_Academic": "personal",
               "Genre_1": "fiction",
               "Genre_2": "horror",
               "Genre_3": "fantasy"}


def validate_book(json, create_type):
    try:
        if 'ISBN' in json and len(str(json['ISBN'])) == 13 or len(str(json['ISBN'])) == 10:
            json['ISBN'] = json['ISBN']
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
            json['Publish_Year'] = json['Publish_Year']
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
            json['Chapters'] = json['Chapters']
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
            #json['Owned'] = True if json['Owned'] == 'yes' else False
        else:
            return 'Owned is required for creating a book (yes/no)', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'Favorite' in json:
            json['Favorite'] = json['Favorite'].lower()
        #else:
            #json['Favorite'] = 'no'
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    try:
        if 'Personal_Or_Academic' in json and json['Personal_Or_Academic'].lower() in ['personal', 'academic']:
            json['Personal_Or_Academic'] = json['Personal_Or_Academic'].lower()
            #json['Personal_Or_Academic'] = True if json['Personal_Or_Academic'] == 'academic' else False
        else:
            return 'Personal or academic is required for creating a book (personal/academic)', 400
    except TypeError and ValueError:
        return 'Must be valid characters', 400

    return json, create_type + 'Success', 200




#result = validate_book(normal_data, 'Book')
#print(result)
def add_missing_keys(json_input):
    # Adds potentially missing keys for scenarios:
    #   o Optional frontend fields
    #   o Data not pulled from OL
    #   o Unimportant data is missing from OL
    # This function is useful since it makes some error checking easy later
    json_input.setdefault('Chapters', '')
    json_input.setdefault('Chapters_Completed', '')
    json_input.setdefault('Summary', '')
    #json_input.setdefault('Cover_Image', '') # May not be necessary


    #json_input.setdefault('Author_First_Name_2', '') # May not be necessary
    #json_input.setdefault('Author_Last_Name_2', '') # May not be necessary


    owned_value = json_input.setdefault('Owned', 'no')
    favorite_value = json_input.setdefault('Favorite', 'no')
    completed_value = json_input.setdefault('Completed', 'no')
    currently_reading_value = json_input.setdefault('Currently_Reading', 'no')

    # If the tags are present in JSON we need to convert from frontend syntax (on, off) to backend (yes, no)
    tag_list = [('Owned', owned_value), ('Favorite', favorite_value), ('Completed', completed_value),
                ('Currently_Reading', currently_reading_value)]
    for key, tag in tag_list:
        match tag:
            case 'on':
                json_input.update({key: 'yes'})
            case _:
                json_input.update({key: 'no'})

    json_input.setdefault('Personal_Or_Academic', 'personal') # Will default to personal

    json_input.setdefault('Genre_1', 'fiction') # Will default Genre 1 to fiction
    json_input.setdefault('Genre_2', '')
    json_input.setdefault('Genre_3', '')
    json_input.setdefault('Genre_4', '')

    return json_input


def validate_refactor(json_input):
    tag_values = ['yes', 'no']

    try:
        constructed_json = ''
        for key, value in json_input.items():
            match key, value:

                # Check Book Information
                case ('ISBN', value) if len(value) == 10 or len(value) == 13:
                    # Makes sure isbn is a string
                    json_input['ISBN'] = str(json_input['ISBN']).strip()
                    constructed_json += 'ISBN'

                case ('Title', value) if len(value) > 0:
                    # Strip whitespace and make title capitalization
                    json_input['Title'] = json_input['Title'].strip().title()
                    constructed_json += 'Title'

                case ('Chapters', value) if len(value) >= 0:
                    json_input['Chapters'] = str(json_input['Chapters']).strip()
                    constructed_json += 'Chapters'

                case ('Chapters_Completed', value) if len(value) >= 0 and value <= json_input['Chapters']:
                    json_input['Chapters_Completed'] = str(json_input['Chapters_Completed']).strip()
                    constructed_json += 'Chapters_Completed'

                case ('Summary', value) if len(value) >= 0:
                    json_input['Summary'] = json_input['Summary'].strip()
                    constructed_json += 'Summary'

                case ('Cover_Image', value) if len(value) > 0:
                    json_input['Cover_Image'] = json_input['Cover_Image'].strip()
                    constructed_json += 'Cover_Image'


                # Check Author Information
                case ('Author_First_Name_1', value) if len(value) > 0:
                    json_input['Author_First_Name_1'] = json_input['Author_First_Name_1'].strip()
                    constructed_json += 'Author_First_Name_1'

                case ('Author_Last_Name_1', value) if len(value) > 0:
                    json_input['Author_Last_Name_1'] = json_input['Author_Last_Name_1'].strip()
                    constructed_json += 'Author_Last_Name_1'

                # If there is a second author, if no key:value pair exists book record will ignore the lack of value
                # Will only validate if a second author is present
                case ('Author_First_Name_2', value) if len(value) > 0:
                    json_input['Author_First_Name_2'] = json_input['Author_First_Name_2'].strip()
                    constructed_json += 'Author_First_Name_2'

                case ('Author_Last_Name_2', value) if len(value) > 0:
                    json_input['Author_Last_Name_2'] = json_input['Author_Last_Name_2'].strip()
                    constructed_json += 'Author_Last_Name_2'


                # Check Publisher Information
                case ('Publish_Year', value) if len(value) > 0:
                    json_input['Publish_Year'] = json_input['Publish_Year'].strip()
                    constructed_json += 'Publish_Year'

                case ('Publisher_Name', value) if len(value) > 0:
                    json_input['Publisher_Name'] = json_input['Publisher_Name'].strip()
                    constructed_json += 'Publisher_Name'

                # Tag Information
                case ('Owned', value) if value.lower() in tag_values:
                    json_input['Owned'] = json_input['Owned'].lower()
                    constructed_json += 'Owned'

                case ('Favorite', value) if value.lower() in tag_values:
                    json_input['Favorite'] = json_input['Favorite'].lower()
                    constructed_json += 'Favorite'

                case ('Completed', value) if value.lower() in tag_values:
                    json_input['Completed'] = json_input['Completed'].lower()
                    constructed_json += 'Completed'

                case ('Currently_Reading', value) if value.lower() in tag_values:
                    json_input['Currently_Reading'] = json_input['Currently_Reading'].lower()
                    constructed_json += 'Currently_Reading'

                case ('Personal_Or_Academic', value)  if value.lower() in ['personal', 'academic']:
                    json_input['Personal_Or_Academic'] = json_input['Personal_Or_Academic'].lower()
                    constructed_json += 'Personal_Or_Academic'


                # Genre Information
                case ('Genre_1', value) if value.lower() in ['fiction', 'nonfiction']:
                    json_input['Genre_1'] = json_input['Genre_1'].lower()
                    constructed_json += 'Genre_1'

                case ('Genre_2', value) if len(value) > 0: # Temp until genre list is finished
                    json_input['Genre_2'] = json_input['Genre_2'].lower()
                    constructed_json += 'Genre_2'

                case ('Genre_3', value) if len(value) > 0: # Temp until genre list is finished
                    json_input['Genre_3'] = json_input['Genre_3'].lower()
                    constructed_json += 'Genre_3'

                case ('Genre_4', value) if len(value) > 0: # Temp until genre list is finished
                    json_input['Genre_4'] = json_input['Genre_4'].lower()
                    constructed_json += 'Genre_4'


                case _:  'False'

            constructed_json += '\n'

        #return constructed_json
        return json_input

    except TypeError and ValueError:
        return f'Error: Invalid Entry, could not parse. Try again.', 400




#first = add_missing_keys(normal_data)
#print(first)
create_book(normal_data)
result = read_book('0061091464')
print(result)
#print(result)
#refactor_result = validate_refactor(first)
#print(refactor_result)





if __name__ == '__main__':
    pass
