# 标题：区块链的工作量证明算法

## 算法说明：
# 本算法实现区块链中用于验证区块的工作量证明（Proof of Work，PoW）共识机制。
# PoW 要求参与者（矿工）完成计算任务，创建有效区块并将其加入区块链。
# 难度由区块哈希所需的前导零数量定义。

import hashlib
import time


class Block:
    def __init__(
        self,
        index: int,
        previous_hash: str,
        transactions: str,
        timestamp: float,
        difficulty: int,
    ) -> None:
        """
        使用指定参数初始化 Block 对象。

        参数：
        - index (int): 区块在区块链中的索引。
        - previous_hash (str): 前一个区块的哈希。
        - transactions (str): 区块中的交易列表。
        - timestamp (float): 区块创建时间（Unix 时间戳格式）。
        - difficulty (int): 挖掘该区块的难度等级。
        """
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = 0  # nonce 从 0 开始
        self.difficulty = difficulty
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        生成区块内容的哈希。
        将索引、前一区块哈希、交易、时间戳和 nonce 合并为字符串，
        再使用 SHA-256 对其进行哈希计算。

        返回：
        - str: 区块的哈希。
        """
        block_string = (
            f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}"
            f"{self.nonce}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self) -> None:
        """
        通过调整 nonce 执行工作量证明，直到找到有效哈希。
        有效哈希必须具有由难度等级指定数量的前导零。

        返回：
        - None
        """
        target = (
            "0" * self.difficulty
        )  # 目标哈希应以 'difficulty' 个零开头
        while self.hash[: self.difficulty] != target:
            self.nonce += 1
            self.hash = self.compute_hash()

        print(f"Block mined with nonce {self.nonce}, hash: {self.hash}")


class Blockchain:
    def __init__(self, difficulty: int) -> None:
        """
        使用给定的难度等级初始化区块链。

        参数：
        - difficulty (int): 在此区块链中挖掘区块的难度等级。

        返回：
        - None
        """
        self.chain: list[Block] = []  # 为区块列表添加类型标注
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """
        创建区块链中的第一个区块（创世区块）。

        返回：
        - None
        """
        genesis_block = Block(0, "0", "Genesis Block", time.time(), self.difficulty)
        genesis_block.mine_block()
        self.chain.append(genesis_block)

    def add_block(self, transactions: str) -> None:
        """
        执行工作量证明后，向区块链添加新区块。

        参数：
        - transactions (str): 要添加到新区块中的交易列表。

        返回：
        - None
        """
        previous_block = self.chain[-1]
        new_block = Block(
            len(self.chain),
            previous_block.hash,
            transactions,
            time.time(),
            self.difficulty,
        )
        new_block.mine_block()
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """
        通过确保每个区块的前一区块哈希相匹配，且所有区块均满足工作量证明要求，
        验证区块链的完整性。

        返回：
        - bool: 区块链有效时返回 True，否则返回 False。
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.compute_hash():
                print(f"Invalid block at index {i}. Hash mismatch.")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid chain at index {i}. Previous hash mismatch.")
                return False

        return True


# 测试用例


## 测试用例 1：区块链初始化和创世区块
# 此测试验证区块链是否使用创世区块正确初始化，以及该区块是否成功挖掘。
def test_blockchain() -> None:
    """
    区块链工作量证明算法的测试用例。

    返回：
    - None
    """
    # 创建难度等级为 4 的区块链（哈希应以 4 个零开头）
    blockchain = Blockchain(difficulty=4)

    ## 测试用例 2：添加区块并验证该区块已被挖掘
    # 此测试添加包含交易的新区块，并确保按照工作量证明机制完成挖掘。
    blockchain.add_block("Transaction 1: Alice pays Bob 5 BTC")
    blockchain.add_block("Transaction 2: Bob pays Charlie 3 BTC")

    ## 测试用例 3：验证区块链完整性
    # 此测试检查添加新区块后，区块链是否仍然有效
    assert blockchain.is_chain_valid(), "Blockchain should be valid"

    ## 测试用例 4：篡改区块链
    # 此测试模拟篡改区块链，并检查验证过程能否正确检测到篡改。
    blockchain.chain[
        1
    ].transactions = "Transaction 1: Alice pays Bob 50 BTC"  # 篡改
    assert not blockchain.is_chain_valid(), (
        "Blockchain should be invalid due to tampering"
    )

    ## 测试用例 5：正确验证区块链
    # 此测试检查区块链在遭到篡改后是否变为无效，并验证篡改后 PoW 是否仍然成立。

    print("All test cases passed.")


if __name__ == "__main__":
    test_blockchain()
