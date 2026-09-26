"""
https://en.wikipedia.org/wiki/Karnaugh_map
https://www.allaboutcircuits.com/technical-articles/karnaugh-map-boolean-algebraic-simplification-technique
"""


def simplify_kmap(kmap: list[list[int]]) -> str:
    """
    化简卡诺图（Karnaugh Map）。
    >>> simplify_kmap(kmap=[[0, 1], [1, 1]])
    "A'B + AB' + AB"
    >>> simplify_kmap(kmap=[[0, 0], [0, 0]])
    ''
    >>> simplify_kmap(kmap=[[0, 1], [1, -1]])
    "A'B + AB' + AB"
    >>> simplify_kmap(kmap=[[0, 1], [1, 2]])
    "A'B + AB' + AB"
    >>> simplify_kmap(kmap=[[0, 1], [1, 1.1]])
    "A'B + AB' + AB"
    >>> simplify_kmap(kmap=[[0, 1], [1, 'a']])
    "A'B + AB' + AB"
    """
    simplified_f = []
    for a, row in enumerate(kmap):
        for b, item in enumerate(row):
            if item:
                term = ("A" if a else "A'") + ("B" if b else "B'")
                simplified_f.append(term)
    return " + ".join(simplified_f)


def main() -> None:
    """
    创建并化简卡诺图的主函数。

    >>> main()
    [0, 1]
    [1, 1]
    Simplified Expression:
    A'B + AB' + AB
    """
    kmap = [[0, 1], [1, 1]]

    # 手动生成 [0, 1] 与 [0, 1] 的笛卡尔积

    for row in kmap:
        print(row)

    print("Simplified Expression:")
    print(simplify_kmap(kmap))


if __name__ == "__main__":
    main()
    print(f"{simplify_kmap(kmap=[[0, 1], [1, 1]]) = }")
