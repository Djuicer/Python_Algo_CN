"""
计数求和
Problem 76: https://projecteuler.net/problem=76

将五写成和，恰好有六种不同方式：

4 + 1
3 + 2
3 + 1 + 1
2 + 2 + 1
2 + 1 + 1 + 1
1 + 1 + 1 + 1 + 1

将一百写成至少两个正整数之和，有多少种不同方式？
"""


def solution(m: int = 100) -> int:
    """
    返回将数字 m 写成至少两个正整数之和的不同方式数。

    >>> solution(100)
    190569291
    >>> solution(50)
    204225
    >>> solution(30)
    5603
    >>> solution(10)
    41
    >>> solution(5)
    6
    >>> solution(3)
    2
    >>> solution(2)
    1
    >>> solution(1)
    0
    """
    memo = [[0 for _ in range(m)] for _ in range(m + 1)]
    for i in range(m + 1):
        memo[i][0] = 1

    for n in range(m + 1):
        for k in range(1, m):
            memo[n][k] += memo[n][k - 1]
            if n > k:
                memo[n][k] += memo[n - k - 1][k]

    return memo[m][m - 1] - 1


if __name__ == "__main__":
    print(solution(int(input("Enter a number: ").strip())))
