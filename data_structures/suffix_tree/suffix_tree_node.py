#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11554
#  https://github.com/TheAlgorithms/Python/pull/11554
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

from __future__ import annotations


class SuffixTreeNode:
    def __init__(
        self,
        children: dict[str, SuffixTreeNode] | None = None,
        is_end_of_string: bool = False,
        start: int | None = None,
        end: int | None = None,
        suffix_link: SuffixTreeNode | None = None,
    ) -> None:
        """
        Initializes 后缀 树 节点。

        参数：
            子节点 (dict[str，SuffixTreeNode] | None): 子节点 的 此 节点。
            is_end_of_string (bool): Indicates 如果 此 节点 表示
                                     末尾 的 字符串。
            开始 (int | None): 开始 索引 的 后缀 在 文本。
            末尾 (int | None): 末尾 索引 的 后缀 在 文本。
            suffix_link (SuffixTreeNode | None): 链接 到 另一个 后缀 树 节点。
        """
        self.children = children or {}
        self.is_end_of_string = is_end_of_string
        self.start = start
        self.end = end
        self.suffix_link = suffix_link
