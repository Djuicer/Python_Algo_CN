"""
自幂
Problem 48

级数 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317。

求级数 1^1 + 2^2 + 3^3 + ... + 1000^1000 的最后十位数字。
"""


def solution():
    """
    返回级数 1^1 + 2^2 + 3^3 + ... + 1000^1000 的最后 10 位数字。

    >>> solution()
    '9110846700'
    """
    total = 0
    for i in range(1, 1001):
        total += i**i
    return str(total)[-10:]


if __name__ == "__main__":
    print(solution())
