"""
用于字符串处理的后缀自动机（Suffix Automaton，SAM）。

Reference: https://en.wikipedia.org/wiki/Suffix_automaton
Reference: https://cp-algorithms.com/string/suffix-automaton.html

后缀自动机是识别给定字符串所有后缀（及子串）的最小确定有限自动机（DFA），
时间复杂度为 O(N)，空间复杂度为 O(N)。
"""

from dataclasses import dataclass, field


@dataclass
class State:
    """
    后缀自动机中的状态（节点）。
    """

    length: int = 0
    link: int = -1
    next: dict[str, int] = field(default_factory=dict)


class SuffixAutomaton:
    """
    后缀自动机数据结构。

    >>> sam = SuffixAutomaton("abacaba")
    >>> sam.contains("abac")
    True
    >>> sam.contains("caba")
    True
    >>> sam.contains("xyz")
    False
    >>> sam.count_distinct_substrings()
    21
    >>> sam.count_occurrences("aba")
    2
    >>> sam.count_occurrences("a")
    4
    >>> SuffixAutomaton("")
    Traceback (most recent call last):
        ...
    ValueError: Input string must not be empty.
    """

    def __init__(self, string: str) -> None:
        if not string:
            raise ValueError("Input string must not be empty.")

        self.states: list[State] = [State(length=0, link=-1)]
        self.last: int = 0
        self.string: str = string

        for char in string:
            self.extend(char)

    def extend(self, char: str) -> None:
        """
        通过追加字符 char 扩展后缀自动机。
        均摊时间复杂度：O(1)
        """
        curr = len(self.states)
        self.states.append(State(length=self.states[self.last].length + 1))

        prev_state = self.last
        while prev_state != -1 and char not in self.states[prev_state].next:
            self.states[prev_state].next[char] = curr
            prev_state = self.states[prev_state].link

        if prev_state == -1:
            self.states[curr].link = 0
        else:
            next_state = self.states[prev_state].next[char]
            if self.states[prev_state].length + 1 == self.states[next_state].length:
                self.states[curr].link = next_state
            else:
                clone = len(self.states)
                self.states.append(
                    State(
                        length=self.states[prev_state].length + 1,
                        link=self.states[next_state].link,
                    )
                )
                self.states[clone].next = dict(self.states[next_state].next)

                while (
                    prev_state != -1
                    and self.states[prev_state].next.get(char) == next_state
                ):
                    self.states[prev_state].next[char] = clone
                    prev_state = self.states[prev_state].link

                self.states[next_state].link = clone
                self.states[curr].link = clone

        self.last = curr

    def contains(self, pattern: str) -> bool:
        """
        在 O(|pattern|) 时间内检查 pattern 是否为子串。

        >>> sam = SuffixAutomaton("banana")
        >>> sam.contains("nan")
        True
        >>> sam.contains("apple")
        False
        """
        curr = 0
        for char in pattern:
            if char not in self.states[curr].next:
                return False
            curr = self.states[curr].next[char]
        return True

    def count_distinct_substrings(self) -> int:
        """
        在 O(N) 时间内计算不同子串的总数。

        >>> sam = SuffixAutomaton("abc")
        >>> sam.count_distinct_substrings()
        6
        >>> SuffixAutomaton("aaaa").count_distinct_substrings()
        4
        """
        total = 0
        for state in self.states[1:]:
            total += state.length - self.states[state.link].length
        return total

    def count_occurrences(self, pattern: str) -> int:
        """
        在 O(N + |pattern|) 时间内统计 pattern 作为子串在文本中的出现次数

        >>> sam = SuffixAutomaton("banana")
        >>> sam.count_occurrences("an")
        2
        >>> sam.count_occurrences("na")
        2
        >>> sam.count_occurrences("banana")
        1
        >>> sam.count_occurrences("xyz")
        0
        """
        curr = 0
        for char in pattern:
            if char not in self.states[curr].next:
                return 0
            curr = self.states[curr].next[char]

        # 通过后缀链接树进行标准的 endpos 集合大小计算
        occurrences = [0] * len(self.states)
        order = sorted(
            range(len(self.states)),
            key=lambda state_index: self.states[state_index].length,
            reverse=True,
        )

        # 标记前缀状态的初始结束位置
        temp_last = 0
        for char in self.string:
            temp_last = self.states[temp_last].next[char]
            occurrences[temp_last] = 1

        # 沿后缀链接树向上累加 endpos 集合大小
        for state_index in order:
            if self.states[state_index].link != -1:
                occurrences[self.states[state_index].link] += occurrences[state_index]

        return occurrences[curr]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
