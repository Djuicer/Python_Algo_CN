"""
Lychrel 数
Problem 55: https://projecteuler.net/problem=55

取 47，将其反转后相加，47 + 74 = 121，结果是回文数。

并非所有数字都能如此迅速地产生回文数。例如，
349 + 943 = 1292,
1292 + 2921 = 4213
4213 + 3124 = 7337
也就是说，349 经过三次迭代才得到回文数。

尽管尚无人证明，但人们认为某些数（如 196）永远不会产生回文数。通过“反转并相加”
过程始终不能形成回文数的数称为 Lychrel 数。由于这些数具有理论性质，为解决本题，
在证明并非如此之前，我们都假设一个数是 Lychrel 数。此外，已知对于一万以下的每个数，
它要么 (i) 在少于五十次迭代后成为回文数，要么 (ii) 迄今即使使用现有全部计算能力，
也无人能将其映射为回文数。事实上，10677 是首个被证明需要超过五十次迭代才产生
回文数的数字：
4668731596684224866951378664 (53 iterations, 28-digits).

令人惊讶的是，有些回文数本身也是 Lychrel 数；第一个例子是 4994。
一万以下有多少个 Lychrel 数？
"""


def is_palindrome(n: int) -> bool:
    """
    如果一个数是回文数，则返回 True。
    >>> is_palindrome(12567321)
    False
    >>> is_palindrome(1221)
    True
    >>> is_palindrome(9876789)
    True
    """
    return str(n) == str(n)[::-1]


def sum_reverse(n: int) -> int:
    """
    返回 n 与其反转数之和。
    >>> sum_reverse(123)
    444
    >>> sum_reverse(3478)
    12221
    >>> sum_reverse(12)
    33
    """
    return int(n) + int(str(n)[::-1])


def solution(limit: int = 10000) -> int:
    """
    返回 limit 以下所有 Lychrel 数的数量。
    >>> solution(10000)
    249
    >>> solution(5000)
    76
    >>> solution(1000)
    13
    """
    lychrel_nums = []
    for num in range(1, limit):
        iterations = 0
        a = num
        while iterations < 50:
            num = sum_reverse(num)
            iterations += 1
            if is_palindrome(num):
                break
        else:
            lychrel_nums.append(a)
    return len(lychrel_nums)


if __name__ == "__main__":
    print(f"{solution() = }")
