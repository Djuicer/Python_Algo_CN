"""
根据职位名称和地点，从 Indeed 网站抓取职位信息。
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "httpx2",
# ]
# ///

from __future__ import annotations

from collections.abc import Generator

import httpx2
from bs4 import BeautifulSoup

url = "https://www.indeed.co.in/jobs?q=mobile+app+development&l="


def fetch_jobs(location: str = "mumbai") -> Generator[tuple[str, str]]:
    soup = BeautifulSoup(httpx2.get(url + location, timeout=10).content, "html.parser")
    # 此属性用于查找职位中列出的所有详细信息
    for job in soup.find_all("div", attrs={"data-tn-component": "organicJob"}):
        job_title = job.find("a", attrs={"data-tn-element": "jobTitle"}).text.strip()
        company_name = job.find("span", {"class": "company"}).text.strip()
        yield job_title, company_name


if __name__ == "__main__":
    for i, job in enumerate(fetch_jobs("Bangalore"), 1):
        print(f"Job {i:>2} is {job[0]} at {job[1]}")
