"""
Radix 树 是 数据 结构 该 表示 空间-optimized
trie (前缀 树) 在 其 每个节点 该 是 仅 子节点 是 合并后
with its parent [https://en.wikipedia.org/wiki/Radix_tree]
"""

import unittest


class RadixNode:
    def __init__(self, prefix: str = "", is_leaf: bool = False) -> None:
        # Mapping 从 第一个 字符 的 前缀 的节点
        self.nodes: dict[str, RadixNode] = {}

        # 一个节点 将 为 叶节点 如果 该树 包含 其 单词
        self.is_leaf = is_leaf

        self.prefix = prefix

    def match(self, word: str) -> tuple[str, str, str]:
        """计算 common substring 的 前缀 的节点 并且 单词

        参数：
            单词 (str): 单词 到 比较

        返回值：
            (str, str, str): common substring, remaining prefix, remaining word

        >>> RadixNode("myprefix").match("mystring")
        ('my', 'prefix', 'string')
        """
        x = 0
        for q, w in zip(self.prefix, word):
            if q != w:
                break

            x += 1

        return self.prefix[:x], self.prefix[x:], word[x:]

    def insert_many(self, words: list[str]) -> None:
        """插入 many 单词 在 该树

        参数：
            单词 (列表[str]): 列表 的 单词

        >>> RadixNode("myprefix").insert_many(["mystring", "hello"])
        """
        for word in words:
            self.insert(word)

    def insert(self, word: str) -> None:
        """插入一个 单词 到 该树

        参数：
            单词 (str): 单词 到 插入

        >>> RadixNode("myprefix").insert("mystring")

        >>> root = RadixNode()
        >>> root.insert_many(['myprefix', 'myprefixA', 'myprefixAA'])
        >>> root.print_tree()
        - myprefix   (leaf)
        -- A   (leaf)
        --- A   (leaf)
        """
        ## Handle 情况 其中 单词 为空 通过 使用 如果 branch
        if word == "":
            self.is_leaf = True
            return

        # 情况 1: 如果 单词 是 前缀 的节点
        # 解: 我们 设置 当前节点 作为 叶节点
        if self.prefix == word and not self.is_leaf:
            self.is_leaf = True

        # 情况 2: 该节点 具有 没有 edges 该 具有 前缀 到 单词
        # 解: 我们 创建一个 edge 从 当前节点 到 新 一个
        # 包含 单词
        elif word[0] not in self.nodes:
            self.nodes[word[0]] = RadixNode(prefix=word, is_leaf=True)

        else:
            incoming_node = self.nodes[word[0]]
            matching_string, remaining_prefix, remaining_word = incoming_node.match(
                word
            )

            # 情况 3: 该节点 前缀 是 等于 到 matching
            # 解: 我们 插入 剩余 单词 在 下一个节点
            if remaining_prefix == "":
                self.nodes[matching_string[0]].insert(remaining_word)

            # 情况 4: 单词 是 更大 比 或 等于 到 matching
            # 解: 创建一个 节点 在 之间 两者 节点，更改
            # prefixes 并且 添加 新节点 用于 剩余 单词
            else:
                incoming_node.prefix = remaining_prefix

                aux_node = self.nodes[matching_string[0]]
                self.nodes[matching_string[0]] = RadixNode(matching_string, False)
                self.nodes[matching_string[0]].nodes[remaining_prefix[0]] = aux_node

                if remaining_word == "":
                    self.nodes[matching_string[0]].is_leaf = True
                else:
                    self.nodes[matching_string[0]].insert(remaining_word)

    def find(self, word: str) -> bool:
        """返回值 是否 单词 是 在 该树

        参数：
            单词 (str): 单词 到 检查

        返回值：
            bool: True 如果 单词 appears 在 该树

        >>> RadixNode("myprefix").find("mystring")
        False
        """
        incoming_node = self.nodes.get(word[0], None)
        if not incoming_node:
            return False
        else:
            _matching_string, remaining_prefix, remaining_word = incoming_node.match(
                word
            )
            # 如果 其中 是 剩余 前缀，单词 可以't 为 在 该树
            if remaining_prefix != "":
                return False
            # 此 applies 当 单词 并且 前缀 是 等于
            elif remaining_word == "":
                return incoming_node.is_leaf
            # 我们 具有 单词 剩余 因此 我们 检查 下一个节点
            else:
                return incoming_node.find(remaining_word)

    def delete(self, word: str) -> bool:
        """删除一个 单词 从 该树 如果 它 存在

        参数：
            单词 (str): 单词 到 为 已删除

        返回值：
            bool: True 如果 单词 曾是 找到 并且 已删除. False 如果 单词 是 未找到

        >>> RadixNode("myprefix").delete("mystring")
        False
        """
        incoming_node = self.nodes.get(word[0], None)
        if not incoming_node:
            return False
        else:
            _matching_string, remaining_prefix, remaining_word = incoming_node.match(
                word
            )
            # 如果 其中 是 剩余 前缀，单词 可以't 为 在 该树
            if remaining_prefix != "":
                return False
            # 我们 具有 单词 剩余 因此 我们 检查 下一个节点
            elif remaining_word != "":
                return incoming_node.delete(remaining_word)
            # 如果 它 是 不 叶节点，我们 don't 具有 到 删除
            elif not incoming_node.is_leaf:
                return False
            else:
                # 我们 删除 节点 如果 没有 edges 前进 从 它
                if len(incoming_node.nodes) == 0:
                    del self.nodes[word[0]]
                    # 我们 合并 当前节点 带有 其 仅 子节点
                    if len(self.nodes) == 1 and not self.is_leaf:
                        merging_node = next(iter(self.nodes.values()))
                        self.is_leaf = merging_node.is_leaf
                        self.prefix += merging_node.prefix
                        self.nodes = merging_node.nodes
                # 如果 其中 是 更多 比 1 edge，我们 仅 mark 它 作为 非-叶节点
                elif len(incoming_node.nodes) > 1:
                    incoming_node.is_leaf = False
                # 如果 其中 是 1 edge，我们 合并 它 带有 其 子节点
                else:
                    merging_node = next(iter(incoming_node.nodes.values()))
                    incoming_node.is_leaf = merging_node.is_leaf
                    incoming_node.prefix += merging_node.prefix
                    incoming_node.nodes = merging_node.nodes

                return True

    def print_tree(self, height: int = 0) -> None:
        """打印 树

        参数：
            高度 (int，可选): 高度 的 printed 节点
        """
        if self.prefix != "":
            print("-" * height, self.prefix, "  (leaf)" if self.is_leaf else "")

        for value in self.nodes.values():
            value.print_tree(height + 1)


def test_trie() -> None:
    words = "banana bananas bandana band apple all beast".split()
    root = RadixNode()
    root.insert_many(words)

    assert all(root.find(word) for word in words)
    assert not root.find("bandanas")
    assert not root.find("apps")
    root.delete("all")
    assert not root.find("all")
    root.delete("banana")
    assert not root.find("banana")
    assert root.find("bananas")


class TestRadixNode(unittest.TestCase):
    def test_trie(self) -> None:
        words = "banana bananas bandana band apple all beast".split()
        root = RadixNode()
        root.insert_many(words)

        assert all(root.find(word) for word in words)
        assert not root.find("bandanas")
        assert not root.find("apps")
        root.delete("all")
        assert not root.find("all")
        root.delete("banana")
        assert not root.find("banana")
        assert root.find("bananas")

    def test_trie_2(self) -> None:
        """
        现在 添加 新 测试 情况 该 inserts
        foobbb，fooaaa，foo 在 给定 顺序 并且 checks
        用于 不同 assertions
        """
        words = "foobbb fooaaa foo".split()
        root = RadixNode()
        root.insert_many(words)

        assert all(root.find(word) for word in words)
        root.delete("foo")
        assert not root.find("foo")
        assert root.find("foobbb")
        assert root.find("fooaaa")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
