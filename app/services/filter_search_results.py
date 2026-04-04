import json


def filter_results(filter_json, json_result):
    # JSON from frontend filters
    filter_json_dict = dict(filter_json)
    print(filter_json_dict)

    # Boolean filters
    filter_owned = filter_json_dict.get('owned')
    filter_favorite = filter_json_dict.get('favorite')
    filter_completed = filter_json_dict.get('completed')
    filter_currently_reading = filter_json_dict.get('currently-reading')

    # Filters that are not strings
    filter_personal_or_academic = filter_json_dict.get('personal-or-academic')
    filter_genre_1 = filter_json_dict.get('genre-1')
    filter_genre = str(filter_json_dict.get('genre')).split(',')[0]
    print(f'Genre to search: {filter_genre}')


    json_result_dict = dict(json_result)

    for key, value in json_result_dict.copy().items():

        if filter_currently_reading == 'true':
            if value.get('Currently_Reading') != 'yes':
                json_result_dict.pop(key)
                continue

        if filter_favorite == 'true':
            if value.get('Favorite') != 'yes':
                json_result_dict.pop(key)
                continue

        if filter_owned == 'true':
            if value.get('Owned') != 'yes':
                json_result_dict.pop(key)
                continue

        if filter_completed == 'true':
            if value.get('Completed') != 'yes':
                json_result_dict.pop(key)
                continue


        # These three break view all books need to fix

        genre_num = 2
        if filter_genre != '':
            while genre_num < 5:
                genre_value = value.get(f'Genre_{genre_num}')

                if genre_value == filter_genre:
                    break

                if genre_value is None:
                    json_result_dict.pop(key)
                    break
                elif genre_value != filter_genre:
                    json_result_dict.pop(key)
                    break
                genre_num += 1

        if filter_genre_1 != 'any':
            if value.get('Genre_1') != filter_genre_1:
                json_result_dict.pop(key)
                continue

        if filter_personal_or_academic != 'any':
            if value.get('Personal_Or_Academic') != filter_personal_or_academic:
                json_result_dict.pop(key)
                continue


    return json_result_dict




if __name__ == '__main__':
    pass