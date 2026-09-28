"""
输出：

Enter Infix Equation = + b ^c
 Symbol  |  栈  | 后缀表达式
----------------------------
   c     |         | c
   ^     | ^       | c
   b     | ^       | cb
   +     | +       | cb^
   | +       | cb^
         |         | cb^+

         +b^c (Infix) ->  +^bc (前缀)
"""


def infix_2_postfix(infix: str) -> str:
    """
    >>> infix_2_postfix("a+b^c")  # doctest: +NORMALIZE_WHITESPACE
     Symbol  |  Stack  | Postfix
    ----------------------------
       a     |         | a
       +     | +       | a
       b     | +       | ab
       ^     | +^      | ab
       c     | +^      | abc
             | +       | abc^
             |         | abc^+
    'abc^+'

    >>> infix_2_postfix("1*((-a)*2+b)")   # doctest: +NORMALIZE_WHITESPACE
      Symbol  |    Stack     |   Postfix
    -------------------------------------------
       1     |              | 1
       *     | *            | 1
       (     | *(           | 1
       (     | *((          | 1
       -     | *((-         | 1
       a     | *((-         | 1a
       )     | *(           | 1a-
       *     | *(*          | 1a-
       2     | *(*          | 1a-2
       +     | *(+          | 1a-2*
       b     | *(+          | 1a-2*b
       )     | *            | 1a-2*b+
             |              | 1a-2*b+*
    '1a-2*b+*'

    >>> infix_2_postfix("")
     Symbol  |  Stack  | Postfix
    ----------------------------
    ''

    >>> infix_2_postfix("(()")
    Traceback (most recent call last):
        ...
    ValueError: invalid expression

    >>> infix_2_postfix("())")
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """
    stack = []
    post_fix = []
    priority = {
        "^": 3,
        "*": 2,
        "/": 2,
        "%": 2,
        "+": 1,
        "-": 1,
    }  # 优先级 的 每个 运算符
    print_width = max(len(infix), 7)

    # 打印 table header 用于 输出
    print(
        "Symbol".center(8),
        "Stack".center(print_width),
        "Postfix".center(print_width),
        sep=" | ",
    )
    print("-" * (print_width * 3 + 7))

    for x in infix:
        if x.isalpha() or x.isdigit():
            post_fix.append(x)  # 如果 x 是 Alphabet / Digit，添加 它 到 后缀表达式
        elif x == "(":
            stack.append(x)  # 如果 x 是 "(" 压入 到 栈
        elif x == ")":  # 如果 x 是 ")" 弹出 栈 until "(" 是 遇到
            if len(stack) == 0:  # close bracket 不使用 开放 bracket
                raise IndexError("list index out of range")

            while stack[-1] != "(":
                post_fix.append(stack.pop())  # 弹出 栈 & 添加 content 到 后缀表达式
            stack.pop()
        elif len(stack) == 0:
            stack.append(x)  # 如果 栈 为空，压入 x 到 栈
        else:  # 当 优先级 的 x 是 不 > 优先级 的 元素 在 该栈
            while stack and stack[-1] != "(" and priority[x] <= priority[stack[-1]]:
                post_fix.append(stack.pop())  # 弹出 栈 & 添加 到 后缀表达式
            stack.append(x)  # 压入 x 到 栈

        print(
            x.center(8),
            ("".join(stack)).ljust(print_width),
            ("".join(post_fix)).ljust(print_width),
            sep=" | ",
        )  # 输出 在 表格形式 格式

    while len(stack) > 0:  # 当 栈 非空
        if stack[-1] == "(":  # 开放 bracket 带有 没有 close bracket
            raise ValueError("invalid expression")

        post_fix.append(stack.pop())  # 弹出 栈 & 添加 到 后缀表达式
        print(
            " ".center(8),
            ("".join(stack)).ljust(print_width),
            ("".join(post_fix)).ljust(print_width),
            sep=" | ",
        )  # 输出 在 表格形式 格式

    return "".join(post_fix)  # 返回 后缀表达式 作为 str


def infix_2_prefix(infix: str) -> str:
    """
    >>> infix_2_prefix("a+b^c")  # doctest: +NORMALIZE_WHITESPACE
     Symbol  |  Stack  | Postfix
    ----------------------------
       c     |         | c
       ^     | ^       | c
       b     | ^       | cb
       +     | +       | cb^
       a     | +       | cb^a
             |         | cb^a+
    '+a^bc'

    >>> infix_2_prefix("1*((-a)*2+b)") # doctest: +NORMALIZE_WHITESPACE
     Symbol  |    Stack     |   Postfix
    -------------------------------------------
       (     | (            |
       b     | (            | b
       +     | (+           | b
       2     | (+           | b2
       *     | (+*          | b2
       (     | (+*(         | b2
       a     | (+*(         | b2a
       -     | (+*(-        | b2a
       )     | (+*          | b2a-
       )     |              | b2a-*+
       *     | *            | b2a-*+
       1     | *            | b2a-*+1
             |              | b2a-*+1*
    '*1+*-a2b'

    >>> infix_2_prefix('')
     Symbol  |  Stack  | Postfix
    ----------------------------
    ''

    >>> infix_2_prefix('(()')
    Traceback (most recent call last):
        ...
    IndexError: list index out of range

    >>> infix_2_prefix('())')
    Traceback (most recent call last):
        ...
    ValueError: invalid expression
    """
    reversed_infix = list(infix[::-1])  # 反转 infix equation

    for i in range(len(reversed_infix)):
        if reversed_infix[i] == "(":
            reversed_infix[i] = ")"  # 更改 "(" 到 ")"
        elif reversed_infix[i] == ")":
            reversed_infix[i] = "("  # 更改 ")" 到 "("

    # call infix_2_postfix 在 Infix，返回 反转 的 后缀表达式
    return (infix_2_postfix("".join(reversed_infix)))[::-1]


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    Infix = input("\nEnter an Infix Equation = ")  # 输入 Infix equation
    Infix = "".join(Infix.split())  # 移除 spaces 从 输入
    print("\n\t", Infix, "(Infix) -> ", infix_2_prefix(Infix), "(Prefix)")
