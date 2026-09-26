# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "httpx2",
# ]
# ///

import json
import os
import re
import sys
import urllib.request

import httpx2
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def download_images_from_google_query(query: str = "dhaka", max_images: int = 5) -> int:
    """
    使用给定查询词搜索 Google，并将图片下载到文件夹中。

    参数：
         query : 用户提供的图片搜索词，默认为 "dhaka"。
        image_numbers : [说明]，默认为 5。

    返回：
        成功下载的图片数量。

    # 注释掉运行缓慢（调用耗时 4.20 秒）的 doctest
    # >>> download_images_from_google_query()
    5
    # >>> download_images_from_google_query("potato")
    5
    """
    max_images = min(max_images, 50)  # 防止滥用！
    params = {
        "q": query,
        "tbm": "isch",
        "hl": "en",
        "ijn": "0",
    }

    html = httpx2.get(
        "https://www.google.com/search", params=params, headers=headers, timeout=10
    )
    soup = BeautifulSoup(html.text, "html.parser")
    matched_images_data = "".join(
        re.findall(r"AF_initDataCallback\(([^<]+)\);", str(soup.select("script")))
    )

    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    matched_google_image_data = re.findall(
        r"\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",",
        matched_images_data_json,
    )
    if not matched_google_image_data:
        return 0

    removed_matched_google_images_thumbnails = re.sub(
        r"\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]",
        "",
        str(matched_google_image_data),
    )

    matched_google_full_resolution_images = re.findall(
        r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
        removed_matched_google_images_thumbnails,
    )
    for index, fixed_full_res_image in enumerate(matched_google_full_resolution_images):
        if index >= max_images:
            return index
        original_size_img_not_fixed = bytes(fixed_full_res_image, "ascii").decode(
            "unicode-escape"
        )
        original_size_img = bytes(original_size_img_not_fixed, "ascii").decode(
            "unicode-escape"
        )
        opener = urllib.request.build_opener()
        opener.addheaders = [
            (
                "User-Agent",
                (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    " (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
                    " Edge/18.19582"
                ),
            )
        ]
        urllib.request.install_opener(opener)
        path_name = f"query_{query.replace(' ', '_')}"
        if not os.path.exists(path_name):
            os.makedirs(path_name)
        urllib.request.urlretrieve(  # noqa: S310
            original_size_img, f"{path_name}/original_size_img_{index}.jpg"
        )
    return index


if __name__ == "__main__":
    try:
        image_count = download_images_from_google_query(sys.argv[1])
        print(f"{image_count} images were downloaded to disk.")
    except IndexError:
        print("Please provide a search term.")
        raise
