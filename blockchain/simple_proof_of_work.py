"""
工作量证明（Proof of Work，PoW）的实现。
该算法用于在区块链技术中达成共识并保障网络安全。
"""

import hashlib


def proof_of_work(
    block_number: int, transactions: str, previous_hash: str, difficulty: int
) -> tuple[int, str]:
    """
    查找一个 nonce，使区块的 SHA-256 哈希以指定数量的零（difficulty）开头。

    >>> proof_of_work(1, "test", "abc", 1)[1].startswith("0")
    True
    >>> # Consistency check: same input must produce same output
    >>> res1 = proof_of_work(1, "data", "hash", 2)
    >>> res2 = proof_of_work(1, "data", "hash", 2)
    >>> res1 == res2
    True
    >>> # Difficulty 0 should return nonce 0 immediately
    >>> proof_of_work(1, "data", "hash", 0)[0]
    0
    """
    if difficulty < 0:
        raise ValueError("difficulty must be a non-negative integer")

    prefix = "0" * difficulty
    nonce = 0

    while True:
        # 创建表示全部区块数据的单个字符串
        text = f"{block_number}{transactions}{previous_hash}{nonce}"

        # 计算 SHA-256 哈希
        current_hash = hashlib.sha256(text.encode()).hexdigest()

        # 检查哈希是否满足难度要求
        if current_hash.startswith(prefix):
            return nonce, current_hash

        nonce += 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 用法示例：
    example_tx = "Alice sends 1 BTC to Bob"
    prev_h = "00000abcdef1234567890"
    diff = 4

    print(f"Mining block... (Difficulty: {diff})")
    nonce, hash_found = proof_of_work(1, example_tx, prev_h, diff)

    print(f"Success! Nonce: {nonce}")
    print(f"Hash: {hash_found}")
