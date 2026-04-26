from app.services.Mediator.mediator_helpers import is_none, is_author_info_none, is_book_info_none


def test_is_none():
    assert is_none(None) == True
    assert is_none('null') == True
    assert is_none('None') == True
    assert is_none('') == True
    assert is_none('Not none') == False


def test_is_author_none():
    response_true = is_author_info_none('')
    response_false = is_author_info_none('Not None')
    assert response_true == True
    assert response_false == False

def test_is_book_none():
    response_true1 = is_book_info_none('', '')
    response_true2 = is_book_info_none('title', 'title')
    response_false = is_book_info_none('Not None', '')
    assert response_true1 == True
    assert response_true2 == True
    assert response_false == False