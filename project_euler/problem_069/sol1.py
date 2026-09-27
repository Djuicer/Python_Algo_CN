"""
欧拉函数最大值
Problem 69: https://projecteuler.net/problem=69

Euler 欧拉函数 φ(n)（有时称为 phi 函数）用于确定小于 n 且与 n 互素的数的数量。
例如，1, 2, 4, 5, 7 和 8 均小于九且与九互素，因此 φ(9)=6。

n	Relatively Prime	φ(n)	n/φ(n)
2	1	                1	    2
3	1,2	                2	    1.5
4	1,3	                2	    2
5	1,2,3,4	            4	    1.25
6	1,5		            2	    3
7	1,2,3,4,5,6	        6	    1.1666...
8	1,3,5,7		        4	    2
9	1,2,4,5,7,8	        6	    1.5
10	1,3,7,9	            4	    2.5

可以看出，当 n ≤ 10 时，n=6 使 n/φ(n) 取得最大值。

找出使 n/φ(n) 最大的 n ≤ 1,000,000。
"""


def solution(n: int = 10**6) -> int:
    """
    返回问题的解。
    算法：
    1. 使用乘积公式（见下方链接）预计算所有自然数 k（k <= n）的 φ(k)
    https://en.wikipedia.org/wiki/Euler%27s_totient_function#Euler's_product_formula

    2. 计算所有 k ≤ n 的 k/φ(k)，并返回使其达到最大值的 k

    >>> solution(10)
    6

    >>> solution(100)
    30

    >>> solution(9973)
    2310

    """

    if n <= 0:
        raise ValueError("Please enter an integer greater than 0")

    phi = list(range(n + 1))
    for number in range(2, n + 1):
        if phi[number] == number:
            phi[number] -= 1
            for multiple in range(number * 2, n + 1, number):
                phi[multiple] = (phi[multiple] // number) * (number - 1)

    answer = 1
    for number in range(1, n + 1):
        if (answer / phi[answer]) < (number / phi[number]):
            answer = number

    return answer


if __name__ == "__main__":
    print(solution())
