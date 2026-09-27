"""
https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm
Smith-Waterman 算法是一种用于序列比对的动态规划算法，特别适合查找两个序列
（如 DNA 或蛋白质序列）之间的相似性。在此实现中，间隙采用线性罚分，
即比对中每引入一个间隙，得分就减少固定值。需要注意的是，
Smith-Waterman 算法也支持其他间隙罚分方法。
"""


def score_function(
    source_char: str,
    target_char: str,
    match: int = 1,
    mismatch: int = -1,
    gap: int = -2,
) -> int:
    """
    根据字符对是否匹配来计算得分。
    如果字符匹配则返回 1，不匹配则返回 -1，任一字符为间隙则返回 -2。
    >>> score_function('A', 'A')
    1
    >>> score_function('A', 'C')
    -1
    >>> score_function('-', 'A')
    -2
    >>> score_function('A', '-')
    -2
    >>> score_function('-', '-')
    -2
    """
    if "-" in (source_char, target_char):
        return gap
    return match if source_char == target_char else mismatch


def smith_waterman(
    query: str,
    subject: str,
    match: int = 1,
    mismatch: int = -1,
    gap: int = -2,
) -> list[list[int]]:
    """
    执行 Smith-Waterman 局部序列比对算法。
    返回表示得分矩阵的 2D 列表。矩阵中的每个值对应以该位置结尾的最佳局部比对得分。
    >>> smith_waterman('ACAC', 'CA')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]
    >>> smith_waterman('acac', 'ca')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]
    >>> smith_waterman('ACAC', 'ca')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]
    >>> smith_waterman('acac', 'CA')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]
    >>> smith_waterman('ACAC', '')
    [[0], [0], [0], [0], [0]]
    >>> smith_waterman('', 'CA')
    [[0, 0, 0]]
    >>> smith_waterman('ACAC', 'CA')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]

    >>> smith_waterman('acac', 'ca')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]

    >>> smith_waterman('ACAC', 'ca')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]

    >>> smith_waterman('acac', 'CA')
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]]

    >>> smith_waterman('ACAC', '')
    [[0], [0], [0], [0], [0]]

    >>> smith_waterman('', 'CA')
    [[0, 0, 0]]

    >>> smith_waterman('AGT', 'AGT')
    [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]

    >>> smith_waterman('AGT', 'GTA')
    [[0, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 0, 2, 0]]

    >>> smith_waterman('AGT', 'GTC')
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0]]

    >>> smith_waterman('AGT', 'G')
    [[0, 0], [0, 0], [0, 1], [0, 0]]

    >>> smith_waterman('G', 'AGT')
    [[0, 0, 0, 0], [0, 0, 1, 0]]

    >>> smith_waterman('AGT', 'AGTCT')
    [[0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 3, 1, 1]]

    >>> smith_waterman('AGTCT', 'AGT')
    [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3], [0, 0, 0, 1], [0, 0, 0, 1]]

    >>> smith_waterman('AGTCT', 'GTC')
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3], [0, 0, 1, 1]]
    """
    # 将 query 和 subject 都转换为大写
    query = query.upper()
    subject = subject.upper()

    # 初始化得分矩阵
    m = len(query)
    n = len(subject)
    score = [[0] * (n + 1) for _ in range(m + 1)]
    kwargs = {"match": match, "mismatch": mismatch, "gap": gap}

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 计算每个单元格的得分
            match = score[i - 1][j - 1] + score_function(
                query[i - 1], subject[j - 1], **kwargs
            )
            delete = score[i - 1][j] + gap
            insert = score[i][j - 1] + gap

            # 取最高得分
            score[i][j] = max(0, match, delete, insert)

    return score


def traceback(score: list[list[int]], query: str, subject: str) -> str:
    r"""
    执行回溯以查找最优局部比对。
    从矩阵中得分最高的单元格开始递归回溯，直到找到得分为 0 的位置。
    返回比对字符串。
    >>> traceback([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]], 'ACAC', 'CA')
    'CA\nCA'
    >>> traceback([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]], 'acac', 'ca')
    'CA\nCA'
    >>> traceback([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]], 'ACAC', 'ca')
    'CA\nCA'
    >>> traceback([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 2], [0, 1, 0]], 'acac', 'CA')
    'CA\nCA'
    >>> traceback([[0, 0, 0]], 'ACAC', '')
    ''
    """
    # 将 query 和 subject 都转换为大写
    query = query.upper()
    subject = subject.upper()
    # 查找得分矩阵中最大值的索引
    max_value = float("-inf")
    i_max = j_max = 0
    for i, row in enumerate(score):
        for j, value in enumerate(row):
            if value > max_value:
                max_value = value
                i_max, j_max = i, j
    # 查找最优比对的回溯逻辑
    i = i_max
    j = j_max
    align1 = ""
    align2 = ""
    gap = score_function("-", "-")
    # 防止 query 或 subject 为空
    if i == 0 or j == 0:
        return ""
    while i > 0 and j > 0:
        if score[i][j] == score[i - 1][j - 1] + score_function(
            query[i - 1], subject[j - 1]
        ):
            # 最优路径为对角方向，取两个字母
            align1 = query[i - 1] + align1
            align2 = subject[j - 1] + align2
            i -= 1
            j -= 1
        elif score[i][j] == score[i - 1][j] + gap:
            # 最优路径为垂直方向
            align1 = query[i - 1] + align1
            align2 = f"-{align2}"
            i -= 1
        else:
            # 最优路径为水平方向
            align1 = f"-{align1}"
            align2 = subject[j - 1] + align2
            j -= 1

    return f"{align1}\n{align2}"


if __name__ == "__main__":
    query = "HEAGAWGHEE"
    subject = "PAWHEAE"

    score = smith_waterman(query, subject, match=1, mismatch=-1, gap=-2)
    print(traceback(score, query, subject))
