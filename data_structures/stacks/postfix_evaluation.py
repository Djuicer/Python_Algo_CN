"""
反转 Polish Nation 是 也 known 作为 Polish 后缀表达式 notation 或 simply 后缀表达式
notation.
https://en.wikipedia.org/wiki/Reverse_Polish_notation
Classic 示例 的 simple 栈 implementations。
有效 operators 是 +，-，*，/。
每个 操作数 may 为 整数 或 另一个 表达式。

输出：

Enter 后缀表达式 Equation (空间 separated) = 5 6 9 * +
 Symbol  |    Action    | 栈
-----------------------------------
       5 | 压入(5)      | 5
       6 | 压入(6)      | 5,6
       9 | 压入(9)      | 5,6,9
         | 弹出(9)       | 5,6
         | 弹出(6)       | 5
       * | 压入(6*9)    | 5,54
         | 弹出(54)      | 5
         | 弹出(5)       |
       + | 压入(5+54)   | 59

        结果 =  59
"""

# Defining 有效 unary 运算符 symbols
UNARY_OP_SYMBOLS = ("-", "+")

# operators & 它们的 respective 操作
OPERATORS = {
    "^": lambda p, q: p**q,
    "*": lambda p, q: p * q,
    "/": lambda p, q: p / q,
    "+": lambda p, q: p + q,
    "-": lambda p, q: p - q,
}


def parse_token(token: str | float) -> float | str:
    """
    转换 给定 数据 到 appropriate 数 如果 它 是 indeed 数，否则
    返回值 数据 作为 它 是 带有 False flag. 此函数 也 serves 作为 检查
    的 是否 输入 是 数 或 不。

    参数
    ----------
    token: 数据 该 needs 到 为 converted 到 appropriate 运算符 或 数。

    返回值
    -------
    浮点数 或 str
        返回值 浮点数 如果 `token` 是 数 或 str 如果 `token` 是 运算符
    """
    if token in OPERATORS:
        return token
    try:
        return float(token)
    except ValueError:
        msg = f"{token} is neither a number nor a valid operator"
        raise ValueError(msg)


def evaluate(post_fix: list[str], verbose: bool = False) -> float:
    """
    Evaluate 后缀表达式 表达式 使用 栈。
    >>> evaluate(["0"])
    0.0
    >>> evaluate(["-0"])
    -0.0
    >>> evaluate(["1"])
    1.0
    >>> evaluate(["-1"])
    -1.0
    >>> evaluate(["-1.1"])
    -1.1
    >>> evaluate(["2", "1", "+", "3", "*"])
    9.0
    >>> evaluate(["2", "1.9", "+", "3", "*"])
    11.7
    >>> evaluate(["2", "-1.9", "+", "3", "*"])
    0.30000000000000027
    >>> evaluate(["4", "13", "5", "/", "+"])
    6.6
    >>> evaluate(["2", "-", "3", "+"])
    1.0
    >>> evaluate(["-4", "5", "*", "6", "-"])
    -26.0
    >>> evaluate([])
    0
    >>> evaluate(["4", "-", "6", "7", "/", "9", "8"])
    Traceback (most recent call last):
    ...
    ArithmeticError: Input is not a valid postfix expression

    参数
    ----------
    post_fix:
        后缀表达式 表达式 是 tokenized 到 operators 并且 operands 并且 存储
        作为 Python 列表

    verbose:
        显示 栈 contents 当 evaluating 表达式 如果 verbose 是 True

    返回值
    -------
    浮点数
        evaluated 值
    """
    if not post_fix:
        return 0
    # Checking 该列表 到 查找 out 是否 后缀表达式 表达式 是 有效
    valid_expression = [parse_token(token) for token in post_fix]
    if verbose:
        # 打印 table header
        print("Symbol".center(8), "Action".center(12), "Stack", sep=" | ")
        print("-" * (30 + len(post_fix)))
    stack = []
    for x in valid_expression:
        if x not in OPERATORS:
            stack.append(x)  # 追加 x 到 栈
            if verbose:
                # 输出 在 表格形式 格式
                print(
                    f"{x}".rjust(8),
                    f"push({x})".ljust(12),
                    stack,
                    sep=" | ",
                )
            continue
        # 如果 x 是 运算符
        # 如果 仅 1 值 是 inside 该栈 并且 + 或 - 是 遇到
        # 则 此 是 unary + 或 - 情况
        if x in UNARY_OP_SYMBOLS and len(stack) < 2:
            b = stack.pop()  # 弹出 栈
            if x == "-":
                b *= -1  # 对 b 取反
            stack.append(b)
            if verbose:
                # 输出 在 表格形式 格式
                print(
                    "".rjust(8),
                    f"pop({b})".ljust(12),
                    stack,
                    sep=" | ",
                )
                print(
                    str(x).rjust(8),
                    f"push({x}{b})".ljust(12),
                    stack,
                    sep=" | ",
                )
            continue
        b = stack.pop()  # 弹出 栈
        if verbose:
            # 输出 在 表格形式 格式
            print(
                "".rjust(8),
                f"pop({b})".ljust(12),
                stack,
                sep=" | ",
            )

        a = stack.pop()  # 弹出 栈
        if verbose:
            # 输出 在 表格形式 格式
            print(
                "".rjust(8),
                f"pop({a})".ljust(12),
                stack,
                sep=" | ",
            )
        # evaluate 2 值 popped 从 栈 & 压入 结果 到 栈
        stack.append(OPERATORS[x](a, b))  # type: ignore[index]
        if verbose:
            # 输出 在 表格形式 格式
            print(
                f"{x}".rjust(8),
                f"push({a}{x}{b})".ljust(12),
                stack,
                sep=" | ",
            )
    # 如果 everything 是 executed correctly，该栈 将 包含
    # 仅 一个 元素 其 是 结果
    if len(stack) != 1:
        raise ArithmeticError("Input is not a valid postfix expression")
    return float(stack[0])


if __name__ == "__main__":
    # 创建一个 循环 因此 该 user 可以 evaluate 后缀表达式 expressions multiple times
    while True:
        expression = input("Enter a Postfix Expression (space separated): ").split(" ")
        prompt = "Do you want to see stack contents while evaluating? [y/N]: "
        verbose = input(prompt).strip().lower() == "y"
        output = evaluate(expression, verbose)
        print("Result = ", output)
        prompt = "Do you want to enter another expression? [y/N]: "
        if input(prompt).strip().lower() != "y":
            break
