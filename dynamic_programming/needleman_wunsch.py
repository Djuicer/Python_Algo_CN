"""用于全局序列比对的 Needleman-Wunsch 算法。

参考资料：
    https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

Needleman-Wunsch 算法 (1970) 是一种动态规划算法，用于在生物信息学和计算生物学中
查找两个序列（如 DNA、RNA 或蛋白质序列）之间的最优全局比对。

局部比对算法（如 Smith-Waterman）查找得分最高的局部子区域，
而 Needleman-Wunsch 从头到尾对两个序列的完整长度进行比对。

算法：
1. 初始化：
   - 构造大小为 (m + 1) x (n + 1) 的矩阵，其中 m 和 n 是序列长度。
   - 初始化边界条件：
     score_matrix[i][0] = i * gap_score
     score_matrix[0][j] = j * gap_score

2. 填充矩阵（状态转移方程）：
   对于每个单元格 (i, j)：
     diagonal = score_matrix[i - 1][j - 1] + (match_score if seq1[i-1] == seq2[j-1]
                                              else mismatch_score)
     deletion = score_matrix[i - 1][j] + gap_score
     insertion = score_matrix[i][j - 1] + gap_score
     score_matrix[i][j] = max(diagonal, deletion, insertion)

3. 回溯：
   - 从右下角单元格 (m, n) 开始，回溯到 (0, 0)。
   - 每一步确定产生最高得分的方向（对角、向上或向左），并以逆序组装比对后的序列。

复杂度：
    时间复杂度：O(m * n)，其中 m 和 n 是序列长度。
    空间复杂度：O(m * n)，用于存储回溯所需的得分矩阵。
"""

from __future__ import annotations


def needleman_wunsch(
    sequence1: str,
    sequence2: str,
    match_score: int = 1,
    mismatch_score: int = -1,
    gap_score: int = -1,
) -> tuple[str, str, int]:
    """使用 Needleman-Wunsch 算法计算最优全局序列比对。

    参数：
        sequence1: 要比对的第一个输入序列。
        sequence2: 要比对的第二个输入序列。
        match_score: 两个字符匹配时获得的分数（默认值：1）。
        mismatch_score: 字符不匹配时的罚分（默认值：-1）。
        gap_score: 引入间隙 '-' 时的罚分（默认值：-1）。

    返回：
        包含以下内容的元组：
        - aligned_sequence1: 插入间隙后的第一个比对序列。
        - aligned_sequence2: 插入间隙后的第二个比对序列。
        - alignment_score: 最优比对的总得分。

    异常：
        ValueError: 如果 gap_score 为正数（间隙分数必须为零或罚分）。

    示例：
        >>> # Wikipedia classic example
        >>> needleman_wunsch(
        ...     "GCATGCG", "GATTACA", match_score=1, mismatch_score=-1, gap_score=-1
        ... )
        ('GCA-TGCG', 'G-ATTACA', 0)

        >>> # Identical sequences
        >>> needleman_wunsch(
        ...     "ACGT", "ACGT", match_score=2, mismatch_score=-1, gap_score=-2
        ... )
        ('ACGT', 'ACGT', 8)

        >>> # Completely mismatched sequences
        >>> needleman_wunsch(
        ...     "AAAA", "TTTT", match_score=1, mismatch_score=-1, gap_score=-2
        ... )
        ('AAAA', 'TTTT', -4)

        >>> # One sequence is empty
        >>> needleman_wunsch("AGTC", "", match_score=1, mismatch_score=-1, gap_score=-1)
        ('AGTC', '----', -4)

        >>> # Both sequences are empty
        >>> needleman_wunsch("", "")
        ('', '', 0)

        >>> # Protein sequence example
        >>> needleman_wunsch(
        ...     "HEAGAWGHEE", "PAWHEAE", match_score=2, mismatch_score=-1, gap_score=-2
        ... )
        ('HEAGAWGHE-E', '---PAW-HEAE', -1)

        >>> # Invalid gap score
        >>> needleman_wunsch("A", "C", gap_score=5)
        Traceback (most recent call last):
            ...
        ValueError: gap_score must be non-positive (<= 0)
    """
    if gap_score > 0:
        msg = "gap_score must be non-positive (<= 0)"
        raise ValueError(msg)

    first_sequence_length = len(sequence1)
    second_sequence_length = len(sequence2)

    # 初始化 (m + 1) x (n + 1) 动态规划得分矩阵
    score_matrix = [
        [0] * (second_sequence_length + 1) for _ in range(first_sequence_length + 1)
    ]

    # 填充边界条件的罚分
    for row_index in range(first_sequence_length + 1):
        score_matrix[row_index][0] = row_index * gap_score
    for col_index in range(second_sequence_length + 1):
        score_matrix[0][col_index] = col_index * gap_score

    # 使用动态规划填充得分矩阵
    for row_index in range(1, first_sequence_length + 1):
        for col_index in range(1, second_sequence_length + 1):
            char1 = sequence1[row_index - 1]
            char2 = sequence2[col_index - 1]
            substitution = match_score if char1 == char2 else mismatch_score

            diagonal_score = score_matrix[row_index - 1][col_index - 1] + substitution
            deletion_score = score_matrix[row_index - 1][col_index] + gap_score
            insertion_score = score_matrix[row_index][col_index - 1] + gap_score

            score_matrix[row_index][col_index] = max(
                diagonal_score, deletion_score, insertion_score
            )

    # 从右下角 (m, n) 回溯到左上角 (0, 0)
    aligned_chars_first: list[str] = []
    aligned_chars_second: list[str] = []
    curr_row = first_sequence_length
    curr_col = second_sequence_length

    while curr_row > 0 or curr_col > 0:
        if curr_row > 0 and curr_col > 0:
            char1 = sequence1[curr_row - 1]
            char2 = sequence2[curr_col - 1]
            substitution = match_score if char1 == char2 else mismatch_score

            # 检查对角步骤是否最优
            if (
                score_matrix[curr_row][curr_col]
                == score_matrix[curr_row - 1][curr_col - 1] + substitution
            ):
                aligned_chars_first.append(char1)
                aligned_chars_second.append(char2)
                curr_row -= 1
                curr_col -= 1
                continue

        # 检查垂直步骤（第二个序列中的间隙）是否最优
        if (
            curr_row > 0
            and score_matrix[curr_row][curr_col]
            == score_matrix[curr_row - 1][curr_col] + gap_score
        ):
            aligned_chars_first.append(sequence1[curr_row - 1])
            aligned_chars_second.append("-")
            curr_row -= 1
        else:
            # 水平步骤（第一个序列中的间隙）
            aligned_chars_first.append("-")
            aligned_chars_second.append(sequence2[curr_col - 1])
            curr_col -= 1

    aligned_sequence1 = "".join(reversed(aligned_chars_first))
    aligned_sequence2 = "".join(reversed(aligned_chars_second))
    final_score = score_matrix[first_sequence_length][second_sequence_length]

    return aligned_sequence1, aligned_sequence2, final_score


if __name__ == "__main__":
    import doctest

    doctest.testmod()
