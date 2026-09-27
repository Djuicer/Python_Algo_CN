"""
5 位数 16807=75 同时也是五次幂。类似地，9 位数 134217728=89 是九次幂。
有多少个 n 位正整数同时也是 n 次幂？
"""

"""
最大底数可以是 9，因为所有 n 位数 < 10^n。
由于 9**23 有 22 位，因此最大幂可以是 22。
利用这些结论计算结果。
"""


def solution(max_base: int = 10, max_power: int = 22) -> int:
    """
    返回所有同时为 n 次幂的 n 位数的数量。
    >>> solution(10, 22)
    49
    >>> solution(0, 0)
    0
    >>> solution(1, 1)
    0
    >>> solution(-1, -1)
    0
    """
    bases = range(1, max_base)
    powers = range(1, max_power)
    return sum(
        1 for power in powers for base in bases if len(str(base**power)) == power
    )


if __name__ == "__main__":
    print(f"{solution(10, 22) = }")
