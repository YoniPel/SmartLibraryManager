import requests
from django.conf import settings


def fetch_book_details_by_isbn(isbn):
    """
    The function uses Google Books API in order to retrieve information about the book using the ISBN as the identifier.
    Because every ISBN can contain more than one result, we use all of the results in order to retrieve the information.
    It means that if one parameter doesn't appear in the first result, the function will check in the other results
    in order to find the parameter there.
    :param isbn: the isbn of the specified book
    :return: a dictionary that contains information about the book
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={settings.GOOGLE_BOOKS_API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        raw_data = response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        return None

    book_details = {
        "title": None,
        "author": None,
        "description": None,
        "published_date": None,
        "page_count": None,
        "cover_image": None,
        "isbn": isbn
    }

    if "items" in raw_data:
        for item in raw_data['items']:
            data = item['volumeInfo']

            if not book_details["title"]:
                book_details["title"] = data.get("title", None)

            if not book_details["author"]:
                authors = data.get("authors", [])
                author = authors[0] if authors else None
                book_details["author"] = author

            if not book_details["description"]:
                book_details["description"] = data.get("description", None)

            if not book_details["published_date"]:
                book_details["published_date"] = data.get("publishedDate", None)

            if not book_details["page_count"]:
                book_details["page_count"] = data.get("pageCount", None)

            if not book_details["cover_image"]:
                image_links = data.get("imageLinks", {})
                thumbnail = image_links.get("thumbnail")
                if thumbnail:
                    # because we use https, if we will try to use an image from http it will failed
                    secure_thumbnail = thumbnail.replace("http://", "https://")
                    book_details["cover_image"] = secure_thumbnail

    # if we didn't find the data from Google Books API, use a default data
    book_details["title"] = book_details["title"] or "שם ספר לא ידוע"
    book_details["author"] = book_details["author"] or "מחבר לא ידוע"
    book_details["page_count"] = book_details["page_count"] or "מספר עמודים לא ידוע"
    book_details["cover_image"] = book_details["cover_image"] or "אין תמונה זמינה לספר"

    return book_details


def fetch_book_details_by_book_name(title):
    """
    The function uses Google Books API in order to retrieve information about the book using the name of the book
    as the identifier. Because every name can contain more than one result, we use all of the results in order to
    retrieve the information. It means that if one parameter doesn't appear in the first result, the function will check
     in the other results in order to find the parameter there.
    :param title the name of the specified book
    :return: a dictionary that contains information about the book
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key={settings.GOOGLE_BOOKS_API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        raw_data = response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        return None

    book_details = {
        "title": title,
        "author": None,
        "description": None,
        "published_date": None,
        "page_count": None,
        "cover_image": None,
        "isbn": None
    }

    if "items" in raw_data:
        for item in raw_data['items']:
            data = item['volumeInfo']

            if not book_details["author"]:
                authors = data.get("authors", [])
                author = authors[0] if authors else None
                book_details["author"] = author

            if not book_details["description"]:
                book_details["description"] = data.get("description", None)

            if not book_details["published_date"]:
                book_details["published_date"] = data.get("publishedDate", None)

            if not book_details["page_count"]:
                book_details["page_count"] = data.get("pageCount", None)

            if not book_details["cover_image"]:
                image_links = data.get("imageLinks", {})
                thumbnail = image_links.get("thumbnail")
                if thumbnail:
                    # because we use https, if we will try to use an image from http it will failed
                    secure_thumbnail = thumbnail.replace("http://", "https://")
                    book_details["cover_image"] = secure_thumbnail

            if not book_details["isbn"]:
                book_details["isbn"] = extract_isbn_from_data(data)

    # if we didn't find the data from Google Books API, use a default data
    book_details["author"] = book_details["author"] or "מחבר לא ידוע"
    book_details["page_count"] = book_details["page_count"] or "מספר עמודים לא ידוע"
    book_details["cover_image"] = book_details["cover_image"] or "אין תמונה זמינה לספר"
    book_details["isbn"] = book_details["isbn"] or "לא נמצא מזהה ISBN"

    return book_details


def extract_isbn_from_data(data):
    """
    The function tries to retrieve isbn_13 if possible, if not, isbn_10
    :param data: the volumeInfo dictionary
    :return: isbn
    """
    identifiers_list = data.get("industryIdentifiers", [])
    isbn_10 = None

    if identifiers_list:

        for identifier_dict in identifiers_list:

            if identifier_dict["type"] == "ISBN_13":
                return identifier_dict["identifier"]
            if identifier_dict["type"] == "ISBN_10":
                isbn_10 = identifier_dict["identifier"]

        return isbn_10

    return None


