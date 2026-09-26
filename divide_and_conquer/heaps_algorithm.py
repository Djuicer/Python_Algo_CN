"""
Heap 算法（Heap's Algorithm）返回列表的所有可能排列。
每次只交换两个元素，从上一个排列生成下一个排列，
以尽量减少元素移动。
更多信息：
https://en.wikipedia.org/wiki/Heap%27s_algorithm.
"""


def heaps(arr: list) -> list:
    """
    Heap 算法的纯 Python 实现（递归版本），
    返回列表的所有排列。
    >>> heaps([])
    [()]
    >>> heaps([0])
    [(0,)]
    >>> heaps([-1, 1])
    [(-1, 1), (1, -1)]
    >>> heaps([1, 2, 3])
    [(1, 2, 3), (2, 1, 3), (3, 1, 2), (1, 3, 2), (2, 3, 1), (3, 2, 1)]
    >>> from itertools import permutations
    >>> sorted(heaps([1,2,3])) == sorted(permutations([1,2,3]))
    True
    >>> all(sorted(heaps(x)) == sorted(permutations(x))
    ...     for x in ([], [0], [-1, 1], [1, 2, 3]))
    True
    """

    if len(arr) <= 1:
        return [tuple(arr)]

    res = []

    def generate(k: int, arr: list) -> None:
        if k == 1:
            res.append(tuple(arr[:]))
            return

        generate(k - 1, arr)

        for i in range(k - 1):
            if k % 2 == 0:  # k 为偶数
                arr[i], arr[k - 1] = arr[k - 1], arr[i]
            else:  # k 为奇数
                arr[0], arr[k - 1] = arr[k - 1], arr[0]
            generate(k - 1, arr)

    generate(len(arr), arr)
    return res


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    arr = [int(item) for item in user_input.split(",")]
    print(heaps(arr))
