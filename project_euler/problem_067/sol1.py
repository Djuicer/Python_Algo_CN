"""
题目说明：
从下面三角形的顶端开始，每次移动到下一行相邻的数，从顶端到底端的最大总和为 23。
3
7 4
2 4 6
8 5 9 3
即 3 + 7 + 4 + 9 = 23。
求 triangle.txt（右键单击并选择 'Save Link/Target As...'）中从顶端到底端的最大总和；
该文件是一个包含一百行三角形的 15K 文本文件。
"""

import os


def solution():
    """
    求出上述题意中三角形的最大总和。

    >>> solution()
    7273
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    triangle = os.path.join(script_dir, "triangle.txt")

    with open(triangle) as f:
        triangle = f.readlines()

    a = []
    for line in triangle:
        numbers_from_line = []
        for number in line.strip().split(" "):
            numbers_from_line.append(int(number))
        a.append(numbers_from_line)

    for i in range(1, len(a)):
        for j in range(len(a[i])):
            number1 = a[i - 1][j] if j != len(a[i - 1]) else 0
            number2 = a[i - 1][j - 1] if j > 0 else 0
            a[i][j] += max(number1, number2)
    return max(a[-1])


if __name__ == "__main__":
    print(solution())
