"""
问题：
    给定一个由不同整数组成的数组，求从数组中选择元素并使所选元素之和
    等于目标数 tar 的不同方式数。

示例

输入：
    * N = 3
    * target = 5
    * array = [1, 2, 5]

输出：
    9

思路：
    基本思想是通过递归寻找使所选元素之和为 `target` 的方式。
    对于每个元素，有两种选择：

        1. 将该元素加入所选元素集合。
        2. 不将该元素加入所选元素集合。
"""


def combination_sum_iv(array: list[int], target: int) -> int:
    """
    检查所有可能的组合，并以指数时间复杂度返回可能组合的数量。

    >>> combination_sum_iv([1,2,5], 5)
    9
    """

    def count_of_possible_combinations(target: int) -> int:
        if target < 0:
            return 0
        if target == 0:
            return 1
        return sum(count_of_possible_combinations(target - item) for item in array)

    return count_of_possible_combinations(target)


def combination_sum_iv_dp_array(array: list[int], target: int) -> int:
    """
    检查所有可能的组合，并返回可能组合的数量。
    由于这里使用动态规划（Dynamic Programming）数组，时间复杂度为 O(N^2)。

    >>> combination_sum_iv_dp_array([1,2,5], 5)
    9
    """

    def count_of_possible_combinations_with_dp_array(
        target: int, dp_array: list[int]
    ) -> int:
        if target < 0:
            return 0
        if target == 0:
            return 1
        if dp_array[target] != -1:
            return dp_array[target]
        answer = sum(
            count_of_possible_combinations_with_dp_array(target - item, dp_array)
            for item in array
        )
        dp_array[target] = answer
        return answer

    dp_array = [-1] * (target + 1)
    return count_of_possible_combinations_with_dp_array(target, dp_array)


def combination_sum_iv_bottom_up(n: int, array: list[int], target: int) -> int:
    """
    使用自底向上的方法检查所有可能的组合，并返回可能组合的数量。
    由于这里使用动态规划数组，时间复杂度为 O(N^2)。

    >>> combination_sum_iv_bottom_up(3, [1,2,5], 5)
    9
    """

    dp_array = [0] * (target + 1)
    dp_array[0] = 1

    for i in range(1, target + 1):
        for j in range(n):
            if i - array[j] >= 0:
                dp_array[i] += dp_array[i - array[j]]

    return dp_array[target]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    target = 5
    array = [1, 2, 5]
    print(combination_sum_iv(array, target))
