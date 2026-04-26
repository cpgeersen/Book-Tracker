import json
import os
from pathlib import Path

import requests

from app.services.Book.Book import is_in_book_table, create_book, update_book_cover_image, is_note_id_in_database, \
    create_book_note, update_book_note
from app.services.validate_json.validate_book_json import validate_book_from_local

SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500


def mediator_create(json_input, create_type, main_app=None):
    try:
        if create_type == 'book-local':
            isbn = json_input['ISBN']

            # !!WIP!! Note: This fix my break, look out in future
            if not is_in_book_table(isbn):
                json.dumps({'Error': 'Book already in database'}), FOUND
            json_input = validate_book_from_local(json_input)
            result = create_book(json_input)
            return result

        # This is only called through the OL search when a POST request is sent
        # This means the cache is all ready created and passed to this function
        elif create_type == 'book-ol':
            isbn = json_input['ISBN']

            if not is_in_book_table(isbn):
                json.dumps({'Error': 'Book already in database'}), FOUND

            # Get URL before validating json
            image_url = json_input['Cover_Image_URL']

            json_input = validate_book_from_local(json_input)

            result = create_book(json_input)

            # When the book exists, do not create the cover image again
            if result[1] == 302:
                return result

            # Download cover image from cache_response['Cover_Image_URL']
            # to /static/cover_images
            image_data = requests.get(image_url).content

            # Use cover image naming, uses jpg since OL stores cover images this way
            file_name = isbn + '_' + 'cover_image.jpg'
            file_path = os.path.join(Path(main_app.static_folder) / "images" / "cover_images", file_name)

            # Write the images to the correct path
            with open(file_path, 'wb') as image:
                image.write(image_data)

            # Update cover image file path in database
            update_book_cover_image(isbn, f'/static/images/cover_images/{file_name}')

            return result
            # !!WIP!! Error here
            return 'WIP'

        elif create_type == 'note':
            json_input = json.loads(json_input)
            if len(json_input.get('Note_Content')) > 0:
                note_id_in_database = is_note_id_in_database(json_input)
                if not note_id_in_database:
                    result = create_book_note(json_input)
                    return result
                else:
                    result = update_book_note(json_input)
                    return result
            else:
                return json.dumps({'Error': 'Empty Note'})
        else:
            return 'Error: Not a valid call'
    except (TypeError, ValueError, AttributeError):
        return f'Error: Invalid Entry, could not parse. Try again.', BAD_REQUEST
    except KeyError as error:  # If any required keys are missing from JSON
        return error, BAD_REQUEST
