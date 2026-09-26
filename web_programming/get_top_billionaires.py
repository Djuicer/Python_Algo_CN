"""
注意：可能出现 json.decoding 错误。
此代码在部分环境中可用，在其他环境中可能失败。
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
#     "rich",
# ]
# ///

from datetime import UTC, date, datetime

import httpx2
from rich import box
from rich import console as rich_console
from rich import table as rich_table

LIMIT = 10
TODAY = datetime.now(tz=UTC)
API_URL = (
    "https://www.forbes.com/forbesapi/person/rtb/0/position/true.json"
    "?fields=personName,gender,source,countryOfCitizenship,birthDate,finalWorth"
    f"&limit={LIMIT}"
)


def years_old(birth_timestamp: int, today: date | None = None) -> int:
    """
    根据给定出生日期计算周岁。计算仅使用年、月、日，忽略一天中的具体时间。

    参数：
        birth_timestamp: 出生日期。
        today: 可用于编写测试；为 None 时使用 datetime.date.today()。

    返回：
        int: 周岁年龄。

    示例：
    >>> today = date(2024, 1, 12)
    >>> years_old(birth_timestamp=datetime(1959, 11, 20).timestamp(), today=today)
    64
    >>> years_old(birth_timestamp=datetime(1970, 2, 13).timestamp(), today=today)
    53
    >>> all(
    ...     years_old(datetime(today.year - i, 1, 12).timestamp(), today=today) == i
    ...     for i in range(1, 111)
    ... )
    True
    """
    today = today or TODAY.date()
    birth_date = datetime.fromtimestamp(birth_timestamp, tz=UTC).date()
    return (today.year - birth_date.year) - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def get_forbes_real_time_billionaires() -> list[dict[str, int | str]]:
    """
    使用 Forbes API 获取实时排名前 10 的亿万富豪。

    返回：
        实时排名前 10 的亿万富豪数据列表。
    """
    response_json = httpx2.get(API_URL, timeout=10).json()
    return [
        {
            "Name": person["personName"],
            "Source": person["source"],
            "Country": person["countryOfCitizenship"],
            "Gender": person["gender"],
            "Worth ($)": f"{person['finalWorth'] / 1000:.1f} Billion",
            "Age": str(years_old(person["birthDate"] / 1000)),
        }
        for person in response_json["personList"]["personsLists"]
    ]


def display_billionaires(forbes_billionaires: list[dict[str, int | str]]) -> None:
    """
    在 rich 表格中显示 Forbes 实时亿万富豪信息。

    参数：
        forbes_billionaires (list): Forbes 实时排名前 10 的亿万富豪
    """

    table = rich_table.Table(
        title=f"Forbes Top {LIMIT} Real-Time Billionaires at {TODAY:%Y-%m-%d %H:%M}",
        style="green",
        highlight=True,
        box=box.SQUARE,
    )
    for key in forbes_billionaires[0]:
        table.add_column(key)

    for billionaire in forbes_billionaires:
        table.add_row(*billionaire.values())

    rich_console.Console().print(table)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    display_billionaires(get_forbes_real_time_billionaires())
