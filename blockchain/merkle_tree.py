"""
默克尔树（Merkle Tree）的构建与验证

本模块实现默克尔树的构建，以及用于验证区块链数据完整性的包含证明。

每个叶节点都是一笔交易的 SHA-256 哈希，内部节点则通过对子节点哈希的
拼接结果进行哈希计算得到。

参考资料：
https://en.wikipedia.org/wiki/Merkle_tree
"""

import hashlib


def sha256(data: str) -> str:
    """
    计算给定字符串的 SHA-256 哈希。

    参数：
        data (str): 输入字符串。

    返回：
        str: 输入内容的十六进制 SHA-256 哈希。

    示例：
        >>> sha256("abc")
        'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    """
    return hashlib.sha256(data.encode()).hexdigest()


def build_merkle_tree(leaves: list[str]) -> list[list[str]]:
    """
    根据给定的叶节点构建默克尔树。

    参数：
        leaves: 数据字符串（交易）列表。

    返回：
        表示树中各层的列表，其中最后一层包含默克尔根。

    >>> len(build_merkle_tree(["a", "b", "c", "d"])[-1][0])
    64
    """
    if not leaves:
        raise ValueError("Leaf list cannot be empty.")

    current_level = [sha256(x) for x in leaves]
    tree = [current_level]

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            next_level.append(sha256(left + right))
        current_level = next_level
        tree.append(current_level)

    return tree


def merkle_root(leaves: list[str]) -> str:
    """
    返回给定数据列表的默克尔根哈希。

    >>> r = merkle_root(["tx1", "tx2", "tx3"])
    >>> isinstance(r, str)
    True
    """
    return build_merkle_tree(leaves)[-1][0]


def verify_proof(leaf: str, proof: list[str], root: str) -> bool:
    """
    使用默克尔证明验证某个叶节点是否包含在树中。

    参数：
        leaf: 原始数据字符串。
        proof: 沿路径向上的兄弟节点哈希列表。
        root: 预期的默克尔根哈希。

    返回：
        证明有效时返回 True，否则返回 False。

    >>> data = ["a", "b", "c", "d"]
    >>> tree = build_merkle_tree(data)
    >>> root = tree[-1][0]
    >>> leaf = "a"
    >>> proof = [sha256("b"), sha256(sha256("c") + sha256("d"))]
    >>> verify_proof(leaf, proof, root)
    True
    """
    computed_hash = sha256(leaf)
    for sibling in proof:
        combined = sha256(computed_hash + sibling)
        computed_hash = combined
    return computed_hash == root


if __name__ == "__main__":
    import doctest

    doctest.testmod()
