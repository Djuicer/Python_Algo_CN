"""
高约数三角数
问题 12
三角数数列通过累加自然数生成。因此，第 7 个三角数为
1 + 2 + 3 + 4 + 5 + 6 + 7 = 28。前十项为：

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

下面列出前七个三角数的因数：

 1: 1
 3: 1,3
 6: 1,2,3,6
10: 1,2,5,10
15: 1,3,5,15
21: 1,3,7,21
28: 1,2,4,7,14,28
可以看出，28 是第一个拥有超过五个约数的三角数。

第一个拥有超过五百个约数的三角数是多少？
"""


def count_divisors(n):
    n_divisors = 1
    i = 2
    while i * i <= n:
        multiplicity = 0
        while n % i == 0:
            n //= i
            multiplicity += 1
        n_divisors *= multiplicity + 1
        i += 1
    if n > 1:
        n_divisors *= 2
    return n_divisors


def solution():
    """返回第一个拥有超过五百个约数的三角数。

    >>> solution()
    76576500
    """
    t_num = 1
    i = 1

    while True:
        i += 1
        t_num += i

        if count_divisors(t_num) > 500:
            break

    return t_num


if __name__ == "__main__":
    print(solution())
