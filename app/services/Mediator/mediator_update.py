import json
import os

import requests

from app.services.Book.Book import update_book_summary, update_book_chapters_completed, update_book_chapters, \
    update_book_tags, update_book_cover_image, create_book_genre, update_book_genre, read_book, update_book_title, \
    delete_book_author_record, update_book_publisher_year, is_publisher_in_database, read_publisher_id_by_name, \
    update_book_publisher_id, create_new_publisher
from app.services.Mediator.mediator_helpers import is_book_info_none, is_author_info_none
from app.services.OpenLibrary.openlibrary import complete_book_from_isbn_ol
from app.services.OpenLibrary.openlibrary_search_cache import cache
from app.services.openlibrary_data_resolution.resolve_author import resolve_author_olid
from app.services.user_settings.user_settings import update_user_settings
from app.services.validate_json.validate_book_json import validate_tags
from app.services.validate_json.validate_openlibrary_json import validate_isbn_search


def mediator_update(json_input, update_type):
    try:
        if update_type == 'summary':
            json_input = json.loads(json_input)
            response = update_book_summary(json_input['ISBN'], json_input['Summary'])
            return response

        elif update_type == 'chapters':
            json_input = json.loads(json_input)
            if json_input['Chapters_Completed'] > json_input['Chapters']:
                update_book_chapters_completed(json_input['ISBN'], json_input['Chapters'])

            response = update_book_chapters(json_input['ISBN'], json_input['Chapters'])
            return response

        elif update_type == 'chapters-completed':
            json_input = json.loads(json_input)
            response = update_book_chapters_completed(json_input['ISBN'], json_input['Chapters_Completed'])
            return response

        elif update_type == 'tag':
            json_input = json.loads(json_input)
            json_input_converted_tags = validate_tags(json_input)
            response = update_book_tags(json_input['Tag_ID'], json_input_converted_tags['Owned'],
                                        json_input_converted_tags['Favorite'], json_input_converted_tags['Completed'],
                                        json_input_converted_tags['Currently_Reading'],
                                        json_input_converted_tags['Personal_Or_Academic'])
            return response

        elif update_type == 'cover-image':
            json_input = json.loads(json_input)
            response = update_book_cover_image(json_input['ISBN'], json_input['Cover_Image_Path'])
            return response

        elif update_type == 'genres':
            json_input = dict(json.loads(json_input))

            genre_number = 1
            while genre_number < 5:
                if json_input[f'Genre_{genre_number}_ID_Old'] is None:
                    if json_input[f'Genre_{genre_number}_ID_New'] == 'None':
                        genre_number += 1
                        continue
                    else:
                        create_book_genre(json_input['ISBN'], json_input[f'Genre_{genre_number}_ID_New'])

                if json_input[f'Genre_{genre_number}_ID_New'] != json_input[f'Genre_{genre_number}_ID_Old']:
                    update_book_genre(json_input['ISBN'], json_input[f'Genre_{genre_number}_ID_Old'],
                                      json_input[f'Genre_{genre_number}_ID_New'])

                genre_number += 1

        elif update_type == 'openlibrary':
            json_input = json.loads(json_input)
            isbn = json_input['ISBN']

            # Get current book information
            old_json_data = json.loads(read_book(isbn))

            # First see if book information is in cache
            cache_response = cache(isbn)

            # Creates a new cache record when none exist
            if cache_response is None:
                print('Calling OpenLibrary API')

                # Pull OpenLibrary Data for ISBN
                ol_response = complete_book_from_isbn_ol(isbn)

                # Validate the data and put into an easier form
                validated_ol_response = validate_isbn_search(ol_response, isbn)

                # Add validated json to the cache
                cache_response = cache(isbn, validated_ol_response)

            is_cover_image_updated = False
            if json_input.get('Cover_Image_Update') is not None:
                # Download cover image from cache_response['Cover_Image_URL']
                # to /static/cover_images
                image_url = cache_response['Cover_Image_URL']
                image_data = requests.get(image_url).content

                # Use cover image naming, uses jpg since OL stores cover images this way
                file_name = isbn + '_' + 'cover_image.jpg'
                file_path = os.path.join('app', 'static', 'images', 'cover_images', file_name)

                # Write the images to the correct path
                with open(file_path, 'wb') as image:
                    image.write(image_data)

                # Update cover image file path in database
                update_book_cover_image(isbn, f'/static/images/cover_images/{file_name}')
                is_cover_image_updated = True

            # Update book title if not correct
            old_title = old_json_data.get('Title')
            cache_title = cache_response.get('Title')
            is_title_update = False

            if not is_book_info_none(cache_title, old_title):
                update_book_title(isbn, cache_title)
                is_title_update = True

            # Update book summary if requested
            cache_summary = cache_response.get('Summary')
            is_summary_updated = False

            if json_input['Summary_Update'] is not None:
                update_book_summary(isbn, cache_summary)
                is_summary_updated = True

            # Update author names
            cache_author_1_olid = cache_response.get('Author_1_OLID')
            is_author_1_updated = False

            if not is_author_info_none(cache_author_1_olid):
                is_author_1_updated = resolve_author_olid(old_json_data, cache_response, author_num='1')

            # When there is a second author
            cache_author_2_olid = cache_response.get('Author_2_OLID')
            is_author_2_updated = False

            if not is_author_info_none(cache_author_2_olid):
                is_author_2_updated = resolve_author_olid(old_json_data, cache_response, author_num='2')

            # There is a second author, but there should not be one
            elif old_json_data.get('Author_First_Name_2') is not None:
                delete_book_author_record(old_json_data.get('ISBN'),
                                          old_json_data.get('Author_First_Name_2'),
                                          old_json_data.get('Author_Last_Name_2'))

            # Update book publish year if possible
            old_publisher_year = old_json_data.get('Publish_Year')
            cache_publish_year = cache_response.get('Publish_Year')
            is_publish_year_updated = False

            if not is_book_info_none(cache_publish_year, old_publisher_year):
                update_book_publisher_year(isbn, cache_publish_year)
                is_publish_year_updated = True

            # Update publisher information
            cache_publisher_name = cache_response.get('Publisher_Name')
            old_publisher_name = old_json_data.get('Publisher_Name')
            is_publisher_updated = False

            if not is_book_info_none(cache_publisher_name, old_publisher_name):
                # Check if the new publisher already in the database
                is_publisher_present = is_publisher_in_database(cache_publisher_name)

                if is_publisher_present:
                    publisher_id = read_publisher_id_by_name(cache_publisher_name)['Publisher_ID']
                    update_book_publisher_id(old_json_data.get('ISBN'), publisher_id[0])
                    is_publisher_updated = True
                else:
                    # Publisher is not present, create new publisher with data and update
                    publisher_id = create_new_publisher(cache_publisher_name)['Publisher_ID']
                    update_book_publisher_id(old_json_data.get('ISBN'), publisher_id[0])
                    is_publisher_updated = True

            # Builds dict for updated items
            updated_records = {'Updated': 'False'}
            if is_title_update:
                updated_records['Title'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_summary_updated:
                updated_records['Summary'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_publish_year_updated:
                updated_records['Publish_Year'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_cover_image_updated:
                updated_records['Cover_Image'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_publisher_updated:
                updated_records['Publisher'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_author_1_updated:
                updated_records['Author_1'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_author_2_updated:
                updated_records['Author_2'] = 'Updated'
                updated_records['Updated'] = 'True'

            return updated_records

        elif update_type == 'user-settings':
            json_input = json.loads(json_input)
            user_name = str(json_input['Username']).strip()
            theme = str(json_input['Theme'])

            update_user_settings(user_name, theme)

    except TypeError:
        pass  # !!WIP TypeError!!
