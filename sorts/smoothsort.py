"""
平滑排序（Smoothsort）算法实现。

平滑排序由 Edsger W. Dijkstra 提出，是一种自适应的原地比较排序。
最坏时间复杂度为 O(n log n)，对于近乎有序的数据可改善至 O(n)。
通过莱昂纳多堆（Leonardo Heap）森林实现自适应行为。

Reference:
    https://en.wikipedia.org/wiki/Smoothsort
    https://www.cs.utexas.edu/~EWD/ewd07xx/EWD796a.PDF
"""

# 预先计算的莱昂纳多数：L(0)=1、L(1)=1、L(k)=L(k-1)+L(k-2)+1。
# 46 个值足以覆盖实际使用的列表规模。
_LEONARDO: list[int] = [1, 1]
while _LEONARDO[-1] < 2**31:
    _LEONARDO.append(_LEONARDO[-1] + _LEONARDO[-2] + 1)


def _sift(seq: list[int], root: int, order: int) -> None:
    """
    恢复给定 ``order`` 阶莱昂纳多树内部的最大堆性质。

    将 ``seq[root]`` 向下筛选，直到子树满足莱昂纳多
    最大堆不变式：每个节点均 >= 其两个子节点。
    0 阶和 1 阶树只有一个节点，已满足该不变式。

    在根索引为 ``root`` 的 k 阶莱昂纳多树中：
      - 右子树根位于 ``root - 1``
      - 左子树根位于 ``root - 1 - L(k-2)``

    Args:
        seq:   待排序列表（原地修改）。
        root:  待修复莱昂纳多树的根索引。
        order: 以 ``root`` 为根的莱昂纳多树的阶。

    示例：
        >>> data = [3, 5, 4]
        >>> _sift(data, 2, 2)
        >>> data
        [3, 4, 5]

        >>> data = [1, 2, 3]
        >>> _sift(data, 2, 2)
        >>> data
        [1, 2, 3]

        >>> data = [7]
        >>> _sift(data, 0, 1)
        >>> data
        [7]

        >>> data = [9, 1, 8, 5, 3]
        >>> _sift(data, 4, 3)
        >>> data
        [3, 1, 9, 5, 8]
    """
    while order > 1:
        right = root - 1  # 右子树根
        left = root - 1 - _LEONARDO[order - 2]  # 左子树根

        if seq[left] >= seq[right] and seq[left] > seq[root]:
            seq[root], seq[left] = seq[left], seq[root]
            root = left
            order -= 1
        elif seq[right] > seq[left] and seq[right] > seq[root]:
            seq[root], seq[right] = seq[right], seq[root]
            root = right
            order -= 2
        else:
            break


def _trinkle(
    seq: list[int],
    pos: int,
    heap_sizes: list[int],
    idx: int,
) -> None:
    """
    同时恢复堆根之间和各堆内部的顺序。

    只要左邻堆根更大，就将 ``pos`` 处的值沿森林的根链
    向左移动，然后调用 ``_sift``，修复
    最终位置上的堆。

    Args:
        seq:        待排序列表（原地修改）。
        pos:        正在插入或刚暴露的根索引。
        heap_sizes: 当前森林中各莱昂纳多树的阶（从左到
                    右）；``heap_sizes[idx]`` 是根位于
                    ``pos`` 的树的阶。
        idx:        以 ``pos`` 为根的树在 ``heap_sizes`` 中的位置。

    示例：
        >>> data = [1, 5, 3]
        >>> _trinkle(data, 2, [1, 1], 1)
        >>> data
        [1, 3, 5]

        >>> data = [3, 5, 4]
        >>> _trinkle(data, 2, [2], 0)
        >>> data
        [3, 4, 5]
    """
    while idx > 0:
        prev_root = pos - _LEONARDO[heap_sizes[idx]]
        if seq[pos] >= seq[prev_root]:
            break
        # 仅当 prev_root 也 >= 自身子节点时交换，否则
        # 移动它会破坏左侧的堆。
        if heap_sizes[idx] > 1:
            right = pos - 1
            left = pos - 1 - _LEONARDO[heap_sizes[idx] - 2]
            if seq[prev_root] <= seq[right] or seq[prev_root] <= seq[left]:
                break
        seq[pos], seq[prev_root] = seq[prev_root], seq[pos]
        pos = prev_root
        idx -= 1

    _sift(seq, pos, heap_sizes[idx])


def smoothsort(seq: list[int]) -> list[int]:
    """
    使用平滑排序原地排序列表并返回该列表。

    平滑排序（Edsger W. Dijkstra，1981）是一种自适应原地排序，
    最坏时间复杂度为 O(n log n)，输入已有序时的最好时间为
    O(n)。通过维护莱昂纳多堆森林来改进堆排序，
    森林结构反映序列中已排序的前缀。

    Args:
        seq: 待排序的整数列表。

    Returns:
        按升序排列后的同一个列表对象。

    示例：
        >>> smoothsort([4, 1, 3, 9, 7])
        [1, 3, 4, 7, 9]
        >>> smoothsort([])
        []
        >>> smoothsort([1])
        [1]
        >>> smoothsort([5, 4, 3, 2, 1])
        [1, 2, 3, 4, 5]
        >>> smoothsort([3, 3, 2, 1, 2])
        [1, 2, 2, 3, 3]
        >>> smoothsort([1, 2, 3, 4, 5])
        [1, 2, 3, 4, 5]
        >>> smoothsort([-3, 0, -1, 5, 2])
        [-3, -1, 0, 2, 5]
    """
    n = len(seq)
    if n < 2:
        return seq

    # ``heap_sizes[i]`` 为从左到右第 i 棵树的莱昂纳多阶。
    heap_sizes: list[int] = []

    # ------------------------------------------------------------------
    # 阶段 1：在 seq[0..n-1] 上构建莱昂纳多堆森林。
    # ------------------------------------------------------------------
    for i in range(n):
        # 若最右侧两棵树的阶连续，则合并它们。
        if len(heap_sizes) >= 2 and heap_sizes[-2] == heap_sizes[-1] + 1:
            heap_sizes.pop()
            heap_sizes[-1] += 1
        elif heap_sizes and heap_sizes[-1] == 1:
            heap_sizes.append(0)
        else:
            heap_sizes.append(1)

        _trinkle(seq, i, heap_sizes, len(heap_sizes) - 1)

    # ------------------------------------------------------------------
    # 阶段 2：从右向左取出最大元素。
    # ------------------------------------------------------------------
    for i in range(n - 1, -1, -1):
        order = heap_sizes.pop()
        if order > 1:
            # 暴露两个子树根，并分别重新执行 trinkle 调整。
            right_order = order - 2
            left_order = order - 1
            right_pos = i - 1
            left_pos = i - 1 - _LEONARDO[right_order]

            heap_sizes.append(left_order)
            _trinkle(seq, left_pos, heap_sizes, len(heap_sizes) - 1)

            heap_sizes.append(right_order)
            _trinkle(seq, right_pos, heap_sizes, len(heap_sizes) - 1)

    return seq


if __name__ == "__main__":
    import doctest
    import random

    results = doctest.testmod(verbose=False)
    assert results.failed == 0, f"{results.failed} doctest(s) failed"

    for trial in range(5000):
        sample = random.choices(range(-50, 50), k=random.randint(0, 30))
        got = smoothsort(sample[:])
        assert got == sorted(sample), (
            f"Trial {trial}: smoothsort({sample!r}) -> {got!r}, "
            f"expected {sorted(sample)!r}"
        )

    print("All doctests and 5 000 random trials passed.")
