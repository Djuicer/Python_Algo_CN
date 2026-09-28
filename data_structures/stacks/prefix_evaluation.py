"""
Program 到 evaluate 前缀 表达式。
https://en.wikipedia.org/wiki/Polish_notation
"""

operators = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
}


def is_operand(c) -> bool:
    """
    若满足以下条件则返回 True： 给定 char c 是 操作数，e.g. 它 是 数

    >>> is_operand("1")
    True
    >>> is_operand("+")
    False
    """
    return c.isdigit()


def evaluate(expression) -> float:
    """
    Evaluate 给定 表达式 在 前缀 notation。
    Asserts 该 给定 表达式 是 有效。

    >>> evaluate("+ 9 * 2 6")
    21
    >>> evaluate("/ * 10 2 + 4 1 ")
    4.0
    >>> evaluate("2")
    2
    >>> evaluate("+ * 2 3 / 8 4")
    8.0
    """
    stack = []

    # 迭代 超过 字符串 在 反转 顺序
    for c in expression.split()[::-1]:
        # 压入 操作数 到 栈
        if is_operand(c):
            stack.append(int(c))

        else:
            # 弹出 值 从 栈 可以 计算 结果
            # 压入 结果 到 该栈 again
            o1 = stack.pop()
            o2 = stack.pop()
            stack.append(operators[c](o1, o2))

    return stack.pop()


def evaluate_recursive(expression: list[str]) -> float:
    """
    Alternative 递归 实现

    >>> evaluate_recursive(['2'])
    2
    >>> expression = ['+', '*', '2', '3', '/', '8', '4']
    >>> evaluate_recursive(expression)
    8.0
    >>> expression
    []
    >>> evaluate_recursive(['+', '9', '*', '2', '6'])
    21
    >>> evaluate_recursive(['/', '*', '10', '2', '+', '4', '1'])
    4.0
    """

    op = expression.pop(0)
    if is_operand(op):
        return int(op)

    operation = operators[op]

    a = evaluate_recursive(expression)
    b = evaluate_recursive(expression)
    return operation(a, b)


# Driver 代码
if __name__ == "__main__":
    test_expression = "+ 9 * 2 6"
    print(evaluate(test_expression))

    test_expression = "/ * 10 2 + 4 1 "
    print(evaluate(test_expression))
