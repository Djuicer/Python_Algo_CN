"""
一个采用工作量证明（Proof of Work，PoW）的简单区块链实现。

此教学示例展示：
- 包含索引、时间戳、数据、前一区块哈希、nonce 和哈希的区块结构
- 通过工作量证明进行挖矿
- 验证链的完整性

Author: Letitia Gilbert
"""

import hashlib
from time import time


class Block:
    """
    表示区块链中的单个区块。

    属性：
        index (int): 区块在链中的位置。
        timestamp (float): 区块的创建时间。
        data (str): 区块中存储的数据。
        previous_hash (str): 前一个区块的哈希。
        nonce (int): 用于挖矿的数值。
        hash (str): 区块内容的 SHA256 哈希。
    """

    def __init__(
        self, index: int, data: str, previous_hash: str, difficulty: int = 2
    ) -> None:
        self.index = index
        self.timestamp = time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce, self.hash = self.mine_block(difficulty)

    def compute_hash(self, nonce: int) -> str:
        """
        使用给定 nonce 计算区块的 SHA256 哈希。

        参数：
            nonce (int): 要包含在哈希计算中的 nonce。

        返回：
            str: 十六进制哈希字符串。

        >>> block = Block(0, "Genesis", "0", difficulty=2)
        >>> len(block.compute_hash(0)) == 64
        True
        >>> isinstance(block.compute_hash(0), str)
        True
        """
        block_string = (
            f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{nonce}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> tuple[int, str]:
        """
        简单的工作量证明挖矿算法。

        参数：
            difficulty (int): 哈希所需的前导零数量。

        返回：
            Tuple[int, str]: 满足难度要求的有效 nonce 及所得哈希。

        >>> block = Block(0, "Genesis", "0", difficulty=2)
        >>> block.hash.startswith('00')
        True
        """
        if difficulty < 1:
            raise ValueError("Difficulty must be at least 1")
        nonce = 0
        target = "0" * difficulty
        while True:
            hash_result = self.compute_hash(nonce)
            if hash_result.startswith(target):
                return nonce, hash_result
            nonce += 1


class Blockchain:
    """
    维护区块列表的简单区块链类。

    属性：
        chain (List[Block]): 构成区块链的区块列表。
    """

    def __init__(self, difficulty: int = 2) -> None:
        self.difficulty = difficulty
        self.chain: list[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        """
        创建区块链中的第一个区块。

        返回：
            Block: 创世区块。

        >>> bc = Blockchain()
        >>> bc.chain[0].index
        0
        >>> bc.chain[0].hash.startswith('00')
        True
        """
        return Block(0, "Genesis Block", "0", self.difficulty)

    def add_block(self, data: str) -> Block:
        """
        使用给定数据向区块链添加新区块。

        参数：
            data (str): 要存储在区块中的数据。

        返回：
            Block: 新添加的区块。

        >>> bc = Blockchain()
        >>> new_block = bc.add_block("Test Data")
        >>> new_block.index
        1
        >>> new_block.previous_hash == bc.chain[0].hash
        True
        >>> new_block.hash.startswith('00')
        True
        >>> bc.is_valid()
        True
        """
        prev_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), data, prev_hash, self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_valid(self) -> bool:
        """
        验证区块链的完整性。

        返回：
            bool: 链有效时返回 True，否则返回 False。

        >>> bc = Blockchain()
        >>> new_block = bc.add_block("Test")
        >>> new_block.index
        1
        >>> new_block.previous_hash == bc.chain[0].hash
        True
        >>> new_block.hash.startswith('00')
        True
        >>> bc.is_valid()
        True
        >>> bc.chain[1].previous_hash = "tampered"
        >>> bc.is_valid()
        False

        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.previous_hash != prev.hash:
                return False
            if not current.hash.startswith("0" * self.difficulty):
                return False
            if current.hash != current.compute_hash(current.nonce):
                return False
        return True
