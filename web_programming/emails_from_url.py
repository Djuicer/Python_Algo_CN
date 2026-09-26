"""从 URL 获取站点的电子邮箱地址。"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

from __future__ import annotations

__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Alpha"

import re
from html.parser import HTMLParser
from urllib import parse

import httpx2


class Parser(HTMLParser):
    def __init__(self, domain: str) -> None:
        super().__init__()
        self.urls: list[str] = []
        self.domain = domain

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """
        解析 HTML，并从标签中提取 URL。
        """
        # 仅解析 'anchor' 标签
        if tag == "a":
            # 检查已定义的属性列表
            for name, value in attrs:
                # href 已定义、非空、不是 # 且不在 urls 中时处理
                if name == "href" and value not in (*self.urls, "", "#"):
                    url = parse.urljoin(self.domain, value)
                    self.urls.append(url)


# 获取主域名 (example.com)
def get_domain_name(url: str) -> str:
    """
    获取主域名。

    >>> get_domain_name("https://a.b.c.d/e/f?g=h,i=j#k")
    'c.d'
    >>> get_domain_name("Not a URL!")
    ''
    """
    return ".".join(get_sub_domain_name(url).split(".")[-2:])


# 获取子域名 (sub.example.com)
def get_sub_domain_name(url: str) -> str:
    """
    >>> get_sub_domain_name("https://a.b.c.d/e/f?g=h,i=j#k")
    'a.b.c.d'
    >>> get_sub_domain_name("Not a URL!")
    ''
    """
    return parse.urlparse(url).netloc


def emails_from_url(url: str = "https://github.com") -> list[str]:
    """
    接收 url 并返回所有有效 URL。
    """
    # 从 url 获取基础域名
    domain = get_domain_name(url)

    # 初始化解析器
    parser = Parser(domain)

    try:
        # 打开 URL
        r = httpx2.get(url, timeout=10, follow_redirects=True)

        # 将原始 HTML 交给解析器以获取链接
        parser.feed(r.text)

        # 获取并遍历链接
        valid_emails = set()
        for link in parser.urls:
            # 打开 URL
            # 检查链接是否已经是绝对 URL
            if not link.startswith("http://") and not link.startswith("https://"):
                # 链接以域名开头时仅补充协议，否则进行规范化
                if link.startswith(domain):
                    link = f"https://{link}"
                else:
                    link = parse.urljoin(f"https://{domain}", link)
            try:
                read = httpx2.get(link, timeout=10, follow_redirects=True)
                # 获取有效电子邮箱地址
                emails = re.findall("[a-zA-Z0-9]+@" + domain, read.text)
                # 不在集合中时添加
                for email in emails:
                    valid_emails.add(email)
            except ValueError:
                pass
    except ValueError:
        raise SystemExit(1)

    # 最后返回排序且去重后的电子邮箱地址列表
    return sorted(valid_emails)


if __name__ == "__main__":
    emails = emails_from_url("https://github.com")
    print(f"{len(emails)} emails found:")
    print("\n".join(sorted(emails)))
