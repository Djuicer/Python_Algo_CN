"""
在飞镖游戏中，玩家向靶盘投掷三支飞镖；靶盘被均分为二十个区域，编号从一到二十。
￼
飞镖的得分由其落点所在区域的编号决定。落在红色/绿色外环之外得零分。该环内的黑色和
米色区域表示单倍得分，而红色/绿色外环与中环分别表示双倍和三倍得分。

靶盘中心有两个同心圆，称为牛眼区（bull region 或 bulls-eye）。外牛眼值 25 分，
内牛眼为双倍区，值 50 分。

规则有许多变体，但最流行的玩法中，玩家从 301 或 501 分开始，率先将累计分数减至零者
获胜。不过通常采用“双倍结束”规则，即玩家最后一支飞镖必须命中双倍区（包括靶盘中心
的双倍牛眼）才能获胜；若其他飞镖使累计分数降至一或更低，则该组三支飞镖记为“爆镖”。

玩家能够以当前分数结束比赛时称为“结镖”（checkout）；最高结镖分数为 170：
T20 T20 D25（两个三倍 20 和一个双倍牛眼）。

恰有十一种不同方式可以从 6 分结镖：

D3
D1  D2
S2  D2
D2  D1
S4  D1
S1  S1  D2
S1  T1  D1
S1  S3  D1
D1  D1  D1
D1  S2  D1
S2  S2  D1

注意，D1 D2 与 D2 D1 的结束双倍区不同，因此视为不同方式；但组合 S1 T1 D1
与 T1 S1 D1 视为相同方式。

此外，考虑组合时不计脱靶；例如，D3 与 0 D3、0 0 D3 相同。

令人难以置信的是，结镖方式总计有 42336 种。

玩家从小于 100 的分数结镖有多少种不同方式？

解法：
    首先按类型分别构造可能的飞镖分值列表。然后遍历双倍区以及后续可能的 2 次投掷。
    如果这三支飞镖的总分小于给定上限，则增加计数器。
"""

from itertools import combinations_with_replacement


def solution(limit: int = 100) -> int:
    """
    计算玩家从小于 limit 的分数结镖时不同方式的数量。
    >>> solution(171)
    42336
    >>> solution(50)
    12577
    """
    singles: list[int] = [*list(range(1, 21)), 25]
    doubles: list[int] = [2 * x for x in range(1, 21)] + [50]
    triples: list[int] = [3 * x for x in range(1, 21)]
    all_values: list[int] = singles + doubles + triples + [0]

    num_checkouts: int = 0
    double: int
    throw1: int
    throw2: int
    checkout_total: int

    for double in doubles:
        for throw1, throw2 in combinations_with_replacement(all_values, 2):
            checkout_total = double + throw1 + throw2
            if checkout_total < limit:
                num_checkouts += 1

    return num_checkouts


if __name__ == "__main__":
    print(f"{solution() = }")
