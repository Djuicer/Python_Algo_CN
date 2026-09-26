def generate_parentheses_iterative(length: int) -> list[str]:
    """
    生成所有有效的括号组合（迭代方法）。

    算法步骤如下：
    1. 初始化一个空列表以保存组合。
    2. 初始化一个栈以记录尚未完成的组合。
    3. 从空字符串开始，将其与 '(' 和 ')'
       的数量一起入栈。
    4. 当栈非空时：
        a. 从栈中弹出一个未完成组合及其左右括号数量。
        b. 若组合长度等于 2*length，则将其加入结果。
        c. 若左括号数 < length，则将添加 '(' 后的新组合入栈。
        d. 若右括号数 < 左括号数，则将添加 ')' 后的新组合入栈。
    5. 返回包含所有有效组合的结果。

    Args:
        length: 期望的括号组合长度

    Returns:
        表示有效括号组合的字符串列表

    时间复杂度：
        O(2^(2*length))

    空间复杂度：
        O(2^(2*length))

    >>> generate_parentheses_iterative(3)
    ['()()()', '()(())', '(())()', '(()())', '((()))']
    >>> generate_parentheses_iterative(2)
    ['()()', '(())']
    >>> generate_parentheses_iterative(1)
    ['()']
    >>> generate_parentheses_iterative(0)
    ['']
    """
    if length == 0:
        return [""]

    result: list[str] = []
    stack: list[tuple[str, int, int]] = []

    # 栈中每个元素均为元组 (current_combination, open_count, close_count)
    stack.append(("", 0, 0))

    while stack:
        current_combination, open_count, close_count = stack.pop()

        if len(current_combination) == 2 * length:
            result.append(current_combination)
            continue

        if open_count < length:
            stack.append((current_combination + "(", open_count + 1, close_count))

        if close_count < open_count:
            stack.append((current_combination + ")", open_count, close_count + 1))

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(generate_parentheses_iterative(3))
