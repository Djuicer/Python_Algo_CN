"""
组合选择

Problem 47

最先具有两个不同素因数的两个连续整数是：

14 = 2 x 7
15 = 3 x 5

最先具有三个不同素因数的三个连续整数是：

644 = 2² x 7 x 23
645 = 3 x 5 x 43
646 = 2 x 17 x 19.

找出最先出现的四个连续整数，使每个整数都有四个不同的素因数。
其中第一个数是多少？
"""

from functools import lru_cache


def unique_prime_factors(n: int) -> set:
    """
    查找一个整数的不同素因数。
    测试中包含排序，因为只关心集合，不关心其生成顺序。
    >>> sorted(set(unique_prime_factors(14)))
    [2, 7]
    >>> sorted(set(unique_prime_factors(644)))
    [2, 7, 23]
    >>> sorted(set(unique_prime_factors(646)))
    [2, 17, 19]
    """
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors


@lru_cache
def upf_len(num: int) -> int:
    """
    缓存给定值的 upf() 长度结果。
    >>> upf_len(14)
    2
    """
    return len(unique_prime_factors(num))


def equality(iterable: list) -> bool:
    """
    检查可迭代对象中的所有元素是否相等。
    >>> equality([1, 2, 3, 4])
    False
    >>> equality([2, 2, 2, 2])
    True
    >>> equality([1, 2, 3, 2, 1])
    False
    """
    return len(set(iterable)) in (0, 1)


def run(n: int) -> list[int]:
    """
    运行核心过程以求解问题。
    >>> run(3)
    [644, 645, 646]
    """

    # group 列表推导式的递增变量。
    # 这是每组待测试数值列表中的第一个数。
    base = 2

    while True:
        # 依次递增所生成范围内的每个值
        group = [base + i for i in range(n)]

        # 将各元素传入 unique_prime_factors 函数
        # 在末尾追加目标数
        checker = [upf_len(x) for x in group]
        checker.append(n)

        # 如果列表中的所有数都相等，则返回 group 变量
        if equality(checker):
            return group

        # 将 base 变量加 1
        base += 1


def solution(n: int = 4) -> int | None:
    """返回最先出现且各有四个不同素因数的四个连续整数中的第一个值。
    >>> solution()
    134043
    """
    results = run(n)
    return results[0] if len(results) else None


if __name__ == "__main__":
    print(solution())
