"""
Author: Alexander Joslin
GitHub: github.com/echoaj

Explanation:  https://medium.com/@haleesammar/implemented-in-js-dijkstras-2-stack-
              算法-用于-evaluating-mathematical-expressions-fc0837dae1ea

我们 可以 使用 Dijkstra's 两个 栈 算法 到 solve equation
such 作为: (5 + ((4 * 2) * (2 + 3)))

这些 是 算法'S RULES：
RULE 1: Scan 表达式 从左到右. 当 操作数 是 遇到,
        压入 它 到 操作数 栈。

RULE 2: 当 运算符 是 遇到 在 表达式,
        压入 它 到 运算符 栈。

RULE 3: 当 左 parenthesis 是 遇到 在 表达式，ignore 它。

RULE 4: 当 右 parenthesis 是 遇到 在 表达式,
        弹出 运算符 off 运算符 栈.  两个 operands 它 必须
        operate 在 必须 为 最后一个 两个 operands pushed 到 操作数 栈。
        我们 therefore 弹出 操作数 栈 twice，执行 操作,
        并且 压入 结果 后端 到 操作数 栈 因此 它 将 为 可用
        用于 使用 作为 操作数 的 下一个 运算符 popped off 运算符 栈。

RULE 5: 当 整个 infix 表达式 具有 been scanned，该值 左 在
        操作数 栈 表示 该值 的 表达式。

NOTE:   它 仅 works 带有 whole 数。
"""

__author__ = "Alexander Joslin"

import operator as op

from .stack import Stack


def dijkstras_two_stack_algorithm(equation: str) -> int:
    """
    DocTests
    >>> dijkstras_two_stack_algorithm("(5 + 3)")
    8
    >>> dijkstras_two_stack_algorithm("((9 - (2 + 9)) + (8 - 1))")
    5
    >>> dijkstras_two_stack_algorithm("((((3 - 2) - (2 + 3)) + (2 - 4)) + 3)")
    -3

    :param equation: 字符串
    :返回: 结果: 整数
    """
    operators = {"*": op.mul, "/": op.truediv, "+": op.add, "-": op.sub}

    operand_stack: Stack[int] = Stack()
    operator_stack: Stack[str] = Stack()

    for i in equation:
        if i.isdigit():
            # 规则 1
            operand_stack.push(int(i))
        elif i in operators:
            # 规则 2
            operator_stack.push(i)
        elif i == ")":
            # 规则 4
            opr = operator_stack.peek()
            operator_stack.pop()
            num1 = operand_stack.peek()
            operand_stack.pop()
            num2 = operand_stack.peek()
            operand_stack.pop()

            total = operators[opr](num2, num1)
            operand_stack.push(total)

    # 规则 5
    return operand_stack.peek()


if __name__ == "__main__":
    equation = "(5 + ((4 * 2) * (2 + 3)))"
    # answer = 45
    print(f"{equation} = {dijkstras_two_stack_algorithm(equation)}")
