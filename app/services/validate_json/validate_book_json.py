import json


def validate_book_for_frontend(json_input):
    # Converts the tag values to reflect the frontend
    if not isinstance(json_input, dict):
        json_input = json.loads(json_input)

    json_input['Owned'] = 'on' if json_input['Owned'] == 'yes' else 'off'
    json_input['Favorite'] = 'on' if json_input['Favorite'] == 'yes' else 'off'
    json_input['Completed'] = 'on' if json_input['Completed'] == 'yes' else 'off'
    json_input['Currently_Reading'] = 'on' if json_input['Currently_Reading'] == 'yes' else 'off'

    # Rare case that genre_1 is not fiction or nonfiction
    # This is just a presentation issue since genre number is not tracked in database
    genre_1 = json_input.get('Genre_1')
    genre_2 = json_input.get('Genre_2')
    genre_3 = json_input.get('Genre_2')
    genre_4 = json_input.get('Genre_2')

    genre_1_list = ['fiction', 'nonfiction']

    if genre_1 not in genre_1_list:
        if genre_2 in genre_1_list:
            json_input['Genre_1'] = genre_2
            json_input['Genre_2'] = genre_1
        elif genre_3 in genre_1_list:
            json_input['Genre_1'] = genre_3
            json_input['Genre_3'] = genre_1
        elif genre_4 in genre_1_list:
            json_input['Genre_1'] = genre_4
            json_input['Genre_4'] = genre_1

    return json.dumps(json_input)


def validate_book_from_local(json_input):
    json_output = {}

    # Call each validation function to build the json input for the database
    json_output.update(validate_book(json_input))
    json_output.update(validate_author(json_input))
    json_output.update(validate_publisher(json_input))
    json_output.update(validate_genres(json_input))
    json_output.update(validate_tags(json_input))

    return json.dumps(json_output)


def validate_book(json_input):
    json_output = {}

    isbn = str(json_input.get('ISBN', ''))
    title = json_input.get('Title', '')
    if isbn == '' or isbn == 'None' or isbn is None:
        raise KeyError('Error: Book must have an ISBN.')
    if len(isbn) != 10 and len(isbn) != 13:
        return ValueError('Error: Book must have a valid ISBN (10 or 13 integers).')
    if title == '' or title == 'None' or title is None:
        raise KeyError('Error: Book must have a title.')

    chapters = json_input.get('Chapters', '0')
    chapters_completed = json_input.get('Chapters_Completed', '0')
    summary = json_input.get('Summary', '')
    cover_image = json_input.get('Cover_Image', '')

    json_output.update({'ISBN': isbn.strip()})
    json_output.update({'Title': title.strip().title()})
    json_output.update({'Chapters': chapters.strip()})
    json_output.update({'Chapters_Completed': chapters_completed.strip()})
    json_output.update({'Summary': summary})
    json_output.update({'Cover_Image': cover_image})

    return json_output


def validate_author(json_input):
    json_output = {}

    author_first_name_1 = json_input.get('Author_First_Name_1', '')
    author_last_name_1 = json_input.get('Author_Last_Name_1', '')
    author_full_name_1 = json_input.get('Author_Full_Name_1', '')

    if (author_first_name_1 == '' or author_first_name_1 == 'None' or
        author_first_name_1 is None):
        raise KeyError('Error: Book must have an author.')
    if (author_last_name_1 == '' or author_last_name_1 == 'None' or
        author_last_name_1 is None):
        raise KeyError('Error: Book must have an author.')

    json_output.update({'Author_First_Name_1': author_first_name_1.strip()})
    json_output.update({'Author_Last_Name_1': author_last_name_1.strip()})
    json_output.update({'Author_Full_Name_1': author_full_name_1.strip()})



    author_first_name_2 = json_input.get('Author_First_Name_2', '')
    author_last_name_2 = json_input.get('Author_Last_Name_2', '')
    author_full_name_2 = json_input.get('Author_Full_Name_2', '')

    if (author_first_name_2 == '' or author_first_name_2 == 'None' or
        author_first_name_2 is None):
        return json_output
    if (author_last_name_2 == '' or author_last_name_2 == 'None' or
        author_last_name_2 is None):
        return json_output

    json_output.update({'Author_First_Name_2': author_first_name_2.strip()})
    json_output.update({'Author_Last_Name_2': author_last_name_2.strip()})
    json_output.update({'Author_Full_Name_2': author_full_name_2.strip()})

    return json_output


def validate_publisher(json_input):
    json_output = {}

    publisher_name = json_input.get('Publisher_Name', '')
    publisher_year = json_input.get('Publish_Year', '')
    if publisher_name == '' or publisher_name == 'None' or publisher_name is None:
        raise KeyError('Error: Book must have a publisher.')
    if publisher_year == '' or publisher_year == 'None' or publisher_year is None:
        raise KeyError('Error: Book must have a publish year.')

    json_output.update({'Publisher_Name': publisher_name.strip().title()})
    json_output.update({'Publish_Year': publisher_year.strip()})

    return json_output


def validate_tags(json_input):
    json_output = {}

    owned_value = json_input.get('Owned', 'no')
    favorite_value = json_input.get('Favorite', 'no')
    completed_value = json_input.get('Completed', 'no')
    currently_reading_value = json_input.get('Currently_Reading', 'no')

    # If the tags are present in JSON we need to convert from frontend syntax (on, off) to backend (yes, no)
    tag_list = [('Owned', owned_value), ('Favorite', favorite_value), ('Completed', completed_value),
                ('Currently_Reading', currently_reading_value)]


    for key, tag in tag_list:
        match tag.lower():
            case 'on':
                json_output.update({key: 'yes'})
            case 'off':
                json_output.update({key: 'no'})
            case _: json_output.update({key: tag})

    # Then add Personal_Or_Academic
    personal_or_academic = json_input.get('Personal_Or_Academic', 'personal')  # Will default to personal
    json_output.update({'Personal_Or_Academic': personal_or_academic})

    return json_output


def validate_genres(json_input):
    json_output = {}

    # Add possible missing genres
    genre_1 = json_input.get('Genre_1', 'fiction')  # Will default Genre 1 to fiction
    genre_2 = json_input.get('Genre_2', '')
    genre_3 = json_input.get('Genre_3', '')
    genre_4 = json_input.get('Genre_4', '')

    # Add genres to the json output
    json_output.update({'Genre_1': genre_1})
    json_output.update({'Genre_2': genre_2})
    json_output.update({'Genre_3': genre_3})
    json_output.update({'Genre_4': genre_4})

    return json_output


if __name__ == '__main__':
    pass