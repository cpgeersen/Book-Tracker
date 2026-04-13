
SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

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

bad_data = {   "Title": "The Thief of Always",
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

def test_add_book_success(client):
    client.post('/book/add-local', data=normal_data)
    get_response = client.get('/book/add-local', data=normal_data['ISBN'])
    assert get_response.status_code == SUCCESS

def test_add_book_bad_request(client):
    response = client.post('/book/add-local', data=normal_data)
    print(response)
    assert response.status_code == FOUND

# def test_a(client):
#     #with pytest.raises(TypeError):
#     response = client.post('/book/add-local', data={})
#     assert response.status_code == BAD_REQUEST




















