"""
Project Euler Problem 122: https://projecteuler.net/problem=122

高效求幂

计算 n^15 最朴素的方法需要十四次乘法：

                                               n x n x ... x n = n^15.

但使用“二进制”方法只需六次乘法：

                                                         n x n = n^2
                                                     n^2 x n^2 = n^4
                                                     n^4 x n^4 = n^8
                                                     n^8 x n^4 = n^12
                                                    n^12 x n^2 = n^14
                                                      n^14 x n = n^15

还可以只用五次乘法完成计算：

                                                                n x n = n^2
                                                              n^2 x n = n^3
                                                            n^3 x n^3 = n^6
                                                            n^6 x n^6 = n^12
                                                           n^12 x n^3 = n^15

定义 m(k) 为计算 n^k 所需的最少乘法次数；例如 m(15) = 5。

求 sum_{k = 1}^200 m(k)。

本题利用这样一个事实：对于适用于本题的较小 n，每个数的解都可通过增大最大元素构成。

参考资料：
- https://en.wikipedia.org/wiki/Addition_chain
"""


def solve(nums: list[int], goal: int, depth: int) -> bool:
    """
    在 nums 长度不超过 depth 的条件下，检查 nums 中的数能否得到等于 goal 的和。

    >>> solve([1], 2, 2)
    True
    >>> solve([1], 2, 0)
    False
    """
    if len(nums) > depth:
        return False
    for el in nums:
        if el + nums[-1] == goal:
            return True
        nums.append(el + nums[-1])
        if solve(nums=nums, goal=goal, depth=depth):
            return True
        del nums[-1]
    return False


def solution(n: int = 200) -> int:
    """
    计算不超过 n 的每个数所需最少乘法次数之和。

    >>> solution(1)
    0
    >>> solution(2)
    1
    >>> solution(14)
    45
    >>> solution(15)
    50
    """
    total = 0
    for i in range(2, n + 1):
        max_length = 0
        while True:
            nums = [1]
            max_length += 1
            if solve(nums=nums, goal=i, depth=max_length):
                break
        total += max_length
    return total


if __name__ == "__main__":
    print(f"{solution() = }")
