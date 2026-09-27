"""
袋中有一个红色圆片和一个蓝色圆片。在一场概率游戏中，玩家随机取出一个圆片并记录颜色。
每轮结束后将圆片放回袋中，再加入一个红色圆片，然后再次随机取出一个圆片。

玩家支付 £1 参加游戏；游戏结束时，若取出的蓝色圆片多于红色圆片，则玩家获胜。

如果游戏进行四轮，玩家获胜概率恰为 11/120。因此，在预期出现亏损之前，庄家为胜者
分配的最高奖金应为 £10。注意，任何赔付都是整数英镑，并包含最初支付的 £1 游戏费，
所以在该示例中玩家实际赢得 £9。

求进行十五轮的单局游戏应分配的最高奖金。


解法：
    对每个由红蓝圆片组成且红色多于蓝色的 15 圆片序列，计算其概率并加入玩家获胜的
    总概率。如果庄家希望避免预期亏损，该概率的倒数即为奖金上界。
"""

from itertools import product


def solution(num_turns: int = 15) -> int:
    """
    求进行十五轮的单局游戏应分配的最高奖金。
    >>> solution(4)
    10
    >>> solution(10)
    225
    """
    total_prob: float = 0.0
    prob: float
    num_blue: int
    num_red: int
    ind: int
    col: int
    series: tuple[int, ...]

    for series in product(range(2), repeat=num_turns):
        num_blue = series.count(1)
        num_red = num_turns - num_blue
        if num_red >= num_blue:
            continue
        prob = 1.0
        for ind, col in enumerate(series, 2):
            if col == 0:
                prob *= (ind - 1) / ind
            else:
                prob *= 1 / ind

        total_prob += prob

    return int(1 / total_prob)


if __name__ == "__main__":
    print(f"{solution() = }")
