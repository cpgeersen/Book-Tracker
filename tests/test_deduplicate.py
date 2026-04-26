from app.services.deduplicate_books import de_duplicate_books_refactor

book_1 = {
        "ISBN": "9780060913076",
        "Title": "The crying of lot 49",
        "Author_Full_Name_1": "Thomas Pynchon",
        "Author_First_Name_1": "Thomas",
        "Author_Last_Name_1": "Pynchon",
        "Author_1_OLID": "OL384171A",
        "Author_Full_Name_2": "Antonio-Prometeo Moya",
        "Author_First_Name_2": "Antonio-Prometeo",
        "Author_Last_Name_2": "Moya",
        "Author_2_OLID": "OL8502455A",
        "Publisher_Name": "Perennial Library",
        "Publisher_OLID": '',
        "Publish_Year": "1986",
        "Summary": "Oedipa Maas, executor of the will of Pierce Inverarity, journeys through a bizarre underground of secret societies, jazz clubs, beatniks, and her own psyche.  Readers accustomed to postmodern literature will revel in Pynchon's second novel.",
        "Cover_Image_URL": "https://covers.openlibrary.org/b/id/39753-L.jpg"
    }

book_2 = {
        "ISBN": "0553106201",
        "Title": "The Crying of Lot 49",
        "Author_Full_Name_1": "Thomas Pynchon",
        "Author_First_Name_1": "Thomas",
        "Author_Last_Name_1": "Pynchon",
        "Author_1_OLID": "OL384171A",
        "Author_Full_Name_2": "Antonio-Prometeo Moya",
        "Author_First_Name_2": "Antonio-Prometeo",
        "Author_Last_Name_2": "Moya",
        "Author_2_OLID": "OL8502455A",
        "Publisher_Name": "Bantam Books",
        "Publisher_OLID": '',
        "Publish_Year": "1967",
        "Summary": "Oedipa Maas, executor of the will of Pierce Inverarity, journeys through a bizarre underground of secret societies, jazz clubs, beatniks, and her own psyche.  Readers accustomed to postmodern literature will revel in Pynchon's second novel.",
        "Cover_Image_URL": "https://covers.openlibrary.org/b/id/6481855-L.jpg"
    }


def test_deduplicate_success(client):
    client.post('/book/add-local', data=book_1)
    client.post('/book/add-local', data=book_2)
    response = de_duplicate_books_refactor()
    print(response)
    assert response['Duplicate_Book_Result_1'].get('Title') is not None
    assert len(response['Duplicate_Book_Result_1'].get('ISBNs')) == 2










