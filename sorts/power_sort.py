"""
PowerSort：一种自适应归并排序算法。

PowerSort 是一种自适应的稳定排序算法，通过以最优方式
合并输入中已有的有序段（Run，即连续的
有序元素序列），高效处理部分有序的数据。它由 J. Ian Munro 和 Sebastian
Wild 提出，自 Python 3.11 起集成到标准库中。

算法步骤：
1. 检测自然形成的有序段（升序或降序序列）
2. 使用基于节点幂的归并策略确定最优合并顺序
3. 维护有序段栈，根据计算出的节点幂进行合并

时间复杂度：最坏为 O(n log n)，近乎有序数据为 O(n)
空间复杂度：合并缓冲区需要 O(n)

参考资料：
- https://en.wikipedia.org/wiki/Powersort
- https://arxiv.org/abs/1805.04154 (Original paper by Munro and Wild)

运行 doctest：
python -m doctest -v power_sort.py

手动测试请运行：
python power_sort.py
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def _find_run(
    arr: list, start: int, end: int, key: Callable[[Any], Any] | None = None
) -> int:
    """
    检测从 'start' 开始的有序段（升序或降序序列）。


    若为降序段，则原地反转为升序。
    返回检测到的有序段的结束索引（不包含该位置）。


    参数：
        arr: 待搜索的列表
        start: 有序段的起始索引
        end: 搜索范围的结束索引（不包含该位置）
        key: 可选的比较键函数


    返回：
        检测到的有序段的结束索引（不包含该位置）


    >>> arr = [3, 2, 1, 4, 5, 6]
    >>> _find_run(arr, 0, 6)
    3
    >>> arr
    [1, 2, 3, 4, 5, 6]
    >>> arr = [1, 2, 3, 2, 1]
    >>> _find_run(arr, 0, 5)
    3
    >>> arr
    [1, 2, 3, 2, 1]
    """
    if start >= end - 1:
        return start + 1

    key_func = key if key else lambda element: element
    run_end = start + 1

    # 检查有序段是升序还是降序
    if key_func(arr[run_end]) < key_func(arr[start]):
        # 降序段
        while run_end < end and key_func(arr[run_end]) < key_func(arr[run_end - 1]):
            run_end += 1
        # 反转降序段，使其升序
        arr[start:run_end] = reversed(arr[start:run_end])
    else:
        # 升序段
        while run_end < end and key_func(arr[run_end]) >= key_func(arr[run_end - 1]):
            run_end += 1

    return run_end


def _node_power(total_length: int, b1: int, n1: int, b2: int, n2: int) -> int:
    """
    计算两个相邻有序段的节点幂（Node Power）。


    它决定栈中的合并优先级。节点幂为满足
    floor(a * 2^p) != floor(b * 2^p) 的最小整数 p，其中：
    - a = (b1 + n1/2) / n
    - b = (b2 + n2/2) / n


    参数：
        total_length: 数组总长度
        b1: 第一个有序段的起始索引
        n1: 第一个有序段的长度
        b2: 第二个有序段的起始索引
        n2: 第二个有序段的长度


    返回：
        计算出的节点幂


    >>> _node_power(100, 0, 25, 25, 25)
    2
    >>> _node_power(100, 0, 50, 50, 50)
    1
    """
    # 计算中点：a = (b1 + n1/2) / total_length，
    # b = (b2 + n2/2) / total_length
    # 为避免浮点运算，使用 a = (2*b1 + n1) / (2*total_length) 和
    # b = (2*b2 + n2) / (2*total_length)
    # 要求满足 floor(a * 2^p) != floor(b * 2^p) 的最小 p
    # 即 floor((2*b1 + n1) * 2^p / (2*total_length)) !=
    # floor((2*b2 + n2) * 2^p / (2*total_length))

    a = 2 * b1 + n1
    b = 2 * b2 + n2
    two_n = 2 * total_length

    # 查找使下式成立的最小幂 p：floor(a * 2^p / two_n) !=
    # floor(b * 2^p / two_n)
    power = 0
    while (a * (1 << power)) // two_n == (b * (1 << power)) // two_n:
        power += 1

    return power


def _merge(
    arr: list,
    start1: int,
    end1: int,
    end2: int,
    key: Callable[[Any], Any] | None = None,
) -> None:
    """
    使用辅助空间，在原位置合并两个相邻有序段。


    合并 arr[start1:end1] 与 arr[end1:end2]。


    参数：
        arr: 包含有序段的列表
        start1: 第一个有序段的起始索引
        end1: 第一个有序段的结束索引（第二个有序段的起始位置）
        end2: 第二个有序段的结束索引
        key: 可选的比较键函数


    >>> arr = [1, 3, 5, 2, 4, 6]
    >>> _merge(arr, 0, 3, 6)
    >>> arr
    [1, 2, 3, 4, 5, 6]
    >>> arr = [5, 6, 7, 1, 2, 3]
    >>> _merge(arr, 0, 3, 6)
    >>> arr
    [1, 2, 3, 5, 6, 7]
    """
    key_func = key if key else lambda element: element

    # 将有序段复制到临时存储区
    left = arr[start1:end1]
    right = arr[end1:end2]

    i = j = 0
    k = start1

    # 合并两个有序段
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    # 复制剩余元素
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def power_sort(
    collection: list,
    *,
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> list:
    """
    使用 PowerSort 算法对列表排序。


    PowerSort 是一种自适应归并排序，检测数据中已有的有序段，
    并使用基于节点幂的合并策略以获得最优性能。


    参数：
        collection: 元素可比较的可变有序集合
        key: 可选函数，用于提取各元素的比较键
        reverse: 为 True 时按降序排列


    返回：
        按参数指定顺序排列后的同一个集合


    时间复杂度：最坏为 O(n log n)，近乎有序数据为 O(n)
    空间复杂度：O(n)


    示例：
    >>> power_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> power_sort([])
    []
    >>> power_sort([1])
    [1]
    >>> power_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> power_sort([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> power_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> power_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])
    [1, 1, 2, 3, 4, 5, 5, 6, 9]
    >>> power_sort(['banana', 'apple', 'cherry'])
    ['apple', 'banana', 'cherry']
    >>> power_sort([3.14, 2.71, 1.41, 1.73])
    [1.41, 1.73, 2.71, 3.14]
    >>> power_sort([5, 2, 8, 1, 9], reverse=True)
    [9, 8, 5, 2, 1]
    >>> power_sort(['apple', 'pie', 'a', 'longer'], key=len)
    ['a', 'pie', 'apple', 'longer']
    >>> power_sort([(1, 'b'), (2, 'a'), (1, 'a')], key=lambda x: x[0])
    [(1, 'b'), (1, 'a'), (2, 'a')]
    >>> power_sort([1, 2, 3, 2, 1, 2, 3, 4])
    [1, 1, 2, 2, 2, 3, 3, 4]
    >>> result = power_sort(list(range(100)))
    >>> result == list(range(100))
    True
    >>> result = power_sort(list(reversed(range(50))))
    >>> result == list(range(50))
    True
    """
    if len(collection) <= 1:
        return collection

    # 创建副本，以免修改不可变的原始输入
    arr = list(collection)
    total_length = len(arr)

    # 调整键函数以实现逆序排序
    needs_final_reverse = False
    if reverse:
        if key:
            original_key = key

            def reverse_key(element: Any) -> Any:
                """
                用于数值的反向键函数。

                参数：
                    element: 待处理的元素

                返回：
                    数值类型返回相反数，其他类型返回原值

                >>> reverse_key(5)
                -5
                >>> reverse_key('hello')
                'hello'
                """
                val = original_key(element)
                if isinstance(val, int | float):
                    return -val
                return val

            key = reverse_key
            needs_final_reverse = True
        else:

            def reverse_cmp(element: Any) -> Any:
                """
                用于数值的反向比较函数。

                参数：
                    element: 待处理的元素

                返回：
                    数值类型返回相反数，其他类型返回原值

                >>> reverse_cmp(10)
                -10
                >>> reverse_cmp('test')
                'test'
                """
                if isinstance(element, int | float):
                    return -element
                return element

            key = reverse_cmp
            needs_final_reverse = True

    # 保存有序段的栈：每项为 (start_index, length, power)
    stack: list[tuple[int, int, int]] = []

    start = 0
    while start < total_length:
        # 查找下一个有序段
        run_end = _find_run(arr, start, total_length, key)
        run_length = run_end - start

        # 计算该有序段的节点幂
        if len(stack) == 0:
            power = 0
        else:
            prev_start, prev_length, _ = stack[-1]
            power = _node_power(
                total_length, prev_start, prev_length, start, run_length
            )

        # 根据节点幂的比较结果，合并栈中的有序段
        while len(stack) > 0 and stack[-1][2] >= power:
            # 合并栈顶有序段与当前有序段
            prev_start, prev_length, _ = stack.pop()
            _merge(arr, prev_start, prev_start + prev_length, run_end, key)

            # 更新当前有序段，使其包含合并后的范围
            start = prev_start
            run_length = run_end - start

            # 重新计算节点幂
            if len(stack) == 0:
                power = 0
            else:
                prev_prev_start, prev_prev_length, _ = stack[-1]
                power = _node_power(
                    total_length, prev_prev_start, prev_prev_length, start, run_length
                )

        # 将当前有序段压栈
        stack.append((start, run_length, power))
        start = run_end

    # 合并栈中所有剩余的有序段
    while len(stack) > 1:
        start2, length2, _ = stack.pop()
        start1, length1, _ = stack.pop()
        _merge(arr, start1, start1 + length1, start2 + length2, key)

        # 为合并后的有序段重新计算节点幂
        if len(stack) == 0:
            power = 0
        else:
            prev_start, prev_length, _ = stack[-1]
            merged_length = start2 + length2 - start1
            power = _node_power(
                total_length, prev_start, prev_length, start1, merged_length
            )

        stack.append((start1, start2 + length2 - start1, power))

    # 处理非数值类型的逆序排序
    if (
        reverse
        and needs_final_reverse
        and key
        and len(arr) > 0
        and not isinstance(arr[0], int | float)
    ):
        # 对于非数值类型，需要反转最终结果
        # 检查是否使用了数值取负
        arr.reverse()

    return arr


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("\nPowerSort Interactive Testing")
    print("=" * 40)

    try:
        user_input = input("Enter numbers separated by a comma:\n").strip()
        if user_input == "":
            unsorted = []
        else:
            unsorted = [int(item.strip()) for item in user_input.split(",")]

        print(f"\nOriginal: {unsorted}")
        sorted_list = power_sort(unsorted)
        print(f"Sorted:   {sorted_list}")

        # 测试逆序
        sorted_reverse = power_sort(unsorted, reverse=True)
        print(f"Reverse:  {sorted_reverse}")

    except ValueError:
        print("Invalid input. Please enter valid integers separated by commas.")
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
