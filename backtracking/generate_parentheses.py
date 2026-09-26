"""
author: Aayush Soni
给定 n 对括号，编写函数生成所有
有效的括号组合。
Input: n = 2
Output: ["(())","()()"]
Leetcode link: https://leetcode.com/problems/generate-parentheses/description/
"""


def backtrack(
    partial: str, open_count: int, close_count: int, n: int, result: list[str]
) -> None:
    """
    使用递归生成所有有效的配对括号组合。

    :param partial: 表示当前组合的字符串。
    :param open_count: 表示左括号数量的整数。
    :param close_count: 表示右括号数量的整数。
    :param n: 表示括号总对数的整数。
    :param result: 保存有效组合的列表。
    :return: None

    使用递归探索所有可能的组合，
    确保每一步的括号都满足配对约束。

    示例：
    >>> result = []
    >>> backtrack("", 0, 0, 2, result)
    >>> result
    ['(())', '()()']
    """
    if len(partial) == 2 * n:
        # 组合完成后，将其加入结果。
        result.append(partial)
        return

    if open_count < n:
        # 若还能添加左括号，则添加并递归。
        backtrack(partial + "(", open_count + 1, close_count, n, result)

    if close_count < open_count:
        # 若还能添加右括号（不会使组合失效），
        # 则添加并递归。
        backtrack(partial + ")", open_count, close_count + 1, n, result)


def generate_parenthesis(n: int) -> list[str]:
    """
    生成给定 n 对括号的所有有效组合。

    :param n: 表示括号对数的整数。
    :return: 包含有效组合的字符串列表。

    使用递归方式生成组合。

    时间复杂度：O(2^(2n))，最坏情况下有 2^(2n) 个组合。
    空间复杂度：O(n)，其中 'n' 为括号对数。

    示例 1：
    >>> generate_parenthesis(3)
    ['((()))', '(()())', '(())()', '()(())', '()()()']

    示例 2：
    >>> generate_parenthesis(1)
    ['()']

    示例 3：
    >>> generate_parenthesis(0)
    ['']
    """

    result: list[str] = []
    backtrack("", 0, 0, n, result)
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
