"""
https://math.oxford.emory.edu/site/cs171/postfixExpressions/
https://en.wikipedia.org/wiki/Shunting_yard_algorithm
"""


def postfix_to_infix(postfix_expression: str) -> str:
    """
    返回值 infix 表达式 用于 给定 后缀表达式 表达式 作为 argument
    >>> postfix_to_infix("")
    Traceback (most recent call last):
        ...
    ValueError: Invalid postfix expression.
    >>> postfix_to_infix("123+*4+")
    '((1*(2+3))+4)'
    >>> postfix_to_infix("abc*+de*f+g*+")
    '((a+(b*c))+(((d*e)+f)*g))'
    >>> postfix_to_infix("xy^5z*/2+")
    '(((x^y)/(5*z))+2)'
    >>> postfix_to_infix("232^^")
    '(2^(3^2))'
    >>> postfix_to_infix("32+")
    '(3+2)'
    """

    # 检查 用于 无效输入。
    if postfix_expression is None or postfix_expression == "":
        raise ValueError("Invalid postfix expression.")

    # 创建一个 栈 到 存储 operands 并且 operators。
    stack = []

    # 迭代 超过 后缀表达式 表达式。
    for item in postfix_expression:
        # 如果 元素 是 操作数，压入 它 到 该栈。
        if item not in ["+", "-", "*", "/", "^"]:
            stack.append(item)
        else:
            # 如果 元素 是 运算符，弹出 顶部 两个 operands 从 该栈
            # 并且 concatenate 运算符 之间 它们。
            operand_2 = stack.pop()
            operand_1 = stack.pop()
            infix_expression = "(" + operand_1 + item + operand_2 + ")"

            # 压入 得到 infix 表达式 到 该栈。
            stack.append(infix_expression)

    # 顶部 元素 的栈 是 最终 infix 表达式。
    return stack.pop()


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    # Enter posfix 表达式 带有 没有 whitespaces。
    postfix_expression = "512+4*+3-"

    try:
        infix_expression = postfix_to_infix(postfix_expression)
        print("Infix expression: " + infix_expression)
    except ValueError as e:
        print(e)
