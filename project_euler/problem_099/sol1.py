"""
问题：

比较以指数形式写成的两个数（如 2'11 和 3'7）并不困难，任何计算器都能验证
2^11 = 2048 < 3^7 = 2187。

然而，要确认 632382^518061 > 519432^525806 困难得多，因为两数都超过三百万位。

使用 22K 文本文件 base_exp.txt，其中包含一千行，每行是一对底数/指数；
确定数值最大者所在的行号。

注意：文件前两行表示上述示例中的两个数。
"""

import os
from math import log10


def solution(data_file: str = "base_exp.txt") -> int:
    """
    >>> solution()
    709
    """
    largest: float = 0
    result = 0
    for i, line in enumerate(open(os.path.join(os.path.dirname(__file__), data_file))):
        a, x = list(map(int, line.split(",")))
        if x * log10(a) > largest:
            largest = x * log10(a)
            result = i + 1
    return result


if __name__ == "__main__":
    print(solution())
