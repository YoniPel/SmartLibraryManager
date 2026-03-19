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

    if raw_data.get('totalItems', 0) == 0:
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

            _update_book_dict_from_data(book_details, data)

    # if we didn't find the data from Google Books API, use a default data
    book_details["title"] = book_details["title"] or "שם ספר לא ידוע"
    _update_default_values_to_book_dict(book_details)
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

    if raw_data.get('totalItems', 0) == 0:
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

    # checks for the right book
    found_book = False

    if "items" in raw_data:
        for item in raw_data['items']:
            data = item['volumeInfo']

            if title in data['title']:
                found_book = True
                _update_book_dict_from_data(book_details, data)

                if not book_details["isbn"]:
                    book_details["isbn"] = _extract_isbn_from_data(data)

                # if we found all of the values, no need to keep looking
                if all(book_details.values()):
                    break

    if not found_book:
        return None

    # if we didn't find the data from Google Books API, use a default data
    _update_default_values_to_book_dict(book_details)
    book_details["isbn"] = book_details["isbn"] or None

    return book_details


def _update_book_dict_from_data(book_details, data):
    """
    the function updates the book_details dict based on data
    :param book_details: book_details dict
    :param data: the 'volumeInfo' key in item inside the response from Google Books
    :return: updates the dict based on the values inside data
    """
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


def _update_default_values_to_book_dict(book_details):
    """
    the function updates the values of some of the key in book_details in case the data wasn't found in Google Books
    :param book_details: book_details dict
    :return: updates the dict with default values
    """
    book_details["author"] = book_details["author"] or "מחבר לא ידוע"
    book_details["page_count"] = book_details["page_count"] or 0
    book_details["cover_image"] = book_details["cover_image"] or None


def _extract_isbn_from_data(data):
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
