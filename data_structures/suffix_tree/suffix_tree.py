#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11554
#  https://github.com/TheAlgorithms/Python/pull/11554
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

from data_structures.suffix_tree.suffix_tree_node import SuffixTreeNode


class SuffixTree:
    def __init__(self, text: str) -> None:
        """
        Initializes 后缀 树 带有 给定 文本。

        参数：
            文本 (str): 文本 用于 其 后缀 树 是 到 为 built。
        """
        self.text: str = text
        self.root: SuffixTreeNode = SuffixTreeNode()
        self.build_suffix_tree()

    def build_suffix_tree(self) -> None:
        """
        Builds 后缀 树 用于 给定 文本 通过 添加 所有 suffixes。
        """
        text = self.text
        n = len(text)
        for i in range(n):
            suffix = text[i:]
            self._add_suffix(suffix, i)

    def _add_suffix(self, suffix: str, index: int) -> None:
        """
        Adds 后缀 到 后缀 树。

        参数：
            后缀 (str): 后缀 到 添加。
            索引 (int): 起始 索引 的 后缀 在 原始 文本。
        """
        node = self.root
        for char in suffix:
            if char not in node.children:
                node.children[char] = SuffixTreeNode()
            node = node.children[char]
        node.is_end_of_string = True
        node.start = index
        node.end = index + len(suffix) - 1

    def search(self, pattern: str) -> bool:
        """
        搜索 模式 在 后缀 树。

        参数：
            模式 (str): 模式 到 搜索。

        返回值：
            bool: True 如果 模式 是 找到，False 否则。
        """
        node = self.root
        for char in pattern:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
