"""
统计星期日
Problem 19

已知以下信息，你也可以自行查阅相关资料。

1900 年 1 月 1 日是星期一。
九月有三十天，
四月、六月和十一月也是如此。
其余月份有三十一天，
唯有二月例外，
平年二十八天，
闰年则为二十九天。

能被 4 整除的年份是闰年，但世纪年份必须能被 400 整除才是闰年。

在二十世纪（1901 年 1 月 1 日至 2000 年 12 月 31 日）期间，有多少个月的 1 日是星期日？
"""


def solution():
    """返回二十世纪（1901 年 1 月 1 日至 2000 年 12 月 31 日）期间每月 1 日为星期一的次数。

    >>> solution()
    171
    """
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    day = 6
    month = 1
    year = 1901

    sundays = 0

    while year < 2001:
        day += 7

        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            if day > days_per_month[month - 1] and month != 2:
                month += 1
                day = day - days_per_month[month - 2]
            elif day > 29 and month == 2:
                month += 1
                day = day - 29
        elif day > days_per_month[month - 1]:
            month += 1
            day = day - days_per_month[month - 2]

        if month > 12:
            year += 1
            month = 1

        if year < 2001 and day == 1:
            sundays += 1
    return sundays


if __name__ == "__main__":
    print(solution())
