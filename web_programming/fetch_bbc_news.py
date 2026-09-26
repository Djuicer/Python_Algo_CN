# Created by sarathkaul on 12/11/19

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

import httpx2

_NEWS_API = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey="


def fetch_bbc_news(bbc_news_api_key: str) -> None:
# 获取 JSON 格式的文章列表
    bbc_news_page = httpx2.get(_NEWS_API + bbc_news_api_key, timeout=10).json()
    # 列表中的每篇文章都是字典
    for i, article in enumerate(bbc_news_page["articles"], 1):
        print(f"{i}.) {article['title']}")


if __name__ == "__main__":
    fetch_bbc_news(bbc_news_api_key="<Your BBC News API key goes here>")
