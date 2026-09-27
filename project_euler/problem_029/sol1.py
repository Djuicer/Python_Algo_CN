"""
考虑满足 2 <= a <= 5 且 2 <= b <= 5 的所有整数幂 ab：

2^2=4,  2^3=8,   2^4=16,  2^5=32
3^2=9,  3^3=27,  3^4=81,  3^5=243
4^2=16, 4^3=64,  4^4=256, 4^5=1024
5^2=25, 5^3=125, 5^4=625, 5^5=3125

将它们按数值排序并去除重复项，可得到以下包含 15 个不同项的数列：

4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243, 256, 625, 1024, 3125

满足 2 <= a <= 100 且 2 <= b <= 100 的 ab 所生成的数列中有多少个不同项？
"""


def solution(n: int = 100) -> int:
    """返回满足 2 <= a <= 100 且 2 <= b <= 100 的 a^b 数列中的不同项数。

    >>> solution(100)
    9183
    >>> solution(50)
    2184
    >>> solution(20)
    324
    >>> solution(5)
    15
    >>> solution(2)
    1
    >>> solution(1)
    0
    """
    collect_powers = set()

    current_pow = 0

    n = n + 1  # 最大上界

    for a in range(2, n):
        for b in range(2, n):
            current_pow = a**b  # 计算当前幂
            collect_powers.add(current_pow)  # 将结果加入集合
    return len(collect_powers)


if __name__ == "__main__":
    print("Number of terms ", solution(int(str(input()).strip())))
