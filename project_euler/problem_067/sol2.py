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


def solution() -> int:
    """
    求出上述题意中三角形的最大总和。
    >>> solution()
    7273
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    triangle_path = os.path.join(script_dir, "triangle.txt")

    with open(triangle_path) as in_file:
        triangle = [[int(i) for i in line.split()] for line in in_file]

    while len(triangle) != 1:
        last_row = triangle.pop()
        curr_row = triangle[-1]
        for j in range(len(last_row) - 1):
            curr_row[j] += max(last_row[j], last_row[j + 1])
    return triangle[0][0]


if __name__ == "__main__":
    print(solution())
