"""
Problem: https://projecteuler.net/problem=54

在扑克游戏中，一手牌由五张牌组成，牌型从低到高排列如下：

高牌（High Card）：点数最高的牌。
一对（One Pair）：两张点数相同的牌。
两对（Two Pairs）：两个不同的对子。
三条（Three of a Kind）：三张点数相同的牌。
顺子（Straight）：所有牌的点数连续。
同花（Flush）：所有牌花色相同。
葫芦（Full House）：一个三条和一个对子。
四条（Four of a Kind）：四张点数相同的牌。
同花顺（Straight Flush）：所有牌花色相同且点数连续。
皇家同花顺（Royal Flush）：同一花色的 Ten、Jack、Queen、King、Ace。

牌的点数顺序为：
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

如果两名玩家的牌型相同，则组成该牌型的最高点数者获胜；例如，一对八胜过一对五。
如果牌型点数也相同，例如双方都有一对 Queen，则比较各手牌中的最高牌；
若最高牌相同，再比较次高牌，依此类推。

文件 poker.txt 包含随机发给两名玩家的一千手牌。文件每行包含十张牌（以单个空格分隔）：
前五张属于玩家 1，后五张属于玩家 2。可以假定所有手牌均有效（没有无效字符或重复牌），
每名玩家的手牌没有特定顺序，并且每手牌都有明确的胜者。

玩家 1 赢了多少手？

参考资料：
https://en.wikipedia.org/wiki/Texas_hold_%27em
https://en.wikipedia.org/wiki/List_of_poker_hands

Codewars 上的类似问题：
https://www.codewars.com/kata/ranking-poker-hands
https://www.codewars.com/kata/sortable-poker-hands
"""

from __future__ import annotations

import os


class PokerHand:
    """根据输入字符串创建表示扑克牌手牌的对象，该字符串表示玩家手牌与公共牌组成的
    最佳 5 张牌组合。

    属性（只读）：
        hand：表示由五张牌组成的手牌的字符串

    方法：
        compare_with(opponent)：接收玩家手牌（self）和对手手牌（opponent），
            按德州扑克规则比较两手牌。根据玩家手牌是否优于对手手牌，
            返回 3 个字符串之一（Win、Loss、Tie）。

        hand_name()：返回由牌型名称和高牌两部分组成的字符串。

    支持的运算符：
        富比较运算符：<, >, <=, >=, ==, !=

    支持的内置方法和函数：
        list.sort(), sorted()
    """

    _HAND_NAME = (
        "High card",
        "One pair",
        "Two pairs",
        "Three of a kind",
        "Straight",
        "Flush",
        "Full house",
        "Four of a kind",
        "Straight flush",
        "Royal flush",
    )

    _CARD_NAME = (
        "",  # 元组索引从零开始，因此用作占位符
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Jack",
        "Queen",
        "King",
        "Ace",
    )

    def __init__(self, hand: str) -> None:
        """
        初始化手牌。hand 应为 str 类型，并且只能包含五张以空格分隔的牌。

        牌应采用以下格式：
        [card value][card suit]

        第一个字符表示牌的点数：
        2, 3, 4, 5, 6, 7, 8, 9, T(en), J(ack), Q(ueen), K(ing), A(ce)

        第二个字符表示花色：
        S(pades), H(earts), D(iamonds), C(lubs)

        例如："6S 4C KC AS TH"
        """
        if not isinstance(hand, str):
            msg = f"Hand should be of type 'str': {hand!r}"
            raise TypeError(msg)
        # split 会移除重复空白，因此无需 strip
        if len(hand.split(" ")) != 5:
            msg = f"Hand should contain only 5 cards: {hand!r}"
            raise ValueError(msg)
        self._hand = hand
        self._first_pair = 0
        self._second_pair = 0
        self._card_values, self._card_suit = self._internal_state()
        self._hand_type = self._get_hand_type()
        self._high_card = self._card_values[0]

    @property
    def hand(self):
        """返回自身手牌。"""
        return self._hand

    def compare_with(self, other: PokerHand) -> str:
        """
        确定自身手牌与另一手牌的比较结果。
        按德州扑克规则返回 'Win'、'Loss' 或 'Tie'。

        以下是一些示例：
        >>> player = PokerHand("2H 3H 4H 5H 6H")  # Stright flush
        >>> opponent = PokerHand("KS AS TS QS JS")  # Royal flush
        >>> player.compare_with(opponent)
        'Loss'

        >>> player = PokerHand("2S AH 2H AS AC")  # Full house
        >>> opponent = PokerHand("2H 3H 5H 6H 7H")  # Flush
        >>> player.compare_with(opponent)
        'Win'

        >>> player = PokerHand("2S AH 4H 5S 6C")  # High card
        >>> opponent = PokerHand("AD 4C 5H 6H 2C")  # High card
        >>> player.compare_with(opponent)
        'Tie'
        """
        # 按以下优先顺序打破平局：
        # 1. 第一组对子（默认为 0）
        # 2. 第二组对子（默认为 0）
        # 3. 因牌已排序，按逆序比较所有牌。

        # 仅当牌型为以下类型之一时，第一组和第二组对子才可能为非零值：
        # 21：四条
        # 20：葫芦
        # 17：三条
        # 16：两对
        # 15：一对
        if self._hand_type > other._hand_type:
            return "Win"
        elif self._hand_type < other._hand_type:
            return "Loss"
        elif self._first_pair == other._first_pair:
            if self._second_pair == other._second_pair:
                return self._compare_cards(other)
            else:
                return "Win" if self._second_pair > other._second_pair else "Loss"
        return "Win" if self._first_pair > other._first_pair else "Loss"

    # 此函数不属于题目要求，仅为扩展功能
    def hand_name(self) -> str:
        """
        按以下格式返回牌型名称：
        'hand name, high card'

        以下是一些示例：
        >>> PokerHand("KS AS TS QS JS").hand_name()
        'Royal flush'

        >>> PokerHand("2D 6D 3D 4D 5D").hand_name()
        'Straight flush, Six-high'

        >>> PokerHand("JC 6H JS JD JH").hand_name()
        'Four of a kind, Jacks'

        >>> PokerHand("3D 2H 3H 2C 2D").hand_name()
        'Full house, Twos over Threes'

        >>> PokerHand("2H 4D 3C AS 5S").hand_name()  # Low ace
        'Straight, Five-high'

        Source: https://en.wikipedia.org/wiki/List_of_poker_hands
        """
        name = PokerHand._HAND_NAME[self._hand_type - 14]
        high = PokerHand._CARD_NAME[self._high_card]
        pair1 = PokerHand._CARD_NAME[self._first_pair]
        pair2 = PokerHand._CARD_NAME[self._second_pair]
        if self._hand_type in [22, 19, 18]:
            return name + f", {high}-high"
        elif self._hand_type in [21, 17, 15]:
            return name + f", {pair1}s"
        elif self._hand_type in [20, 16]:
            join = "over" if self._hand_type == 20 else "and"
            return name + f", {pair1}s {join} {pair2}s"
        elif self._hand_type == 23:
            return name
        else:
            return name + f", {high}"

    def _compare_cards(self, other: PokerHand) -> str:
        # enumerate 同时提供列表元素及其索引
        for index, card_value in enumerate(self._card_values):
            if card_value != other._card_values[index]:
                return "Win" if card_value > other._card_values[index] else "Loss"
        return "Tie"

    def _get_hand_type(self) -> int:
        # 内部表示牌型的数字：
        # 23: Royal flush
        # 22: Straight flush
        # 21: Four of a kind
        # 20: Full house
        # 19: Flush
        # 18: Straight
        # 17: Three of a kind
        # 16: Two pairs
        # 15: One pair
        # 14: High card
        if self._is_flush():
            if self._is_five_high_straight() or self._is_straight():
                return 23 if sum(self._card_values) == 60 else 22
            return 19
        elif self._is_five_high_straight() or self._is_straight():
            return 18
        return 14 + self._is_same_kind()

    def _is_flush(self) -> bool:
        return len(self._card_suit) == 1

    def _is_five_high_straight(self) -> bool:
        # 如果手牌是五点高顺子（Ace 作低牌），则将 Ace 从列表开头移到末尾。
        # 检查第一个元素是否为 Ace，以免再次改变。
        # 五点高顺子（Ace 作低牌）：AH 2H 3S 4C 5D
        # 为什么在此使用 sorted？调用一次此函数会将列表变为 [5, 4, 3, 2, 14]，
        # 因此后续调用（这种情况很少）需要比较排序后的版本。
        # 参见 test_poker_hand.py 中的 test_multiple_calls_five_high_straight
        if sorted(self._card_values) == [2, 3, 4, 5, 14]:
            if self._card_values[0] == 14:
                # 注意，列表已按逆序排序
                ace_card = self._card_values.pop(0)
                self._card_values.append(ace_card)
            return True
        return False

    def _is_straight(self) -> bool:
        for i in range(4):
            if self._card_values[i] - self._card_values[i + 1] != 1:
                return False
        return True

    def _is_same_kind(self) -> int:
        # 内部使用的同点数组合值：
        # 7：四条
        # 6：葫芦
        # 3：三条
        # 2：两对
        # 1：一对
        # 0：False
        kind = val1 = val2 = 0
        for i in range(4):
            # 每次比较两张牌；如果点数相同，则增加 'kind' 并将牌的点数赋给 val1。
            # 如果该点数再次出现，则因已有 3 张同点数牌而将 'kind' 加 2。
            # 如果遇到与 val1 不同的点数，则对 val2 执行相同操作。
            if self._card_values[i] == self._card_values[i + 1]:
                if not val1:
                    val1 = self._card_values[i]
                    kind += 1
                elif val1 == self._card_values[i]:
                    kind += 2
                elif not val2:
                    val2 = self._card_values[i]
                    kind += 1
                elif val2 == self._card_values[i]:
                    kind += 2
        # 保持牌型的一致性（参见 _get_hand_type 函数中的说明）
        kind = kind + 2 if kind in [4, 5] else kind
        # first 表示 'compare_with' 中首先比较的对子
        first = max(val1, val2)
        second = min(val1, val2)
        # 如果是葫芦（三张同点数牌加两张同点数牌），确保 first 对应三张牌；
        # 否则交换二者。
        if kind == 6 and self._card_values.count(first) != 3:
            first, second = second, first
        self._first_pair = first
        self._second_pair = second
        return kind

    def _internal_state(self) -> tuple[list[int], set[str]]:
        # 手牌在内部表示为牌点数列表和花色集合
        trans: dict = {"T": "10", "J": "11", "Q": "12", "K": "13", "A": "14"}
        new_hand = self._hand.translate(str.maketrans(trans)).split()
        card_values = [int(card[:-1]) for card in new_hand]
        card_suit = {card[-1] for card in new_hand}
        return sorted(card_values, reverse=True), card_suit

    def __repr__(self) -> str:
        return f'{self.__class__}("{self._hand}")'

    def __str__(self) -> str:
        return self._hand

    # 富比较运算符（供内置函数 list.sort() 和 sorted() 使用）
    # 这不属于题目要求，而是一项额外功能：可以直接用内置函数对 PokerHand 对象列表排序。
    def __eq__(self, other):
        if isinstance(other, PokerHand):
            return self.compare_with(other) == "Tie"
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, PokerHand):
            return self.compare_with(other) == "Loss"
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, PokerHand):
            return self < other or self == other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PokerHand):
            return not self < other and self != other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PokerHand):
            return not self < other
        return NotImplemented

    def __hash__(self):
        return object.__hash__(self)


def solution() -> int:
    # Project Euler 第 54 题的解法
    # 输入来自 poker_hands.txt 文件
    answer = 0
    script_dir = os.path.abspath(os.path.dirname(__file__))
    poker_hands = os.path.join(script_dir, "poker_hands.txt")
    with open(poker_hands) as file_hand:
        for line in file_hand:
            player_hand = line[:14].strip()
            opponent_hand = line[15:].strip()
            player, opponent = PokerHand(player_hand), PokerHand(opponent_hand)
            output = player.compare_with(opponent)
            if output == "Win":
                answer += 1
    return answer


if __name__ == "__main__":
    solution()
