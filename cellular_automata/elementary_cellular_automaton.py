"""
初等元胞自动机——规则 30
-----------------------

由 Stephen Wolfram 提出的一维元胞自动机。
每个元胞的下一状态取决于其当前状态及紧邻的两个元胞。

参考资料：
    https://en.wikipedia.org/wiki/Rule_30
"""


def rule_30_step(current: list[int]) -> list[int]:
    """
    按照 Wolfram 的规则 30 计算一维元胞自动机的下一代。

    每个元胞的下一状态由其左侧、自身和右侧元胞决定。

    参数：
        current (list[int]): 由 0（死亡）和 1（存活）组成的当前代列表。

    返回：
        list[int]: 由 0 和 1 组成的下一代列表。

    示例：
        >>> rule_30_step([0, 0, 1, 0, 0])
        [0, 1, 1, 1, 0]
    """
    next_gen = []
    for i in range(len(current)):
        left = current[i - 1] if i > 0 else 0
        center = current[i]
        right = current[i + 1] if i < len(current) - 1 else 0

        # 将相邻元胞组合为 3 位模式
        pattern = (left << 2) | (center << 1) | right

        # 规则 30 的二进制形式：00011110（30 的位表示）
        next_gen.append((30 >> pattern) & 1)

    return next_gen


def generate_rule_30(size: int = 31, generations: int = 15) -> list[list[int]]:
    """
    生成规则 30 元胞自动机的多代状态。

    参数：
        size (int): 每一代的元胞数量，默认值为 31。
        generations (int): 演化的代数，默认值为 15。

    返回：
        list[list[int]]: 各代状态的列表（每一代均为由 0 和 1 组成的列表）。

    示例：
        >>> len(generate_rule_30(15, 5))
        5
    """
    grid = [[0] * size for _ in range(generations)]
    grid[0][size // 2] = 1  # 初始状态仅在中央放置一个活细胞

    for i in range(1, generations):
        grid[i] = rule_30_step(grid[i - 1])

    return grid


if __name__ == "__main__":
    # 运行示例模拟
    generations = generate_rule_30(31, 15)
    for row in generations:
        print("".join("█" if cell else " " for cell in row))
