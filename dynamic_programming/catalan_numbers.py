"""
输出从 0 到 n 的所有卡特兰数，其中 n 由用户输入。

 * 卡特兰数是一个正整数数列，出现在组合数学的许多计数问题中 [1]。
 * 这些问题包括计算 [2]：
 * - 长度为 2n 的 Dyck 词数量
 * - 由 n 对括号组成的良构表达式数量
 *   （例如，`()()` 有效，而 `())(` 无效）
 * - 对 n + 1 个因子添加完整括号的不同方式数
 *   （例如，当 n = 2 时，C(n) = 2，(ab)c 和 a(bc)
 *   是两种有效的加括号方式）
 * - 具有 n + 1 个叶节点的满二叉树数量

 * 卡特兰数满足以下递推关系，本算法将使用该关系 [1]。
 * C(0) = C(1) = 1
 * C(n) = sum(C(i).C(n-i-1)), from i = 0 to n-1

 * 此外，第 n 个卡特兰数可以使用以下闭式公式计算 [1]：
 * C(n) = (1 / (n + 1)) * (2n choose n)

 * 来源：
 *  [1] https://brilliant.org/wiki/catalan-numbers/
 *  [2] https://en.wikipedia.org/wiki/Catalan_number
"""


def catalan_numbers(upper_limit: int) -> "list[int]":
    """
    返回从 0 到 `upper_limit` 的卡特兰数数列。

    >>> catalan_numbers(5)
    [1, 1, 2, 5, 14, 42]
    >>> catalan_numbers(2)
    [1, 1, 2]
    >>> catalan_numbers(-1)
    Traceback (most recent call last):
    ValueError: Limit for the Catalan sequence must be ≥ 0
    """
    if upper_limit < 0:
        raise ValueError("Limit for the Catalan sequence must be ≥ 0")

    catalan_list = [0] * (upper_limit + 1)

    # 边界条件：C(0) = C(1) = 1
    catalan_list[0] = 1
    if upper_limit > 0:
        catalan_list[1] = 1

    # 递推关系：C(i) = sum(C(j).C(i-j-1)), from j = 0 to i
    for i in range(2, upper_limit + 1):
        for j in range(i):
            catalan_list[i] += catalan_list[j] * catalan_list[i - j - 1]

    return catalan_list


if __name__ == "__main__":
    print("\n********* Catalan Numbers Using Dynamic Programming ************\n")
    print("\n*** Enter -1 at any time to quit ***")
    print("\nEnter the upper limit (≥ 0) for the Catalan number sequence: ", end="")
    try:
        while True:
            N = int(input().strip())
            if N < 0:
                print("\n********* Goodbye!! ************")
                break
            else:
                print(f"The Catalan numbers from 0 through {N} are:")
                print(catalan_numbers(N))
                print("Try another upper limit for the sequence: ", end="")
    except NameError, ValueError:
        print("\n********* Invalid input, goodbye! ************\n")

    import doctest

    doctest.testmod()
