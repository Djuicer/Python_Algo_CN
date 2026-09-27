"""
素数排列

Problem 49

等差数列 1487, 4817, 8147 的每一项都增加 3330，它有两个特别之处：
(i) 三项均为素数；
(ii) 这三个 4 位数互为排列。

由三个 1、2 或 3 位素数组成的等差数列都不具有该性质，但还存在另一个
由 4 位数组成的递增数列。

将该数列的三项连接起来，会形成哪个 12 位数？

解法：

首先生成所有 4 位素数，然后遍历这些素数，并通过排列形成新数。
使用二分查找检查排列所得数字是否在素数列表中，并将其加入候选列表。

之后，由于已知答案为 12 位数，使用 3 层嵌套循环暴力枚举所有通过检查的候选数列。
该解法的暴力搜索约需 1 秒。
"""

import math
from itertools import permutations


def is_prime(number: int) -> bool:
    """以 O(sqrt(n)) 的时间复杂度检查一个数是否为素数。

    如果一个数恰好有两个因数（1 和它本身），则它是素数。

    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(27)
    False
    >>> is_prime(87)
    False
    >>> is_prime(563)
    True
    >>> is_prime(2999)
    True
    >>> is_prime(67483)
    False
    """

    if 1 < number < 4:
        # 2 和 3 是质数
        return True
    elif number < 2 or number % 2 == 0 or number % 3 == 0:
        # 负数、0、1、所有偶数以及 3 的倍数都不是质数
        return False

    # 所有质数都形如 6k +/- 1
    for i in range(5, int(math.sqrt(number) + 1), 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


def search(target: int, prime_list: list) -> bool:
    """
    使用二分查找（Binary Search）在列表中查找一个数。
    >>> search(3, [1, 2, 3])
    True
    >>> search(4, [1, 2, 3])
    False
    >>> search(101, list(range(-100, 100)))
    False
    """

    left, right = 0, len(prime_list) - 1
    while left <= right:
        middle = (left + right) // 2
        if prime_list[middle] == target:
            return True
        elif prime_list[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return False


def solution():
    """
    返回该问题的解。
    >>> solution()
    296962999629
    """
    prime_list = [n for n in range(1001, 10000, 2) if is_prime(n)]
    candidates = []

    for number in prime_list:
        tmp_numbers = []

        for prime_member in permutations(list(str(number))):
            prime = int("".join(prime_member))

            if prime % 2 == 0:
                continue

            if search(prime, prime_list):
                tmp_numbers.append(prime)

        tmp_numbers.sort()
        if len(tmp_numbers) >= 3:
            candidates.append(tmp_numbers)

    passed = []
    for candidate in candidates:
        length = len(candidate)
        found = False

        for i in range(length):
            for j in range(i + 1, length):
                for k in range(j + 1, length):
                    if (
                        abs(candidate[i] - candidate[j])
                        == abs(candidate[j] - candidate[k])
                        and len({candidate[i], candidate[j], candidate[k]}) == 3
                    ):
                        passed.append(
                            sorted([candidate[i], candidate[j], candidate[k]])
                        )
                        found = True

                    if found:
                        break
                if found:
                    break
            if found:
                break

    answer = set()
    for seq in passed:
        answer.add("".join([str(i) for i in seq]))

    return max(int(x) for x in answer)


if __name__ == "__main__":
    print(solution())
