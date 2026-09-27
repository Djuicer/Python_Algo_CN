"""
姓名得分
问题 22

使用 names.txt（右键单击并选择 'Save Link/Target As...'），这是一个包含五千多个
名字的 46K 文本文件。首先按字母顺序排序，然后计算每个名字的字母值，
再乘以该名字在列表中的字母顺序位置，得到姓名得分。

例如，列表按字母顺序排序后，COLIN 的值为 3 + 15 + 12 + 9 + 14 = 53，
它是列表中的第 938 个名字。因此，COLIN 的得分为 938 x 53 = 49714。

文件中所有姓名得分的总和是多少？
"""

import os


def solution():
    """返回文件中所有姓名得分的总和。

    >>> solution()
    871198282
    """
    with open(os.path.dirname(__file__) + "/p022_names.txt") as file:
        names = str(file.readlines()[0])
        names = names.replace('"', "").split(",")

    names.sort()

    name_score = 0
    total_score = 0

    for i, name in enumerate(names):
        for letter in name:
            name_score += ord(letter) - 64

        total_score += (i + 1) * name_score
        name_score = 0
    return total_score


if __name__ == "__main__":
    print(solution())
