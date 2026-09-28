#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11554
#  https://github.com/TheAlgorithms/Python/pull/11554
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

import unittest

from data_structures.suffix_tree.suffix_tree import SuffixTree


class TestSuffixTree(unittest.TestCase):
    def setUp(self) -> None:
        """集合 向上 初始 conditions 对于每个 测试。"""
        self.text = "banana"
        self.suffix_tree = SuffixTree(self.text)

    def test_search_existing_patterns(self) -> None:
        """测试 搜索 用于 patterns 该 exist 在 后缀 树。"""
        patterns = ["ana", "ban", "na"]
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                assert self.suffix_tree.search(pattern), (
                    f"Pattern '{pattern}' should be found."
                )

    def test_search_non_existing_patterns(self) -> None:
        """测试 搜索 用于 patterns 该 do 不 exist 在 后缀 树。"""
        patterns = ["xyz", "apple", "cat"]
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                assert not self.suffix_tree.search(pattern), (
                    f"Pattern '{pattern}' should not be found."
                )

    def test_search_empty_pattern(self) -> None:
        """测试 搜索 用于 空 模式。"""
        assert self.suffix_tree.search(""), "An empty pattern should be found."

    def test_search_full_text(self) -> None:
        """测试 搜索 用于 已满 文本。"""
        assert self.suffix_tree.search(self.text), (
            "The full text should be found in the suffix tree."
        )

    def test_search_substrings(self) -> None:
        """测试 搜索 用于 substrings 的 已满 文本。"""
        substrings = ["ban", "ana", "a", "na"]
        for substring in substrings:
            with self.subTest(substring=substring):
                assert self.suffix_tree.search(substring), (
                    f"Substring '{substring}' should be found."
                )


if __name__ == "__main__":
    unittest.main()
