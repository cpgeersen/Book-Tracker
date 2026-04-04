import json


def filter_results(filter_json, json_result):
    # JSON from frontend filters
    filter_json_dict = dict(filter_json)
    print(filter_json_dict)

    # Boolean filters
    filter_owned = bool(filter_json_dict.get('owned'))
    filter_favorite = bool(filter_json_dict.get('favorite'))
    filter_read = bool(filter_json_dict.get('read'))
    filter_currently_reading = bool(filter_json_dict.get('currently-reading'))

    # Filters that are not strings
    filter_personal_or_academic = filter_json_dict.get('personal-or-academic')
    filter_genre_1 = filter_json_dict.get('genre-1')
    filter_genre = filter_json_dict.get('genre')


    json_result_dict = dict(json_result)
    return_json = {}

    for key, value in json_result_dict.copy().items():

        if filter_currently_reading:
            if value.get('Currently_Reading') != 'yes':
                del json_result_dict[key]
                continue

        if filter_favorite:
            if value.get('Favorite') != 'yes':
                del json_result_dict[key]
                continue

        if filter_owned:
            if value.get('Owned') != 'yes':
                del json_result_dict[key]
                continue


    return json_result_dict











#if filter_genre is not None:
#    for genre_num in range(2, 5):
#        if value.get(f'Genre_{genre_num}') is None:
#            del key
#            break
#        elif value.get(f'Genre_{genre_num}') != filter_genre:
#            del key
#            break

#if filter_genre_1 is not None:
#    if value.get('Genre_1') != filter_genre_1:
#        del key
#        continue

#if filter_personal_or_academic:
#    if value.get('Personal_Or_Academic') != filter_personal_or_academic:
#        del key
#        continue









if __name__ == '__main__':
    pass