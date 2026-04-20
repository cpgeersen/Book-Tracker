import json

from app.services.Book.Book import delete_book_cover_image, delete_book, delete_book_note, delete_genre, read_book
from app.services.user_settings.delete_database import reset_database, purge_cover_images


def mediator_delete(json_input, delete_type):
    if delete_type == 'book':
        json_input = json.loads(json_input)
        print(json_input)

        isbn = json_input['ISBN']

        delete_book_cover_image(isbn, json_input['Cover_Image_Path'])

        delete_book(isbn)

        return json.dumps({'Success': 'Book Deleted'})

    elif delete_type == 'note':
        json_input = json.loads(json_input)
        response = delete_book_note(json_input)
        return response

    elif delete_type == 'cover-image':
        json_input = json.loads(json_input)
        response = delete_book_cover_image(json_input['ISBN'], json_input['Cover_Image_Path'])
        return response

    elif delete_type == 'genre':
        print(json_input)
        isbn = json_input['ISBN']

        json_output = dict()

        if json_input.get('Genre_2') == 'on':
            response = delete_genre(isbn, json_input['Genre_ID_2'])
            if response[1] == 200:
                json_output.update({'Genre_2_Deleted': 'True'})

        if json_input.get('Genre_3') == 'on':
            response = delete_genre(isbn, json_input['Genre_ID_3'])
            if response[1] == 200:
                json_output.update({'Genre_3_Deleted': 'True'})

        if json_input.get('Genre_4') == 'on':
            response = delete_genre(isbn, json_input['Genre_ID_4'])
            if response[1] == 200:
                json_output.update({'Genre_4_Deleted': 'True'})

        return json_output

    elif delete_type == 'dedupe':
        json_input = json.loads(json_input)
        json_input = json.loads(read_book(json_input['ISBN']))

        # Used to fix slight mismatch in delete and internal tracking of cover image
        json_input.update({'Cover_Image_Path': json_input['Cover_Image']})
        print(json_input)
        return mediator_delete(json.dumps(json_input), 'book')

    elif delete_type == 'delete-database':
        return reset_database('RESET')
    elif delete_type == 'all-cover-images':
        return purge_cover_images()

    else:
        return 'Error: Not a valid call'