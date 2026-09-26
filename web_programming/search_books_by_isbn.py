"""
从 https://openlibrary.org 获取图书和作者数据。

ISBN: https://en.wikipedia.org/wiki/International_Standard_Book_Number
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

from json import JSONDecodeError

import httpx2


def get_openlibrary_data(olid: str = "isbn/0140328726") -> dict:
    """
    给定 'isbn/0140328726'，以 Python 字典返回 Open Library 图书数据。
    给定 '/authors/OL34184A'，以 Python 字典返回作者数据。
    此代码必须同时支持带或不带前导斜杠 ('/') 的 olid。

    # 若 doctest 耗时过长或结果可能变化，则将其注释掉
    # >>> get_openlibrary_data(olid='isbn/0140328726')  # doctest: +ELLIPSIS
    {'publishers': ['Puffin'], 'number_of_pages': 96, 'isbn_10': ['0140328726'], ...
    # >>> get_openlibrary_data(olid='/authors/OL7353617A')  # doctest: +ELLIPSIS
    {'name': 'Adrian Brisku', 'created': {'type': '/type/datetime', ...
    """
    new_olid = olid.strip().strip("/")  # 移除首尾空白和斜杠
    if new_olid.count("/") != 1:
        msg = f"{olid} is not a valid Open Library olid"
        raise ValueError(msg)
    return httpx2.get(
        f"https://openlibrary.org/{new_olid}.json", timeout=10, follow_redirects=True
    ).json()


def summarize_book(ol_book_data: dict) -> dict:
    """
    给定 Open Library 图书数据，以 Python 字典返回摘要。
    """
    desired_keys = {
        "title": "Title",
        "publish_date": "Publish date",
        "authors": "Authors",
        "number_of_pages": "Number of pages",
        "isbn_10": "ISBN (10)",
        "isbn_13": "ISBN (13)",
    }
    data = {better_key: ol_book_data[key] for key, better_key in desired_keys.items()}
    data["Authors"] = [
        get_openlibrary_data(author["key"])["name"] for author in data["Authors"]
    ]
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = ", ".join(value)
    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    while True:
        isbn = input("\nEnter the ISBN code to search (or 'quit' to stop): ").strip()
        if isbn.lower() in ("", "q", "quit", "exit", "stop"):
            break

        if len(isbn) not in (10, 13) or not isbn.isdigit():
            print(f"Sorry, {isbn} is not a valid ISBN.  Please, input a valid ISBN.")
            continue

        print(f"\nSearching Open Library for ISBN: {isbn}...\n")

        try:
            book_summary = summarize_book(get_openlibrary_data(f"isbn/{isbn}"))
            print("\n".join(f"{key}: {value}" for key, value in book_summary.items()))
        except JSONDecodeError:
            print(f"Sorry, there are no results for ISBN: {isbn}.")
