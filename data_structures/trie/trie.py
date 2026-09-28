"""
Trie/前缀 树 是 kind 的 搜索 树 使用 到 提供 quick lookup
的 单词/patterns 在 集合 的 单词. basic Trie however 具有 O(n^2) 空间复杂度
making 它 impractical 在 practice. 它 however 提供 O(最大值(search_string，长度 的
longest 单词)) lookup 时间 making 它 optimal 方法 当 空间 是 不 问题。
"""


class TrieNode:
    def __init__(self) -> None:
        self.nodes: dict[str, TrieNode] = {}  # Mapping 从 char 到 TrieNode
        self.is_leaf = False

    def insert_many(self, words: list[str]) -> None:
        """
        插入一个 列表 的 单词 到 Trie
        :param 单词: 列表 的 字符串 单词
        :返回: None
        """
        for word in words:
            self.insert(word)

    def insert(self, word: str) -> None:
        """
        插入一个 单词 到 Trie
        :param 单词: 单词 到 为 已插入
        :返回: None
        """
        curr = self
        for char in word:
            if char not in curr.nodes:
                curr.nodes[char] = TrieNode()
            curr = curr.nodes[char]
        curr.is_leaf = True

    def find(self, word: str) -> bool:
        """
        Tries 到 查找 单词 在 Trie
        :param 单词: 单词 到 look 用于
        :返回: 若满足以下条件则返回 True： 单词 是 找到，False 否则
        """
        curr = self
        for char in word:
            if char not in curr.nodes:
                return False
            curr = curr.nodes[char]
        return curr.is_leaf

    def delete(self, word: str) -> None:
        """
        删除一个 单词 在 Trie
        :param 单词: 单词 到 删除
        :返回: None
        """

        def _delete(curr: TrieNode, word: str, index: int) -> bool:
            if index == len(word):
                # 如果 单词 不存在
                if not curr.is_leaf:
                    return False
                curr.is_leaf = False
                return len(curr.nodes) == 0
            char = word[index]
            char_node = curr.nodes.get(char)
            # 如果 char 不 在 当前 trie 节点
            if not char_node:
                return False
            # Flag 到 检查是否 节点 可以 为 已删除
            delete_curr = _delete(char_node, word, index + 1)
            if delete_curr:
                del curr.nodes[char]
                return len(curr.nodes) == 0
            return delete_curr

        _delete(self, word, 0)


def print_words(node: TrieNode, word: str) -> None:
    """
    打印 所有 单词 在 Trie
    :param 节点: 根节点 的 Trie
    :param 单词: 单词 变量 应 为 空 在 开始
    :返回: None
    """
    if node.is_leaf:
        print(word, end=" ")

    for key, value in node.nodes.items():
        print_words(value, word + key)


def test_trie() -> bool:
    words = "banana bananas bandana band apple all beast".split()
    root = TrieNode()
    root.insert_many(words)
    # print_words(根节点，"")
    assert all(root.find(word) for word in words)
    assert root.find("banana")
    assert not root.find("bandanas")
    assert not root.find("apps")
    assert root.find("apple")
    assert root.find("all")
    root.delete("all")
    assert not root.find("all")
    root.delete("banana")
    assert not root.find("banana")
    assert root.find("bananas")
    return True


def print_results(msg: str, passes: bool) -> None:
    print(str(msg), "works!" if passes else "doesn't work :(")


def pytests() -> None:
    assert test_trie()


def main() -> None:
    """
    >>> pytests()
    """
    print_results("Testing trie functionality", test_trie())


if __name__ == "__main__":
    main()
