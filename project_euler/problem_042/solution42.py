"""
三角数数列的第 n 项为 tn = ½n(n+1)；因此前十个三角数为：

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

将单词中的每个字母转换为其字母表位置对应的数字并求和，可得到单词值。例如，
SKY 的单词值为 19 + 11 + 25 = 55 = t10。如果单词值是三角数，
则称该单词为三角单词。

words.txt（右键单击并选择 'Save Link/Target As...'）是一个包含近两千个常用
英语单词的 16K 文本文件，其中有多少个三角单词？
"""

import os

# 预先计算前 100 个三角数的列表
TRIANGULAR_NUMBERS = [int(0.5 * n * (n + 1)) for n in range(1, 101)]


def solution():
    """
    计算单词文件中三角单词的数量。

    >>> solution()
    162
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    words_file_path = os.path.join(script_dir, "words.txt")

    words = ""
    with open(words_file_path) as f:
        words = f.readline()

    words = [word.strip('"') for word in words.strip("\r\n").split(",")]
    words = [
        word
        for word in [sum(ord(x) - 64 for x in word) for word in words]
        if word in TRIANGULAR_NUMBERS
    ]
    return len(words)


if __name__ == "__main__":
    print(solution())
