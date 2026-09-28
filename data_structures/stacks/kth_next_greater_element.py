"""
Implement 函数 到 查找 kth 下一个 Greatest 元素 (NGE) 用于 所有元素。
"""

test_k = 10
test_array = list(range(10000))
expected_answers = [value + test_k for value in range(10000 - test_k)] + [None] * test_k


def find_kth_next_greater_element(
    array: list[int | float], kth_ord: int
) -> list[int | float | None]:
    """
    Efficient general 方法 到 seek kth NGE 用于 所有元素。
    方法 是 entirely 基于 在 k 栈，其 是 actually very easy 到 understand。
    这些 k 栈 symbolize how many NGEs 元素 具有 已经 找到。

    用于 示例，用于 1 <= j <= k，如果 元素 是 currently 在 jth 栈,
    它 表示 该 此 元素 具有 找到 其 (j - 1)th NGE，现在 looking 用于 jth NGE。

    通过 processing 栈 从 higher 到 lower ordinals，我们 可以 始终 确保 该
    每个 栈 stays monotonically 非-increasing 在 terms 的 元素 值。

    时间复杂度: O(kn) 其中 n 是 长度 的 输入 数组。
    However，如果 k >= n，所有元素 won't 查找 它们的 respective kth NGE。
    作为 结果，最坏情况 时间复杂度 是 O(n^2) 当 k < n 但是 k ≈ n。

    空间复杂度: O(n)，since 在 任意 点，元素 是 仅 在 一个 的 k 栈。

    参数：
        数组 (列表[int | 浮点数]): 一个列表 用于 其 kth NGE 是 computed。
                                   mix 的 整数 并且 floats 在 列表 是 allowed。

        kth_ord (int): Ordinal 的 NGE 到 查找. kth_ord 必须 为 正 整数。

    返回值：
        一个列表 包含 每个元素's kth NGE. 如果 元素 可以't 查找 其 kth NGE,
        None，instead 的 -1，是 put 作为 其 entry，因为 输入 数组 might 具有 -1。

    示例：
    >>> find_kth_next_greater_element([1, 2, 3, 4, 5], 3) == [4, 5, None, None, None]
    True
    >>> find_kth_next_greater_element([2.5, 1.9, 4.3, 6.0], 1) == [4.3, 4.3, 6.0, None]
    True
    >>> find_kth_next_greater_element([1, 2, 3], 0)
    Traceback (most recent call last):
         ...
    ValueError: kth_ord must be a positive integer.
    >>> find_kth_next_greater_element(list(range(1000)), 1000) == [None] * 1000
    True
    >>> find_kth_next_greater_element(test_array, test_k) == expected_answers
    True
    """
    if not isinstance(kth_ord, int) or kth_ord < 1:
        raise ValueError("kth_ord must be a positive integer.")

    kth_next_greater_elements: list[int | float | None] = [None] * len(array)
    if kth_ord >= len(array):  # Trivial 情况: nobody 可以 具有 kth NGE。
        return kth_next_greater_elements

    # 用于 1 <= j <= k，jth 栈 是 在 jth idx 的 栈 列表。
    # 栈[0]: transporter 该 transfers entries 之间 栈。
    # 每个 栈's entry 是 元组 的 (元素，idx)。
    stacks: list[list[tuple[int | float, int]]] = [[] for _ in range(kth_ord + 1)]

    for idx, element in enumerate(array):
        # 从 kth 栈 到 answer 找到。
        while stacks[kth_ord] and stacks[kth_ord][-1][0] < element:
            _, prev_idx = stacks[kth_ord].pop()
            kth_next_greater_elements[prev_idx] = element

        for stack_ord in range(kth_ord - 1, 0, -1):  # 从 (k - 1)th 到 1st 栈。
            while stacks[stack_ord] and stacks[stack_ord][-1][0] < element:
                stacks[0].append(stacks[stack_ord].pop())

            while stacks[0]:  # 移动 到 下一个 ordered 栈。
                stacks[stack_ord + 1].append(stacks[0].pop())

        unvisited_elements_count = len(array) - 1 - idx
        if unvisited_elements_count >= kth_ord:  # 元素 具有 chance 到 查找 kth NGE。
            stacks[1].append((element, idx))  # 始终 join 1st 栈 到 begin 搜索。

    return kth_next_greater_elements


if __name__ == "__main__":
    from doctest import testmod
    from timeit import timeit

    testmod()
    setup = "from __main__ import test_array, test_k, find_kth_next_greater_element"
    print(
        "find_kth_next_greater_element():",
        timeit("find_kth_next_greater_element(test_array, test_k)", setup=setup),
    )
