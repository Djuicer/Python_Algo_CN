# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

import httpx2


def get_apod_data(api_key: str) -> dict:
    """
    获取 APOD（每日天文图片）数据。
    从 https://api.nasa.gov/ 获取 API 密钥。
    """
    url = "https://api.nasa.gov/planetary/apod"
    return httpx2.get(url, params={"api_key": api_key}, timeout=10).json()


def save_apod(api_key: str, path: str = ".") -> dict:
    apod_data = get_apod_data(api_key)
    img_url = apod_data["url"]
    img_name = img_url.split("/")[-1]
    response = httpx2.get(img_url, timeout=10)

    with open(f"{path}/{img_name}", "wb+") as img_file:
        img_file.write(response.content)
    del response
    return apod_data


def get_archive_data(query: str) -> dict:
    """
    从 NASA 归档中获取特定查询的数据。
    """
    url = "https://images-api.nasa.gov/search"
    return httpx2.get(url, params={"q": query}, timeout=10).json()


if __name__ == "__main__":
    print(save_apod("YOUR API KEY"))
    apollo_2011_items = get_archive_data("apollo 2011")["collection"]["items"]
    print(apollo_2011_items[0]["data"][0]["description"])
