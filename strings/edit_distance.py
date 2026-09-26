def edit_distance(source: str, target: str) -> int:
    """
    编辑距离（Edit Distance）是一种字符串度量，用于量化
    两个字符串的差异。通过计算将一个字符串转换为另一个字符串
    所需的最少操作次数来度量。

    此实现假设插入、删除和替换操作的代价
    始终为 1

    参数：
    source: 初始字符串，用于计算它与 target 之间的
        编辑距离
    target: 对 source 执行 n 次操作后得到的目标字符串

    >>> edit_distance("GATTIC", "GALTIC")
    1
    >>> edit_distance("NUM3", "HUM2")
    2
    >>> edit_distance("cap", "CAP")
    3
    >>> edit_distance("Cat", "")
    3
    >>> edit_distance("cat", "cat")
    0
    >>> edit_distance("", "123456789")
    9
    >>> edit_distance("Be@uty", "Beautyyyy!")
    5
    >>> edit_distance("lstring", "lsstring")
    1
    """
    if len(source) == 0:
        return len(target)
    elif len(target) == 0:
        return len(source)

    delta = int(source[-1] != target[-1])  # 替换
    return min(
        edit_distance(source[:-1], target[:-1]) + delta,
        edit_distance(source, target[:-1]) + 1,
        edit_distance(source[:-1], target) + 1,
    )


if __name__ == "__main__":
    print(edit_distance("ATCGCTG", "TAGCTAA"))  # 答案为 4
