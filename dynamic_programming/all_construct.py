"""
列出使用给定子字符串列表构造目标字符串的所有方式。
"""

from __future__ import annotations


def all_construct(target: str, word_bank: list[str] | None = None) -> list[list[str]]:
    """
    返回一个列表，其中包含字符串（`target`）可由给定子字符串列表
    （`word_bank`）构造出的所有可能组合。

    >>> all_construct("hello", ["he", "l", "o"])
    [['he', 'l', 'l', 'o']]
    >>> all_construct("purple",["purp","p","ur","le","purpl"])
    [['purp', 'le'], ['p', 'ur', 'p', 'le']]
    """

    word_bank = word_bank or []
    # 创建表格
    table_size: int = len(target) + 1

    table: list[list[list[str]]] = []
    for _ in range(table_size):
        table.append([])
    # 初始值
    table[0] = [[]]  # 因为空字符串对应空组合

    # 遍历索引
    for i in range(table_size):
        # 条件
        if table[i] != []:
            for word in word_bank:
                # 切片条件
                if target[i : i + len(word)] == word:
                    new_combinations: list[list[str]] = [
                        [word, *way] for way in table[i]
                    ]
                    # 将 word 添加到当前位置保存的每个组合中
                    # 然后将该组合放入 table[i+len(word)]
                    table[i + len(word)] += new_combinations

    # 组合采用逆序，因此将其反转以获得更合适的输出
    for combination in table[len(target)]:
        combination.reverse()

    return table[len(target)]


if __name__ == "__main__":
    print(all_construct("jwajalapa", ["jwa", "j", "w", "a", "la", "lapa"]))
    print(all_construct("rajamati", ["s", "raj", "amat", "raja", "ma", "i", "t"]))
    print(
        all_construct(
            "hexagonosaurus",
            ["h", "ex", "hex", "ag", "ago", "ru", "auru", "rus", "go", "no", "o", "s"],
        )
    )
