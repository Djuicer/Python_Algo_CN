"""
从英国 CarbonIntensity API 获取 CO2 排放数据。
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

from datetime import date

import httpx2

BASE_URL = "https://api.carbonintensity.org.uk/intensity"


# 最近半小时的排放量
def fetch_last_half_hour() -> str:
    last_half_hour = httpx2.get(BASE_URL, timeout=10).json()["data"][0]
    return last_half_hour["intensity"]["actual"]


# 指定日期范围内的排放量
def fetch_from_to(start, end) -> list:
    return httpx2.get(f"{BASE_URL}/{start}/{end}", timeout=10).json()["data"]


if __name__ == "__main__":
    for entry in fetch_from_to(start=date(2020, 10, 1), end=date(2020, 10, 3)):
        print("from {from} to {to}: {intensity[actual]}".format(**entry))
    print(f"{fetch_last_half_hour() = }")
