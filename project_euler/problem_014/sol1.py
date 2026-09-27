"""
Problem 14: https://projecteuler.net/problem=14

题目说明：
在正整数集合上定义如下迭代数列：

    n → n/2 (n is even)
    n → 3n + 1 (n is odd)

从 13 开始应用上述规则，可生成以下数列：

    13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

可以看出，这个从 13 开始并以 1 结束的数列包含 10 项。尽管这一结论尚未得到
证明（Collatz 问题），但人们认为所有起始数最终都会到达 1。

在一百万以下，哪个起始数会产生最长的链？
"""


def solution(n: int = 1000000) -> int:
    """返回小于 n 且按以下公式生成最长数列的数：
    n → n/2 (n is even)
    n → 3n + 1 (n is odd)

    >>> solution(1000000)
    837799
    >>> solution(200)
    171
    >>> solution(5000)
    3711
    >>> solution(15000)
    13255
    """
    largest_number = 1
    pre_counter = 1
    counters = {1: 1}

    for input1 in range(2, n):
        counter = 0
        number = input1

        while True:
            if number in counters:
                counter += counters[number]
                break
            if number % 2 == 0:
                number //= 2
                counter += 1
            else:
                number = (3 * number) + 1
                counter += 1

        if input1 not in counters:
            counters[input1] = counter

        if counter > pre_counter:
            largest_number = input1
            pre_counter = counter
    return largest_number


if __name__ == "__main__":
    print(solution(int(input().strip())))
