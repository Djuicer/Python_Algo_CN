"""
本文件从 " ZenQuotes API " 获取引语。它使用免费层级，无需 API 密钥。

有关更多详情和高级功能，请访问：
    https://zenquotes.io/
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

import pprint

import httpx2

API_ENDPOINT_URL = "https://zenquotes.io/api"


def quote_of_the_day() -> list:
    return httpx2.get(API_ENDPOINT_URL + "/today", timeout=10).json()


def random_quotes() -> list:
    return httpx2.get(API_ENDPOINT_URL + "/random", timeout=10).json()


if __name__ == "__main__":
    """
    response object has all the info with the quote
    To retrieve the actual quote access the response.json() object as below
    response.json() is a list of json object
        response.json()[0]['q'] = actual quote.
        response.json()[0]['a'] = author name.
        response.json()[0]['h'] = in html format.
    """
    response = random_quotes()
    pprint.pprint(response)
