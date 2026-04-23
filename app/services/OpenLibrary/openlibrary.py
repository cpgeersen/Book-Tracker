from app.services.OpenLibrary.openlibrary_api import search_books_by_isbn, get_work_data, get_author_info_from_authorid, \
    search_books_by_title, get_book_info_from_cover_key, search_books_by_author


def complete_book_from_isbn_ol(isbn):
    ol_data = search_books_by_isbn(isbn)

    if "error" in ol_data:
        return {"error": "ISBN not present in OpenLibrary, please use another ISBN or search via Title"}

    publish_year = ol_data.get("publish_date")

    publishers = ol_data.get("publishers", [])
    publisher = publishers[0] if publishers else None

    isbn_list = []
    if "isbn_10" in ol_data:
        isbn_list.extend(ol_data["isbn_10"])
    if "isbn_13" in ol_data:
        isbn_list.extend(ol_data["isbn_13"])

    cover_image_url = None
    if "covers" in ol_data and isinstance(ol_data["covers"], list) and len(ol_data["covers"]) > 0:
        cover_id = ol_data["covers"][0]
        cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

    work_key = None
    if "works" in ol_data and isinstance(ol_data["works"], list) and len(ol_data["works"]) > 0:
        if "key" in ol_data["works"][0]:
            work_key = ol_data["works"][0]["key"]


    author_1 = None
    author_1_olid = None
    author_2 = None
    author_2_olid = None
    publisher_olid = None
    summary = None
    title = None

    if work_key:
        work_data = get_work_data(work_key)

        if isinstance(work_data, dict):

            title = ol_data.get("title")

            if "description" in work_data:
                if isinstance(work_data["description"], dict):
                    summary = work_data["description"].get("value")
                else:
                    summary = work_data["description"]

            if "publishers" in work_data:
                for pub in work_data["publishers"]:
                    if isinstance(pub, dict) and "key" in pub:
                        publisher_olid = pub["key"]
                        break

            if "authors" in work_data:
                authors = work_data["authors"]

                if len(authors) >= 1:
                    a1 = authors[0]
                    if "author" in a1 and "key" in a1["author"]:
                        author_1_olid = a1["author"]["key"]
                        a1_data = get_author_info_from_authorid(author_1_olid)
                        if isinstance(a1_data, dict):
                            author_1 = a1_data.get("personal_name", "")

                            if author_1 == '':
                                author_1 = a1_data.get("name", "")

                            if ',' in author_1:
                                name_list = str(author_1).split(',')
                                first_name = name_list[1].strip()
                                last_name = name_list[0].strip()
                                author_1 = first_name + ' ' + last_name

                if len(authors) >= 2:
                    a2 = authors[1]
                    if "author" in a2 and "key" in a2["author"]:
                        author_2_olid = a2["author"]["key"]
                        a2_data = get_author_info_from_authorid(author_2_olid)
                        if isinstance(a2_data, dict):
                            author_2 = a2_data.get("personal_name", "")

                            if author_2 == '':
                                author_2 = a2_data.get("name", "")

                            if ',' in str(author_2):
                                name_list = str(author_2).split(',')
                                first_name = name_list[1].strip()
                                last_name = name_list[0].strip()
                                author_2 = first_name + ' ' + last_name

    return {
        "Title": title,
        "Author_1": author_1,
        "Author_1_OLID": author_1_olid,
        "Author_2": author_2,
        "Author_2_OLID": author_2_olid,
        "Publisher": publisher,
        "Publisher_OLID": publisher_olid,
        "Summary": summary,
        "Publish_Year": publish_year,
        "Cover_Image_URL": cover_image_url
    }

def complete_books_from_title_ol(query, limit=5):
    search_results = search_books_by_title(query=query, limit=limit)

    if "error" in search_results:
        return search_results

    if "docs" not in search_results or len(search_results["docs"]) == 0:
        return {"error": "No search results found for the given title."}

    docs = search_results["docs"]
    final_results = {}

    for index, result in enumerate(docs, start=1):
        cover_edition_key = result.get('cover_edition_key')

        # When there is no cover edition key, iterate to the next
        # result since it is not usable without one
        if cover_edition_key is None:
            continue

        # Get book information about on result cover edition key
        cover_edition_result = get_book_info_from_cover_key(cover_edition_key)

        title = cover_edition_result.get("title")
        if title is None:
            continue

        # Not sure if we should have first year or publish year of this edition
        publish_year = result.get("first_publish_year")
        if publish_year is None:
            continue

        isbn = cover_edition_result.get('isbn_13')
        if isbn is not None:
            isbn = isbn[0]
        else:
            # Try to get an ISBN 10 number if ISBN 13 not available
            isbn = cover_edition_result.get('isbn_10')
            if isbn is not None:
                isbn = isbn[0]
            else:
                continue


        publisher = cover_edition_result.get('publishers')
        if publisher is not None:
            publisher = publisher[0]
        else:
            continue

        cover_image_url = None
        if "cover_i" in result:
            cover_id = result["cover_i"]
            cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        work_key = result.get("key")

        author_1 = None
        author_1_olid = None
        author_2 = None
        author_2_olid = None
        publisher_olid = None
        summary = None

        if work_key:
            work_data = get_work_data(work_key)

            if isinstance(work_data, dict):

                if "description" in work_data:
                    if isinstance(work_data["description"], dict):
                        summary = work_data["description"].get("value")
                    else:
                        summary = work_data["description"]

                if "publishers" in work_data:
                    for pub in work_data["publishers"]:
                        if isinstance(pub, dict) and "key" in pub:
                            publisher_olid = pub["key"]
                            break

                if "authors" in work_data:
                    authors = work_data["authors"]

                    if len(authors) >= 1:
                        a1 = authors[0]
                        if "author" in a1 and "key" in a1["author"]:
                            author_1_olid = a1["author"]["key"]
                            a1_data = get_author_info_from_authorid(author_1_olid)
                            if isinstance(a1_data, dict):
                                author_1 = a1_data.get("personal_name", "")

                                if author_1 == '':
                                    author_1 = a1_data.get("name", "")

                                if ',' in author_1:
                                    name_list = str(author_1).split(',')
                                    first_name = name_list[1].strip()
                                    last_name = name_list[0].strip()
                                    author_1 = first_name + ' ' + last_name


                    if len(authors) >= 2:
                        a2 = authors[1]
                        if "author" in a2 and "key" in a2["author"]:
                            author_2_olid = a2["author"]["key"]
                            a2_data = get_author_info_from_authorid(author_2_olid)
                            if isinstance(a2_data, dict):
                                author_2 = a2_data.get("personal_name", "")

                                if author_2 == '':
                                    author_2 = a2_data.get("name", "")

                                if ',' in str(author_2):
                                    name_list = str(author_2).split(',')
                                    first_name = name_list[1].strip()
                                    last_name = name_list[0].strip()
                                    author_2 = first_name + ' ' + last_name

        final_results[f"Book_Result_{index}"] = {
            "Title": title,
            "Publish_Year": publish_year,
            "ISBN": isbn,
            "Publisher": publisher,
            "Publisher_OLID": publisher_olid,
            "Author_1": author_1,
            "Author_1_OLID": author_1_olid,
            "Author_2": author_2,
            "Author_2_OLID": author_2_olid,
            "Summary": summary,
            "Cover_Image_URL": cover_image_url
        }

    return final_results

def complete_books_from_author_ol(first_name, last_name, limit=5):
    search_results = search_books_by_author(first_name, last_name, limit=limit)

    if "error" in search_results:
        return search_results

    if "docs" not in search_results or len(search_results["docs"]) == 0:
        return {"error": "No search results found for the given author."}

    docs = search_results["docs"]
    final_results = {}

    for index, result in enumerate(docs, start=1):
        cover_edition_key = result.get('cover_edition_key')

        # When there is no cover edition key, iterate to the next
        # result since it is not usable without one
        if cover_edition_key is None:
            continue

        # Get book information about on result cover edition key
        cover_edition_result = get_book_info_from_cover_key(cover_edition_key)

        title = cover_edition_result.get("title")
        if title is None:
            continue

        # Not sure if we should have first year or publish year of this edition
        publish_year = result.get("first_publish_year")
        if publish_year is None:
            continue

        isbn = cover_edition_result.get('isbn_13')
        if isbn is not None:
            isbn = isbn[0]
        else:
            # Try to get an ISBN 10 number if ISBN 13 not available
            isbn = cover_edition_result.get('isbn_10')
            if isbn is not None:
                isbn = isbn[0]
            else:
                continue


        publisher = cover_edition_result.get('publishers')
        if publisher is not None:
            publisher = publisher[0]
        else:
            continue

        cover_image_url = None
        if "cover_i" in result:
            cover_id = result["cover_i"]
            cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        work_key = result.get("key")

        author_1 = None
        author_1_olid = None
        author_2 = None
        author_2_olid = None
        publisher_olid = None
        summary = None

        if work_key:
            work_data = get_work_data(work_key)

            if isinstance(work_data, dict):

                if "description" in work_data:
                    if isinstance(work_data["description"], dict):
                        summary = work_data["description"].get("value")
                    else:
                        summary = work_data["description"]

                if "publishers" in work_data:
                    for pub in work_data["publishers"]:
                        if isinstance(pub, dict) and "key" in pub:
                            publisher_olid = pub["key"]
                            break

                if "authors" in work_data:
                    authors = work_data["authors"]

                    if len(authors) >= 1:
                        a1 = authors[0]
                        if "author" in a1 and "key" in a1["author"]:
                            author_1_olid = a1["author"]["key"]
                            a1_data = get_author_info_from_authorid(author_1_olid)
                            if isinstance(a1_data, dict):
                                author_1 = a1_data.get("personal_name", "")

                                if author_1 == '':
                                    author_1 = a1_data.get("name", "")

                                if ',' in author_1:
                                    name_list = str(author_1).split(',')
                                    first_name = name_list[1].strip()
                                    last_name = name_list[0].strip()
                                    author_1 = first_name + ' ' + last_name

                    if len(authors) >= 2:
                        a2 = authors[1]
                        if "author" in a2 and "key" in a2["author"]:
                            author_2_olid = a2["author"]["key"]
                            a2_data = get_author_info_from_authorid(author_2_olid)
                            if isinstance(a2_data, dict):
                                author_2 = a2_data.get("personal_name", "")

                                if author_2 == '':
                                    author_2 = a2_data.get("name", "")

                                if ',' in str(author_2):
                                    name_list = str(author_2).split(',')
                                    first_name = name_list[1].strip()
                                    last_name = name_list[0].strip()
                                    author_2 = first_name + ' ' + last_name

        final_results[f"Book_Result_{index}"] = {
            "Title": title,
            "Publish_Year": publish_year,
            "ISBN": isbn,
            "Publisher": publisher,
            "Publisher_OLID": publisher_olid,
            "Author_1": author_1,
            "Author_1_OLID": author_1_olid,
            "Author_2": author_2,
            "Author_2_OLID": author_2_olid,
            "Summary": summary,
            "Cover_Image_URL": cover_image_url
        }

    return final_results