"""
Champernowne 常数
Problem 40
将正整数依次连接，可构造出一个无理小数：

0.123456789101112131415161718192021...

可以看出，小数部分的第 12 位是 1。

如果 dn 表示小数部分的第 n 位，求下列表达式的值。

d1 x d10 x d100 x d1000 x d10000 x d100000 x d1000000
"""


def solution():
    """返回结果。

    >>> solution()
    210
    """
    constant = []
    i = 1

    while len(constant) < 1e6:
        constant.append(str(i))
        i += 1

    constant = "".join(constant)

    return (
        int(constant[0])
        * int(constant[9])
        * int(constant[99])
        * int(constant[999])
        * int(constant[9999])
        * int(constant[99999])
        * int(constant[999999])
    )


if __name__ == "__main__":
    print(solution())
