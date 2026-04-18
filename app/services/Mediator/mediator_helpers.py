
def is_none(value):
    match value:
        case None:
            return True
        case 'null':
            return True
        case 'None':
            return True
        case '':
            return True
        case _:
            return False

def is_author_info_none(author_olid):
    if is_none(author_olid):
        return True
    else:
        return False

def is_book_info_none(new_book_info, old_book_info):
    if is_none(new_book_info):
        return True
    elif str(new_book_info).lower() == str(old_book_info).lower():
        return True
    else:
        return False


def sort_results_by_title(result):
    result = dict(sorted(result.items(), key=lambda kv: kv[1]['Title']))
    return result