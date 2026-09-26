"""
根据出版物标题、出版年份、期刊卷号和页码，从 Google Scholar 获取引用次数。
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "httpx2",
# ]
# ///

import httpx2
from bs4 import BeautifulSoup


def get_citation(base_url: str, params: dict) -> str:
    """
    根据出版物标题、期刊、卷号、页码和出版年份返回其引用次数。

    参数：
    - base_url: 向 Google Scholar 发起请求的基础 URL。
    - params: 包含出版物信息的字典。

    返回：
    - 包含引用次数的字符串。
    """
    # 使用指定参数向 URL 发送 GET 请求
    soup = BeautifulSoup(
        httpx2.get(base_url, params=params, timeout=10).content, "html.parser"
    )
    # 查找包含引用信息、class 为 'gs_ri' 的 div 元素
    div = soup.find("div", attrs={"class": "gs_ri"})
    # 查找 div 中的所有链接，并获取第三个链接（引用次数）
    anchors = div.find("div", attrs={"class": "gs_fl"}).find_all("a")
    return anchors[2].get_text()  # 返回第三个链接的文本


if __name__ == "__main__":
    # 定义待查询引用次数的出版物参数
    params = {
        "title": (
            "Precisely geometry controlled microsupercapacitors for ultrahigh areal "
            "capacitance, volumetric capacitance, and energy density"
        ),
        "journal": "Chem. Mater.",
        "volume": 30,
        "pages": "3979-3990",
        "year": 2018,
        "hl": "en",  # 使用的语言（英语）
    }
    # 使用指定 URL 和参数调用 get_citation 函数
    print(get_citation("https://scholar.google.com/scholar_lookup", params=params))
