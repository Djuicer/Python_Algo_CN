"""

Project Euler Problem 207: https://projecteuler.net/problem=207

题目说明：
对于某些正整数 k，存在形如 4**t = 2**t + k 的整数划分，其中 4**t、2**t 和 k
均为正整数，t 为实数。前两个这样的划分是 4**1 = 2**1 + 2 和
4**1.5849625... = 2**1.5849625... + 6。
当 t 也是整数时，该划分称为完美划分。
对于任意 m ≥ 1，令 P(m) 表示满足 k ≤ m 的此类划分中完美划分所占的比例。
因此 P(6) = 1/2。
下表列出了 P(m) 的一些值

   P(5) = 1/1
   P(10) = 1/2
   P(15) = 2/3
   P(20) = 1/2
   P(25) = 1/2
   P(30) = 2/5
   ...
   P(180) = 1/4
   P(185) = 3/13

求满足 P(m) < 1/12345 的最小 m。

解法：
由方程 4**t = 2**t + k 解出 t 得：
    t = log2(sqrt(4*k+1)/2 + 1/2)
要使 t 为实数，sqrt(4*k+1) 必须是整数，这由函数 check_t_real(k) 实现。
对于完美划分，t 必须是整数。为显著加快划分搜索，不在每次迭代中将 k 增加一，
而是使用整数 i 通过 k = (i**2 - 1) / 4 找到下一个有效 k，且 k 必须为正整数。
满足该条件时即找到一个划分；若 t 为整数，则该划分是完美划分。整数 i 每次增加 1，
直到 完美划分数 / 总划分数 低于给定值。

"""

import math


def check_partition_perfect(positive_integer: int) -> bool:
    """

    检查 t = f(positive_integer) = log2(sqrt(4*positive_integer+1)/2 + 1/2)
    是否为实数。

    >>> check_partition_perfect(2)
    True

    >>> check_partition_perfect(6)
    False

    """

    exponent = math.log2(math.sqrt(4 * positive_integer + 1) / 2 + 1 / 2)

    return exponent == int(exponent)


def solution(max_proportion: float = 1 / 12345) -> int:
    """
    找出完美划分数占总划分数的比例低于 max_proportion 时的 m。

    >>> solution(1) > 5
    True

    >>> solution(1/2) > 10
    True

    >>> solution(3 / 13) > 185
    True

    """

    total_partitions = 0
    perfect_partitions = 0

    integer = 3
    while True:
        partition_candidate = (integer**2 - 1) / 4
        # 如果候选值是整数，则 k 存在一个划分
        if partition_candidate == int(partition_candidate):
            partition_candidate = int(partition_candidate)
            total_partitions += 1
            if check_partition_perfect(partition_candidate):
                perfect_partitions += 1
        if (
            perfect_partitions > 0
            and perfect_partitions / total_partitions < max_proportion
        ):
            return int(partition_candidate)
        integer += 1


if __name__ == "__main__":
    print(f"{solution() = }")
