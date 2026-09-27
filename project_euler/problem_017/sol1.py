"""
数词字母计数
Problem 17: https://projecteuler.net/problem=17

如果将数字 1 到 5 写成英文单词：one、two、three、four、five，
则总共使用了 3 + 3 + 5 + 4 + 4 = 19 个字母。

如果将从 1 到 1000（one thousand）的所有数字都写成英文单词，总共会使用多少个字母？


注意：空格和连字符不计。例如，342（three hundred and forty-two）包含 23 个字母，
115（one hundred and fifteen）包含 20 个字母。数字写法中使用 "and" 遵循英式用法。
"""


def solution(n: int = 1000) -> int:
    """返回用英文写出从 1 到 n 的所有数字所需的字母数，其中 n 小于或等于 1000。
    >>> solution(1000)
    21124
    >>> solution(5)
    19
    """
    # zero、one、two、...、nineteen 的字母数（zero 从不读出，因此记为 0）
    ones_counts = [0, 3, 3, 5, 4, 4, 3, 5, 5, 4, 3, 6, 6, 8, 8, 7, 7, 9, 8, 8]
    # twenty、thirty、...、ninety 的字母数（小于 20 的数记为 0，
    # 因为十几的数词形式不规则）
    tens_counts = [0, 0, 6, 6, 5, 5, 5, 7, 6, 6]

    count = 0

    for i in range(1, n + 1):
        if i < 1000:
            if i >= 100:
        # 加上 "n hundred" 的字母数
                count += ones_counts[i // 100] + 7

                if i % 100 != 0:
            # 如果数字不是 100 的倍数，则加上 "and" 的字母数
                    count += 3

            if 0 < i % 100 < 20:
        # 加上 one、two、three、...、nineteen 的字母数
        # （若十几的数词形式规则，本可与下方逻辑合并）
                count += ones_counts[i % 100]
            else:
        # 加上 twenty、twenty one、...、ninety nine 的字母数
                count += ones_counts[i % 10]
                count += tens_counts[(i % 100 - i % 10) // 10]
        else:
            count += ones_counts[i // 1000] + 8
    return count


if __name__ == "__main__":
    print(solution(int(input().strip())))
