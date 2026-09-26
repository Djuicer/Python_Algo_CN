"""
使用以下规则在给定文本中查找模式。

坏字符规则关注文本中的失配字符。
查找模式中该字符在失配位置左侧的下一次出现，

若失配字符在模式左侧出现，
则移动模式，使其与文本中的对应字符对齐。

若失配字符未在模式左侧出现，
则将整个模式移动到文本中
失配位置之后。

若没有失配，则模式与该文本片段匹配。

时间复杂度：使用坏字符启发式时，平均为 O(n/m)
    n=主字符串长度
    m=模式字符串长度

注意：坏字符位移需要使用 while 循环，才能真正跳过
    相应位置。for 循环不会采用重新赋值后的循环变量来推进迭代。
"""


class BoyerMooreSearch:
    """
    用法示例：

        bms = BoyerMooreSearch(text="ABAABA", pattern="AB")
        positions = bms.bad_character_heuristic()

    'positions' 包含模式匹配的位置。
    """

    def __init__(self, text: str, pattern: str) -> None:
        self.text, self.pattern = text, pattern
        self.textLen, self.patLen = len(text), len(pattern)

    def match_in_pattern(self, char: str) -> int:
        """
        逆序查找 char 在 pattern 中的索引。

        Parameters :
            char (chr): 待搜索的字符

        Returns :
            i (int): 从后向前找到的 char 在 pattern 中的索引
            -1 (int): 在 pattern 中未找到 char 时返回

        >>> bms = BoyerMooreSearch(text="ABAABA", pattern="AB")
        >>> bms.match_in_pattern("B")
        1
        """

        for i in range(self.patLen - 1, -1, -1):
            if char == self.pattern[i]:
                return i
        return -1

    def mismatch_in_text(self, current_pos: int) -> int:
        """
        从末尾开始与 pattern 比较，找出 text 中
        失配字符的索引。

        Parameters :
            current_pos (int): text 中的当前索引位置

        Returns :
            i (int): 从后向前找到的 text 中失配字符的索引
            -1 (int): pattern 与文本片段完全匹配时返回

        >>> bms = BoyerMooreSearch(text="ABAABA", pattern="AB")
        >>> bms.mismatch_in_text(2)
        3
        """

        for i in range(self.patLen - 1, -1, -1):
            if self.pattern[i] != self.text[current_pos + i]:
                return current_pos + i
        return -1

    def bad_character_heuristic(self) -> list[int]:
        """
        使用坏字符启发式查找模式在文本中的
        位置。使用 while 循环使位移真正跳过
        相应位置，平均性能达到 O(n/m)，而非
        for 循环产生的 O(nm) 暴力搜索。

        >>> bms = BoyerMooreSearch(text="ABAABA", pattern="AB")
        >>> bms.bad_character_heuristic()
        [0, 3]

        >>> bms = BoyerMooreSearch(text="AAAAA", pattern="AB")
        >>> bms.bad_character_heuristic()
        []

        >>> bms = BoyerMooreSearch(text="ABABAB", pattern="ABA")
        >>> bms.bad_character_heuristic()
        [0, 2]

        >>> bms = BoyerMooreSearch(text="", pattern="AB")
        >>> bms.bad_character_heuristic()
        []

        >>> bms2 = BoyerMooreSearch(text="AAAAAA", pattern="AA")
        >>> bms2.bad_character_heuristic()
        [0, 1, 2, 3, 4]

        >>> bms3 = BoyerMooreSearch(text="ABCDEF", pattern="XY")
        >>> bms3.bad_character_heuristic()
        []
        """

        positions = []
        i = 0
        while i <= self.textLen - self.patLen:
            mismatch_index = self.mismatch_in_text(i)
            if mismatch_index == -1:
                positions.append(i)
                i += 1
            else:
                match_index = self.match_in_pattern(self.text[mismatch_index])
                # 使用 max 避免向后移动
                i = max(i + 1, mismatch_index - match_index)
        return positions


if __name__ == "__main__":
    import doctest

    doctest.testmod()
