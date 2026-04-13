import json

from app.services.Book.Book import delete_book_cover_image, delete_book, read_book_notes, delete_book_note


def mediator_delete(json_input, delete_type):
    if delete_type == 'book':
        json_input = json.loads(json_input)
        delete_book_cover_image(json_input['ISBN'], json_input['Cover_Image_Path'])
        delete_book(json_input['ISBN'])

        note_ids = read_book_notes(json_input)
        for value in note_ids.values():
            response = delete_book_note(value)

        return json.dumps({'Success': 'Book Deleted'})

    elif delete_type == 'note':
        json_input = json.loads(json_input)
        response = delete_book_note(json_input)
        return response

    elif delete_type == 'cover-image':
        json_input = json.loads(json_input)
        response = delete_book_cover_image(json_input['ISBN'], json_input['Cover_Image_Path'])
        return response

    else:
        return 'Error: Not a valid call'