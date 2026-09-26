# 实现鸽巢排序（Pigeonhole Sort）的 Python 程序

# 鸽巢排序算法


def pigeonhole_sort(a) -> None:
    """
    >>> a = [8, 3, 2, 7, 4, 6, 8]
    >>> b = sorted(a)  # a nondestructive sort
    >>> pigeonhole_sort(a)  # a destructive sort
    >>> a == b
    True

    >>> pigeonhole_sort([])
    """
    if not a:
        return
    # 列表的值域大小（即所需的鸽巢数量）

    min_val = min(a)  # min() 求最小值
    max_val = max(a)  # max() 求最大值

    size = max_val - min_val + 1  # size 为最大值与最小值之差加一

    # 长度等于 size 的鸽巢列表
    holes = [0] * size

    # 填充鸽巢。
    for x in a:
        assert isinstance(x, int), "integers only please"
        holes[x - min_val] += 1

    # 按顺序将元素放回数组。
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            a[i] = count + min_val
            i += 1


def main() -> None:
    a = [8, 3, 2, 7, 4, 6, 8]
    pigeonhole_sort(a)
    print("Sorted order is:", *a)


if __name__ == "__main__":
    main()
