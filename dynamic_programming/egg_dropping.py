"""
计算最坏情况下找到临界楼层所需的最少尝试次数，鸡蛋从该楼层落下时会开始破碎。
"""

# 鸡蛋掉落问题是一个经典的动态规划问题。
# - 给定 `k` 个鸡蛋和一栋有 `n` 层的建筑。目标是确定找到最高楼层 `F`
#   所需的最少尝试次数，鸡蛋从该楼层落下时会破碎。如果鸡蛋从楼层 `F`
#   落下会破碎，那么从 `F` 以上的任何楼层落下也会破碎。
#   该问题要求将最坏情况下的尝试次数降至最低。


def egg_dropping(eggs: int, floors: int) -> int:
    """
    使用动态规划计算给定 `eggs` 和 `floors` 时最坏情况下所需的最少尝试次数。

    >>> egg_dropping(1, 5)
    5
    >>> egg_dropping(2, 6)
    3
    >>> egg_dropping(2, 10)
    4
    """

    # 边界条件：没有楼层需要 0 次尝试，一层楼需要 1 次尝试
    if floors in (0, 1):
        return floors
    if eggs == 1:
        return floors

    # 创建 DP 表以存储子问题的结果
    dp = [[0 for _ in range(floors + 1)] for _ in range(eggs + 1)]

    # 填充只有一个鸡蛋时的边界条件（即 `i` 层楼需要尝试 `i` 次）
    for i in range(1, floors + 1):
        dp[1][i] = i

    # 计算每种组合在最坏情况下的最少尝试次数
    for e in range(2, eggs + 1):
        for f in range(1, floors + 1):
            dp[e][f] = 10**9  # 初始化为无穷大
            for x in range(1, f + 1):
                res = 1 + max(dp[e - 1][x - 1], dp[e][f - x])
                dp[e][f] = min(dp[e][f], res)

    return dp[eggs][floors]


if __name__ == "__main__":
    print("\n********* Egg Dropping Problem Using Dynamic Programming ************\n")
    print("\n*** Enter -1 at any time to quit ***")
    print("\nEnter the number of eggs and floors separated by a space: ", end="")
    try:
        while True:
            input_data = input().strip()
            if input_data == "-1":
                print("\n********* Goodbye!! ************")
                break
            else:
                eggs, floors = map(int, input_data.split())
                print(
                    f"The minimum number of attempts required with {eggs} eggs and "
                    f"{floors} floors is:"
                )
                print(egg_dropping(eggs, floors))
                print("Try another combination of eggs and floors: ", end="")
    except NameError, ValueError:
        print("\n********* Invalid input, goodbye! ************\n")
