"""
获奖字符串
Problem 191

某学校向出勤和守时表现良好的学生提供现金奖励。如果连续三天缺席，或迟到超过一次，
则失去奖励资格。

在 n 天期间，为每个学生生成一个三元字符串，由 L（迟到）、O（准时）和 A（缺席）组成。

尽管 4 天期间可形成八十一个三元字符串，但恰有四十三个字符串可以获奖：

OOOO OOOA OOOL OOAO OOAA OOAL OOLO OOLA OAOO OAOA
OAOL OAAO OAAL OALO OALA OLOO OLOA OLAO OLAA AOOO
AOOA AOOL AOAO AOAA AOAL AOLO AOLA AAOO AAOA AAOL
AALO AALA ALOO ALOA ALAO ALAA LOOO LOOA LOAO LOAA
LAOO LAOA LAAO

30 天期间存在多少个“获奖”字符串？

References:
    - The original Project Euler project page:
      https://projecteuler.net/problem=191
"""

cache: dict[tuple[int, int, int], int] = {}


def _calculate(days: int, absent: int, late: int) -> int:
    """
    一个用于递归的小型辅助函数，主要用于为下方的 solution() 函数提供简洁接口。

    调用时应传入天数（对应所需“获奖字符串”的长度）、连续缺席天数的初始值，
    以及迟到总天数的初始值。

    >>> _calculate(days=4, absent=0, late=0)
    43
    >>> _calculate(days=30, absent=2, late=0)
    0
    >>> _calculate(days=30, absent=1, late=0)
    98950096
    """

    # 如果缺席两次，或连续迟到 3 天，则不再可能产生获奖字符串
    if late == 3 or absent == 2:
        return 0

    # 如果已无剩余天数且未违反其他规则，则得到一个获奖字符串
    if days == 0:
        return 1

    # 没有简便解法，因此需要进行递归计算

    # 首先检查该组合是否已在缓存中；若是，则返回所存值，
    # 因为从当前状态开始的可能获奖字符串数量已经确定
    key = (days, absent, late)
    if key in cache:
        return cache[key]

    # 根据今天的出勤情况，计算从当前状态开始的三种可能分支

    # 1) 如果迟到（但未缺席），"absent" 计数器保持不变，"late" 计数器增加一
    state_late = _calculate(days - 1, absent, late + 1)

    # 2) 如果缺席，"absent" 计数器增加 1，"late" 计数器重置为 0
    state_absent = _calculate(days - 1, absent + 1, 0)

    # 3) 如果准时，重置 "late" 计数器并保持 absent 计数器不变
    state_ontime = _calculate(days - 1, absent, 0)

    prizestrings = state_late + state_absent + state_ontime

    cache[key] = prizestrings
    return prizestrings


def solution(days: int = 30) -> int:
    """
    使用带缓存的简单递归函数，返回给定天数下可能的获奖字符串数量。

    >>> solution()
    1918080160
    >>> solution(4)
    43
    """

    return _calculate(days, absent=0, late=0)


if __name__ == "__main__":
    print(solution())
