"""
计数排序（Counting Sort）算法的纯 Python 实现
运行 doctest 请使用以下命令：
python -m doctest -v counting_sort.py
或
python3 -m doctest -v counting_sort.py
手动测试请运行：
python counting_sort.py
"""


def counting_sort(collection):
    """计数排序算法的纯 Python 实现
    :param collection: 可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return: 按升序排列后的同一个集合
    示例：
    >>> counting_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> counting_sort([])
    []
    >>> counting_sort([-2, -5, -45])
    [-45, -5, -2]
    """
    # 集合为空时返回空集合
    if collection == []:
        return []

    # 获取集合的相关信息
    coll_len = len(collection)
    coll_max = max(collection)
    coll_min = min(collection)

    # 创建计数数组
    counting_arr_length = coll_max + 1 - coll_min
    counting_arr = [0] * counting_arr_length

    # 统计各个数在集合中出现的次数
    for number in collection:
        counting_arr[number - coll_min] += 1

    # 将每个位置与其前面的位置累加。此时 counting_arr[i] 表示
    # 集合中小于或等于 i 的元素数量
    for i in range(1, counting_arr_length):
        counting_arr[i] = counting_arr[i] + counting_arr[i - 1]

    # 创建输出集合
    ordered = [0] * coll_len

    # 从后向前将元素放入输出集合，保持原有相对顺序
    # （稳定排序），并更新 counting_arr
    for i in reversed(range(coll_len)):
        ordered[counting_arr[collection[i] - coll_min] - 1] = collection[i]
        counting_arr[collection[i] - coll_min] -= 1

    return ordered


def counting_sort_string(string):
    """
    >>> counting_sort_string("thisisthestring")
    'eghhiiinrsssttt'
    """
    return "".join([chr(i) for i in counting_sort([ord(c) for c in string])])


if __name__ == "__main__":
    # 测试字符串排序
    assert counting_sort_string("thisisthestring") == "eghhiiinrsssttt"

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(counting_sort(unsorted))
