"""
stock 跨度 problem 是 financial problem 其中 我们 具有 series 的 n daily
price quotes 用于 stock 并且 我们 need 到 计算 跨度 的 stock's price 用于 所有 n days。

跨度 Si 的 stock's price 在 给定 day i 是 定义 作为 最大值
数 的 consecutive days 仅 之前 给定 day，用于 其 price 的 stock
在 当前 day 是 较小 比 或 等于 到 其 price 在 给定 day。
"""


def calculate_span(price: list[int]) -> list[int]:
    """
    计算 跨度 值 用于 给定 列表 的 stock prices。
    参数：
        price: 列表 的 stock prices。
    返回值：
        列表 的 跨度 值。

    >>> calculate_span([10, 4, 5, 90, 120, 80])
    [1, 1, 2, 4, 5, 1]
    >>> calculate_span([100, 50, 60, 70, 80, 90])
    [1, 1, 2, 3, 4, 5]
    >>> calculate_span([5, 4, 3, 2, 1])
    [1, 1, 1, 1, 1]
    >>> calculate_span([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> calculate_span([10, 20, 30, 40, 50])
    [1, 2, 3, 4, 5]
    >>> calculate_span([100, 80, 60, 70, 60, 75, 85])
    [1, 1, 1, 2, 1, 4, 6]
    """
    n = len(price)
    s = [0] * n
    # 创建一个 栈 并且 压入 索引 的 fist 元素 到 它
    st = []
    st.append(0)

    # 跨度 值 的 第一个元素 是 始终 1
    s[0] = 1

    # 计算 跨度 值 用于 rest 的 元素
    for i in range(1, n):
        # 弹出 元素 从 栈 当 栈 是 不
        # 空 并且 顶部 的 栈 是 更小 比 price[i]
        while len(st) > 0 and price[st[-1]] <= price[i]:
            st.pop()

        # 如果 栈 变为 空，则 price[i] 是 更大
        # 比 所有元素 在 左 的 它，i.e. price[0],
        # price[1]，..price[i-1]. 否则 price[i]  是
        # 更大 比 元素 之后 顶部 的 栈
        s[i] = i + 1 if len(st) <= 0 else (i - st[-1])

        # 压入 此 元素 到 栈
        st.append(i)

    return s


# utility 函数 到 打印 元素 的 数组
def print_array(arr, n) -> None:
    for i in range(n):
        print(arr[i], end=" ")


# Driver program 到 测试 above 函数
price = [10, 4, 5, 90, 120, 80]

# 计算 跨度 值
S = calculate_span(price)

# 打印 计算得出 跨度 值
print_array(S, len(price))
